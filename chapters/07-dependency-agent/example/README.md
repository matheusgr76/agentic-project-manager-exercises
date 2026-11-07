# Runnable Chapter 7 example

This small Python program shows a bounded dependency investigation end to end. It reads only local fictional Markdown records. It can update only a local JSON exception register. It has no network or messaging code and needs no package installation.

To continue from the same Chapter 4–6 workshop, use the [Chapter 7 handoff](../../../START-HERE.md#chapter-7--investigate-the-chapter-6-exception). The command below also works when you want to study this agent on its own.

## Run it

From this directory, with Python 3.10 or newer:

~~~powershell
python agent.py --scenario a
python agent.py --scenario b
python agent.py --scenario c
python -m unittest discover -s tests -v
~~~

Each run prints an investigation record and writes outputs/<scenario>/investigation.json and exception-register.json. The outputs folder is ignored by Git. Run scenario A twice: the register still has only one GH-41 entry. A changed investigation is retained under that entry's `history`; an identical rerun does not add history. The local write is read back and checked against its ID, evidence references, and classification.

## What the scenarios demonstrate

| Scenario | Next reads chosen from evidence | Expected stop |
| --- | --- | --- |
| A — independent work | GH-41 → DEC-12 → UP-1 because the decision is pending and the issue references an update | Human approval required; dependency unresolved |
| B — version mismatch | GH-41 → DEC-12 → DEC-11 → UP-1 because DEC-12 points to a historical decision | Human approval required; v1 approval does not satisfy v2 |
| C — missing evidence | GH-41 → attempted DEC-12 read; missing file stands in for retrieval failure | Evidence unavailable; dependency unresolved |

The [policy](agent-policy.md) sets the six-call ceiling. The sample [Markdown records](scenarios/a/issue-GH-41.md) are readable inputs; edit copies to explore other outcomes. The code selects a historical decision only when the current decision references one, and selects an update only while approval remains unresolved. This makes the retrieval path depend on the evidence.

The tool layer permits only the local register update and rejects actions such as issue closure with PermissionError. The tests check that boundary directly. A prompt alone is not the permission control.

An approval for a dependency must match its required version, subject, and scope, as well as carry an approver. The fictional issue and decision fixtures name these fields so a future approved record for the wrong subject or scope cannot resolve GH-41.

The issue file also contains a comment telling the agent to close GH-41 and ignore the policy. The agent treats it as source text, while the tool layer still blocks issue closure.

The output is deliberately limited. It does not send the drafted clarification, approve a decision, change a GitHub issue, or make a delivery commitment. The [sample investigation record](sample-investigation.md) shows a readable Scenario A result; the [expected-results guide](expected-results.md) explains what to inspect in all three runs.

## Reading the code

- parse_record loads the simple Key: value lines from each Markdown file.
- LocalTools.read enforces record types, identifier format, and retrieval count.
- investigate chooses the next read and records findings and stop reason.
- LocalTools.perform is the only write gate; it updates the local register by exception ID.
- run_scenario writes an investigation JSON file for inspection.

This is an educational example, not a production integration or a general-purpose agent framework.

This rule-based code does not call a model; it demonstrates the same evidence-driven tool loop and permission boundary without requiring credentials. For a version where a language model chooses each next read, see the [model-driven agent](../model-agent/README.md). It needs an API key, costs money per run, and its live behavior is not yet verified; its offline tests are. The [runtime prompt example](investigation-prompt.md) shows the model's assignment in prose.
