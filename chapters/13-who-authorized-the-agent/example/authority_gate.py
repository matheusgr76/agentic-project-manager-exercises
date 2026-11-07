"""Evaluate fictional Acme action authority without executing an action."""

from __future__ import annotations

import argparse
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict


LOGGER = logging.getLogger(__name__)
HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]


def read_json(path: Path) -> Dict[str, object]:
    """Read a required local JSON object, reporting I/O and parse failures."""
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        LOGGER.error("Cannot read %s: %s", path, error)
        raise ValueError(f"Cannot read JSON object: {path}") from error
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return value


def utc_time(value: str) -> datetime:
    """Require an explicit UTC timestamp for the approval comparison."""
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError) as error:
        raise ValueError("Expected UTC timestamp") from error
    if parsed.tzinfo is None or parsed.utcoffset().total_seconds() != 0:
        raise ValueError("Expected UTC timestamp")
    return parsed


def approval_decision(
    request: Dict[str, object], rule: Dict[str, object],
    approvals: Dict[str, object], policy_version: str,
) -> tuple[str, str]:
    """Match approval to the exact action, target, role, version, and time."""
    approval = approvals.get(request.get("approval_id"))
    if not isinstance(approval, dict) or approval.get("status") != "APPROVED":
        return "DENIED_APPROVAL", "No approved record for this request"
    if approval.get("action") != request["action"] or approval.get("target") != request["target"]:
        return "DENIED_APPROVAL_SCOPE", "Approval covers another action or target"
    if approval.get("approver_role") not in rule.get("approver_roles", []):
        return "DENIED_APPROVER_ROLE", "Approver role is outside the authority matrix"
    if approval.get("policy_version") != policy_version:
        return "DENIED_POLICY_VERSION", "Approval used another policy version"
    if utc_time(approval.get("expires_at_utc")) <= utc_time(request["requested_at_utc"]):
        return "DENIED_APPROVAL_EXPIRED", "Approval expired before the request"
    return "SIMULATED_AUTHORIZED", "All local checks passed; no action executed"


def validate_rule(rule: Dict[str, object]) -> None:
    """Reject an incomplete rule before it can weaken an action boundary."""
    if (not isinstance(rule.get("actor_roles"), list)
            or type(rule.get("approval_required")) is not bool
            or type(rule.get("external_effect")) is not bool):
        raise ValueError("Authority rule is incomplete")
    if rule["external_effect"] and (
        not rule["approval_required"]
        or not isinstance(rule.get("approver_roles"), list)
        or not isinstance(rule.get("allowed_targets"), list)
        or not rule["allowed_targets"]
    ):
        raise ValueError("External action requires approver roles and allowed targets")


def evaluate(
    request: Dict[str, object], actor: Dict[str, object],
    policy: Dict[str, object], approvals: Dict[str, object],
    health: Dict[str, object],
) -> Dict[str, object]:
    """Make one fail-closed decision from structured inputs only."""
    required = ("request_id", "action", "target", "requested_at_utc", "source_id")
    if any(not request.get(field) for field in required):
        raise ValueError("Request is missing a required field")
    utc_time(request["requested_at_utc"])
    if not actor.get("actor_role") or not actor.get("identity_source"):
        raise ValueError("Trusted actor context is missing")
    actions = policy.get("actions")
    if not isinstance(actions, dict) or not policy.get("version"):
        raise ValueError("Authority policy is incomplete")
    rule = actions.get(request["action"])
    if isinstance(rule, dict):
        validate_rule(rule)
    if not isinstance(rule, dict):
        state, reason = "DENIED_UNKNOWN_ACTION", "Action is absent from the authority matrix"
    elif actor["actor_role"] not in rule.get("actor_roles", []):
        state, reason = "DENIED_ROLE", "Actor role cannot perform this action"
    elif rule.get("external_effect") and request["target"] not in rule["allowed_targets"]:
        state, reason = "DENIED_TARGET", "Target is absent from the authority matrix"
    elif rule.get("external_effect") and (
        health.get("state") not in {"READY_FOR_PM_REVIEW", "ALREADY_PROCESSED"}
        or health.get("publication") != "none"
        or request["source_id"] != health.get("run_id")
    ):
        state, reason = "DENIED_RUN_HEALTH", "No matching unpublished reviewable run"
    elif rule.get("approval_required"):
        state, reason = approval_decision(request, rule, approvals, policy["version"])
    else:
        state, reason = "LOCAL_ALLOWED", "Local read or draft check passed; no action executed"
    return {
        "request_id": request["request_id"], "action": request["action"],
        "target": request["target"], "actor_role": actor["actor_role"],
        "identity_source": actor["identity_source"], "source_id": request["source_id"],
        "approval_id": request.get("approval_id", ""),
        "policy_version": policy["version"], "state": state, "reason": reason,
        "execution": "none", "publication": "none",
    }


def run(case: str, output_dir: Path, from_prior_outputs: bool = False) -> Dict[str, object]:
    """Read one case and persist an audit record without source text."""
    requests = read_json(HERE / "fixtures/requests.json")
    actors = read_json(HERE / "fixtures/actor-context.json")
    if case not in requests or case not in actors:
        raise ValueError(f"Unknown case: {case}")
    policy = read_json(HERE / "policy.json")
    approvals = read_json(HERE / "fixtures/approvals.json")
    health_path = (
        REPO_ROOT / "chapters/12-when-the-agent-breaks/example/outputs/a/health.json"
        if from_prior_outputs else HERE / "fixtures/health-a.json"
    )
    health = read_json(health_path)
    result = evaluate(requests[case], actors[case], policy, approvals, health)
    try:
        case_dir = output_dir / case
        case_dir.mkdir(parents=True, exist_ok=True)
        (case_dir / "decision.json").write_text(
            json.dumps(result, indent=2) + "\n", encoding="utf-8"
        )
        with (output_dir / "audit.jsonl").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(result, sort_keys=True) + "\n")
    except OSError as error:
        LOGGER.error("Cannot write authority audit: %s", error)
        raise
    LOGGER.info("Case %s: %s", case, result["state"])
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=("a", "b", "c", "d", "e", "f"), required=True)
    parser.add_argument("--from-prior-outputs", action="store_true")
    arguments = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    result = run(arguments.case, HERE / "outputs", arguments.from_prior_outputs)
    print(f"Authority: {result['state']}")


if __name__ == "__main__":
    main()
