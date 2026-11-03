"""Run a bounded investigation against fictional Markdown records."""

from __future__ import annotations

import argparse
import json
import logging
import re
from pathlib import Path
from typing import Dict, List, Optional


LOGGER = logging.getLogger(__name__)
EXAMPLE_DIR = Path(__file__).resolve().parent
VALID_ID = re.compile(r"^[A-Z]+-[0-9]+$")
RECORD_TYPES = {"issue", "decision", "update"}


def parse_record(path: Path) -> Dict[str, str]:
    """Read simple Key: value lines from a local Markdown record."""
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as error:
        LOGGER.error("Record read failed: %s (%s)", path.name, type(error).__name__)
        raise

    record: Dict[str, str] = {}
    for line in content.splitlines():
        if ":" not in line or line.startswith("#"):
            continue
        key, _, value = line.partition(":")
        if key.strip() and value.strip():
            record[key.strip().lower().replace(" ", "_")] = value.strip()

    if record.get("id") is None:
        raise ValueError(f"Record has no ID: {path}")
    LOGGER.info("Read record %s from %s", record["id"], path)
    return record


def load_limit(policy_path: Path) -> int:
    policy = parse_record(policy_path)
    try:
        limit = int(policy["max_retrievals"])
    except (KeyError, ValueError) as error:
        raise ValueError("Policy requires a positive Max retrievals value") from error
    if limit < 1:
        raise ValueError("Max retrievals must be positive")
    return limit


class LocalTools:
    """Expose bounded source reads and one local register write."""

    def __init__(self, records_dir: Path, register_path: Path, max_calls: int) -> None:
        self.records_dir = records_dir
        self.register_path = register_path
        self.max_calls = max_calls
        self.calls = 0
        self.trace: List[str] = []

    def read(self, record_type: str, record_id: str) -> Dict[str, str]:
        if record_type not in RECORD_TYPES or not VALID_ID.fullmatch(record_id):
            raise ValueError("Unsupported record type or identifier")
        if self.calls >= self.max_calls:
            raise RuntimeError("Retrieval limit reached")

        self.calls += 1
        self.trace.append(f"READ {record_type} {record_id}")
        path = self.records_dir / f"{record_type}-{record_id}.md"
        LOGGER.info("Retrieval %s/%s: %s", self.calls, self.max_calls, path)
        try:
            record = parse_record(path)
        except FileNotFoundError as error:
            raise FileNotFoundError(
                f"Missing {record_type} record {record_id}"
            ) from error
        if record["id"] != record_id:
            raise ValueError(f"Record ID mismatch in {path}")
        return record

    def perform(self, action: str, result: Dict[str, object]) -> None:
        if action != "update_register":
            LOGGER.warning("Blocked unauthorized action: %s", action)
            raise PermissionError(f"Action is not permitted: {action}")

        register: Dict[str, object] = {}
        if self.register_path.exists():
            try:
                register = json.loads(self.register_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as error:
                raise ValueError("Cannot read local exception register") from error

        exception_id = str(result["exception_id"])
        register[exception_id] = result
        self.register_path.parent.mkdir(parents=True, exist_ok=True)
        self.register_path.write_text(
            json.dumps(register, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        LOGGER.info("Updated local exception register: %s", exception_id)


def new_result(exception_id: str) -> Dict[str, object]:
    return {
        "exception_id": exception_id,
        "classification": "UNRESOLVED",
        "evidence_references": [],
        "findings": [],
        "unresolved_questions": [],
        "recommended_action": "",
        "executed_action": "",
        "authority_used": [],
        "stop_reason": "",
        "retrieval_calls": 0,
        "retrieval_trace": [],
    }


def add_evidence(result: Dict[str, object], record: Dict[str, str]) -> None:
    references = result["evidence_references"]
    assert isinstance(references, list)
    references.append(record["id"])


def assess_decision(
    result: Dict[str, object],
    issue: Dict[str, str],
    decision: Dict[str, str],
    previous: Optional[Dict[str, str]],
) -> None:
    findings = result["findings"]
    questions = result["unresolved_questions"]
    assert isinstance(findings, list) and isinstance(questions, list)

    required = issue.get("required_version")
    version = decision.get("version")
    if decision.get("status") != "APPROVED":
        findings.append(f"{decision['id']} is not formally approved for version {required}.")
        if previous and previous.get("status") == "APPROVED":
            findings.append(
                f"{previous['id']} approves version {previous.get('version')} only."
            )
        questions.append("Who will approve the required data definition and when?")
        result["recommended_action"] = "Draft a clarification request for PM approval."
        result["stop_reason"] = "human_approval_required"
        return

    if not decision.get("approver") or version != required:
        findings.append("Approval evidence is incomplete or for the wrong version.")
        questions.append("Which version and approver govern this dependency?")
        result["recommended_action"] = "Ask the PM to verify the decision record."
        result["stop_reason"] = "human_approval_required"
        return

    findings.append(f"{decision['id']} approves the required version {required}.")
    result["classification"] = "RESOLVED"
    result["stop_reason"] = "investigation_complete"


def investigate(exception_id: str, tools: LocalTools) -> Dict[str, object]:
    """Choose reads from evidence and stop at the authority boundary."""
    result = new_result(exception_id)
    findings = result["findings"]
    assert isinstance(findings, list)

    try:
        issue = tools.read("issue", exception_id)
        add_evidence(result, issue)
        dependency = issue.get("dependency")
        if not dependency:
            raise ValueError("Issue has no dependency reference")

        decision = tools.read("decision", dependency)
        add_evidence(result, decision)

        previous = None
        previous_id = decision.get("previous_decision")
        if previous_id:
            previous = tools.read("decision", previous_id)
            add_evidence(result, previous)

        if decision.get("status") != "APPROVED" and issue.get("update"):
            update = tools.read("update", issue["update"])
            add_evidence(result, update)
            findings.append(
                f"{update['id']} is discussion evidence, not formal approval."
            )

        if "independent" in issue.get("latest_update", "").lower():
            findings.append("Independent interface work has started.")
        assess_decision(result, issue, decision, previous)
    except (OSError, ValueError, RuntimeError) as error:
        LOGGER.warning("Investigation stopped: %s", error)
        findings.append(f"Evidence retrieval failed: {error}")
        result["unresolved_questions"] = ["What does the missing source establish?"]
        result["recommended_action"] = "Ask the PM to inspect the missing evidence."
        result["stop_reason"] = (
            "retrieval_limit" if "limit" in str(error).lower() else "evidence_unavailable"
        )

    result["retrieval_calls"] = tools.calls
    result["retrieval_trace"] = tools.trace.copy()
    result["authority_used"] = tools.trace.copy() + ["WRITE local exception register"]
    result["executed_action"] = "Updated local exception register"
    tools.perform("update_register", result)
    return result


def run_scenario(scenario: str, output_dir: Path) -> Dict[str, object]:
    records_dir = EXAMPLE_DIR / "scenarios" / scenario
    if not records_dir.is_dir():
        raise ValueError(f"Unknown scenario: {scenario}")

    tools = LocalTools(
        records_dir=records_dir,
        register_path=output_dir / "exception-register.json",
        max_calls=load_limit(EXAMPLE_DIR / "agent-policy.md"),
    )
    result = investigate("GH-41", tools)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "investigation.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", choices=("a", "b", "c"), required=True)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    output_dir = args.output_dir or EXAMPLE_DIR / "outputs" / args.scenario
    result = run_scenario(args.scenario, output_dir)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
