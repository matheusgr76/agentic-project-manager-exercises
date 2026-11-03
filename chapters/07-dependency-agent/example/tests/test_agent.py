"""Behavior checks for the fictional dependency agent."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from agent import EXAMPLE_DIR, LocalTools, investigate, run_scenario


class DependencyAgentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.output_dir = Path(self.temp_dir.name)

    def test_scenario_a_preserves_pending_approval_and_updates_register(self) -> None:
        issue_path = EXAMPLE_DIR / "scenarios" / "a" / "issue-GH-41.md"
        original_issue = issue_path.read_bytes()
        result = run_scenario("a", self.output_dir)

        self.assertEqual(result["classification"], "UNRESOLVED")
        self.assertEqual(result["stop_reason"], "human_approval_required")
        self.assertEqual(result["retrieval_calls"], 3)
        self.assertEqual(result["evidence_references"], ["GH-41", "DEC-12", "UP-1"])
        self.assertIn("Updated local exception register", result["executed_action"])
        self.assertNotIn("close_issue", str(result["authority_used"]))
        self.assertEqual(issue_path.read_bytes(), original_issue)

        run_scenario("a", self.output_dir)
        register = json.loads(
            (self.output_dir / "exception-register.json").read_text(encoding="utf-8")
        )
        self.assertEqual(list(register), ["GH-41"])
        self.assertEqual(register["GH-41"]["executed_action"], result["executed_action"])

    def test_scenario_b_does_not_apply_old_version_approval(self) -> None:
        result = run_scenario("b", self.output_dir)

        self.assertEqual(result["classification"], "UNRESOLVED")
        self.assertEqual(result["retrieval_calls"], 4)
        self.assertIn("DEC-11", result["evidence_references"])
        self.assertTrue(
            any("version 1 only" in finding for finding in result["findings"])
        )

    def test_scenario_c_stops_when_decision_is_unavailable(self) -> None:
        result = run_scenario("c", self.output_dir)

        self.assertEqual(result["classification"], "UNRESOLVED")
        self.assertEqual(result["stop_reason"], "evidence_unavailable")
        self.assertEqual(result["retrieval_calls"], 2)
        self.assertEqual(result["evidence_references"], ["GH-41"])

    def test_retrieval_limit_stops_investigation(self) -> None:
        tools = LocalTools(
            EXAMPLE_DIR / "scenarios" / "a",
            self.output_dir / "exception-register.json",
            max_calls=2,
        )

        result = investigate("GH-41", tools)

        self.assertEqual(result["stop_reason"], "retrieval_limit")
        self.assertEqual(result["retrieval_calls"], 2)

    def test_approved_decision_skips_informal_update(self) -> None:
        records_dir = self.output_dir / "approved"
        records_dir.mkdir()
        (records_dir / "issue-GH-41.md").write_text(
            "ID: GH-41\nDependency: DEC-12\nRequired version: 2\n"
            "Update: UP-1\nStatus: IN_PROGRESS\n",
            encoding="utf-8",
        )
        (records_dir / "decision-DEC-12.md").write_text(
            "ID: DEC-12\nVersion: 2\nStatus: APPROVED\n"
            "Approver: Product Manager\n",
            encoding="utf-8",
        )
        tools = LocalTools(
            records_dir,
            self.output_dir / "exception-register.json",
            max_calls=6,
        )

        result = investigate("GH-41", tools)

        self.assertEqual(result["classification"], "RESOLVED")
        self.assertEqual(result["retrieval_calls"], 2)
        self.assertEqual(result["evidence_references"], ["GH-41", "DEC-12"])

    def test_tool_layer_blocks_source_write(self) -> None:
        register_path = self.output_dir / "exception-register.json"
        tools = LocalTools(EXAMPLE_DIR / "scenarios" / "a", register_path, 6)

        with self.assertRaises(PermissionError):
            tools.perform("close_issue", {"exception_id": "GH-41"})

        self.assertFalse(register_path.exists())

    def test_tool_layer_rejects_invalid_identifier(self) -> None:
        tools = LocalTools(
            EXAMPLE_DIR / "scenarios" / "a",
            self.output_dir / "exception-register.json",
            6,
        )

        with self.assertRaises(ValueError):
            tools.read("issue", "../GH-41")

        self.assertEqual(tools.calls, 0)


if __name__ == "__main__":
    unittest.main()
