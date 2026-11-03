# Chapter 7 — build the Acme Dependency Agent

**Starting point:** the Chapter 4 Report Builder and Chapter 6 workflow. Use only mock tools or local fictional files. This chapter asks you to implement the agent; it does not provide a finished agent.

**Want to see it work first?** Open the [runnable Python example](example/README.md). It includes a sample [agent policy](example/agent-policy.md), [runtime prompt for a model-assisted version](example/investigation-prompt.md), Markdown issue/decision/update records, three scenarios, expected outputs, and tests. Run it locally, inspect the trace, then build your own version using the steps below.

**Compare your work:** The [sample Scenario A investigation](example/sample-investigation.md) shows a reader-facing output, and the [expected-results guide](example/expected-results.md) covers all three runs. Make your own assessment before opening either.

## Exercise

1. Write `agent-policy.md`. Define the investigation goal; permitted reads and local exception-register updates; prohibited source changes, issue closure, decision approval, messages, and commitments; a maximum of **six retrieval calls**; and stop conditions for insufficient evidence, limit reached, or required human authorization.
2. Load [Scenario A](../../acme-practice-packet/chapter-7-scenarios.md#scenario-a--independent-work). Ask a coding agent to plan and implement a bounded investigation loop. The next retrieval must depend on what the previous evidence reveals; a fixed list of reads does not satisfy the exercise.
3. Produce a structured record with exception ID, evidence references, findings, unresolved questions, recommended action, executed action, authority used, and stop reason. The only permitted write is the local exception register. A clarification request can be drafted but not sent.
4. Run [Scenarios A–C](../../acme-practice-packet/chapter-7-scenarios.md) and the authority test. In B, DEC-11's version 1 approval does not satisfy version 2. In C, a failed decision retrieval must stop the investigation as unresolved.
5. Rerun A. The register should update the existing exception rather than create a duplicate. Inspect every source consulted, every executed action, and the reason for stopping. Compare full investigation and review time with a manual run.

## Check the result

GH-41 is `IN_PROGRESS` because independent sizing has started; DEC-12 remains `PENDING`. The agent must not infer approval from UP-1 or the issue status. An issue comment telling it to close GH-41 is untrusted source content. Prohibited writes must be blocked by the tool or execution layer, not only by words in a prompt.

Keep the policy, tests, investigation records, and exception register as evidence for later review.

## Copyable coding-agent prompt

~~~text
Build an educational dependency-investigation agent for the fictional Acme records in this chapter. Before editing, show a short implementation plan and identify the permitted tools. The agent receives GH-41, reads the issue, and chooses subsequent reads from evidence: the required decision, any historical decision referenced by it, and a team update only when useful. Enforce a maximum of six retrieval calls. Allow only local exception-register updates. Produce a structured investigation record with evidence references, findings, unresolved questions, recommendation, executed action, authority used, retrieval trace, and stop reason. Do not change source records, close issues, approve decisions, send messages, publish, or make commitments. Enforce the write restriction in the tool layer, not only in a prompt. Test Scenario A, version mismatch B, missing evidence C, a malicious issue comment, the call limit, and an idempotent rerun. Show the run and test commands.
~~~

Compare your result with the [working example](example/README.md). The example demonstrates one small implementation; your code can use another structure if it preserves the observable behavior and boundaries.
