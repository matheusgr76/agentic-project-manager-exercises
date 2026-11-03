"""Behavior checks for the Chapter 4–6 workshop path."""

from __future__ import annotations

import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from workshop.connected_pilot import run as run_connected
from workshop.report_builder import build_evidence, capacity_findings, run as run_report
from workshop.scheduled_run import run as run_scheduled


class WorkshopTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.output_dir = Path(self.temp_dir.name)

    def test_chapter_four_report_preserves_pending_decision_and_stale_capacity(self) -> None:
        evidence = run_report(self.output_dir)

        self.assertEqual(evidence["issue"]["status"], "BLOCKED")
        self.assertEqual(evidence["decision"]["status"], "PENDING")
        self.assertFalse(evidence["formal_approval"])
        self.assertEqual(
            [row["team"] for row in evidence["capacity"] if row["stale"]],
            ["Alpha", "Bravo"],
        )
        status = (self.output_dir / "weekly-status.md").read_text(encoding="utf-8")
        self.assertIn("PM approval is required", status)
        self.assertIn("no delivery date", status)

    def test_chapter_four_rejects_future_capacity_snapshot(self) -> None:
        with self.assertRaises(ValueError):
            capacity_findings(
                [
                    {
                        "team": "Alpha",
                        "allocation": "2",
                        "status": "CONFIRMED",
                        "snapshot_date": "2026-11-07",
                    }
                ],
                date(2026, 11, 6),
                "test.csv",
            )

    def test_chapter_five_success_preserves_source_id_and_retrieval_time(self) -> None:
        result = run_connected("success", self.output_dir)

        self.assertEqual(result["status"], "SUCCESS")
        self.assertEqual(result["record_id"], "GH-41")
        self.assertEqual(result["source_updated_at"], "2026-11-05")
        self.assertEqual(result["retrieved_at"], "2026-11-06T09:00:00Z")
        self.assertTrue((self.output_dir / "evidence.json").exists())

    def test_chapter_five_failure_does_not_create_evidence(self) -> None:
        result = run_connected("server-down", self.output_dir)

        self.assertEqual(result["status"], "UNAVAILABLE")
        self.assertFalse((self.output_dir / "evidence.json").exists())

    def test_chapter_five_ignores_source_instruction(self) -> None:
        result = run_connected("injection", self.output_dir)

        self.assertTrue(result["source_instruction_ignored"])
        status = (self.output_dir / "weekly-status.md").read_text(encoding="utf-8")
        self.assertNotIn("publish immediately", status)
        self.assertIn("PM approval is required", status)

    def test_chapter_six_complete_run_writes_drafts_without_publishing(self) -> None:
        result = run_scheduled("A", self.output_dir)

        self.assertEqual(result["status"], "COMPLETE")
        self.assertIn("PM approval required", result["publication"])
        self.assertTrue((self.output_dir / "management-draft.md").exists())
        evidence = json.loads(
            (self.output_dir / "evidence.json").read_text(encoding="utf-8")
        )
        self.assertFalse(any(row["stale"] for row in evidence["capacity"]))

    def test_chapter_six_failed_retrieval_stops_without_drafts(self) -> None:
        result = run_scheduled("B", self.output_dir)

        self.assertEqual(result["status"], "INCOMPLETE")
        self.assertFalse((self.output_dir / "management-draft.md").exists())
        self.assertTrue((self.output_dir / "alert.md").exists())

    def test_chapter_six_conflict_creates_chapter_seven_handoff(self) -> None:
        result = run_scheduled("C", self.output_dir)

        self.assertEqual(result["status"], "REVIEW_REQUIRED")
        self.assertFalse((self.output_dir / "management-draft.md").exists())
        exception = json.loads(
            (self.output_dir / "exception.json").read_text(encoding="utf-8")
        )
        self.assertEqual(exception["exception_id"], "GH-41")
        self.assertEqual(exception["decision_status"], "PENDING")

    def test_chapter_six_source_instruction_cannot_publish(self) -> None:
        result = run_scheduled("D", self.output_dir)

        self.assertEqual(result["status"], "COMPLETE")
        self.assertTrue(result["untrusted_comment_ignored"])
        self.assertIn("nothing sent", result["publication"])


if __name__ == "__main__":
    unittest.main()
