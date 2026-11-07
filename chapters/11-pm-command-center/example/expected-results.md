# Expected results

All three pages are generated from fictional local exercise outputs. The browser page and `view-model.json` should agree.

## A — reviewable, dated view

The page state is `REVIEW_REQUIRED`. DEC-12/v2 appears as PENDING from E-01. GH-41 appears as UNDATED_CONTEXT, with no dated as-of claim. R1/risk appears in the Hypotheses section, not as a confirmed release delay. The notice preserves the Chapter 9 freshness warning: the November 9 risk assessment predates the November 12 report. The source details identify the underlying records. Publication remains `none`.

## B — contradiction

The page state is `CONFLICT`. The notice shows both disputed GH-41 claims: the dependency artifact says `RESOLVED` and the report says `IN_PROGRESS`. It asks for the current GH-41 record. DEC-12 remains a separate pending fact. The human review queue contains a reconciliation instruction instead of routine next steps. It does not choose the resolved claim from the invented Chapter 9 conflict fixture.

## C — incomplete inputs

The page state is `INCOMPLETE`. The notice says a required specialist output is missing. The page can still show its dated knowledge records, but it cannot claim the project view is complete.

Each rerun replaces exactly one local HTML file and one JSON view model for that scenario. No run sends or changes anything outside the local outputs directory.
