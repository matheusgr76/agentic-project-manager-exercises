# Chapter 14 — Was It Worth Building?

Acme's PM has a working demonstration and a governance plan. The CEO asks whether the effort paid for itself. This chapter uses a **fictional, illustrative** six-task sample to test the whole cost of assisted work: operator time, review, correction, and fallback when an output is rejected. It does not claim that Acme observed these results or improved delivery.

## Work in the chapter's cadence

1. Define the unit of work and what counts as accepted output before calculating time saved. Use the [measurement contract](example/measurement-policy.md).
2. Inspect the [paired task records](example/work-samples.csv). Calculate the first task's baseline and assisted minutes by hand. Then find the rejected output and its fallback.
3. Run the [local evaluator](example/README.md) in `recorded` mode. Compare the sample total with the monthly projection and the full twelve-month cost.
4. Run `counterfactual` mode. It changes one fictional acceptance assumption. Explain why its favorable result is a sensitivity test, not an observed improvement.
5. Use the [decision prompt](example/evaluation-prompt.md) and [expected results](example/expected-results.md) to recommend continue, change, or retire. State what remains unmeasured and what would make the recommendation change.

The code uses only local files and Python's standard library. It does not send information or change a project system. The calculation is an example of how to evaluate a pilot, not a price quote or financial forecast for the reader's organization.
