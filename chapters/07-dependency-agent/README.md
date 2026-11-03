# Chapter 7 — build the Acme Dependency Agent

**Starting point:** the Chapter 4 Report Builder and Chapter 6 workflow. Use only mock tools or local fictional files. This chapter asks you to implement the agent; it does not provide a finished agent.

## Exercise

1. Write `agent-policy.md`. Define the investigation goal; permitted reads and local exception-register updates; prohibited source changes, issue closure, decision approval, messages, and commitments; a maximum of **six retrieval calls**; and stop conditions for insufficient evidence, limit reached, or required human authorization.
2. Load [Scenario A](../../acme-practice-packet/chapter-7-scenarios.md#scenario-a--independent-work). Ask a coding agent to plan and implement a bounded investigation loop. The next retrieval must depend on what the previous evidence reveals; a fixed list of reads does not satisfy the exercise.
3. Produce a structured record with exception ID, evidence references, findings, unresolved questions, recommended action, executed action, authority used, and stop reason. The only permitted write is the local exception register. A clarification request can be drafted but not sent.
4. Run [Scenarios A–C](../../acme-practice-packet/chapter-7-scenarios.md) and the authority test. In B, DEC-11's version 1 approval does not satisfy version 2. In C, a failed decision retrieval must stop the investigation as unresolved.
5. Rerun A. The register should update the existing exception rather than create a duplicate. Inspect every source consulted, every executed action, and the reason for stopping. Compare full investigation and review time with a manual run.

## Check the result

GH-41 is `IN_PROGRESS` because independent sizing has started; DEC-12 remains `PENDING`. The agent must not infer approval from UP-1 or the issue status. An issue comment telling it to close GH-41 is untrusted source content. Prohibited writes must be blocked by the tool or execution layer, not only by words in a prompt.

Keep the policy, tests, investigation records, and exception register as evidence for later review.
