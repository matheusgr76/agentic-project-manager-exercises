# Expected fictional plan states

Case A includes a specific accepted-output rule. A missing rule produces
`ACCEPTANCE_RULE_MISSING` and blocks the plan, even if the numeric target exists.

| Case | State | Blocking condition |
| --- | --- | --- |
| A | `PLAN_READY_FOR_HUMAN_REVIEW` | None; still no permission to deploy or expand. |
| B | `PLAN_BLOCKED` | `BASELINE_MISSING` |
| C | `PLAN_BLOCKED` | `ACCESS_NOT_READ_ONLY_APPROVED` |
| D | `PLAN_BLOCKED` | `TARGET_MISSING` |
| E | `PLAN_BLOCKED` | `STOP_RULE_MISSING` |

Case A has inclusive phase dates: days 1–30 run **November 16–December 15, 2026**; days 31–60 run **December 16, 2026–January 14, 2027**; days 61–90 run **January 15–February 13, 2027**. The output carries Chapter 14's fictional `-3216` twelve-month projected net value and `NOT_MEASURED` delivery improvement as context. It always says `NO_AUTOMATIC_EXPANSION` and `execution: none`.

Each command writes `outputs/<case>/plan.json` and `plan.md`. The markdown is a readable draft; the JSON keeps the state and source fields inspectable. `--from-prior-outputs` reads Chapter 14's generated `outputs/recorded.json` after running that chapter's example. No command uses a live system.
