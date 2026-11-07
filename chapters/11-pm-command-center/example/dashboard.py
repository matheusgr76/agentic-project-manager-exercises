"""Build a read-only Acme PM Command Center from local chapter outputs."""

from __future__ import annotations

import argparse
import html
import json
import logging
from pathlib import Path
from typing import Dict, List


LOGGER = logging.getLogger(__name__)
HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]


def read_json(path: Path, label: str) -> Dict[str, object]:
    """Read a required local artifact and fail visibly on missing or invalid data."""
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        LOGGER.error("Cannot read %s: %s", label, error)
        raise ValueError(f"Cannot read {label}: {path}") from error
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def validate(handoff: Dict[str, object], knowledge: Dict[str, object]) -> None:
    """Require fields that let a PM distinguish status from source evidence."""
    if handoff.get("status") not in {"REVIEW_REQUIRED", "CONFLICT", "INCOMPLETE"}:
        raise ValueError("Unsupported handoff status")
    answers = knowledge.get("answers")
    if not isinstance(answers, dict):
        raise ValueError("Knowledge answer map is missing")
    for key in ("DEC-12/v2", "GH-41", "R1/risk"):
        if not isinstance(answers.get(key), dict):
            raise ValueError(f"Missing knowledge answer: {key}")
        if not isinstance(answers[key].get("sources"), list):
            raise ValueError(f"Missing source list: {key}")
    if not knowledge.get("as_of"):
        raise ValueError("Knowledge as-of date is missing")


def source_labels(answer: Dict[str, object]) -> List[str]:
    """Keep source IDs and paths visible without following source text as instructions."""
    if any(not isinstance(source, dict) or not {"event_id", "source_ref"} <= source.keys()
           for source in answer["sources"]):
        raise ValueError("Source entry is missing its ID or reference")
    return [
        f"{source['event_id']}: {source['source_ref']}"
        for source in answer["sources"]
    ]


def build_model(
    handoff: Dict[str, object], knowledge: Dict[str, object]
) -> Dict[str, object]:
    """Separate established records, hypotheses, and proposed human actions."""
    validate(handoff, knowledge)
    answers = knowledge["answers"]
    decision = answers["DEC-12/v2"]
    dependency = answers["GH-41"]
    risk = answers["R1/risk"]
    state = handoff["status"]
    if decision["status"] == "CONFLICT":
        state = "CONFLICT"
    return {
        "state": state,
        "as_of": knowledge["as_of"],
        "alerts": build_alerts(handoff, state),
        "facts": [
            {"label": "Decision DEC-12/v2", "value": decision.get("value") or decision["status"],
             "quality": (
                 f"As of {knowledge['as_of']}; source effective "
                 f"{decision.get('effective_at') or 'undated'}; "
                 f"authority {decision.get('authority') or 'unrecorded'}; {decision['status']}"
             ), "sources": source_labels(decision)},
            {"label": "GH-41 investigation", "value": dependency["status"],
             "quality": "No dated as-of claim", "sources": source_labels(dependency)},
            {"label": "Reporting run", "value": handoff.get("source_statuses", {}).get(
                "report", "not recorded"),
             "quality": handoff.get("source_dates", {}).get("report", "not recorded"),
             "sources": ["Chapter 9 coordinator handoff"]},
        ],
        "hypotheses": [
            {"label": "R1 release risk", "value": risk.get("value") or risk["status"],
             "quality": f"Hypothesis; review state {risk['status']}",
             "sources": source_labels(risk)},
        ],
        "human_review": (
            ["Recover or rerun the missing Risk Analyst output before acting"]
            if state == "INCOMPLETE" and "risk" in handoff.get("missing_artifacts", [])
            else ["Reconcile missing or conflicting records before acting"]
            if state != "REVIEW_REQUIRED" else [
                "Confirm DEC-12/v2 approval with its decision owner",
                handoff.get("proposed_action", "Refresh source dates before acting"),
            ]
        ),
        "activity": component_activity(handoff),
        "source_dates": handoff.get("source_dates", {}),
        "shared_references": handoff.get("shared_references", []),
        "publication": "none",
    }


def build_alerts(handoff: Dict[str, object], state: str) -> List[str]:
    """Keep missing, conflicting, and stale evidence prominent."""
    alerts = []
    if state == "INCOMPLETE":
        alerts.append(
            "Required specialist output is missing; do not treat this as a complete view."
        )
    if state == "CONFLICT":
        alerts.append(
            "Sources disagree. "
            + str(handoff.get("pm_question") or "Confirm the disputed source before reporting.")
        )
        if handoff.get("disagreement"):
            alerts.append(str(handoff["disagreement"]))
    if handoff.get("freshness_note"):
        dates = handoff.get("source_dates", {})
        risk_date = dates.get("risk") if isinstance(dates, dict) else None
        report_date = dates.get("report") if isinstance(dates, dict) else None
        date_context = (
            f"Risk assessment {risk_date}; report {str(report_date)[:10]}. "
            if risk_date and report_date else ""
        )
        alerts.append(date_context + str(handoff["freshness_note"]))
    return alerts


def component_activity(handoff: Dict[str, object]) -> Dict[str, str]:
    """Pair each specialist status with its recorded date or date gap."""
    statuses = handoff.get("source_statuses", {})
    dates = handoff.get("source_dates", {})
    activity = {
        name: f"{status} · {dates.get(name, 'date unavailable')}"
        for name, status in statuses.items()
    }
    if handoff.get("shared_references"):
        activity["shared references"] = ", ".join(handoff["shared_references"])
    return activity


def card(item: Dict[str, object]) -> str:
    """Render one source-backed card with all dynamic text escaped."""
    sources = "".join(f"<li>{html.escape(str(source))}</li>" for source in item["sources"])
    return (
        '<article class="card">'
        f'<h3>{html.escape(str(item["label"]))}</h3>'
        f'<p class="value">{html.escape(str(item["value"]))}</p>'
        f'<p class="quality">{html.escape(str(item["quality"]))}</p>'
        f'<details><summary>Sources</summary><ul>{sources}</ul></details>'
        '</article>'
    )


def render_html(model: Dict[str, object], stylesheet: str) -> str:
    """Build a standalone local page with no script or action endpoint."""
    alerts = "".join(f"<li>{html.escape(str(item))}</li>" for item in model["alerts"])
    facts = "".join(card(item) for item in model["facts"])
    hypotheses = "".join(card(item) for item in model["hypotheses"])
    reviews = "".join(
        f"<li>{html.escape(str(item))}</li>" for item in model["human_review"]
    )
    activity = "".join(
        f"<li><strong>{html.escape(str(key))}</strong>: {html.escape(str(value))}</li>"
        for key, value in model["activity"].items()
    )
    return (
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<title>Acme PM Command Center</title>'
        f"<style>{stylesheet}</style></head><body>"
        '<main><header><p class="eyebrow">FICTIONAL ACME · LOCAL EXERCISE</p>'
        '<h1>PM Command Center</h1>'
        f'<p>Knowledge as of {html.escape(str(model["as_of"]))} · '
        f'Coordinator state: <strong>{html.escape(str(model["state"]))}</strong></p></header>'
        f'<section class="notice"><h2>Review before acting</h2><ul>{alerts}</ul></section>'
        '<section><h2>Recorded position at selected date</h2>'
        f'<div class="grid">{facts}</div></section>'
        f'<section><h2>Hypotheses</h2><div class="grid">{hypotheses}</div></section>'
        f'<section class="split"><div><h2>Human review queue</h2><ul>{reviews}</ul></div>'
        f'<div><h2>Component snapshots</h2><ul>{activity}</ul></div></section>'
        '<footer>Read-only view. No issue, decision, message, or forecast was changed.'
        '</footer></main></body></html>'
    )


def input_paths(scenario: str, from_prior_outputs: bool) -> Dict[str, Path]:
    """Select committed fixtures or generated Chapters 9 and 10 outputs."""
    if from_prior_outputs:
        if scenario != "a":
            raise ValueError("Prior-output mode supports Scenario A only")
        return {
            "handoff": (
                REPO_ROOT
                / "chapters/09-one-agent-is-not-enough/example/outputs/a/handoff.json"
            ),
            "knowledge": (
                REPO_ROOT
                / "chapters/10-project-that-remembers/example/outputs/a/knowledge.json"
            ),
        }
    return {
        "handoff": HERE / "fixtures" / f"handoff-{scenario}.json",
        "knowledge": HERE / "fixtures" / "knowledge-a.json",
    }


def run(scenario: str, output_dir: Path, from_prior_outputs: bool = False) -> Dict[str, object]:
    """Write one read-only page and its inspectable view model."""
    paths = input_paths(scenario, from_prior_outputs)
    handoff = read_json(paths["handoff"], "handoff")
    knowledge = read_json(paths["knowledge"], "knowledge")
    model = build_model(handoff, knowledge)
    try:
        stylesheet = (HERE / "style.css").read_text(encoding="utf-8")
    except OSError as error:
        LOGGER.error("Stylesheet read failed: %s", error)
        raise
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "index.html").write_text(render_html(model, stylesheet), encoding="utf-8")
    (output_dir / "view-model.json").write_text(
        json.dumps(model, indent=2) + "\n", encoding="utf-8"
    )
    LOGGER.info("Built Command Center scenario %s: %s", scenario, model["state"])
    return model


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", choices=("a", "b", "c"), default="a")
    parser.add_argument("--from-prior-outputs", action="store_true")
    arguments = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    model = run(
        arguments.scenario, HERE / "outputs" / arguments.scenario,
        arguments.from_prior_outputs,
    )
    print(f"Command Center: {model['state']}")


if __name__ == "__main__":
    main()
