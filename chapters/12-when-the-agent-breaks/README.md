# Chapter 12 — When the Agent Breaks at 2 A.M.

Acme's Command Center has a readable view. This exercise adds a local run gate that checks whether its inputs are complete and fresh, records failure reasons, and avoids processing the same successful run twice. All incidents, dates, and run IDs here are **fictional test cases**. The program makes no network call and does not publish a report.

Start with the [runnable example](example/README.md). Record your predicted state for each case before running it. Compare it with [expected results](example/expected-results.md), then change one input and explain the result from the source fields.

## Work in the chapter's cadence

1. Define the minimum information a run must have before the PM may review it: source status, dated risk evidence, a bounded attempt number, and a stable run ID.
2. Run A twice. The second pass must not add a second successful entry to the ledger.
3. Run B, then B-recovered. The first is blocked; the second is a controlled retry after a fictional source repair.
4. Run C. Explain why an otherwise complete view is too old to present as current.
5. Read the attempt audit and decide what a human should do next. Write a failure note using the [prompt](example/failure-prompt.md). Do not change an Acme decision or publish a result.

The [policy](example/run-policy.md) names the gates. The exercise tests behavior, including invalid input and a changed payload under an existing run ID. A later live integration would need its own network timeout, retry, and authorization design.
