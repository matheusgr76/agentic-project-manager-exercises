"""Behavior checks for the Chapter 4–6 workshop path."""

from __future__ import annotations

import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from workshop.connected_pilot import run as run_connected
from workshop.report_builder import (
    build_evidence, capacity_findings, run as run_report, validate_updates,
)
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
        self.assertEqual(evidence["status_conflicts"], [])
        self.assertTrue(all(
            item["input_file"] and item["record_id"]
            for item in evidence["source_references"]
        ))
        self.assertEqual(
            [row["team"] for row in evidence["capacity"] if row["stale"]],
            ["Alpha", "Bravo"],
        )
        status = (self.output_dir / "weekly-status.md").read_text(encoding="utf-8")
        self.assertIn("PM approval is required", status)
        self.assertIn("no delivery date", status)

    def test_chapter_four_flags_explicit_status_conflict_with_sources(self) -> None:
        issue = {
            "id": "GH-41", "title": "Bravo integration sizing",
            "status": "IN_PROGRESS", "owner": "Bravo",
            "updated_at": "2026-11-05", "dependency": "DEC-12",
        }
        evidence = build_evidence(issue_override=issue)
        conflict = evidence["status_conflicts"][0]
        self.assertEqual(conflict["issue_record_id"], "GH-41")
        self.assertEqual(conflict["decision_record_id"], "DEC-12")
        self.assertTrue(conflict["issue_source"])
        self.assertTrue(conflict["decision_source"])

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

    def test_chapter_four_rejects_blank_capacity_status(self) -> None:
        with self.assertRaisesRegex(ValueError, "missing fields: status"):
            capacity_findings(
                [{
                    "team": "Alpha", "allocation": "2", "status": "",
                    "snapshot_date": "2026-11-05",
                }],
                date(2026, 11, 6),
                "test.csv",
            )

    def test_chapter_four_rejects_malformed_update_dates_and_authors(self) -> None:
        valid = (
            "UP-1 | 2026-11-05 | Alpha lead | Option B looks good\n"
            "UP-2 | 2026-11-05 | Bravo lead | data contract still blocks the full estimate\n"
            "UP-3 | 2026-11-05 | CTO | New allocations are not yet confirmed\n"
        )
        validate_updates(valid)
        with self.assertRaisesRegex(ValueError, "Invalid update date"):
            validate_updates(valid.replace("UP-1 | 2026-11-05", "UP-1 | invalid"))
        with self.assertRaisesRegex(ValueError, "missing ID, date, author"):
            validate_updates(valid.replace("UP-2 | 2026-11-05 | Bravo lead", "UP-2 | 2026-11-05 | "))

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

    def test_chapter_five_missing_issue_retains_unresolved_dependency(self) -> None:
        result = run_connected("missing", self.output_dir)
        self.assertEqual(result["status"], "MISSING")
        self.assertEqual(result["dependency_id"], "DEC-12")
        self.assertEqual(result["dependency_status"], "UNRESOLVED")
        self.assertFalse(result["evidence_created"])

    def test_chapter_five_rejects_partial_retrieved_issue(self) -> None:
        with self.assertRaisesRegex(ValueError, "missing required fields"):
            build_evidence(issue_override={"id": "GH-41", "status": "BLOCKED"})

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
        draft = (self.output_dir / "management-draft.md").read_text(encoding="utf-8")
        self.assertIn("fictional test capacity", draft)
        self.assertIn("newer fictional test snapshot records confirmed capacity", draft)
        self.assertNotIn("Obtain the formal decision and current capacity", draft)

    def test_chapter_six_repeated_run_retains_both_records(self) -> None:
        first = run_scheduled("A", self.output_dir)
        second = run_scheduled("A", self.output_dir)

        self.assertNotEqual(first["run_id"], second["run_id"])
        for result in (first, second):
            record = self.output_dir / f"{result['run_id']}.json"
            self.assertTrue(record.exists())
            self.assertEqual(
                json.loads(record.read_text(encoding="utf-8"))["run_id"],
                result["run_id"],
            )

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
