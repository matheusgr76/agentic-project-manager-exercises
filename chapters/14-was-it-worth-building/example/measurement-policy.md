# Fictional measurement contract

**Question:** Did the assisted process reduce effort enough to cover build and recurring costs while maintaining usable output? The six rows are invented paired tasks for teaching; they are not observations from Chapters 1–13 or a real Acme pilot.

**Unit:** One completed weekly-report or dependency-review task. `baseline_minutes` is the invented manual time for the same task. Assisted time is operator + review + correction minutes. If `pilot_accepted=no`, the task also requires a complete manual fallback equal to its baseline minutes. We credit no avoided manual work for a rejected output. `false_alert=yes` records a reviewer distraction; its time is already included in `review_minutes` and must not be added twice.

**Projection:** The sample contains six tasks and the hypothetical month contains 24 in the same task mix. Multiply the sample net minutes by 24/6. Convert at the fictional labor value per hour. Recurring cost is monthly maintenance plus infrastructure. Twelve-month total cost includes the one-time build cost. Return percentage is `(projected labor value - total cost) / total cost * 100`. Simple payback is shown only if projected monthly labor value exceeds recurring monthly cost; it is not a discounted cash-flow forecast.

**Quality and outcomes:** Count accepted pilot outputs and false alerts. The exercise does not measure delivery speed, schedule reliability, stakeholder trust, or causal project outcomes. The evaluator writes `NOT_MEASURED` for delivery improvement. A six-task, invented sample cannot establish a population result. The `counterfactual` mode changes only F-03 to accepted after its recorded correction time; it is a sensitivity case, not new evidence.

**Decision boundary:** A positive time or cost estimate is not permission to publish, write an issue, or expand agent access. The Chapter 13 authority checks still apply. A PM should validate the actual task mix, acceptance criteria, cost of failures, and local labor value before making a real investment decision.
