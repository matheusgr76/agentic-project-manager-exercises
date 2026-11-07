"""Build a local, source-backed Acme status report for Chapter 4."""

from __future__ import annotations

import argparse
import logging
from datetime import date, datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from workshop.config import (
    INPUTS_DIR,
    MAX_CAPACITY_AGE_DAYS,
    OUTPUTS_DIR,
    REPORT_DATE,
    TARGET_DECISION_ID,
    TARGET_DECISION_VERSION,
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
        required_fields = ("team", "allocation", "status", "snapshot_date")
        missing_fields = [
            field for field in required_fields
            if not str(row.get(field, "")).strip()
        ]
        if missing_fields:
            raise ValueError(
                "Capacity row has missing fields: " + ", ".join(missing_fields)
            )
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
                "input_file": source_name,
                "record_id": row["team"],
            }
        )
    return findings


def validate_updates(updates: str) -> None:
    """Require a dated author and the expected claim for each update."""
    required_updates = {
        "UP-1": "Option B looks good",
        "UP-2": "data contract still blocks the full estimate",
        "UP-3": "New allocations are not yet confirmed",
    }
    seen = set()
    for line in updates.splitlines():
        if not line.strip():
            continue
        fields = [field.strip() for field in line.split("|", 3)]
        if len(fields) != 4 or not all(fields):
            raise ValueError("Update has a missing ID, date, author, or claim")
        update_id, recorded_at, author, claim = fields
        if update_id not in required_updates or update_id in seen:
            raise ValueError(f"Unknown or duplicate update: {update_id}")
        try:
            date.fromisoformat(recorded_at)
        except ValueError as error:
            raise ValueError(f"Invalid update date: {update_id}") from error
        if required_updates[update_id] not in claim:
            raise ValueError(f"Supporting claim is missing: {update_id}")
        seen.add(update_id)
    if seen != set(required_updates):
        raise ValueError(f"Required updates are missing: {sorted(set(required_updates) - seen)}")


def check_updates() -> None:
    validate_updates(read_text(INPUTS_DIR / "updates.md"))


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
    for issue in issues:
        if any(not str(issue[field]).strip() for field in (
            "id", "title", "status", "owner", "updated_at"
        )):
            raise ValueError(f"Issue has a missing required field: {issue.get('id')}")
        try:
            datetime.fromisoformat(issue["updated_at"].replace("Z", "+00:00"))
        except ValueError as error:
            raise ValueError(f"Invalid issue update date: {issue['id']}") from error
    for decision in decisions:
        if any(not str(decision.get(field, "")).strip() for field in (
            "id", "subject", "status", "version"
        )):
            raise ValueError(f"Decision has a missing required field: {decision.get('id')}")
        if decision["effective_date"].strip():
            try:
                date.fromisoformat(decision["effective_date"])
            except ValueError as error:
                raise ValueError(f"Invalid decision effective date: {decision['id']}") from error
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
        required_fields = ("title", "status", "owner", "updated_at", "dependency")
        missing_fields = [
            field for field in required_fields
            if not str(issue_override.get(field, "")).strip()
        ]
        if missing_fields:
            raise ValueError(
                "Mock issue is missing required fields: " + ", ".join(missing_fields)
            )
        try:
            datetime.fromisoformat(issue_override["updated_at"].replace("Z", "+00:00"))
        except ValueError as error:
            raise ValueError("Mock issue has an invalid update date") from error
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
    capacity_source: str = "acme-practice-packet/inputs/capacity.csv",
    issue_source: str = "acme-practice-packet/inputs/issues.csv",
    retrieval_provenance: Optional[Dict[str, str]] = None,
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
        and decision["version"] == TARGET_DECISION_VERSION
        and bool(decision["approver"].strip())
        and bool(decision["effective_date"].strip())
    )
    if decision["status"] == "APPROVED" and not approved:
        LOGGER.warning("DEC-12 approval record is incomplete")
    status_conflicts = []
    if (issue["status"] in ("IN_PROGRESS", "RESOLVED") and not approved) or (
        issue["status"] == "BLOCKED" and approved
    ):
        status_conflicts.append({
            "issue_status": issue["status"],
            "decision_status": decision["status"],
            "issue_source": issue_source,
            "issue_record_id": issue["id"],
            "decision_source": "acme-practice-packet/inputs/decisions.csv",
            "decision_record_id": decision["id"],
        })
        LOGGER.warning("Explicit status conflict: %s versus %s", issue["id"], decision["id"])
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
        "status_conflicts": status_conflicts,
        "approval_warning": (
            "DEC-12 is marked APPROVED but its version, approver, or effective date is invalid"
            if decision["status"] == "APPROVED" and not approved else None
        ),
        "issue_retrieval": retrieval_provenance,
        "capacity": findings,
        "source_references": [
            {"input_file": source, "record_id": record_id}
            for source, record_id in (
                (issue_source, "GH-41"),
                ("acme-practice-packet/inputs/issues.csv", "GH-42"),
                ("acme-practice-packet/inputs/issues.csv", "GH-43"),
                ("acme-practice-packet/inputs/decisions.csv", "DEC-12"),
                ("acme-practice-packet/inputs/decisions.csv", "DEC-13"),
                ("acme-practice-packet/inputs/updates.md", "UP-1"),
                ("acme-practice-packet/inputs/updates.md", "UP-2"),
                ("acme-practice-packet/inputs/updates.md", "UP-3"),
            )
        ],
        "unsupported_claims": ["delivery date", "achieved 25% improvement"],
    }


def draft_weekly(evidence: Dict[str, object]) -> str:
    issue = evidence["issue"]
    decision = evidence["decision"]
    contract = evidence["data_contract_issue"]
    scope = evidence["scope_decision"]
    capacity = evidence["capacity"]
    status_conflicts = evidence["status_conflicts"]
    assert isinstance(issue, dict) and isinstance(decision, dict)
    assert isinstance(contract, dict) and isinstance(scope, dict)
    assert isinstance(capacity, list)
    assert isinstance(status_conflicts, list)

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
    conflict_text = (
        "Explicit status conflict between GH-41 and DEC-12 requires PM review. "
        if status_conflicts else ""
    )
    stale = [row["team"] for row in capacity if row["stale"]]
    capacity_source = capacity[0]["source"]
    capacity_text = (
        f"Capacity snapshots are stale for {', '.join(stale)} ({capacity_source})."
        if stale
        else (
            "The fictional test capacity snapshot is within the exercise freshness limit "
            f"({capacity_source}); it does not update Acme's shared capacity record."
            if capacity_source.startswith("workshop/fixtures/")
            else "Capacity snapshots are within the exercise freshness limit."
        )
    )
    if capacity_source.startswith("workshop/fixtures/"):
        capacity_followup = (
            "The November 5 CTO update said allocations were not confirmed (UP-3); "
            "the newer fictional test snapshot records confirmed capacity. Obtain "
            "the formal decision before a simulated forecast, and confirm real "
            "allocations separately before any live forecast (DEC-12, UP-3)."
        )
    else:
        capacity_followup = (
            "The CTO says new allocations are not yet confirmed (UP-3). Obtain "
            "the formal decision and current capacity before a delivery forecast "
            "(DEC-12, UP-3)."
        )
    return (
        "# Weekly management status — draft\n\n"
        f"{position} Independent interface sizing is in progress (GH-42, UP-2). "
        f"Alpha's data contract issue is {contract['status']} (GH-43). "
        f"Proof-of-concept scope is {scope['status']} (DEC-13), which does not "
        "settle the missing-value definition. "
        f"{approval} {conflict_text}{capacity_text} {capacity_followup} The supplied inputs "
        "establish no delivery date or achieved 25% improvement "
        "(GH-41, DEC-12, DEC-13, UP-1–UP-3).\n\n"
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
