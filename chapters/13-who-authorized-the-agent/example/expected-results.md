# Expected local results

All people, requests, and approvals are fictional. Each case writes one local decision and appends one audit entry. No case executes an external action.

| Case | State | Why |
| --- | --- | --- |
| A | `LOCAL_ALLOWED` | Agent may inspect the local Command Center view. |
| B | `DENIED_ROLE` | Source text claims PM authority, but the separate actor context says agent. |
| C | `SIMULATED_AUTHORIZED` | PM role, matching reviewable Chapter 12 run, exact sponsor approval, current version and time. No publication occurs. |
| D | `DENIED_APPROVAL_SCOPE` | Approval covers `weekly-status`, not `board-status`. |
| E | `DENIED_APPROVAL_EXPIRED` | Issue-owner approval expired before the request. |
| F | `LOCAL_ALLOWED` | Agent may pass a local draft check; this program does not create a draft. |

Inspect `outputs/audit.jsonl`. It records request ID, actor role and context source, action, target, policy version, source ID, approval ID, state, and reason. It omits raw source text and credentials. The behavioral tests also reject an unknown action, a stale or mismatched Chapter 12 run, a wrong approver role, an old policy version, and a weakened external-action rule.
