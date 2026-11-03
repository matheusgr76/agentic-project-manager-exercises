"""Gate a fictional Command Center run for freshness, completeness, and replay."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import logging
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Dict, List


LOGGER = logging.getLogger(__name__)
HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]


def read_json(path: Path) -> Dict[str, object]:
    """Read a required JSON object with a visible I/O failure."""
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        LOGGER.error("Cannot read %s: %s", path, error)
        raise ValueError(f"Cannot read JSON object: {path}") from error
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return value


def case_row(path: Path, case: str) -> Dict[str, str]:
    """Select one explicit fictional run case."""
    try:
        with path.open(encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream))
    except OSError as error:
        LOGGER.error("Cannot read cases: %s", error)
        raise ValueError(f"Cannot read cases: {path}") from error
    matches = [row for row in rows if row.get("case") == case]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one case: {case}")
    return matches[0]


def validated_inputs(
    case: Dict[str, str], config: Dict[str, object], model: Dict[str, object]
) -> tuple[datetime, date, int, int]:
    """Reject missing dates, invalid limits, and unsupported case fields."""
    if not case.get("run_id") or case.get("source_status") not in {"OK", "PARTIAL"}:
        raise ValueError("Case requires run ID and OK or PARTIAL source status")
    try:
        run_at = datetime.fromisoformat(case["run_at_utc"].replace("Z", "+00:00"))
        if run_at.tzinfo is None or run_at.utcoffset().total_seconds() != 0:
            raise ValueError("Run time must be UTC")
        risk_date = date.fromisoformat(model["source_dates"]["risk"])
        attempt = int(case["attempt"])
        max_attempts = config["max_attempts"]
        max_age = config["max_risk_age_days"]
    except (KeyError, TypeError, AttributeError, ValueError) as error:
        raise ValueError("Invalid date, attempt, or source_dates.risk") from error
    if (type(max_attempts) is not int or type(max_age) is not int
            or max_attempts < 1 or max_age < 0 or attempt < 1):
        raise ValueError("Attempt and policy limits must be valid integers")
    if model.get("state") != "REVIEW_REQUIRED" or model.get("publication") != "none":
        raise ValueError("Expected unpublished Chapter 11 Scenario A view model")
    return run_at, risk_date, attempt, max_attempts


def evaluate(
    case: Dict[str, str], config: Dict[str, object], model: Dict[str, object],
    ledger: Dict[str, object],
) -> Dict[str, object]:
    """Return one inspectable state without mutating the inputs."""
    run_at, risk_date, attempt, max_attempts = validated_inputs(case, config, model)
    age_days = (run_at.date() - risk_date).days
    if age_days < 0:
        raise ValueError("Risk source date cannot be after run date")
    digest = hashlib.sha256(
        json.dumps(model, sort_keys=True).encode("utf-8")
    ).hexdigest()
    if attempt > max_attempts:
        state, reason = "BLOCKED_ATTEMPT_LIMIT", "Attempt exceeds configured limit"
    elif case["source_status"] != "OK":
        state, reason = "BLOCKED_SOURCE", "Simulated retrieval is partial"
    elif age_days > config["max_risk_age_days"]:
        state, reason = "BLOCKED_STALE", "Risk source exceeds allowed age"
    elif case["run_id"] in ledger:
        prior = ledger[case["run_id"]]
        state = "ALREADY_PROCESSED" if prior["model_sha256"] == digest else "INPUT_CHANGED_REVIEW"
        reason = "Successful run ID already exists"
    else:
        state, reason = "READY_FOR_PM_REVIEW", "Local gate passed; human review required"
    return {
        "case": case["case"], "run_id": case["run_id"], "attempt": attempt,
        "run_at_utc": run_at.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source_status": case["source_status"], "risk_source_date": risk_date.isoformat(),
        "risk_age_days": age_days, "state": state, "reason": reason,
        "model_sha256": digest, "publication": "none",
    }


def run(case_name: str, output_dir: Path, from_prior_outputs: bool = False) -> Dict[str, object]:
    """Evaluate a case and persist its health, audit, and success ledger."""
    case = case_row(HERE / "cases.csv", case_name)
    config = read_json(HERE / "config.json")
    model_path = (
        REPO_ROOT / "chapters/11-pm-command-center/example/outputs/a/view-model.json"
        if from_prior_outputs else HERE / "fixtures/view-model-a.json"
    )
    model = read_json(model_path)
    ledger_path = output_dir / "ledger.json"
    ledger = read_json(ledger_path) if ledger_path.exists() else {}
    result = evaluate(case, config, model, ledger)
    if result["state"] == "READY_FOR_PM_REVIEW":
        ledger[result["run_id"]] = {
            "model_sha256": result["model_sha256"],
            "first_review_ready_at_utc": result["run_at_utc"],
        }
    try:
        case_dir = output_dir / case_name
        case_dir.mkdir(parents=True, exist_ok=True)
        (case_dir / "health.json").write_text(
            json.dumps(result, indent=2) + "\n", encoding="utf-8"
        )
        ledger_path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
        with (output_dir / "attempts.jsonl").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(result, sort_keys=True) + "\n")
    except OSError as error:
        LOGGER.error("Cannot write local run record: %s", error)
        raise
    LOGGER.info("Case %s, run %s: %s", case_name, result["run_id"], result["state"])
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=("a", "b", "b_recovered", "c"), required=True)
    parser.add_argument("--from-prior-outputs", action="store_true")
    arguments = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    result = run(arguments.case, HERE / "outputs", arguments.from_prior_outputs)
    print(f"Run health: {result['state']}")


if __name__ == "__main__":
    main()
