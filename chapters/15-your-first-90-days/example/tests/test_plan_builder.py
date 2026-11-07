"""Behavior tests for the Chapter 15 fictional pilot plan."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from typing import Dict, List, Tuple


HERE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("plan_builder", HERE / "plan_builder.py")
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


def inputs(case: str) -> Tuple[Dict[str, object], Dict[str, object], List[Dict[str, object]]]:
    """Load independent local inputs for test variations."""
    pilots = BUILDER.read_json(HERE / "fixtures/pilot-cases.json")
    value = BUILDER.read_json(HERE / "fixtures/value-recorded.json")
    gates = BUILDER.read_json(HERE / "phase-gates.json")
    return pilots[case], value, gates


class PilotPlanTests(unittest.TestCase):
    def test_bounded_case_is_draft_with_inclusive_phase_dates(self) -> None:
        pilot, value, gates = inputs("a")
        plan = BUILDER.build_plan(pilot, value, gates)
        self.assertEqual(plan["state"], "PLAN_READY_FOR_HUMAN_REVIEW")
        self.assertEqual(plan["blocking_gaps"], [])
        self.assertEqual(
            [(item["start_date"], item["end_date"]) for item in plan["phases"]],
            [
                ("2026-11-16", "2026-12-15"),
                ("2026-12-16", "2027-01-14"),
                ("2027-01-15", "2027-02-13"),
            ],
        )
        self.assertEqual(plan["value_context"]["projected_net_value"], -3216)
        self.assertEqual(plan["value_context"]["delivery_improvement"], "NOT_MEASURED")
        self.assertEqual(plan["scale_decision"], "NO_AUTOMATIC_EXPANSION")
        self.assertEqual(plan["execution"], "none")
        self.assertIn("dated approved source", plan["accepted_output_rule"])

    def test_missing_acceptance_rule_blocks_the_plan(self) -> None:
        pilot, value, gates = inputs("a")
        pilot.pop("accepted_output_rule")
        plan = BUILDER.build_plan(pilot, value, gates)
        self.assertEqual(plan["state"], "PLAN_BLOCKED")
        self.assertIn("ACCEPTANCE_RULE_MISSING", plan["blocking_gaps"])

    def test_missing_baseline_and_target_block_the_plan(self) -> None:
        for case, gap in (("b", "BASELINE_MISSING"), ("d", "TARGET_MISSING")):
            pilot, value, gates = inputs(case)
            plan = BUILDER.build_plan(pilot, value, gates)
            self.assertEqual(plan["state"], "PLAN_BLOCKED")
            self.assertIn(gap, plan["blocking_gaps"])

    def test_write_scope_and_missing_stop_rule_block_the_plan(self) -> None:
        for case, gap in (("c", "ACCESS_NOT_READ_ONLY_APPROVED"),
                          ("e", "STOP_RULE_MISSING")):
            pilot, value, gates = inputs(case)
            plan = BUILDER.build_plan(pilot, value, gates)
            self.assertEqual(plan["state"], "PLAN_BLOCKED")
            self.assertIn(gap, plan["blocking_gaps"])

    def test_human_review_is_required_even_with_other_fields_complete(self) -> None:
        pilot, value, gates = inputs("a")
        pilot["human_review"] = False
        plan = BUILDER.build_plan(pilot, value, gates)
        self.assertIn("REVIEW_MISSING", plan["blocking_gaps"])
        self.assertEqual(plan["state"], "PLAN_BLOCKED")

    def test_invalid_start_date_and_untrusted_value_claim_fail(self) -> None:
        pilot, value, gates = inputs("a")
        pilot["start_date"] = "soon"
        with self.assertRaisesRegex(ValueError, "ISO start date"):
            BUILDER.build_plan(pilot, value, gates)
        pilot, value, gates = inputs("a")
        value["delivery_improvement"] = "PROVEN"
        with self.assertRaisesRegex(ValueError, "fictional recorded"):
            BUILDER.build_plan(pilot, value, gates)

    def test_phase_gap_and_missing_baseline_value_fail_visibly(self) -> None:
        pilot, value, gates = inputs("a")
        gates[1]["first_day"] = 32
        with self.assertRaisesRegex(ValueError, "without gaps"):
            BUILDER.build_plan(pilot, value, gates)
        pilot, value, gates = inputs("a")
        pilot["baseline"]["sample_count"] = True
        self.assertIn("BASELINE_MISSING", BUILDER.build_plan(pilot, value, gates)["blocking_gaps"])

    def test_local_files_match_returned_plan_and_hide_no_action(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            plan = BUILDER.run("a", Path(directory))
            saved = json.loads((Path(directory) / "a/plan.json").read_text(encoding="utf-8"))
            markdown = (Path(directory) / "a/plan.md").read_text(encoding="utf-8")
            self.assertEqual(saved, plan)
            self.assertIn("Target: at least 9 accepted of 10", markdown)
            self.assertIn("Accepted-output rule: A PM accepts", markdown)
            self.assertIn("Stop conditions: missing source date", markdown)
            self.assertIn("No automatic expansion, execution, or publication", markdown)
            self.assertEqual(plan["publication"], "none")


if __name__ == "__main__":
    unittest.main()
