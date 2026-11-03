"""Evaluate a fictional Acme pilot with full task and operating costs."""

from __future__ import annotations

import argparse
import csv
import json
import logging
from pathlib import Path
from typing import Dict, List


LOGGER = logging.getLogger(__name__)
HERE = Path(__file__).resolve().parent
MINUTE_PER_HOUR = 60


def read_samples(path: Path) -> List[Dict[str, str]]:
    """Read paired fictional tasks with a visible file failure."""
    try:
        with path.open(encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream))
    except OSError as error:
        LOGGER.error("Cannot read sample file: %s", error)
        raise ValueError(f"Cannot read sample file: {path}") from error
    if not rows:
        raise ValueError("Sample file is empty")
    return rows


def read_config(path: Path) -> Dict[str, object]:
    """Read the explicit projection assumptions."""
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        LOGGER.error("Cannot read cost assumptions: %s", error)
        raise ValueError(f"Cannot read cost assumptions: {path}") from error
    if not isinstance(value, dict):
        raise ValueError("Cost assumptions must be a JSON object")
    return value


def validate_config(config: Dict[str, object]) -> None:
    """Reject missing, negative, and noninteger cost settings."""
    positive = ("monthly_task_volume", "labor_value_per_hour", "evaluation_months")
    nonnegative = ("one_time_build_cost", "monthly_maintenance_cost",
                   "monthly_infrastructure_cost")
    for key in positive + nonnegative:
        value = config.get(key)
        minimum = 1 if key in positive else 0
        if type(value) is not int or value < minimum:
            raise ValueError(f"Invalid cost assumption: {key}")
    if not config.get("currency") or not config.get("counterfactual_accept_sample_id"):
        raise ValueError("Currency and counterfactual sample ID are required")


def measured_row(row: Dict[str, str], accepted: bool) -> Dict[str, object]:
    """Count all assisted work, including manual fallback for a rejected draft."""
    if not row.get("sample_id") or not row.get("task"):
        raise ValueError("Sample ID and task are required")
    if row.get("pilot_accepted") not in {"yes", "no"}:
        raise ValueError(f"Invalid acceptance for {row['sample_id']}")
    if row.get("false_alert") not in {"yes", "no"}:
        raise ValueError(f"Invalid false-alert flag for {row['sample_id']}")
    keys = ("baseline_minutes", "operator_minutes", "review_minutes", "correction_minutes")
    try:
        minutes = {key: int(row[key]) for key in keys}
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError(f"Invalid minutes for {row['sample_id']}") from error
    if minutes["baseline_minutes"] < 1 or any(minutes[key] < 0 for key in keys):
        raise ValueError(f"Negative or zero task time: {row['sample_id']}")
    fallback = 0 if accepted else minutes["baseline_minutes"]
    assisted = sum(minutes[key] for key in keys[1:]) + fallback
    return {
        "sample_id": row["sample_id"], "task": row["task"],
        "baseline_minutes": minutes["baseline_minutes"],
        "assisted_minutes": assisted, "fallback_minutes": fallback,
        "net_minutes_saved": minutes["baseline_minutes"] - assisted,
        "pilot_accepted": accepted, "false_alert": row["false_alert"] == "yes",
    }


def evaluate(
    rows: List[Dict[str, str]], config: Dict[str, object], scenario: str
) -> Dict[str, object]:
    """Compute sample and projected value without claiming a delivery outcome."""
    validate_config(config)
    if scenario not in {"recorded", "counterfactual"}:
        raise ValueError("Unsupported evaluation scenario")
    ids = [row.get("sample_id") for row in rows]
    if len(set(ids)) != len(ids):
        raise ValueError("Sample IDs must be unique")
    target = config["counterfactual_accept_sample_id"]
    target_rows = [row for row in rows if row.get("sample_id") == target]
    if len(target_rows) != 1 or target_rows[0].get("pilot_accepted") != "no":
        raise ValueError("Counterfactual target must be one rejected sample")
    details = [measured_row(
        row, row.get("pilot_accepted") == "yes" or (
            scenario == "counterfactual" and row["sample_id"] == target
        )
    ) for row in rows]
    baseline = sum(item["baseline_minutes"] for item in details)
    assisted = sum(item["assisted_minutes"] for item in details)
    saved = baseline - assisted
    monthly_value = round(
        saved * config["monthly_task_volume"] / len(details)
        * config["labor_value_per_hour"] / MINUTE_PER_HOUR, 2
    )
    recurring = config["monthly_maintenance_cost"] + config["monthly_infrastructure_cost"]
    total_cost = config["one_time_build_cost"] + recurring * config["evaluation_months"]
    if total_cost == 0:
        raise ValueError("Total cost must be positive for return calculation")
    net_value = round(monthly_value * config["evaluation_months"] - total_cost, 2)
    monthly_margin = monthly_value - recurring
    payback = (
        round(config["one_time_build_cost"] / monthly_margin, 1)
        if monthly_margin > 0 else None
    )
    return {
        "scenario": scenario, "evidence_level": "FICTIONAL_SAMPLE_PROJECTION",
        "currency": config["currency"], "sample_count": len(details),
        "pilot_outputs_accepted": sum(item["pilot_accepted"] for item in details),
        "false_alerts": sum(item["false_alert"] for item in details),
        "sample_baseline_minutes": baseline, "sample_assisted_minutes": assisted,
        "sample_net_minutes_saved": saved,
        "projected_monthly_task_volume": config["monthly_task_volume"],
        "projected_monthly_labor_value": monthly_value,
        "monthly_recurring_cost": recurring, "one_time_build_cost": config["one_time_build_cost"],
        "evaluation_months": config["evaluation_months"],
        "total_cost": total_cost, "projected_net_value": net_value,
        "projected_return_percent": round(net_value / total_cost * 100, 1),
        "simple_payback_months": payback,
        "delivery_improvement": "NOT_MEASURED", "details": details,
    }


def run(scenario: str, output_dir: Path) -> Dict[str, object]:
    """Write an inspectable local result for one evaluation scenario."""
    result = evaluate(
        read_samples(HERE / "work-samples.csv"),
        read_config(HERE / "cost-assumptions.json"), scenario,
    )
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / f"{scenario}.json").write_text(
            json.dumps(result, indent=2) + "\n", encoding="utf-8"
        )
    except OSError as error:
        LOGGER.error("Cannot write evaluation result: %s", error)
        raise
    LOGGER.info("Calculated %s illustrative value: %s", scenario, result["projected_net_value"])
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", choices=("recorded", "counterfactual"), required=True)
    arguments = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    result = run(arguments.scenario, HERE / "outputs")
    print(f"Illustrative net value: {result['projected_net_value']} {result['currency']}")


if __name__ == "__main__":
    main()
