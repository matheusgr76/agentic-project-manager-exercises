# Fictional authority matrix

| Action | Actor role | Approval | Possible effect in a live system | Exercise decision |
| --- | --- | --- | --- | --- |
| Read Command Center view | Agent or PM | None | Read project data | Local check only |
| Draft a review note | Agent or PM | None | Creates a draft if later implemented | Local check only |
| Update GH-41 | PM | Exact issue-owner approval | Changes a shared issue | Simulation only |
| Publish a report | PM | Exact project-sponsor approval | Sends an external report | Simulation only |

The machine-readable rules are in `policy.json`. The `actor-context.json` fixture stands in for identity supplied through a trusted system. The request's `source_text` is untrusted data and cannot change the actor role, action rules, or approval record. No password or API token is stored in this repository.

The local gate requires a Chapter 12 reviewable health state for actions with an external effect. It checks the approval's action, target, approver role, policy version, and expiry. Passing the gate means `SIMULATED_AUTHORIZED`; the code still performs no action. A live system would need independently verified identity, credential scoping, transactional audit storage, and enforcement at the connector boundary.
