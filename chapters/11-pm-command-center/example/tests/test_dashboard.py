"""Behavior checks for the fictional read-only Command Center."""

from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from dashboard import HERE, build_model, read_json, render_html, run  # noqa: E402


class CommandCenterTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.output_dir = Path(temporary.name)

    def test_normal_view_keeps_hypothesis_and_undated_context_separate(self) -> None:
        model = run("a", self.output_dir)
        self.assertEqual(model["state"], "REVIEW_REQUIRED")
        self.assertEqual(model["facts"][0]["value"], "PENDING")
        self.assertEqual(model["facts"][1]["value"], "UNDATED_CONTEXT")
        self.assertEqual(model["hypotheses"][0]["value"], "HYPOTHESIS")
        self.assertIn("predates", " ".join(model["alerts"]))
        self.assertEqual(model["publication"], "none")

    def test_conflict_replaces_routine_review_steps(self) -> None:
        model = run("b", self.output_dir)
        self.assertEqual(model["state"], "CONFLICT")
        self.assertEqual(model["human_review"], [
            "Reconcile missing or conflicting records before acting"
        ])

    def test_missing_specialist_marks_page_incomplete(self) -> None:
        model = run("c", self.output_dir)
        self.assertEqual(model["state"], "INCOMPLETE")
        self.assertIn("missing", " ".join(model["alerts"]).lower())

    def test_untrusted_text_is_escaped_in_html(self) -> None:
        handoff = read_json(HERE / "fixtures" / "handoff-a.json", "handoff")
        knowledge = read_json(HERE / "fixtures" / "knowledge-a.json", "knowledge")
        changed = copy.deepcopy(handoff)
        changed["proposed_action"] = "<script>alert('send')</script>"
        model = build_model(changed, knowledge)
        html = render_html(model, "")
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)

    def test_missing_json_fails_visibly(self) -> None:
        with self.assertRaises(ValueError):
            read_json(self.output_dir / "missing.json", "handoff")

    def test_repeat_run_replaces_two_local_artifacts(self) -> None:
        first = run("a", self.output_dir)
        second = run("a", self.output_dir)
        self.assertEqual(first, second)
        self.assertEqual(
            {path.name for path in self.output_dir.iterdir()},
            {"index.html", "view-model.json"},
        )
        saved = json.loads((self.output_dir / "view-model.json").read_text(encoding="utf-8"))
        self.assertEqual(saved, second)


if __name__ == "__main__":
    unittest.main()
