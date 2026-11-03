"""Behavior tests for Chapter 14's fictional pilot evaluation."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from typing import Dict, List, Tuple


HERE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("evaluator", HERE / "evaluator.py")
EVALUATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EVALUATOR)


def inputs() -> Tuple[List[Dict[str, str]], Dict[str, object]]:
    """Load independent input objects for scenario and edge-case checks."""
    return (
        EVALUATOR.read_samples(HERE / "work-samples.csv"),
        EVALUATOR.read_config(HERE / "cost-assumptions.json"),
    )


class EvaluatorTests(unittest.TestCase):
    def test_recorded_case_counts_rejected_fallback_and_all_costs(self) -> None:
        rows, config = inputs()
        result = EVALUATOR.evaluate(rows, config, "recorded")
        rejected = next(item for item in result["details"] if item["sample_id"] == "F-03")
        self.assertEqual(rejected["fallback_minutes"], 75)
        self.assertEqual(rejected["assisted_minutes"], 150)
        self.assertEqual(result["sample_baseline_minutes"], 395)
        self.assertEqual(result["sample_assisted_minutes"], 352)
        self.assertEqual(result["sample_net_minutes_saved"], 43)
        self.assertEqual(result["pilot_outputs_accepted"], 5)
        self.assertEqual(result["false_alerts"], 1)
        self.assertEqual(result["projected_monthly_labor_value"], 172)
        self.assertEqual(result["monthly_recurring_cost"], 240)
        self.assertEqual(result["total_cost"], 5280)
        self.assertEqual(result["projected_net_value"], -3216)
        self.assertIsNone(result["simple_payback_months"])
        self.assertEqual(result["delivery_improvement"], "NOT_MEASURED")

    def test_counterfactual_changes_only_acceptance_and_is_labeled(self) -> None:
        rows, config = inputs()
        recorded = EVALUATOR.evaluate(rows, config, "recorded")
        alternate = EVALUATOR.evaluate(rows, config, "counterfactual")
        self.assertEqual(alternate["evidence_level"], "FICTIONAL_SAMPLE_PROJECTION")
        self.assertEqual(alternate["sample_assisted_minutes"], 277)
        self.assertEqual(alternate["sample_net_minutes_saved"], 118)
        self.assertEqual(alternate["projected_monthly_labor_value"], 472)
        self.assertEqual(alternate["projected_net_value"], 384)
        self.assertEqual(alternate["projected_return_percent"], 7.3)
        self.assertEqual(alternate["simple_payback_months"], 10.3)
        self.assertEqual(recorded["details"][0], alternate["details"][0])
        self.assertEqual(alternate["delivery_improvement"], "NOT_MEASURED")

    def test_false_alert_review_time_is_not_added_twice(self) -> None:
        rows, config = inputs()
        result = EVALUATOR.evaluate(rows, config, "recorded")
        alert = next(item for item in result["details"] if item["sample_id"] == "F-06")
        self.assertTrue(alert["false_alert"])
        self.assertEqual(alert["assisted_minutes"], 55)

    def test_missing_or_negative_minutes_fail_visibly(self) -> None:
        rows, config = inputs()
        del rows[0]["review_minutes"]
        with self.assertRaisesRegex(ValueError, "Invalid minutes"):
            EVALUATOR.evaluate(rows, config, "recorded")
        rows, config = inputs()
        rows[0]["review_minutes"] = "-2"
        with self.assertRaisesRegex(ValueError, "Negative or zero"):
            EVALUATOR.evaluate(rows, config, "recorded")

    def test_duplicate_id_and_invalid_acceptance_fail_visibly(self) -> None:
        rows, config = inputs()
        rows[1]["sample_id"] = rows[0]["sample_id"]
        with self.assertRaisesRegex(ValueError, "unique"):
            EVALUATOR.evaluate(rows, config, "recorded")
        rows, config = inputs()
        rows[0]["pilot_accepted"] = "maybe"
        with self.assertRaisesRegex(ValueError, "Invalid acceptance"):
            EVALUATOR.evaluate(rows, config, "recorded")

    def test_zero_cost_cannot_produce_return_percentage(self) -> None:
        rows, config = inputs()
        config["one_time_build_cost"] = 0
        config["monthly_maintenance_cost"] = 0
        config["monthly_infrastructure_cost"] = 0
        with self.assertRaisesRegex(ValueError, "Total cost"):
            EVALUATOR.evaluate(rows, config, "recorded")

    def test_run_writes_two_inspectable_scenarios(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            for scenario in ("recorded", "counterfactual"):
                result = EVALUATOR.run(scenario, output)
                saved = json.loads((output / f"{scenario}.json").read_text(encoding="utf-8"))
                self.assertEqual(saved, result)


if __name__ == "__main__":
    unittest.main()
