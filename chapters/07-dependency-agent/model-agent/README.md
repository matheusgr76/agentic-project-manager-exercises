# Model-driven Chapter 7 agent

Here a language model chooses each next tool call. The Python runtime executes the calls, enforces the limits, and writes the only output. Compare with the [rule-based example](../example/README.md), which uses fixed code and no model.

**Status.** The runtime rules are tested offline (30 tests, using a scripted stand-in for the model and a stub of the SDK). **No live model run has been recorded in this repository yet.** `live_check.py` runs scenarios A, B, C and the variation against the real API and writes the report. See [What is verified](#what-is-verified).

## Requirements and cost

| Need | Detail |
| --- | --- |
| Python | 3.10 or newer |
| Package | `pip install -r requirements.txt` (the `anthropic` SDK) |
| Account | An Anthropic API account and key from console.anthropic.com. A chat subscription does not include API use |
| Key | Set `ANTHROPIC_API_KEY` in your terminal. Never paste it into a file in this repository |
| Model | Default `claude-haiku-5-5`. Change with `ACME_MODEL` |
| Cost (estimate, not observed) | A run is bounded at 10 model calls. Estimated from the size of the offline transcripts (characters ÷ 4): a typical 4-call run sends about 3,300 input and 250 output tokens; a high-usage 10-call run about 15,000 input and 3,500 output tokens. At the Haiku 5.5 list prices listed on [Anthropic's pricing page](https://platform.claude.com/docs/en/docs/about-claude/pricing) (checked 2026-11-04 through secondary reports only, because the official page could not be fetched; $0.10 input, $0.50 output per million tokens, prompts up to 100,000 tokens) that is about $0.0005 typical and $0.003 high-usage. These are estimates, not bounds: the number of calls is capped, but the size of each prompt is not. On a model priced 20 times higher, up to about $0.07. Check current prices; `live_check.py` reports observed token usage and the cost calculated from it |

## Run it (from this folder)

~~~powershell
cd chapters/07-dependency-agent/model-agent
pip install -r requirements.txt
$env:ANTHROPIC_API_KEY = "paste-your-key-here"      # macOS/Linux: export ANTHROPIC_API_KEY=...
python model_agent.py --scenario b
python live_check.py                                 # all four cases and one report
python -m unittest discover -s tests -v              # offline, free, no key
~~~

Outputs appear in `outputs/<scenario>/`: `investigation.json` (result), `exception-register.json` (the one permitted write), `transcript.md` and `transcript.json` (every tool request and what the runtime returned). `outputs/` is ignored by Git. `live_check.py` instead writes to `evidence/live/<UTC timestamp>/` (one new folder per batch, never overwritten, meant to be committed) and adds `live-run-report.md` there.

## Three different limits

| Limit | Value | What it bounds |
| --- | --- | --- |
| Retrieval limit | 6 reads (set by `Max retrievals` in the policy) | Records the model may read. Failed reads count. Reads rejected by the ID rule below do not |
| Model-turn limit | 6 + 4 = up to 10 model calls | The whole loop, including rejected reads, rejected submissions and blocked tools. Reaching it records `turn_limit` |
| Retry limit | 2 automatic retries per call, 60-second timeout | One API request. Applies to connection errors, rate limits and server errors. A permanent error such as a bad key is not retried |

## What the model controls, and what it cannot

| The model decides | The runtime enforces |
| --- | --- |
| Which record to read next, or to stop | Only `read_record` and `submit_investigation` exist. Any other name, including `update_register`, is blocked and logged without reaching an internal action |
| Whether the evidence resolves the question | The first read must be the initial issue; afterwards only IDs that appear in records already read. Other reads are rejected and not counted. The records folder restriction still applies |
| The wording of findings | A submission must have every required field with the right type and allowed values, or it is returned to the model with a message |
| | A RESOLVED answer is rejected unless the current decision was read, is APPROVED, names an approver and matches the required version. Cited records must have been read |
| | Records reach the model labeled UNTRUSTED; a comment inside a record cannot grant a permission |

## If something goes wrong

| What happens | What you see | What is saved |
| --- | --- | --- |
| API error (bad key, no network, rate limit, wrong model id, timeout) | A short message and "What to do" on screen, exit code 2. No traceback | `investigation.json` with stop reason `model_api_error`, a failure record in the register, and the transcript up to the failure |
| The model never submits | Stop reason `retrieval_limit`, `turn_limit` or `model_did_not_conclude` | Result, register entry, transcript |
| The model asks for a forbidden tool | The runtime answers BLOCKED; the run continues | Listed in `blocked_actions` |
| A submission is incomplete | The runtime answers REJECTED with the reason; the model may correct it | Listed in `rejected_submissions` |

## Files

| File | Purpose |
| --- | --- |
| `agent-policy.md` | The short instruction and policy. Sent to the model as its system prompt; the runtime reads the retrieval limit from it |
| `model_agent.py` | Runtime: tool schemas, loop, enforcement, transcript. Reuses `LocalTools` from the rule-based example |
| `live_check.py` | Runs the four cases against the live API and writes `live-run-report.md` |
| `tests/test_model_agent.py` | 30 offline tests: version mismatch, missing evidence, forbidden and undeclared tools, malformed submissions, ID boundary, API failure, bounds, UTF-8 |
| `variation/` | A second PM problem (release gate) with records, policy and expected behavior |
| `sample-output/offline-test-artifact-scripted-replay-b.md` | Transcript format from the test double. **Not an observed model run** |

## Build your own variation

1. Copy `variation/` and change the records to match another approval question in your work, using fictional data only.
2. Edit the policy's Goal, Max retrievals and Prohibited lines.
3. Write down the expected reads, classification and what must not happen *before* running.
4. Run with `--records-dir`, `--policy`, `--issue-id`. Compare the transcript with your expectations; add one test per surprise.

## What is verified

| Item | Status |
| --- | --- |
| Limits, blocking, validation, ID boundary, failure records, variation, report logic | Executed: 30 offline tests pass on Linux |
| Unreachable API with the real SDK (retries, exit code 2, saved stop record) | Executed offline |
| Windows | **Not executed.** Text files are now read and written as UTF-8. The earlier Windows failure was reproduced under an ASCII locale (not Windows) and the fix passes there |
| Request accepted by the live API; real model behavior on A, B, C and the variation; observed token usage and cost | **Not executed.** Run `python live_check.py` and keep the report |

Source text such as the comment in GH-41 reaches the model as data labeled UNTRUSTED. Whether a given model ignores it is something to observe in your transcript; the runtime's block does not depend on it.
