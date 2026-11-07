"""Behavior checks for the fictional, time-specific project history."""

from __future__ import annotations

import sys
import json
import tempfile
import unittest
from datetime import date
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from knowledge_base import HERE, assess, load_records, query_history  # noqa: E402


class KnowledgeBaseTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.output_dir = Path(temporary.name)

    def test_initial_state_keeps_undated_investigation_as_context(self) -> None:
        result = assess("a", date(2026, 11, 12), self.output_dir)
        self.assertEqual(result["answers"]["DEC-12/v2"]["value"], "PENDING")
        self.assertEqual(result["answers"]["GH-41"]["status"], "UNDATED_CONTEXT")
        self.assertIsNone(result["answers"]["GH-41"]["value"])
        self.assertEqual(result["answers"]["R1/risk"]["value"], "HYPOTHESIS")

    def test_investigation_citation_points_to_actual_result(self) -> None:
        rows = load_records(HERE / "records.csv", "a")
        investigation = next(row for row in rows if row["event_id"] == "E-02")
        source = HERE.parents[2] / investigation["source_ref"]
        record = json.loads(source.read_text(encoding="utf-8"))
        self.assertEqual(record["exception_id"], investigation["key"])
        self.assertEqual(record["classification"], investigation["value"])

    def test_later_approval_does_not_rewrite_earlier_answer(self) -> None:
        past = assess("b", date(2026, 11, 12), self.output_dir)
        later = assess("b", date(2026, 11, 15), self.output_dir)
        self.assertEqual(past["answers"]["DEC-12/v2"]["value"], "PENDING")
        self.assertEqual(later["answers"]["DEC-12/v2"]["value"], "APPROVED")
        self.assertEqual(later["answers"]["DEC-12/v2"]["superseded_events"], ["E-01"])
        self.assertEqual(later["answers"]["R1/risk"]["status"], "NEEDS_REVALIDATION")
        self.assertEqual(later["answers"]["GH-41"]["status"], "UNDATED_CONTEXT")

    def test_conflict_cites_both_active_decision_sources(self) -> None:
        result = assess("c", date(2026, 11, 15), self.output_dir)
        decision = result["answers"]["DEC-12/v2"]
        self.assertEqual(decision["status"], "CONFLICT")
        self.assertIsNone(decision["value"])
        self.assertEqual([source["event_id"] for source in decision["sources"]], ["E-04", "E-05"])

    def test_invalid_supersedes_link_fails_visibly(self) -> None:
        original = (HERE / "records.csv").read_text(encoding="utf-8")
        invalid = self.output_dir / "invalid.csv"
        invalid.write_text(original.replace(",E-01,decision_log", ",E-99,decision_log"), encoding="utf-8")
        with self.assertRaises(ValueError):
            load_records(invalid, "b")

    def test_self_supersession_fails_visibly(self) -> None:
        original = (HERE / "records.csv").read_text(encoding="utf-8")
        invalid = self.output_dir / "self-link.csv"
        invalid.write_text(
            original.replace(",E-01,decision_log", ",E-04,decision_log"),
            encoding="utf-8",
        )
        with self.assertRaises(ValueError):
            load_records(invalid, "b")

    def test_agreeing_active_records_keep_both_sources(self) -> None:
        rows = [row for row in load_records(HERE / "records.csv", "a")
                if row["key"] == "DEC-12/v2"]
        matching = dict(rows[0])
        matching["event_id"] = "E-99"
        answer = query_history(rows + [matching], "DEC-12/v2", date(2026, 11, 12))
        self.assertEqual(answer["status"], "CURRENT")
        self.assertEqual(answer["value"], "PENDING")
        self.assertEqual(len(answer["sources"]), 2)

    def test_source_path_cannot_escape_repository(self) -> None:
        original = (HERE / "records.csv").read_text(encoding="utf-8")
        invalid = self.output_dir / "invalid-path.csv"
        invalid.write_text(
            original.replace(
                "chapters/10-project-that-remembers/example/fixtures/decision-snapshot.md",
                "../outside.txt",
            ),
            encoding="utf-8",
        )
        with self.assertRaises(ValueError):
            load_records(invalid, "a")

    def test_repeat_run_replaces_one_local_answer(self) -> None:
        first = assess("a", date(2026, 11, 12), self.output_dir)
        second = assess("a", date(2026, 11, 12), self.output_dir)
        self.assertEqual(first, second)
        self.assertEqual([path.name for path in self.output_dir.iterdir()], ["knowledge.json"])
        self.assertEqual(first["publication"], "none")


if __name__ == "__main__":
    unittest.main()
