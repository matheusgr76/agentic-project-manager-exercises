# Chapter 10 — The Project That Remembers

**Continue the same path:** Chapter 9 made the PM's current handoff easier to inspect. Chapter 10 asks what happens when an old conclusion is retrieved later. Use the [offline knowledge-base example](example/README.md) to reconstruct the decision state at a chosen date, mark superseded records, and stop on conflicting sources.

**Starting point:** the shared DEC-12 decision record, Chapter 7's undated GH-41 investigation, Chapter 8's dated risk hypothesis, and Chapter 9's dated handoff. Acme and every new record are fictional. The approval and conflicting export in Scenarios B and C are **invented future variations**, not updates to the shared Acme packet.

## Exercise

1. **Inventory what is worth remembering.** Read [records.csv](example/records.csv). For each key, identify the claim, source, effective date, recorded date, review date, and authority. Notice that the Chapter 7 investigation has no source timestamp. Keep it as undated context rather than assigning it an invented date.
2. **Ask a time-specific question.** Run Scenario A as of November 12. DEC-12/v2 is pending in the shared fictional decision record. The R1 risk remains a hypothesis. The GH-41 investigation can be cited, but its undated source cannot prove what was true on November 12.
3. **Correct old knowledge.** Run Scenario B as of November 15. A clearly labeled invented approval addendum supersedes the pending DEC-12/v2 record. Ask the same question as of November 12: the later addendum must not rewrite history. Check that GH-41 and the risk hypothesis are still not automatically resolved.
4. **Test conflict and invalidation.** Run Scenario C. Two fictional decision sources disagree at the same effective date. The answer must be CONFLICT with both references; it cannot select one by recency or confidence. Break a `supersedes` link in a copy and confirm a visible failure.
5. **Decide when richer retrieval is justified.** Measure how often the small structured history answers actual PM questions and how often a person must correct it. Only add document search or retrieval-augmented generation if the records to be found cannot be maintained reasonably as this small index. Preserve the source, freshness, and correction rules either way.

## Check the result

The example does not call an AI model or company system. It writes one local `knowledge.json` per scenario. It does not approve a decision, close GH-41, remove a risk, send a message, or publish status. An approved DEC-12/v2 entry in the invented Scenario B only changes that decision's answer. The prior pending entry remains in history with an explicit supersession link.

## Copyable coding-agent prompt

~~~text
Build an offline Acme project-history reader from the fictional Chapter 10 CSV. Show a short plan and read/write boundary before editing. Store key, value, effective date, recorded date, review date, source reference, authority, and explicit supersedes link. Answer as-of queries without using later records to rewrite earlier answers. Keep undated Chapter 7 evidence as context, not a dated fact. In the invented approval variation, supersede only DEC-12/v2; do not close GH-41 or erase the R1 risk hypothesis. On two active contradictory decision records, stop with CONFLICT and cite both. Reject invalid links and source paths. Write only local JSON. Test past-date retrieval, supersession, stale review, undated context, conflict, invalid input, and repeat runs. Do not send, approve, publish, or change source files.
~~~

Compare your own result with the [working example](example/README.md) and [expected outputs](example/expected-results.md).
