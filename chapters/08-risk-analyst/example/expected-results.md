# Expected results

All dates and signals are fictional test data. Run from the repository root using the commands in this folder's README.

## A — cross-team pattern

`classification` is `EMERGING_RISK_FOR_REVIEW`; `evidence_references` are S-01, S-02, S-03; `stop_reason` is `human_review_required`. The possible R1 impact is a hypothesis. The output includes an alternative explanation, a PM question, and `probability: not estimated`. When the Chapter 7 file is supplied, GH-41 and DEC-12 appear under `chapter_7_context`, not as new Chapter 8 signal rows.

## B — resolved signals

`classification` is `INSUFFICIENT_EVIDENCE`. S-04 and S-06 appear among excluded signals. S-05 alone cannot establish the cross-team pattern.

## C — stale signal

`classification` is `INSUFFICIENT_EVIDENCE`. S-07 is excluded because its October 23 date is outside the seven-day window. The PM should request a newer Alpha update before treating the pattern as current.

The example never writes a decision or issue, communicates externally, or publishes a forecast. Running A twice replaces the same local analysis file; it does not create duplicate risks.
