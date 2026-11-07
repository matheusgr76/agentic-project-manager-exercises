"""Assess fictional Acme risk signals without external calls."""

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
ASSESSMENT_DATE = date(2026, 11, 9)
MAX_AGE_DAYS = 7
REQUIRED_TEAMS = 3


def read_signals(path: Path, scenario: str) -> List[Dict[str, str]]:
    """Load and validate one scenario from the local CSV."""
    try:
        with path.open(newline="", encoding="utf-8") as source:
            rows = list(csv.DictReader(source))
    except OSError as error:
        LOGGER.error("Signal read failed: %s", error)
        raise

    required = {
        "scenario", "id", "source", "as_of", "team", "signal",
        "status", "release", "dependency",
    }
    if not rows or not required.issubset(rows[0]):
        raise ValueError("Signal CSV is empty or missing required columns")

    selected = [row for row in rows if row["scenario"] == scenario]
    if not selected:
        raise ValueError(f"Unknown scenario: {scenario}")
    for row in selected:
        date.fromisoformat(row["as_of"])
        if row["status"] not in {"OPEN", "RESOLVED"}:
            raise ValueError(f"Invalid status for {row['id']}")
    return selected


def validate_investigation(path: Optional[Path]) -> List[str]:
    """Accept only an unresolved Chapter 7 handoff as extra context."""
    if path is None:
        return []
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        LOGGER.error("Chapter 7 handoff read failed: %s", error)
        raise ValueError("Cannot read Chapter 7 investigation") from error
    if (
        record.get("classification") != "UNRESOLVED"
        or "GH-41" not in record.get("evidence_references", [])
        or "DEC-12" not in record.get("evidence_references", [])
    ):
        raise ValueError("Chapter 7 handoff must cite unresolved GH-41 and DEC-12")
    return [
        reference for reference in record["evidence_references"]
        if reference in {"GH-41", "DEC-12"}
    ]


def assess(rows: List[Dict[str, str]], handoff_refs: List[str]) -> Dict[str, object]:
    """Classify a possible pattern while keeping uncertainty visible."""
    current = []
    excluded = []
    for row in rows:
        age = (ASSESSMENT_DATE - date.fromisoformat(row["as_of"])).days
        if row["status"] == "OPEN" and 0 <= age <= MAX_AGE_DAYS:
            current.append(row)
        else:
            excluded.append({"id": row["id"], "reason": "resolved or outside seven-day window"})

    groups: Dict[tuple[str, str], List[Dict[str, str]]] = {}
    for row in current:
        groups.setdefault((row["release"], row["dependency"]), []).append(row)
    candidates = [
        group for group in groups.values()
        if len({row["team"] for row in group}) >= REQUIRED_TEAMS
    ]
    evidence = candidates[0] if candidates else current
    pattern = bool(candidates)
    return {
        "assessment_date": ASSESSMENT_DATE.isoformat(),
        "classification": "EMERGING_RISK_FOR_REVIEW" if pattern else "INSUFFICIENT_EVIDENCE",
        "risk_statement": (
            "R1 integration and testing may miss the planned window if the v2 "
            "data contract and test environment are not ready."
        ) if pattern else None,
        "evidence_references": [row["id"] for row in evidence],
        "evidence_signals": [
            {
                "id": row["id"], "source": row["source"], "as_of": row["as_of"],
                "team": row["team"], "status": row["status"],
                "dependency": row["dependency"],
            }
            for row in evidence
        ],
        "chapter_7_context": handoff_refs,
        "excluded_signals": excluded,
        "evidence_quality": (
            "three current cross-team records; dates and ownership still require confirmation"
            if pattern else "too few current independent open signals"
        ),
        "alternative_explanation": (
            "The teams may recover time or use a separate test environment; "
            "the records do not resolve that."
        ),
        "proposed_mitigation": (
            "Ask Alpha, Bravo, and Charlie to validate the integration sequence "
            "and a fallback test slot."
        ) if pattern else None,
        "pm_question": (
            "What are the confirmed contract approval and environment-ready dates?"
            if pattern else "Are there newer records that change these signals?"
        ),
        "probability": "not estimated",
        "executed_action": "wrote local analysis only",
        "stop_reason": "human_review_required" if pattern else "insufficient_evidence",
    }


def unavailable_result(scenario: str) -> Dict[str, object]:
    """Stop visibly when the required fictional signal source is absent."""
    return {
        "assessment_date": ASSESSMENT_DATE.isoformat(),
        "scenario": scenario,
        "classification": "INSUFFICIENT_EVIDENCE",
        "evidence_references": [],
        "evidence_signals": [],
        "chapter_7_context": [],
        "evidence_quality": "required signal source unavailable",
        "risk_statement": None,
        "probability": "not estimated",
        "executed_action": "wrote local analysis only",
        "stop_reason": "evidence_unavailable",
    }


def run(scenario: str, output_dir: Path, investigation: Optional[Path] = None) -> Dict[str, object]:
    """Write one local analysis for a selected fictional scenario."""
    try:
        rows = read_signals(HERE / "signals.csv", scenario)
    except FileNotFoundError:
        result = unavailable_result(scenario)
    else:
        result = assess(rows, validate_investigation(investigation))
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "analysis.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    LOGGER.info("Scenario %s: %s", scenario, result["classification"])
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", choices=("a", "b", "c"), default="a")
    parser.add_argument("--investigation", type=Path)
    arguments = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    result = run(arguments.scenario, HERE / "outputs" / arguments.scenario, arguments.investigation)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

