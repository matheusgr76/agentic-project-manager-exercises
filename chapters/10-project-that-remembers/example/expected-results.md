# Expected results

All outputs use fictional records. Scenario B's approval and Scenario C's conflicting export are invented practice variations, not observed Acme outcomes.

## A — November 12

DEC-12/v2 is `CURRENT` with value `PENDING`, sourced to E-01. GH-41 is `UNDATED_CONTEXT`; its investigation has no source date, so there is no as-of claim. R1/risk is a `CURRENT` `HYPOTHESIS` on its review date.

## B — November 15

DEC-12/v2 is `CURRENT` with value `APPROVED` only because the invented E-04 addendum explicitly supersedes E-01. `superseded_events` contains E-01. GH-41 remains `UNDATED_CONTEXT`. R1/risk is `NEEDS_REVALIDATION`, with value `HYPOTHESIS`; the new decision does not resolve the release question.

Run B again with `--as-of 2026-11-12`. DEC-12/v2 returns `PENDING` from E-01. E-04 was not yet effective or recorded for that earlier question.

## C — November 15

DEC-12/v2 is `CONFLICT`, value `null`, with E-04 and E-05 cited. The program does not select one. GH-41 remains undated context; R1/risk needs revalidation.

Every run reports `publication: none` and writes only a local answer. Repeating a run replaces its `knowledge.json` file.
