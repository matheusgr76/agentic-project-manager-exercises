# Chapter 8 — The Risk Nobody Reported

**Continue the same path:** Run Chapter 7 Scenario A, then pass its local investigation to the [Chapter 8 example](example/README.md). Chapter 8 asks whether several weak signals around DEC-12 create a release risk. All new records are fictional scenario inputs, dated after the Chapter 7 packet. They do not amend the shared Acme record.

**Starting point:** the Chapter 7 unresolved GH-41 investigation. The Dependency Agent explains one exception; the Risk Analyst examines whether independent signals point to a wider consequence. The [working example](example/README.md) uses only local files and Python's standard library.

## Exercise

1. **Describe the risk before scoring it.** Read Scenario A in [signals.csv](example/signals.csv). Write a cause-event-effect statement for R1. List each signal ID, source, date, status, team, and dependency. Keep the observed records separate from the possible release effect.
2. **Set an evidence threshold.** Use [risk_policy.md](example/risk_policy.md): three current, open signals from three teams, tied to one release and dependency. Explain why a single delayed task does not meet that threshold. Decide which dates and owners the PM must confirm.
3. **Build and run the analyst.** Have your coding assistant implement an offline assessment that preserves the source references, excludes resolved or stale records, reports missing evidence, and stops for PM review. Run A. Do not calculate a numerical probability from three invented observations.
4. **Challenge the finding.** Run B, where two records are resolved, and C, where one record is stale. Neither should produce an emerging-risk classification. Ask what additional record would change each conclusion. Test malformed inputs and the Chapter 7 handoff.
5. **Decide what happens next.** Draft a validation question and a reversible mitigation. The PM decides whether to put a risk on the formal register, who owns it, and whether the forecast changes. Compare your own result with [expected-results.md](example/expected-results.md).

## Check the result

Scenario A should surface a **risk hypothesis**, with S-01, S-02, and S-03 cited and human review required. The source rows establish reported delays and availability in a fictional test packet; they do not prove that R1 will slip. B and C should stop for insufficient evidence. No run may approve DEC-12, alter GH-41, send a message, or publish a forecast.

## Copyable coding-agent prompt

~~~text
Build the Chapter 8 Acme Risk Analyst against the local fictional CSV and optional Chapter 7 GH-41 investigation. First show a short plan and the permitted read/write boundary. Identify a release-risk hypothesis only when three open signals from distinct teams are dated within seven days and share a release and dependency. Preserve IDs, dates, exclusions, alternative explanations, and the PM's unanswered question. Keep observations separate from predicted impact. Use qualitative evidence language; do not invent a probability. Write only a local analysis file. Test the supported pattern, resolved false positive, stale signal, malformed input, and invalid Chapter 7 handoff. Show the run and test commands. Do not change source records, issues, decisions, messages, or forecasts.
~~~

The [sample analysis](example/sample-analysis.md) and working code show one implementation. Judge your own evidence first.
