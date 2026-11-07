"""Run every Revision A exercise against an isolated fictional repository copy."""

from __future__ import annotations

import argparse
import json
import logging
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
from xml.etree import ElementTree
from zipfile import ZipFile


LOGGER = logging.getLogger(__name__)
WORD_NAMESPACE = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
WORD_TEXT = f"{{{WORD_NAMESPACE['w']}}}t"
WORD_BREAK = f"{{{WORD_NAMESPACE['w']}}}br"
CHAPTER_HEADING = re.compile(r"^Chapter\s+(\d{1,2})\s*[·—–-]", re.IGNORECASE)
VERDICT = re.compile(r"^Overall verdict: (PASS|FAIL)$", re.MULTILINE)


def load_manifest(path: Path) -> list[dict[str, Any]]:
    """Validate the chapter inventory before any exercise runs."""
    chapters = json.loads(path.read_text(encoding="utf-8"))["chapters"]
    numbers = [chapter["number"] for chapter in chapters]
    if numbers != list(range(1, 16)):
        raise ValueError("Manifest must contain Chapters 1 through 15 in order")
    return chapters


def extract_manuscript(path: Path, destination: Path) -> None:
    """Write each Revision A chapter as plain text for the local agent."""
    with ZipFile(path) as document:
        root = ElementTree.fromstring(document.read("word/document.xml"))
    chapters: dict[int, list[str]] = {}
    chapter_number: Optional[int] = None
    for paragraph in root.findall(".//w:body/w:p", WORD_NAMESPACE):
        line = "".join(
            node.text or "" if node.tag == WORD_TEXT else "\n"
            for node in paragraph.iter() if node.tag in {WORD_TEXT, WORD_BREAK}
        ).strip()
        match = CHAPTER_HEADING.match(line)
        if match:
            chapter_number = int(match.group(1))
            chapters.setdefault(chapter_number, [])
        if chapter_number is not None and line:
            chapters[chapter_number].append(line)
    if sorted(chapters) != list(range(1, 16)):
        raise ValueError("Manuscript must have exactly Chapters 1 through 15")
    destination.mkdir(parents=True)
    for number, paragraphs in chapters.items():
        (destination / f"chapter-{number:02d}.txt").write_text(
            "\n\n".join(paragraphs) + "\n", encoding="utf-8"
        )


def copy_repository(source: Path, destination: Path) -> None:
    """Prevent exercise programs from changing the source checkout."""
    if destination.exists():
        raise FileExistsError(f"Run directory already exists: {destination}")
    shutil.copytree(
        source,
        destination,
        ignore=shutil.ignore_patterns(".git", "__pycache__", "outputs", ".pytest_cache"),
    )


def run_command(
    command: list[str], cwd: Path, timeout_seconds: int, attempts: int = 1
) -> dict[str, Any]:
    """Run a bounded command and preserve its observable result."""
    result: dict[str, Any] = {}
    for attempt in range(1, attempts + 1):
        started = datetime.now(timezone.utc).isoformat()
        try:
            completed = subprocess.run(
                command, cwd=cwd, capture_output=True, text=True,
                encoding="utf-8", errors="replace", timeout=timeout_seconds,
                check=False,
            )
            result = {
                "command": command, "attempt": attempt, "started_utc": started,
                "exit_code": completed.returncode, "stdout": completed.stdout[-12000:],
                "stderr": completed.stderr[-12000:],
            }
        except (OSError, subprocess.TimeoutExpired) as error:
            result = {
                "command": command, "attempt": attempt, "started_utc": started,
                "exit_code": None, "error": str(error),
            }
        LOGGER.info("Command attempt %s status %s: %s", attempt, result["exit_code"], command)
        if result["exit_code"] == 0:
            break
    return result


def make_prompt(chapter: dict[str, Any]) -> str:
    """Assess the companion exercise against its manuscript chapter."""
    number = chapter["number"]
    guide = chapter["guide"]
    return (
        f"Validate the GitHub companion exercise for manuscript/chapter-{number:02d}.txt "
        f"against {guide} and its linked fictional inputs. "
        f"The runner already executed the chapter commands; read validation/chapter-{number:02d}.json "
        "for their exit codes, test results, and artifact checks. Do not claim a command "
        "was not run if it appears there. Inspect generated outputs and source records; "
        "compare with worked examples after forming your own conclusion. "
        "Report concrete discrepancies in code, output, guide, or manuscript with file "
        "and source references. Distinguish those from reader tasks that require a "
        "person's approval, a new reader-built program, or real-world timing data. "
        "Those tasks are outside repository validation and are not by themselves failures. "
        "PASS means the available repository exercise satisfies its testable teaching "
        "claims; FAIL requires a demonstrated contradiction or missing behavior. "
        "End with exactly one line: Overall verdict: PASS or Overall verdict: FAIL. "
        "Do not edit files, access company systems, send messages, publish, approve, "
        "or change GitHub records."
    )


def run_model(
    chapter: dict[str, Any], workspace: Path, output: Path,
    executable: str, timeout_seconds: int,
) -> dict[str, Any]:
    """Use the installed Codex CLI for the written part of one chapter."""
    answer_path = output / "answer.md"
    command = [
        executable, "exec", "--ephemeral", "--skip-git-repo-check",
        "--sandbox", "read-only", "--cd", str(workspace),
        "--output-last-message", str(answer_path), "-",
    ]
    prompt = make_prompt(chapter)
    result: dict[str, Any] = {}
    for attempt in range(1, 3):
        try:
            completed = subprocess.run(
                command, input=prompt, cwd=workspace, capture_output=True,
                text=True, encoding="utf-8", errors="replace",
                timeout=timeout_seconds, check=False,
            )
            result = {
                "attempt": attempt, "exit_code": completed.returncode,
                "stdout": completed.stdout[-12000:], "stderr": completed.stderr[-12000:],
            }
        except (OSError, subprocess.TimeoutExpired) as error:
            result = {"attempt": attempt, "exit_code": None, "error": str(error)}
        LOGGER.info("Chapter %s model attempt %s status %s", chapter["number"],
                    attempt, result["exit_code"])
        if result["exit_code"] == 0 and answer_path.is_file() and answer_path.stat().st_size:
            break
    result["answer"] = str(answer_path) if answer_path.is_file() else None
    return result


def run_chapter(
    chapter: dict[str, Any], workspace: Path, run_root: Path,
    executable: str, timeout_seconds: int,
) -> dict[str, Any]:
    """Execute a chapter's programs, then complete its written exercise."""
    number = chapter["number"]
    chapter_output = run_root / f"chapter-{number:02d}"
    chapter_output.mkdir()
    commands = []
    for arguments in chapter["commands"]:
        command = [sys.executable if value == "{python}" else value for value in arguments]
        commands.append(run_command(command, workspace, timeout_seconds))
    if number >= 4:
        test_directory = (
            "workshop/tests" if number <= 6
            else str(Path(chapter["guide"]).parent / "example" / "tests")
        )
        commands.append(run_command(
            [sys.executable, "-m", "unittest", "discover", "-s", test_directory, "-v"],
            workspace, timeout_seconds,
        ))
    missing = [path for path in chapter["artifacts"] if not (workspace / path).is_file()]
    validation_dir = workspace / "validation"
    validation_dir.mkdir(exist_ok=True)
    (validation_dir / f"chapter-{number:02d}.json").write_text(
        json.dumps({"commands": commands, "missing_artifacts": missing}, indent=2),
        encoding="utf-8",
    )
    model = run_model(chapter, workspace, chapter_output, executable, timeout_seconds)
    program_success = all(item["exit_code"] == 0 for item in commands) and not missing
    model_success = model["exit_code"] == 0 and model["answer"] is not None
    verdict_match = VERDICT.search(Path(model["answer"]).read_text(encoding="utf-8")) if model_success else None
    verdict = verdict_match.group(1) if verdict_match else "FAIL"
    return {
        "chapter": number, "guide": chapter["guide"],
        "execution_status": "SUCCESS" if program_success else "FAILURE",
        "validation_status": "PASS" if program_success and model_success and verdict == "PASS" else "FAIL",
        "agent_verdict": verdict,
        "commands": commands, "missing_artifacts": missing, "model": model,
    }


def write_results(run_root: Path, results: list[dict[str, Any]]) -> None:
    """Persist machine-readable and readable progress after each chapter."""
    (run_root / "results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = ["# Revision A exercise run", "", "| Chapter | Execution | Validation |", "| --- | --- | --- |"]
    for item in results:
        lines.append(
            f"| {item['chapter']} | {item['execution_status']} | {item['validation_status']} |"
        )
    lines.extend(["", "Program results and errors are in results.json. Written answers are in each chapter folder."])
    (run_root / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    """Run all chapters while continuing past individual failures."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--manuscript", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--codex", default="codex")
    parser.add_argument("--timeout", type=int, default=600)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    repo = args.repo.resolve()
    output = args.output.resolve()
    if not args.manuscript.is_file() or args.manuscript.suffix.lower() != ".docx":
        parser.error("--manuscript must be an existing DOCX file")
    if args.timeout < 1:
        parser.error("--timeout must be positive")
    if output == repo or repo in output.parents or output in repo.parents:
        parser.error("--output must be separate from --repo")
    chapters = load_manifest(repo / "exercise_manifest.json")
    output.mkdir(parents=True, exist_ok=False)
    workspace = output / "workspace"
    copy_repository(repo, workspace)
    extract_manuscript(args.manuscript, workspace / "manuscript")
    results: list[dict[str, Any]] = []
    for chapter in chapters:
        LOGGER.info("Starting Chapter %s", chapter["number"])
        results.append(run_chapter(chapter, workspace, output, args.codex, args.timeout))
        write_results(output, results)
    return 0 if all(item["validation_status"] == "PASS" for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
