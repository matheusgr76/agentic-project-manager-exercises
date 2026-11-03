# Chapter 13 — Who Authorized the Agent?

The Chapter 12 run gate made a failed run visible. Acme's PM now has to decide which actions the system may take, who can approve them, and what evidence survives afterward. The [local example](example/README.md) checks a fictional authority matrix and writes an audit record. It never calls GitHub, sends a message, or publishes a report.

## Work in the chapter's cadence

1. Start with the [authority matrix](example/authority-matrix.md). Separate reading and drafting from changing a shared record or publishing a report.
2. Run cases A and B. Compare a permitted local read with a publishing request that carries an instruction inside untrusted source text.
3. Run C, D, and E. Check exact target, approver role, expiry, and policy version against the [approval records](example/fixtures/approvals.json). An approval for one target must not authorize another.
4. Read the [audit](example/expected-results.md) and write an accountable handoff using the [review prompt](example/governance-prompt.md).
5. Complete the [governance checklist](example/governance-checklist.md) for a hypothetical live deployment. Name a human owner for access review, credential rotation, retention, and policy changes.

All people, dates, requests, and approvals are fictional. A passing local gate is an authorization decision in a simulation, not proof of a real identity or permission to execute a real external action.
