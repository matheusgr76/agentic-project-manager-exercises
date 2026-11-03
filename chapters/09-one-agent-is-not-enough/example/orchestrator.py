"""Coordinate three fictional Acme outputs without external actions."""

from __future__ import annotations

import argparse
import json
import logging
from datetime import date, datetime
from pathlib import Path
from typing import Dict, List, Optional


LOGGER = logging.getLogger(__name__)
HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
SOURCE_NAMES = ("dependency", "risk", "report")


def read_artifact(path: Path, name: str) -> Optional[Dict[str, object]]:
    """Read one local specialist artifact, allowing an absent input to be reported."""
    try:
        content = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        LOGGER.warning("Missing %s artifact: %s", name, path)
        return None
    except OSError as error:
        LOGGER.error("Cannot read %s artifact: %s", name, error)
        raise

    try:
        record = json.loads(content)
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON in {name} artifact: {path}") from error
    if not isinstance(record, dict):
        raise ValueError(f"Expected a JSON object for {name}: {path}")
    LOGGER.info("Read %s artifact: %s", name, path)
    return record


def validate_artifacts(records: Dict[str, Dict[str, object]]) -> None:
    """Reject artifacts that cannot support a traceable handoff."""
    required = {
        "dependency": ("classification", "evidence_references", "stop_reason"),
        "risk": ("classification", "evidence_references", "assessment_date"),
        "report": ("status", "run_at_utc", "findings", "publication"),
    }
    for name, fields in required.items():
        if any(field not in records[name] for field in fields):
            raise ValueError(f"{name} artifact is missing required fields")
    for name in ("dependency", "risk"):
        if not isinstance(records[name]["evidence_references"], list):
            raise ValueError(f"{name} evidence_references must be a list")
    if not isinstance(records["report"]["findings"], list):
        raise ValueError("report findings must be a list")
    date.fromisoformat(str(records["risk"]["assessment_date"]))
    datetime.fromisoformat(str(records["report"]["run_at_utc"]).replace("Z", "+00:00"))


def coordinate(records: Dict[str, Optional[Dict[str, object]]]) -> Dict[str, object]:
    """Join source claims, then stop at missing evidence or disagreement."""
    missing = [name for name in SOURCE_NAMES if records[name] is None]
    if missing:
        return {
            "status": "INCOMPLETE",
            "missing_artifacts": missing,
            "reason": "A required specialist output is unavailable.",
            "executed_action": "local handoff only",
            "publication": "none",
        }

    complete = {name: records[name] for name in SOURCE_NAMES}
    validate_artifacts(complete)
    return review_handoff(
        complete["dependency"], complete["risk"], complete["report"]
    )


def review_handoff(
    dependency: Dict[str, object],
    risk: Dict[str, object],
    report: Dict[str, object],
) -> Dict[str, object]:
    """Keep each specialist claim distinct in the PM's review record."""
    dependency_refs = set(dependency["evidence_references"])
    risk_context = set(risk.get("chapter_7_context", []))
    report_mentions_pending = any(
        "DEC-12" in finding and "pending" in finding.lower()
        for finding in report["findings"]
    )
    conflict = dependency["classification"] == "RESOLVED" and report_mentions_pending
    return {
        "status": "CONFLICT" if conflict else "REVIEW_REQUIRED",
        "source_statuses": {
            "dependency": dependency["classification"],
            "risk": risk["classification"],
            "report": report["status"],
        },
        "source_dates": {
            "dependency": "not recorded",
            "risk": risk["assessment_date"],
            "report": report["run_at_utc"],
        },
        "shared_references": sorted(dependency_refs & risk_context),
        "risk_signal_references": risk["evidence_references"],
        "disagreement": (
            "Dependency says resolved while the report still says DEC-12 pending. "
            "The source chronology must be checked."
        ) if conflict else None,
        "freshness_note": freshness_note(risk, report),
        "pm_question": (
            "Which DEC-12 status is current, and when did it change?"
            if conflict else "Are the contract and environment dates still current?"
        ),
        "proposed_action": (
            "Reconcile DEC-12 with its owner before drafting a status conclusion."
            if conflict else (
                "Ask owners to refresh the risk signals and confirm a fallback sequence."
            )
        ),
        "executed_action": "local handoff only",
        "publication": "none",
        "decision_owner": "Acme PM",
    }


def freshness_note(risk: Dict[str, object], report: Dict[str, object]) -> str:
    """Describe a known date gap without inventing source chronology."""
    risk_date = date.fromisoformat(str(risk["assessment_date"]))
    report_date = datetime.fromisoformat(
        str(report["run_at_utc"]).replace("Z", "+00:00")
    ).date()
    if risk_date < report_date:
        return (
            "Risk assessment predates the report; confirm its signals again before "
            "using it as current. Dependency investigation has no dated run field."
        )
    return "Confirm all source dates before publication."


def scenario_paths(scenario: str, from_prior_outputs: bool) -> Dict[str, Path]:
    """Select committed fixtures or the reader's generated chapter outputs."""
    if from_prior_outputs:
        if scenario != "a":
            raise ValueError("Prior-output handoff supports Scenario A only")
        return {
            "dependency": (
                REPO_ROOT
                / "chapters/07-dependency-agent/example/outputs/a/investigation.json"
            ),
            "risk": REPO_ROOT / "chapters/08-risk-analyst/example/outputs/a/analysis.json",
            "report": REPO_ROOT / "workshop/outputs/ch6/c/run.json",
        }
    fixture = HERE / "fixtures"
    return {
        "dependency": fixture / (
            "dependency-conflict.json" if scenario == "b" else "dependency-a.json"
        ),
        "risk": fixture / ("missing-risk.json" if scenario == "c" else "risk-a.json"),
        "report": fixture / "report-c.json",
    }


def run(scenario: str, output_dir: Path, from_prior_outputs: bool = False) -> Dict[str, object]:
    """Save a reviewable local handoff for one fictional scenario."""
    paths = scenario_paths(scenario, from_prior_outputs)
    records = {name: read_artifact(path, name) for name, path in paths.items()}
    result = coordinate(records)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "handoff.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    LOGGER.info("Coordinated scenario %s: %s", scenario, result["status"])
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", choices=("a", "b", "c"), default="a")
    parser.add_argument("--from-prior-outputs", action="store_true")
    arguments = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    result = run(
        arguments.scenario,
        HERE / "outputs" / arguments.scenario,
        arguments.from_prior_outputs,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
