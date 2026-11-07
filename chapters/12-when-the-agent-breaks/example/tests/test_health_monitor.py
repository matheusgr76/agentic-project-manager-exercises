"""Behavior tests for the Chapter 12 fictional local run gate."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("health_monitor", HERE / "health_monitor.py")
MONITOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MONITOR)


class HealthMonitorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.output_dir = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_normal_run_requires_review_and_replay_is_idempotent(self) -> None:
        first = MONITOR.run("a", self.output_dir)
        repeat = MONITOR.run("a", self.output_dir)
        ledger = json.loads((self.output_dir / "ledger.json").read_text(encoding="utf-8"))
        self.assertEqual(first["state"], "READY_FOR_PM_REVIEW")
        self.assertEqual(first["risk_age_days"], 3)
        self.assertEqual(first["publication"], "none")
        self.assertEqual(repeat["state"], "ALREADY_PROCESSED")
        self.assertEqual(list(ledger), ["RUN-11-01"])

    def test_committed_fixture_matches_chapter_eleven_sample(self) -> None:
        fixture = MONITOR.read_json(HERE / "fixtures/view-model-a.json")
        prior = MONITOR.read_json(
            MONITOR.REPO_ROOT / "sample-outputs/ch11/a/view-model.json"
        )
        self.assertEqual(fixture, prior)

    def test_partial_retrieval_stops_then_repaired_second_attempt_passes(self) -> None:
        blocked = MONITOR.run("b", self.output_dir)
        self.assertEqual(blocked["state"], "BLOCKED_SOURCE")
        self.assertEqual(json.loads((self.output_dir / "ledger.json").read_text(encoding="utf-8")), {})
        recovered = MONITOR.run("b_recovered", self.output_dir)
        self.assertEqual(recovered["state"], "READY_FOR_PM_REVIEW")
        self.assertEqual(recovered["attempt"], 2)

    def test_old_risk_source_stops_even_when_retrieval_is_complete(self) -> None:
        result = MONITOR.run("c", self.output_dir)
        self.assertEqual(result["risk_age_days"], 7)
        self.assertEqual(result["state"], "BLOCKED_STALE")
        self.assertEqual(json.loads((self.output_dir / "ledger.json").read_text(encoding="utf-8")), {})

    def test_changed_payload_under_successful_run_id_requires_review(self) -> None:
        row = MONITOR.case_row(HERE / "cases.csv", "a")
        config = MONITOR.read_json(HERE / "config.json")
        model = MONITOR.read_json(HERE / "fixtures/view-model-a.json")
        first = MONITOR.evaluate(row, config, model, {})
        model["alerts"] = ["Changed fictional alert"]
        changed = MONITOR.evaluate(
            row, config, model, {row["run_id"]: {"model_sha256": first["model_sha256"]}}
        )
        self.assertEqual(changed["state"], "INPUT_CHANGED_REVIEW")

    def test_attempt_limit_and_missing_date_fail_closed(self) -> None:
        row = MONITOR.case_row(HERE / "cases.csv", "a")
        config = MONITOR.read_json(HERE / "config.json")
        model = MONITOR.read_json(HERE / "fixtures/view-model-a.json")
        row["attempt"] = "3"
        self.assertEqual(
            MONITOR.evaluate(row, config, model, {})["state"], "BLOCKED_ATTEMPT_LIMIT"
        )
        del model["source_dates"]["risk"]
        with self.assertRaisesRegex(ValueError, "source_dates.risk"):
            MONITOR.evaluate(row, config, model, {})


if __name__ == "__main__":
    unittest.main()
