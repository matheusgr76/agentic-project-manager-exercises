# Chapter 11 — The PM Command Center

**Continue the same path:** Chapters 7–10 created investigations, a risk hypothesis, a coordinator handoff, and a time-specific project history. The [Chapter 11 example](example/README.md) puts their outputs in one read-only local browser page. It shows what is recorded, what is only a hypothesis, which source dates differ, and what still needs human review.

**Starting point:** the committed fictional Chapter 9 and 10 outputs in [fixtures](example/fixtures/). Readers can also rebuild the page from their own local Chapter 9 and 10 outputs. The Command Center is a view, not a second project-management database. It does not write to the shared packet, approve DEC-12, close GH-41, send a message, or publish a forecast.

## Exercise

1. **Choose the PM's questions before drawing the page.** List the few things the PM needs at the start of a review: decision state, dependency context, risk hypothesis, reporting run, source dates, and next human decision. Separate recorded position from a forecast or recommendation.
2. **Build the normal view.** Run Scenario A. Open the generated local `index.html`. Trace the DEC-12/v2 and R1/risk cards to their cited sources. Confirm that GH-41 is shown as undated context, the R1 item remains a hypothesis, and the November 9 versus November 12 gap appears in the review notice.
3. **Test a contradiction.** Run Scenario B. Its fictional coordinator handoff says CONFLICT. The page must foreground that state and replace routine next steps with a reconciliation instruction. It must not choose a decision status or present a green release forecast.
4. **Remove an input.** Run Scenario C. The handoff is INCOMPLETE because the Risk Analyst output is missing. The page may display known records, but it must say the view is incomplete and avoid a complete management conclusion.
5. **Review the interface as a PM.** Open the source details on each card. Can you tell which claim is supported, which is a hypothesis, and what a person must do? Compare the time to understand and correct the page with reading the separate artifacts. Keep or remove elements based on that test, not on how impressive the screen looks.

## Check the result

The [working example](example/README.md) generates an `index.html` and a `view-model.json` for each scenario. It has no JavaScript, network requests, action buttons, or account connection. All dynamic text is escaped before it enters HTML. The view model provides a machine-readable trace for tests and reader inspection.

## Copyable coding-agent prompt

~~~text
Build a small read-only local Acme PM Command Center from the Chapter 9 coordinator handoff and Chapter 10 knowledge answer. Show a plan and the read/write boundary before editing. Validate required fields. Separate recorded position, risk hypotheses, human review, component dates, and source references. Show the knowledge as-of date and the November 9/12 snapshot gap. Generate a self-contained local HTML file and a JSON view model. In a conflict or missing-input case, make the stop state prominent and do not show routine actions as approved. Escape all source text before rendering. Test normal, conflict, incomplete, malformed input, untrusted HTML text, and repeat runs. Do not send messages, change issues or decisions, publish a report, or commit to a release date.
~~~

Compare your own page with the [sample screen description](example/sample-screen.md) and [expected results](example/expected-results.md).
