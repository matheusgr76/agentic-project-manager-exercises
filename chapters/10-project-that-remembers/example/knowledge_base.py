"""Query a small fictional project history with explicit source versions."""

from __future__ import annotations

import argparse
import csv
import json
import logging
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional


LOGGER = logging.getLogger(__name__)
HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
FIELDS = {
    "scenario", "event_id", "key", "value", "effective_at", "recorded_at",
    "review_by", "source_ref", "supersedes", "authority",
}
KEYS = ("DEC-12/v2", "GH-41", "R1/risk")
ASSESSMENT_DATES = {"a": "2026-11-12", "b": "2026-11-15", "c": "2026-11-15"}


def load_records(path: Path, scenario: str) -> List[Dict[str, str]]:
    """Read one scenario and verify dates, references, and local sources."""
    try:
        with path.open(newline="", encoding="utf-8") as source:
            reader = csv.DictReader(source)
            if not reader.fieldnames or not FIELDS.issubset(reader.fieldnames):
                raise ValueError("History CSV is missing required columns")
            rows = [row for row in reader if row["scenario"] == scenario]
    except OSError as error:
        LOGGER.error("History read failed: %s", error)
        raise

    if not rows:
        raise ValueError(f"Unknown or empty scenario: {scenario}")
    by_id = {row["event_id"]: row for row in rows}
    if len(by_id) != len(rows):
        raise ValueError("Duplicate event ID in scenario")
    for row in rows:
        if bool(row["effective_at"]) != bool(row["recorded_at"]):
            raise ValueError(f"Incomplete dates for {row['event_id']}")
        for field in ("effective_at", "recorded_at", "review_by"):
            if row[field]:
                date.fromisoformat(row[field])
        source_path = (REPO_ROOT / row["source_ref"]).resolve()
        if not source_path.is_relative_to(REPO_ROOT) or not source_path.is_file():
            raise ValueError(f"Unavailable local source for {row['event_id']}")
        older_id = row["supersedes"]
        if older_id and (
            older_id == row["event_id"]
            or older_id not in by_id
            or by_id[older_id]["key"] != row["key"]
        ):
            raise ValueError(f"Invalid supersedes link for {row['event_id']}")
    LOGGER.info("Loaded %s records for scenario %s", len(rows), scenario)
    return rows


def query_history(
    rows: List[Dict[str, str]], key: str, as_of: date
) -> Dict[str, object]:
    """Resolve a key as it was knowable on a chosen date."""
    matching = [row for row in rows if row["key"] == key]
    undated = [row for row in matching if not row["effective_at"]]
    known = [
        row for row in matching
        if row["effective_at"]
        and date.fromisoformat(row["effective_at"]) <= as_of
        and date.fromisoformat(row["recorded_at"]) <= as_of
    ]
    if not known:
        if undated:
            return undated_answer(key, undated)
        return {"key": key, "status": "UNKNOWN", "value": None, "sources": []}

    superseded = {row["supersedes"] for row in known if row["supersedes"]}
    current = [row for row in known if row["event_id"] not in superseded]
    sources = [
        {"event_id": row["event_id"], "source_ref": row["source_ref"]}
        for row in current
    ]
    if not current or len({row["value"] for row in current}) > 1:
        return {
            "key": key, "status": "CONFLICT", "value": None,
            "sources": sources, "superseded_events": sorted(superseded),
        }

    event = max(current, key=lambda row: (row["recorded_at"], row["event_id"]))
    needs_review = any(
        row["review_by"] and date.fromisoformat(row["review_by"]) < as_of
        for row in current
    )
    return {
        "key": key,
        "status": "NEEDS_REVALIDATION" if needs_review else "CURRENT",
        "value": event["value"],
        "effective_at": event["effective_at"],
        "recorded_at": event["recorded_at"],
        "review_by": event["review_by"] or None,
        "authority": event["authority"],
        "sources": sources,
        "superseded_events": sorted(superseded),
    }


def undated_answer(key: str, records: List[Dict[str, str]]) -> Dict[str, object]:
    """Expose undated evidence without assigning it a historical state."""
    return {
        "key": key,
        "status": "UNDATED_CONTEXT",
        "value": None,
        "sources": [
            {"event_id": row["event_id"], "source_ref": row["source_ref"]}
            for row in records
        ],
        "note": "Source has no effective or recorded date; no as-of claim is made.",
    }


def assess(
    scenario: str, as_of: date, output_dir: Path,
    history_path: Optional[Path] = None,
) -> Dict[str, object]:
    """Write a local time-specific answer without changing source history."""
    records = load_records(history_path or HERE / "records.csv", scenario)
    answers = {key: query_history(records, key, as_of) for key in KEYS}
    result = {
        "scenario": scenario,
        "as_of": as_of.isoformat(),
        "answers": answers,
        "decision_owner": "Acme PM and named decision approver",
        "executed_action": "local knowledge answer only",
        "publication": "none",
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "knowledge.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    LOGGER.info("Saved scenario %s knowledge answer", scenario)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", choices=tuple(ASSESSMENT_DATES), default="a")
    parser.add_argument("--as-of", help="Override fictional as-of date (YYYY-MM-DD)")
    arguments = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    as_of = date.fromisoformat(
        arguments.as_of or ASSESSMENT_DATES[arguments.scenario]
    )
    result = assess(arguments.scenario, as_of, HERE / "outputs" / arguments.scenario)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
