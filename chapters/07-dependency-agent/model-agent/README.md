# Model-driven Chapter 7 agent

Here a language model chooses each next tool call. The Python runtime executes the calls, enforces the limits, and writes the only output. Compare with the [rule-based example](../example/README.md), which uses fixed code and no model.

**Status.** The runtime rules are tested (10 tests, scripted stand-in for the model). **A live run against the Anthropic API has not been executed by the book's author or Claude.** Your first live run is the first real test of the API connection. See [What is verified](#what-is-verified).

## Requirements and cost

| Need | Detail |
| --- | --- |
| Python | 3.10 or newer |
| Package | `pip install -r requirements.txt` (the `anthropic` SDK) |
| Account | An Anthropic API account and key, created at console.anthropic.com. A chat subscription is separate and does not include API use |
| Key | Set `ANTHROPIC_API_KEY` in your terminal. Never paste it into a file in this repository |
| Cost | Pay per use. One run is about 3 to 6 short model calls with small inputs; expect cents or less. Check current prices; a retrieval limit of 6 caps the loop |
| Model | Default `claude-haiku-5-5`. Change with `ACME_MODEL` |

## Run it (from this folder)

~~~powershell
cd chapters/07-dependency-agent/model-agent
pip install -r requirements.txt
$env:ANTHROPIC_API_KEY = "paste-your-key-here"      # macOS/Linux: export ANTHROPIC_API_KEY=...
python model_agent.py --scenario b
python -m unittest discover -s tests -v              # offline, free, no key
~~~

Outputs appear in `outputs/<scenario>/`: `investigation.json` (result), `exception-register.json` (the one permitted write), `transcript.md` and `transcript.json` (every tool request and what the runtime returned). The folder is ignored by Git.

## What the model controls, and what it cannot

| The model decides | The runtime enforces |
| --- | --- |
| Which record to read next, or to stop | Only `read_record` and `submit_investigation` exist |
| Whether the evidence resolves the question | Six retrievals, failed reads included |
| The wording of findings | A RESOLVED answer is rejected unless the current decision was read, is APPROVED, has an approver and matches the required version |
| | Cited records must have been retrieved |
| | Any other tool name is blocked and logged; nothing outside `outputs/` is written |

## Files

| File | Purpose |
| --- | --- |
| `agent-policy.md` | The short instruction and policy. Sent to the model as its system prompt; the runtime reads the retrieval limit from it |
| `model_agent.py` | Runtime: tool schemas, loop, enforcement, transcript. Reuses `LocalTools` from the rule-based example |
| `tests/test_model_agent.py` | Version mismatch, missing evidence, forbidden action, source-text override, retrieval limit, variation |
| `variation/` | A second PM problem (release gate) with records, policy and expected behavior |
| `sample-output/scripted-replay-scenario-b.md` | Transcript format from the test double. **Not an observed model run** |

## Build your own variation

1. Copy `variation/` and change the records to match another approval question in your work, using fictional data only.
2. Edit the policy's Goal, Max retrievals and Prohibited lines.
3. Write down the expected reads, classification and what must not happen *before* running.
4. Run with `--records-dir`, `--policy`, `--issue-id`. Compare the transcript with your expectations; add one test per surprise.

## What is verified

| Item | Status |
| --- | --- |
| Runtime limits, blocking, rejection, register write, variation | Executed: 10 offline tests pass |
| Transcript writer | Executed with the scripted stand-in |
| Block formatting for the API | Executed against a stub only |
| Request accepted by the live API; tool-use behavior of the chosen model; real transcripts | **Not executed. Test on first live run** |

Source text such as the comment in GH-41 reaches the model as data labeled UNTRUSTED. Whether a given model ignores it is something to observe in your transcript; the runtime's block does not depend on it.
