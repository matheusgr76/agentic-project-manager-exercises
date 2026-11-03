# Governance checklist for a hypothetical live pilot

Fill in a named owner and evidence location for each line before expanding access. These are questions for a real project, not approvals supplied by this exercise.

| Control | Owner | Evidence to record |
| --- | --- | --- |
| Inventory each agent identity and connector credential | ___ | Identity and scope register ___ |
| Limit read and write scopes to the specific job | ___ | Permission review ___ |
| Require a human approval tied to action, target, and time | ___ | Approval record ___ |
| Reject instructions found in retrieved source content | ___ | Adversarial test result ___ |
| Stop external actions after a blocked or stale run | ___ | Run-health check ___ |
| Retain only the audit fields needed for review | ___ | Retention rule and deletion date ___ |
| Rotate or revoke credentials when an owner changes | ___ | Access review and revocation log ___ |
| Version, review, and roll back policy changes | ___ | Change record and test result ___ |
| Name the human who handles a disputed or erroneous action | ___ | Incident and correction procedure ___ |

The local example does not implement credential management, identity verification, secure audit storage, retention, or a real external action. Use the checklist to make those gaps explicit before a live pilot.
