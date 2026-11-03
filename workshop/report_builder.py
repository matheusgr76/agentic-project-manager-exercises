"""Build a local, source-backed Acme status report for Chapter 4."""

from __future__ import annotations

import argparse
import logging
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from workshop.config import (
    INPUTS_DIR,
    MAX_CAPACITY_AGE_DAYS,
    OUTPUTS_DIR,
    REPORT_DATE,
    TARGET_DECISION_ID,
    TARGET_ISSUE_ID,
)
from workshop.files import read_csv, read_text, write_json, write_text


LOGGER = logging.getLogger(__name__)


def by_id(rows: List[Dict[str, str]], record_id: str) -> Dict[str, str]:
    for row in rows:
        if row.get("id") == record_id:
            return row
    raise ValueError(f"Required record is missing: {record_id}")


def capacity_findings(
    rows: List[Dict[str, str]],
    report_date: date,
    source_name: str,
) -> List[Dict[str, object]]:
    findings: List[Dict[str, object]] = []
    for row in rows:
        try:
            age = (report_date - date.fromisoformat(row["snapshot_date"])).days
        except (KeyError, ValueError) as error:
            raise ValueError(f"Invalid capacity date for {row.get('team')}") from error
        if age < 0:
            raise ValueError(f"Capacity snapshot is after report date: {row['team']}")
        findings.append(
            {
                "team": row["team"],
                "allocation": row["allocation"],
                "status": row["status"],
                "snapshot_date": row["snapshot_date"],
                "age_days": age,
                "stale": age > MAX_CAPACITY_AGE_DAYS,
                "source": source_name,
            }
        )
    return findings


def check_updates() -> None:
    updates = read_text(INPUTS_DIR / "updates.md")
    if "UP-1" not in updates or "UP-2" not in updates or "UP-3" not in updates:
        raise ValueError("Required team updates are missing")


def load_issues_and_decisions() -> Tuple[
    List[Dict[str, str]],
    List[Dict[str, str]],
]:
    issues = read_csv(
        INPUTS_DIR / "issues.csv",
        ["id", "title", "status", "owner", "updated_at", "dependency"],
    )
    decisions = read_csv(
        INPUTS_DIR / "decisions.csv",
        ["id", "subject", "status", "approver", "effective_date", "version"],
    )
    return issues, decisions


def select_context(
    issues: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    issue_override: Optional[Dict[str, str]],
) -> Dict[str, Dict[str, str]]:
    issue = dict(by_id(issues, TARGET_ISSUE_ID))
    if issue_override is not None:
        if issue_override.get("id") != TARGET_ISSUE_ID:
            raise ValueError("Mock issue ID does not match GH-41")
        issue.update(issue_override)
    decision = by_id(decisions, TARGET_DECISION_ID)
    if issue["dependency"] != decision["id"]:
        raise ValueError("GH-41 dependency does not match DEC-12")
    return {
        "issue": issue,
        "independent_issue": by_id(issues, "GH-42"),
        "data_contract_issue": by_id(issues, "GH-43"),
        "decision": decision,
        "scope_decision": by_id(decisions, "DEC-13"),
    }


def build_evidence(
    issue_override: Optional[Dict[str, str]] = None,
    capacity_override: Optional[List[Dict[str, str]]] = None,
    report_date: date = REPORT_DATE,
    capacity_source: str = "capacity.csv",
) -> Dict[str, object]:
    issues, decisions = load_issues_and_decisions()
    capacity = capacity_override
    if capacity is None:
        capacity = read_csv(
            INPUTS_DIR / "capacity.csv",
            ["team", "allocation", "status", "snapshot_date"],
        )
    check_updates()
    context = select_context(issues, decisions, issue_override)
    issue = context["issue"]
    decision = context["decision"]

    approved = (
        decision["status"] == "APPROVED"
        and bool(decision["approver"].strip())
        and bool(decision["effective_date"].strip())
    )
    if decision["status"] == "APPROVED" and not approved:
        LOGGER.warning("DEC-12 approval record is incomplete")
    findings = capacity_findings(capacity, report_date, capacity_source)
    LOGGER.info(
        "Validated GH-41=%s, DEC-12=%s, formal approval=%s",
        issue["status"],
        decision["status"],
        approved,
    )
    return {
        "report_date": report_date.isoformat(),
        **context,
        "formal_approval": approved,
        "capacity": findings,
        "source_references": [
            "GH-41", "GH-42", "GH-43", "DEC-12", "DEC-13",
            "UP-1", "UP-2", "UP-3",
        ],
        "unsupported_claims": ["delivery date", "achieved 25% improvement"],
    }


def draft_weekly(evidence: Dict[str, object]) -> str:
    issue = evidence["issue"]
    decision = evidence["decision"]
    contract = evidence["data_contract_issue"]
    scope = evidence["scope_decision"]
    capacity = evidence["capacity"]
    assert isinstance(issue, dict) and isinstance(decision, dict)
    assert isinstance(contract, dict) and isinstance(scope, dict)
    assert isinstance(capacity, list)

    if issue["status"] == "BLOCKED":
        position = "Bravo's full integration sizing remains blocked (GH-41, UP-2)."
    else:
        position = (
            f"GH-41 is {issue['status']} while its data decision must be checked."
        )
    approval = (
        "DEC-12 has complete approval evidence."
        if evidence["formal_approval"]
        else "DEC-12 is not verified as formally approved (DEC-12, UP-1)."
    )
    stale = [row["team"] for row in capacity if row["stale"]]
    capacity_source = capacity[0]["source"]
    capacity_text = (
        f"Capacity snapshots are stale for {', '.join(stale)} ({capacity_source})."
        if stale
        else "Capacity snapshots are within the exercise freshness limit."
    )
    return (
        "# Weekly management status — draft\n\n"
        f"{position} Independent interface sizing is in progress (GH-42, UP-2). "
        f"Alpha's data contract issue is {contract['status']} (GH-43). "
        f"Proof-of-concept scope is {scope['status']} (DEC-13), which does not "
        "settle the missing-value definition. "
        f"{approval} {capacity_text} The CTO says new allocations are not yet "
        "confirmed (UP-3). Obtain the formal decision and current capacity "
        "before a delivery forecast. The supplied inputs establish no delivery "
        "date or achieved 25% improvement.\n\n"
        "PM approval is required before publication.\n"
    )


def run(output_dir: Path) -> Dict[str, object]:
    evidence = build_evidence()
    write_json(output_dir / "evidence.json", evidence)
    write_text(output_dir / "weekly-status.md", draft_weekly(evidence))
    return evidence


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=OUTPUTS_DIR / "ch4")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    try:
        evidence = run(args.output_dir)
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, f"Report Builder stopped: {error}\n")
    print(f"Chapter 4 complete: {args.output_dir}")
    print(f"GH-41: {evidence['issue']['status']}; DEC-12: {evidence['decision']['status']}")


if __name__ == "__main__":
    main()
