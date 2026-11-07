# Chapter 9 — One Agent Is Not Enough

**Continue the same path:** The Chapter 7 Dependency Agent investigates GH-41. The Chapter 8 Risk Analyst flags a possible R1 pattern. The Chapter 6 reporting run has its own review status. This chapter gives the PM one traceable handoff from those three outputs. It does not create a swarm of agents or give any component authority to publish.

**Starting point:** run the [offline coordinator](example/README.md) against committed fictional fixtures, then rerun it against the local outputs you produced in Chapters 6–8. The fixtures preserve the existing case C reporting time of November 12 and the Chapter 8 risk assessment date of November 9. The coordinator must say that the earlier risk signals need rechecking; they are not one simultaneous snapshot.

## Exercise

1. **Map the three jobs.** Identify what the Dependency Agent, Risk Analyst, and scheduled reporting workflow each produced, their source references, and their stop reasons. Write a short handoff contract: required fields, allowed local output, and decisions reserved for the PM.
2. **Coordinate a consistent case.** Run Scenario A. Trace GH-41 and DEC-12 across the dependency and risk outputs, keep S-01 to S-03 as separate risk signals, and record the source dates. The local handoff should be `REVIEW_REQUIRED`; it should not claim the older risk assessment is a current forecast.
3. **Force a disagreement.** Run Scenario B. Its invented dependency fixture says GH-41 is `RESOLVED` while the reporting artifact says GH-41 is in progress. Do not select the more confident wording. Stop with `CONFLICT`, preserve both statuses, and ask the GH-41 owner for the current record and effective time. The report's separate DEC-12 pending claim remains visible.
4. **Remove an input.** Run Scenario C. The risk artifact is missing. Stop with `INCOMPLETE`, name the missing component, and do not turn the two remaining outputs into a complete management brief.
5. **Measure the cost of coordination.** Compare the time to collect three outputs, resolve repeated references, review dates, and answer the PM's question with a manual version. Count correction and review time. Add another specialist only if its distinct job improves the whole workflow.

## Check the result

The coordinator reuses specialist artifacts rather than asking each specialist to reread GH-41. It records shared references, individual statuses, dated risk and report outputs, and the missing date on Chapter 7's investigation. Only a local `handoff.json` is written. No message, GitHub issue, decision, report, or release forecast is changed.

## Copyable coding-agent prompt

~~~text
Build a small offline coordinator for the fictional Acme Chapter 7 investigation, Chapter 8 risk analysis, and Chapter 6 report-run record. Show a plan and the read/write boundary first. Validate required fields. Preserve each component's status and source date, deduplicate shared references without merging distinct claims, and mark the November 9 risk assessment as earlier than the November 12 report. Produce a local handoff for PM review. Test a consistent case, an invented GH-41 resolved-versus-in-progress contradiction, a missing risk artifact, malformed input, and a repeat run. Preserve the separate DEC-12 pending claim. A conflict or missing input must stop; do not guess which component is right. Do not send, publish, change source records, approve DEC-12, close GH-41, or commit to R1 dates.
~~~

Inspect the [working example](example/README.md) and [expected results](example/expected-results.md) after your own run.
