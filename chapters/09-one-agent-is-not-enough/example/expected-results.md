# Expected results

These are fictional, deterministic practice outputs. Compare the JSON fields and source references, not incidental wording.

## A — aligned claims, different snapshot dates

`status` is `REVIEW_REQUIRED`. The dependency remains `UNRESOLVED`; the risk is `EMERGING_RISK_FOR_REVIEW`; the Chapter 6 report is `REVIEW_REQUIRED`. Shared references are DEC-12 and GH-41. S-01 to S-03 remain risk-signal references. The handoff says the November 9 assessment predates the November 12 report and that the dependency investigation has no dated run field. It proposes a source refresh before any current status claim.

## B — invented contradiction

`status` is `CONFLICT`. The alternate dependency fixture says `RESOLVED` without an approval record, while the report still says DEC-12 is pending. The coordinator does not choose one; it asks which decision state is current and when it changed.

## C — missing specialist output

`status` is `INCOMPLETE`, with `risk` named in `missing_artifacts`. No completed management brief or release conclusion is produced.

Every run writes one local `handoff.json` and records `publication: none`. Repeating a run replaces the same file.
