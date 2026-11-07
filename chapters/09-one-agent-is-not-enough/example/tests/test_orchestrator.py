"""Behavior checks for the fictional Acme coordinator."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from orchestrator import coordinate, read_artifact, run, scenario_paths  # noqa: E402


class OrchestratorTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.output_dir = Path(temporary.name)

    def test_aligned_artifacts_require_review_and_preserve_dates(self) -> None:
        result = run("a", self.output_dir)
        self.assertEqual(result["status"], "REVIEW_REQUIRED")
        self.assertEqual(result["shared_references"], ["DEC-12", "GH-41"])
        self.assertEqual(result["risk_signal_references"], ["S-01", "S-02", "S-03"])
        self.assertIn("predates", result["freshness_note"])
        self.assertEqual(result["source_dates"]["dependency"], "not recorded")
        self.assertEqual(result["publication"], "none")

    def test_conflict_preserves_both_statuses(self) -> None:
        result = run("b", self.output_dir)
        self.assertEqual(result["status"], "CONFLICT")
        self.assertEqual(result["source_statuses"]["dependency"], "RESOLVED")
        self.assertIn("GH-41 is resolved", result["disagreement"])
        self.assertIn("GH-41 is in progress", result["disagreement"])
        self.assertEqual(result["report_issue_statuses"]["DEC-12"], "PENDING")

    def test_conflict_does_not_depend_on_report_wording(self) -> None:
        paths = scenario_paths("b", False)
        records = {name: read_artifact(path, name) for name, path in paths.items()}
        records["report"]["findings"] = ["GH-41 remains underway."]

        result = coordinate(records)

        self.assertEqual(result["status"], "CONFLICT")

    def test_blocked_report_also_conflicts_with_resolved_dependency(self) -> None:
        paths = scenario_paths("b", False)
        records = {name: read_artifact(path, name) for name, path in paths.items()}
        records["report"]["issue_statuses"]["GH-41"] = "BLOCKED"
        result = coordinate(records)
        self.assertEqual(result["status"], "CONFLICT")
        self.assertIn("GH-41 is blocked", result["disagreement"])

    def test_missing_structured_report_status_fails_visibly(self) -> None:
        paths = scenario_paths("b", False)
        records = {name: read_artifact(path, name) for name, path in paths.items()}
        del records["report"]["issue_statuses"]
        with self.assertRaisesRegex(ValueError, "missing required fields"):
            coordinate(records)

    def test_missing_risk_stops_incomplete(self) -> None:
        result = run("c", self.output_dir)
        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertEqual(result["missing_artifacts"], ["risk"])
        self.assertNotIn("proposed_action", result)

    def test_invalid_json_fails_visibly(self) -> None:
        invalid = self.output_dir / "invalid.json"
        invalid.write_text("{broken", encoding="utf-8")
        with self.assertRaises(ValueError):
            read_artifact(invalid, "risk")

    def test_prior_output_mode_rejects_fixture_variations(self) -> None:
        with self.assertRaises(ValueError):
            run("b", self.output_dir, from_prior_outputs=True)

    def test_repeat_run_replaces_one_local_handoff(self) -> None:
        first = run("a", self.output_dir)
        second = run("a", self.output_dir)
        self.assertEqual(first, second)
        files = [path.name for path in self.output_dir.iterdir()]
        self.assertEqual(files, ["handoff.json"])
        saved = json.loads((self.output_dir / "handoff.json").read_text(encoding="utf-8"))
        self.assertEqual(saved, second)


if __name__ == "__main__":
    unittest.main()
