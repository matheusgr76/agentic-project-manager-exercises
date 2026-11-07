"""Behavior checks for the fictional Acme Risk Analyst."""

from __future__ import annotations

import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from risk_analyst import HERE, read_signals, run, validate_investigation  # noqa: E402


class RiskAnalystTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.output_dir = Path(temporary.name)

    def test_cross_team_pattern_requires_human_review(self) -> None:
        before = (HERE / "signals.csv").read_bytes()
        result = run("a", self.output_dir)
        self.assertEqual(result["classification"], "EMERGING_RISK_FOR_REVIEW")
        self.assertEqual(result["evidence_references"], ["S-01", "S-02", "S-03"])
        self.assertEqual(
            [signal["as_of"] for signal in result["evidence_signals"]],
            ["2026-11-09", "2026-11-09", "2026-11-09"],
        )
        self.assertEqual(result["stop_reason"], "human_review_required")
        self.assertEqual(result["probability"], "not estimated")
        self.assertEqual((HERE / "signals.csv").read_bytes(), before)
        self.assertTrue((self.output_dir / "analysis.json").exists())

    def test_committed_samples_match_current_output(self) -> None:
        """A reader who opens sample-outputs must see what the program writes now."""
        samples = HERE.parents[2] / "sample-outputs" / "ch08"
        handoff = HERE.parents[2] / "sample-outputs" / "ch07" / "a" / "investigation.json"
        for scenario, investigation in (("a", handoff), ("b", None), ("c", None)):
            with self.subTest(scenario=scenario):
                fresh = run(scenario, self.output_dir / scenario, investigation)
                committed = json.loads((samples / scenario / "analysis.json").read_text(encoding="utf-8"))
                self.assertEqual(fresh, committed)

    def test_resolved_and_stale_signals_do_not_create_risk(self) -> None:
        for scenario, excluded in (("b", "S-04"), ("c", "S-07")):
            result = run(scenario, self.output_dir / scenario)
            self.assertEqual(result["classification"], "INSUFFICIENT_EVIDENCE")
            self.assertIn(excluded, [item["id"] for item in result["excluded_signals"]])
            self.assertIsNone(result["risk_statement"])

    def test_invalid_handoff_is_rejected(self) -> None:
        handoff = self.output_dir / "handoff.json"
        handoff.write_text('{"classification":"RESOLVED","evidence_references":["GH-41"]}', encoding="utf-8")
        with self.assertRaises(ValueError):
            validate_investigation(handoff)
        handoff.write_text(
            '{"classification":"UNRESOLVED","evidence_references":["GH-41"]}',
            encoding="utf-8",
        )
        with self.assertRaises(ValueError):
            validate_investigation(handoff)

    def test_malformed_signals_are_rejected(self) -> None:
        source = self.output_dir / "bad.csv"
        with source.open("w", newline="", encoding="utf-8") as output:
            writer = csv.writer(output)
            writer.writerow(["scenario", "id"])
            writer.writerow(["a", "S-1"])
        with self.assertRaises(ValueError):
            read_signals(source, "a")

    def test_rerun_replaces_one_local_artifact(self) -> None:
        first = run("a", self.output_dir)
        second = run("a", self.output_dir)
        self.assertEqual(first, second)
        self.assertEqual([path.name for path in self.output_dir.iterdir()], ["analysis.json"])


if __name__ == "__main__":
    unittest.main()
