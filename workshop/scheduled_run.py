"""Run four fixed, local Chapter 6 reporting-policy cases."""

from __future__ import annotations

import argparse
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict

from workshop.config import (
    CASE_MATRIX,
    OUTPUTS_DIR,
    REPOSITORY_ROOT,
    TARGET_DECISION_ID,
    TARGET_ISSUE_ID,
)
from workshop.files import read_csv, write_json, write_text
from workshop.report_builder import build_evidence, draft_weekly


LOGGER = logging.getLogger(__name__)
CAPACITY_FIXTURE = REPOSITORY_ROOT / "workshop" / "fixtures" / "current-capacity.csv"
CAPACITY_SOURCE = "workshop/fixtures/current-capacity.csv"
CASES = ("A", "B", "C", "D")


def case_row(case: str) -> Dict[str, str]:
    rows = read_csv(
        CASE_MATRIX,
        [
            "case", "run_at_utc", "github_available", "gh41_status",
            "dec12_status", "capacity_snapshot_date", "capacity_state",
            "source_comment", "expected_status",
        ],
    )
    for row in rows:
        if row["case"] == case:
            return row
    raise ValueError(f"Unknown scheduled-run case: {case}")


def classify(row: Dict[str, str]) -> str:
    if row["github_available"] != "true":
        return "INCOMPLETE"
    if row["gh41_status"] == "IN_PROGRESS" and row["dec12_status"] == "PENDING":
        return "REVIEW_REQUIRED"
    return "COMPLETE"


def new_result(row: Dict[str, str], status: str) -> Dict[str, object]:
    return {
        "case": row["case"],
        "run_at_utc": row["run_at_utc"],
        "status": status,
        "publication": "PM approval required; nothing sent",
        "source_inventory": {
            "github_issue": "available" if row["github_available"] == "true" else "failed",
            "decision": row["dec12_status"] if status != "INCOMPLETE" else "not read",
            "capacity_fixture": CAPACITY_SOURCE if status != "INCOMPLETE" else "not read",
            "capacity_snapshot_date": (
                row["capacity_snapshot_date"] if status != "INCOMPLETE" else None
            ),
        },
        "findings": [],
        "artifacts": [],
    }


def build_case_evidence(
    row: Dict[str, str],
    run_time: datetime,
    result: Dict[str, object],
) -> Dict[str, object]:
    capacity = read_csv(
        CAPACITY_FIXTURE,
        ["team", "allocation", "status", "snapshot_date"],
    )
    if any(
        item["snapshot_date"] != row["capacity_snapshot_date"]
        or item["status"] != row["capacity_state"]
        for item in capacity
    ):
        raise ValueError("Capacity fixture does not match the case matrix")
    issue = {
        "id": TARGET_ISSUE_ID,
        "status": row["gh41_status"],
        "updated_at": run_time.date().isoformat(),
    }
    if row["source_comment"]:
        issue["comment"] = row["source_comment"]
        result["untrusted_comment_ignored"] = True
    return build_evidence(
        issue_override=issue,
        capacity_override=capacity,
        report_date=run_time.date(),
        capacity_source=CAPACITY_SOURCE,
    )


def write_review(
    row: Dict[str, str],
    output_dir: Path,
    result: Dict[str, object],
) -> None:
    write_json(
        output_dir / "exception.json",
        {
            "exception_id": TARGET_ISSUE_ID,
            "issue_status": row["gh41_status"],
            "decision_id": TARGET_DECISION_ID,
            "decision_status": row["dec12_status"],
            "source": "Chapter 6 fictional case matrix",
        },
    )
    write_text(
        output_dir / "clarification.md",
        "# Clarification draft\n\nWhat work has started on GH-41, and is "
        "DEC-12 formally approved for the version Bravo needs?\n",
    )
    result["findings"] = ["GH-41 is in progress while DEC-12 is pending."]
    result["artifacts"] = ["evidence.json", "exception.json", "clarification.md"]


def write_drafts(
    evidence: Dict[str, object],
    output_dir: Path,
    result: Dict[str, object],
) -> None:
    write_text(output_dir / "management-draft.md", draft_weekly(evidence))
    write_text(
        output_dir / "engineering-draft.md",
        "# Engineering coordination — draft\n\nGH-41 remains blocked "
        "on pending DEC-12. Confirm the decision before revising the "
        "full integration estimate. PM approval is required before use.\n",
    )
    result["findings"] = ["GH-41 and DEC-12 have consistent states."]
    result["artifacts"] = [
        "evidence.json", "management-draft.md", "engineering-draft.md",
    ]


def run(case: str, output_dir: Path) -> Dict[str, object]:
    row = case_row(case)
    status = classify(row)
    if status != row["expected_status"]:
        raise ValueError("Case matrix expectation conflicts with policy")
    run_time = datetime.fromisoformat(row["run_at_utc"].replace("Z", "+00:00"))
    result = new_result(row, status)
    if status == "INCOMPLETE":
        result["findings"] = ["Required GitHub issue retrieval failed."]
        write_text(
            output_dir / "alert.md",
            "# Local alert\n\nRequired issue source unavailable. PM review needed.\n",
        )
        result["artifacts"] = ["alert.md"]
    else:
        evidence = build_case_evidence(row, run_time, result)
        write_json(output_dir / "evidence.json", evidence)
        if status == "REVIEW_REQUIRED":
            write_review(row, output_dir, result)
        else:
            write_drafts(evidence, output_dir, result)

    write_json(output_dir / "run.json", result)
    LOGGER.info("Scheduled case %s finished with %s", case, status)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=CASES, default="A")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    output_dir = args.output_dir or OUTPUTS_DIR / "ch6" / args.case.lower()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    try:
        result = run(args.case, output_dir)
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, f"Scheduled run stopped: {error}\n")
    print(f"Chapter 6 case {args.case}: {result['status']} — {output_dir}")


if __name__ == "__main__":
    main()
