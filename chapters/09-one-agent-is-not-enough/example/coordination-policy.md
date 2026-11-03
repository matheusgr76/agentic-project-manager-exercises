# Coordination policy

All Acme records and dates are fictional exercise data. The three components retain separate responsibilities: dependency investigation, risk hypothesis, and reporting-run status.

The coordinator may read their local JSON artifacts, validate required fields, compare overlapping references and statuses, and write a local handoff. It may not alter specialist outputs or source records. It has no tool to send messages, approve decisions, close issues, publish reports, or change a forecast.

If a required artifact is missing, stop as `INCOMPLETE`. If claims disagree, stop as `CONFLICT` and show both claims. Otherwise stop as `REVIEW_REQUIRED`. A shared reference is a pointer to a record, not proof that two conclusions agree. Preserve each source date; ask for a refresh when the risk assessment predates the report. The PM decides what to investigate, communicate, register, or publish.
