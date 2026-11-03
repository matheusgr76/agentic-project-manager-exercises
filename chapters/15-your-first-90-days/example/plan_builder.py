"""Build a fictional 90-day PM pilot plan for human review."""

from __future__ import annotations

import argparse
import json
import logging
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, List


LOGGER = logging.getLogger(__name__)
HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]


def read_json(path: Path) -> object:
    """Read a required local JSON file with visible I/O and parse failures."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        LOGGER.error("Cannot read %s: %s", path, error)
        raise ValueError(f"Cannot read JSON: {path}") from error


def positive_int(value: object) -> bool:
    """Accept positive integer counts without accepting booleans."""
    return type(value) is int and value > 0


def charter_gaps(pilot: Dict[str, object]) -> List[str]:
    """Find missing pilot evidence and keep blockers explicit."""
    gaps = []
    if any(not pilot.get(key) for key in ("pilot_id", "owner", "problem", "scope")):
        gaps.append("OWNER_OR_SCOPE_MISSING")
    baseline = pilot.get("baseline")
    if (not isinstance(baseline, dict)
            or not positive_int(baseline.get("sample_count"))
            or not positive_int(baseline.get("median_total_minutes"))):
        gaps.append("BASELINE_MISSING")
    target = pilot.get("target")
    if (not isinstance(target, dict)
            or not positive_int(target.get("sample_count"))
            or not positive_int(target.get("min_accepted"))
            or not positive_int(target.get("max_median_total_minutes"))
            or target["min_accepted"] > target["sample_count"]):
        gaps.append("TARGET_MISSING")
    access = pilot.get("data_access")
    if (not isinstance(access, dict) or access.get("mode") != "read_only"
            or access.get("approved") is not True or not access.get("source")):
        gaps.append("ACCESS_NOT_READ_ONLY_APPROVED")
    if pilot.get("human_review") is not True:
        gaps.append("REVIEW_MISSING")
    stops = pilot.get("stop_conditions")
    if not isinstance(stops, list) or not stops or any(
        not isinstance(item, str) or not item.strip() for item in stops
    ):
        gaps.append("STOP_RULE_MISSING")
    return gaps


def phase_dates(start: date, gates: List[Dict[str, object]]) -> List[Dict[str, object]]:
    """Turn inclusive day ranges into dated phase review windows."""
    if any(not isinstance(gate, dict) for gate in gates):
        raise ValueError("Phase gates must be JSON objects")
    if [(gate.get("first_day"), gate.get("last_day")) for gate in gates] != [
        (1, 30), (31, 60), (61, 90)
    ]:
        raise ValueError("Phase gates must cover days 1–90 without gaps")
    phases = []
    for gate in gates:
        if not all(isinstance(gate.get(key), str) and gate[key] for key in (
            "name", "focus", "exit_evidence"
        )):
            raise ValueError("Phase gate description is missing")
        phases.append({
            "name": gate["name"],
            "start_date": (start + timedelta(days=gate["first_day"] - 1)).isoformat(),
            "end_date": (start + timedelta(days=gate["last_day"] - 1)).isoformat(),
            "focus": gate["focus"], "exit_evidence": gate["exit_evidence"],
        })
    return phases


def build_plan(
    pilot: Dict[str, object], value: Dict[str, object],
    gates: List[Dict[str, object]],
) -> Dict[str, object]:
    """Make a plan draft while refusing to infer real approval or value."""
    try:
        start = date.fromisoformat(pilot["start_date"])
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("Pilot requires an ISO start date") from error
    if (value.get("scenario") != "recorded"
            or value.get("evidence_level") != "FICTIONAL_SAMPLE_PROJECTION"
            or value.get("delivery_improvement") != "NOT_MEASURED"
            or type(value.get("projected_net_value")) not in (int, float)):
        raise ValueError("Expected Chapter 14 fictional recorded evaluation")
    gaps = charter_gaps(pilot)
    return {
        "pilot_id": pilot.get("pilot_id", "not recorded"),
        "state": "PLAN_BLOCKED" if gaps else "PLAN_READY_FOR_HUMAN_REVIEW",
        "blocking_gaps": gaps, "owner": pilot.get("owner", "not recorded"),
        "problem": pilot.get("problem", "not recorded"),
        "scope": pilot.get("scope", "not recorded"),
        "baseline": pilot.get("baseline"), "target": pilot.get("target"),
        "stop_conditions": pilot.get("stop_conditions", []),
        "phases": phase_dates(start, gates),
        "value_context": {
            "source": "Chapter 14 fictional recorded evaluation",
            "projected_net_value": value["projected_net_value"],
            "currency": value.get("currency", "unspecified"),
            "delivery_improvement": value["delivery_improvement"],
        },
        "day_90_decision": "HUMAN_REVIEW_REQUIRED",
        "scale_decision": "NO_AUTOMATIC_EXPANSION",
        "execution": "none", "publication": "none",
    }


def render_markdown(plan: Dict[str, object]) -> str:
    """Write a readable local draft without implying a completed pilot."""
    def single_line(value: object) -> str:
        return str(value).replace("\r", " ").replace("\n", " ")

    baseline = plan["baseline"] if isinstance(plan["baseline"], dict) else {}
    target = plan["target"] if isinstance(plan["target"], dict) else {}
    lines = [
        f"# 90-day pilot draft — {single_line(plan['pilot_id'])}",
        "", f"State: {plan['state']}", f"Owner: {single_line(plan['owner'])}",
        f"Problem: {single_line(plan['problem'])}",
        f"Scope: {single_line(plan['scope'])}",
        f"Blocking gaps: {', '.join(plan['blocking_gaps']) or 'none'}", "",
        f"Baseline: {baseline.get('sample_count', 'missing')} samples; "
        f"median {baseline.get('median_total_minutes', 'missing')} minutes",
        f"Target: at least {target.get('min_accepted', 'missing')} accepted of "
        f"{target.get('sample_count', 'missing')}; median assisted time at most "
        f"{target.get('max_median_total_minutes', 'missing')} minutes",
        "Stop conditions: " + ", ".join(single_line(item) for item in plan["stop_conditions"]),
        "",
    ]
    for phase in plan["phases"]:
        lines.extend([
            f"## {phase['name']} ({phase['start_date']} to {phase['end_date']})",
            phase["focus"], f"Exit evidence: {phase['exit_evidence']}", "",
        ])
    value = plan["value_context"]
    lines.extend([
        "## Day 90 decision boundary",
        f"Prior illustrative net value: {value['projected_net_value']} {value['currency']}",
        f"Delivery improvement: {value['delivery_improvement']}",
        "A person chooses continue, change, or retire from actual pilot evidence.",
        "No automatic expansion, execution, or publication occurred.", "",
    ])
    return "\n".join(lines)


def run(case: str, output_dir: Path, from_prior_outputs: bool = False) -> Dict[str, object]:
    """Build inspectable JSON and Markdown for one fictional charter."""
    pilots = read_json(HERE / "fixtures/pilot-cases.json")
    gates = read_json(HERE / "phase-gates.json")
    if not isinstance(pilots, dict) or not isinstance(gates, list) or case not in pilots:
        raise ValueError(f"Unknown or invalid pilot case: {case}")
    value_path = (
        REPO_ROOT / "chapters/14-was-it-worth-building/example/outputs/recorded.json"
        if from_prior_outputs else HERE / "fixtures/value-recorded.json"
    )
    value = read_json(value_path)
    if not isinstance(pilots[case], dict) or not isinstance(value, dict):
        raise ValueError("Pilot and value inputs must be JSON objects")
    plan = build_plan(pilots[case], value, gates)
    try:
        case_dir = output_dir / case
        case_dir.mkdir(parents=True, exist_ok=True)
        (case_dir / "plan.json").write_text(
            json.dumps(plan, indent=2) + "\n", encoding="utf-8"
        )
        (case_dir / "plan.md").write_text(render_markdown(plan), encoding="utf-8")
    except OSError as error:
        LOGGER.error("Cannot write local pilot plan: %s", error)
        raise
    LOGGER.info("Case %s: %s", case, plan["state"])
    return plan


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=("a", "b", "c", "d", "e"), required=True)
    parser.add_argument("--from-prior-outputs", action="store_true")
    arguments = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    plan = run(arguments.case, HERE / "outputs", arguments.from_prior_outputs)
    print(f"Pilot plan: {plan['state']}")


if __name__ == "__main__":
    main()
