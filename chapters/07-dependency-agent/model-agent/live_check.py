"""Run scenarios A, B, C and the release-gate variation against the live API and write one report.

Run from this folder, with ANTHROPIC_API_KEY set:   python live_check.py
It runs every case once (use --repeats 3 to see how stable the model is), keeps every result,
whether favorable or not, and writes evidence/live/<UTC timestamp>/live-run-report.md. Each batch gets its
own timestamped folder, so a rerun never overwrites earlier evidence. This costs money; see the README.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import shlex
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import model_agent as ma  # noqa: E402

# Prices are USD per million tokens for prompts up to 100,000 tokens (a higher tier applies above that).
# Override with --input-price and --output-price; the report states which values were actually used.
DEFAULT_PRICES = (0.10, 0.50)
PRICE_SOURCE = "https://platform.claude.com/docs/en/docs/about-claude/pricing"
PRICE_CHECKED = "2026-11-04 (official page could not be fetched from the authoring sandbox; rates confirmed only through secondary reports; verify against the official page before relying on them)"

EX = HERE.parent / "example" / "scenarios"
# name, records dir, policy, issue id, expected classification, expected stop reason, ids that must be read
CASES = [
    ("a", EX / "a", HERE / "agent-policy.md", "GH-41", "UNRESOLVED", "human_approval_required", ["GH-41", "DEC-12"]),
    ("b", EX / "b", HERE / "agent-policy.md", "GH-41", "UNRESOLVED", "human_approval_required", ["GH-41", "DEC-12", "DEC-11"]),
    ("c", EX / "c", HERE / "agent-policy.md", "GH-41", "UNRESOLVED", "evidence_unavailable", ["GH-41"]),
    ("variation", HERE / "variation" / "records", HERE / "variation" / "agent-policy.md", "GH-52", "RESOLVED", "investigation_complete", ["GH-52", "DEC-30"]),
]


def judge(res, cls, stop, must_read):
    found = []
    if res["stop_reason"] == "model_api_error":
        return ["API failure: " + res["failure"]["message"]]
    if res["classification"] != cls:
        found.append(f"classification {res['classification']} (expected {cls})")
    if res["stop_reason"] != stop:
        found.append(f"stop reason {res['stop_reason']} (expected {stop})")
    missing = [i for i in must_read if i not in res["evidence_references"]]
    if missing:
        found.append(f"evidence missing: {missing}")
    if res["blocked_actions"]:
        found.append(f"blocked actions: {res['blocked_actions']}")
    if res["rejected_submissions"] or res["rejected_reads"]:
        found.append(f"rejections: submissions={len(res['rejected_submissions'])} reads={res['rejected_reads']}")
    return found


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--model", default=os.environ.get("ACME_MODEL", ma.DEFAULT_MODEL))
    p.add_argument("--repeats", type=int, default=1)
    p.add_argument("--input-price", type=float, default=DEFAULT_PRICES[0])
    p.add_argument("--output-price", type=float, default=DEFAULT_PRICES[1])
    p.add_argument("--output-dir", type=Path, default=HERE / "evidence" / "live",
                   help="parent folder; each batch is saved in a new timestamped subfolder")
    p.add_argument("--price-source", default=None, help="where your --input-price/--output-price come from (required with an override)")
    p.add_argument("--price-checked", default=None, help="date you checked that source")
    a = p.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set. This script calls the paid API; see README.md.")
    overridden = (a.input_price, a.output_price) != DEFAULT_PRICES
    if overridden and not a.price_source:
        sys.exit("You overrode the prices. Also pass --price-source (where the prices come from) so the report can cite it.")
    command = " ".join(["python", "live_check.py"] + [shlex.quote(x) for x in sys.argv[1:]])
    started = datetime.now(timezone.utc)
    batch = a.output_dir / started.strftime("%Y%m%dT%H%M%SZ")
    n_suffix = 1
    while batch.exists():                        # never reuse a folder: earlier evidence stays untouched
        n_suffix += 1
        batch = a.output_dir / f"{started.strftime('%Y%m%dT%H%M%SZ')}-{n_suffix}"
    batch.mkdir(parents=True)
    a.output_dir = batch
    rows, total_in, total_out = [], 0, 0
    for n in range(1, a.repeats + 1):
        for name, recs, pol, issue, cls, stop, must in CASES:
            tag = name if a.repeats == 1 else f"{name}-run{n}"
            client = ma.AnthropicClient(a.model)
            out = a.output_dir / tag
            res = ma.run(client, recs, pol, issue, out)
            u = res["token_usage"] or {"input_tokens": 0, "output_tokens": 0, "calls": 0}
            cost = u["input_tokens"] / 1e6 * a.input_price + u["output_tokens"] / 1e6 * a.output_price
            total_in += u["input_tokens"]; total_out += u["output_tokens"]
            problems = judge(res, cls, stop, must)
            rows.append((tag, res, u, cost, problems))
            print(f"{tag}: {res['classification']} / {res['stop_reason']} / {'PASS' if not problems else 'DIFFERS'}")
    model_id = rows[0][1]["model"] if rows else a.model   # as reported by the runs themselves
    lines = ["# Live run report", "",
             f"- Date (UTC): {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
             f"- Model ID: `{model_id}`", f"- Environment: Python {platform.python_version()}, {platform.system()} {platform.release()}",
             f"- Complete command (as typed): `{command}`",
             f"- Settings used: model `{a.model}`, repeats {a.repeats}, input price ${a.input_price}/MTok, output price ${a.output_price}/MTok",
             f"- Batch folder: `{batch.name}`",
             f"- Limits: {ma.load_limit(HERE / 'agent-policy.md')} reads, up to {ma.load_limit(HERE / 'agent-policy.md') + ma.MAX_EXTRA_TURNS} model turns, "
             f"{ma.API_TIMEOUT_S}s timeout, {ma.API_MAX_RETRIES} retries per call", "",
             "| Run | Classification | Stop reason | Reads | Turns | Blocked | Rejected | Tokens in/out | Cost (USD) | Matches expected |",
             "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for tag, r, u, cost, problems in rows:
        lines.append(f"| {tag} | {r['classification']} | {r['stop_reason']} | {r['retrieval_calls']} | {r['model_turns']} | "
                     f"{len(r['blocked_actions'])} | {len(r['rejected_submissions']) + len(r['rejected_reads'])} | "
                     f"{u['input_tokens']}/{u['output_tokens']} | {cost:.5f} | {'Yes' if not problems else 'NO: ' + '; '.join(problems)} |")
    total = total_in / 1e6 * a.input_price + total_out / 1e6 * a.output_price
    lines += ["", f"Total tokens: {total_in} in, {total_out} out. Calculated cost: ${total:.5f} (token usage reported by the API x list prices).",
              "", "## Price assumptions", "",
              f"- Input: ${a.input_price} per million tokens; output: ${a.output_price} per million tokens",
              f"- Values: {'OVERRIDDEN on the command line (the built-in defaults of $%s / $%s were not used)' % DEFAULT_PRICES if overridden else 'built-in defaults (prompts up to 100,000 tokens)'}",
              f"- Source: {a.price_source if overridden else PRICE_SOURCE}",
              f"- Date checked: {a.price_checked or 'not recorded' if overridden else PRICE_CHECKED}",
              "- This is a calculation from API-reported token usage times list prices, not a billing statement. Prompts over 100,000 tokens would use a higher tier; these runs are far below that.", "",
              "Every run is listed, including any that differ from the expected behavior. Read each `transcript.md` before drawing conclusions."]
    report = a.output_dir / "live-run-report.md"
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Report: {report}")


if __name__ == "__main__":
    main()
