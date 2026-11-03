# Expected local results

All rows are fictional. Start with an empty ignored `outputs` directory and run the cases in this order.

| Command case | Gate state | Success ledger entries afterward | Reason |
| --- | --- | ---: | --- |
| `a` | `READY_FOR_PM_REVIEW` | 1 | Risk source dated November 9 is three days old at November 12 run time. Human review remains required. |
| `a` again | `ALREADY_PROCESSED` | 1 | Same run ID and view-model digest. |
| `b` | `BLOCKED_SOURCE` | 1 | Simulated partial retrieval. |
| `b_recovered` | `READY_FOR_PM_REVIEW` | 2 | Simulated repair, second and final allowed attempt. |
| `c` | `BLOCKED_STALE` | 2 | November 9 risk assessment is seven days old at November 16 run time. |

`outputs/<case>/health.json` records the state and the evidence. `outputs/attempts.jsonl` records each attempt. `outputs/ledger.json` contains only the two successful run IDs. None of these files claims publication. Run `python -m unittest discover -s chapters/12-when-the-agent-breaks/example/tests -v` for the behavioral checks.
