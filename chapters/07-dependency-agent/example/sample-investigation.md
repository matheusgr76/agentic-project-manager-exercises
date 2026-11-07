# Example investigation record — Scenario A

This is a reader-facing rendering of the local JSON output. It is an illustrative result, not a formal Acme decision.

**Exception:** GH-41 depends on DEC-12.

**Evidence consulted:** [GH-41 issue](scenarios/a/issue-GH-41.md), [DEC-12 decision](scenarios/a/decision-DEC-12.md), and [UP-1 team update](scenarios/a/update-UP-1.md). Three retrieval calls were used.

**Confirmed findings:**

- GH-41 is IN_PROGRESS because independent interface sizing has started. Its latest update says the final data contract remains unresolved.
- DEC-12 is PENDING for version 2. No approver is recorded.
- UP-1 says option B looks good. It does not establish formal approval.

**Unresolved question:** Who will formally approve the required version 2 definition, and when?

**Clarification draft:** “Please confirm the approved missing-value definition, version, scope, approver, and effective date for GH-41 before full sizing proceeds.” This is local text awaiting PM review; it has not been sent.

**Recommended action:** Ask the PM to review the clarification draft.

**Executed action:** Update the local exception register keyed by GH-41 and read it back to verify the ID, evidence references, and classification. Changed prior results remain under the entry's history; identical reruns do not add a duplicate. No message was sent and no source record was changed.

**Authority used:** Read three local records; write one local register entry.

**Stop reason:** Human approval is required for the next consequential action. The dependency remains unresolved.

**Confidence:** SUPPORTED. The pending decision record supports the conclusion that the dependency remains unresolved. This assesses the evidence for the conclusion; it does not claim approval.

Compare this with outputs/a/investigation.json after running the example. Wording can differ; the evidence boundary and action record should agree.
