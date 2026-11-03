# Fictional run gate policy

The input is the Chapter 11 Scenario A view model, copied to `fixtures/view-model-a.json`. Its structured `source_dates.risk` field is the date of the Chapter 8 assessment. The gate never derives a date from prose. The local case row supplies run time, source completeness, attempt number, and run ID.

1. Validate the local files and required fields. Invalid files stop with an error; they do not produce a review-ready run.
2. Reject an attempt number above the configured maximum. The exercise does not sleep or automatically retry. An operator chooses the second case after repairing its fictional source.
3. If retrieval is partial, stop as `BLOCKED_SOURCE`. Never substitute old data for missing data.
4. If the risk assessment is older than `max_risk_age_days` at the case time, stop as `BLOCKED_STALE`. A recorded date is required.
5. A passing case is `READY_FOR_PM_REVIEW`, not approved or published. Store one successful entry keyed by run ID with a digest of the view model.
6. A repeated successful run ID and identical digest returns `ALREADY_PROCESSED`. The same ID with different content returns `INPUT_CHANGED_REVIEW` and requires a human decision.

Every evaluated attempt writes a local health record and appends an audit event. Blocked attempts never enter the success ledger. These are local simulations of conditions; `PARTIAL` is a test field, not a real connector outage.
