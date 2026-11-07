# Chapter 2 — worked examples

Use the [CSV packet](source-records.csv) as the evidence. This is one defensible output, not the only acceptable wording. Records A–H form the first assessment. Record I is a separate variation. Records J–N concern the previous release.

## Initial Project Assessment from A–H

**Objective:** Acme wants a 25% forecasting improvement (A). Product proposes a proof of concept before deciding production scope (B). The baseline and improvement measure are not agreed (B), so the target is not yet a measured result.

**Confirmed facts:** Alpha's data definition is not approved (C). Bravo needs a stable definition for full integration sizing but can estimate independent interface work (D). Charlie can draft customer-facing test scenarios while access rules remain open (E). The available capacity snapshot is from the prior Friday, and allocations await confirmation after the previous-release closure inventory (F). Sales has discussed the target but no release date (G). The previous release still needs Product acceptance and support handover confirmation; the effort for these items is not estimated (H).

**Unknowns:** Agreed improvement baseline and method (B); approved data definition (C); proof-of-concept access rules (B, E); confirmed capacity and closure effort (F, H); and a defensible delivery forecast (A, C, D, F, H). The records do not formally assign every decision owner.

**Assumptions to validate:** Product may own proof-of-concept scope and the improvement measure (B). Alpha may own the data-definition proposal (C). Engineering leads may estimate their own teams' work (D, E). These are working assignments, not confirmed authority or capacity.

**Stakeholders and roles:** The CEO requests a report (A); Product proposes proof-of-concept scope (B); Alpha works on the definition (C); Bravo needs it for full sizing and can estimate independent interfaces (D); Charlie can draft customer-facing test scenarios (E); Sales has discussed the target (G); Support awaits handover confirmation (H). Formal decision rights still need confirmation.

**Dependencies and parallel work:** Alpha's definition constrains Bravo's full sizing (C, D). Bravo's independent interface estimate and Charlie's draft test scenarios can proceed in parallel (D, E). Previous-release closure may compete for engineering capacity, but the amount is unknown (F, H).

**Three management priorities:** Confirm the improvement baseline and decision path with Product and engineering (B); resolve the data definition and ask Bravo what it can size now (C, D); obtain closure effort and updated allocations before giving a delivery forecast (F, H). These contacts are proposed actions, not evidence of formal ownership.

**Question for each proposed owner:** Product and engineering: who will define and approve the improvement measure and baseline? Alpha's decision owner: which missing-value definition and version can be approved? Engineering leads: what closure effort remains, and which allocations can be confirmed for the forecast?

**Questions before a delivery commitment:** What is the agreed measure and baseline? Which definition and access rules are approved, by whom, and for which version? What can Bravo fully estimate once those decisions are recorded? What closure effort and current capacity are confirmed? Until these are answered, no delivery date follows from the packet.

### Example briefing to the CEO

The 25% forecasting improvement is a target, but the baseline and method still need agreement (A, B). Product proposes a proof of concept before production scope is decided (B). Alpha's data definition is not approved, which prevents Bravo from completing full integration sizing; independent interface sizing can proceed (C, D). Charlie can draft customer-facing test scenarios, while access rules remain open (E). Capacity is not yet confirmed, and the prior release still needs acceptance and handover work whose engineering effort is unestimated (F, H). Sales has discussed the target without committing a release date (G). At Friday's review, I would report these dependencies, the decisions and estimates needed, and when a forecast can be prepared. The supplied records do not support a delivery-date commitment.

## Variation: add I without deleting C

I is a newer Teams claim that Alpha's definition was approved Thursday morning. It does not provide a decision record, approved version, approver, or Bravo's acknowledgement. A revised assessment should say **approval is reported but not verified in the supplied formal records**. The PM should ask for the decision reference and ask Bravo whether it has received the applicable version before changing the dependency status. C remains evidence of the earlier state, not proof that I is false.

**Example Friday response to the CEO:** “We can report the work that can proceed and the decisions blocking full sizing. A Teams message says the definition was approved, but I need the formal version and Bravo's confirmation before treating the dependency as cleared. Updated capacity and previous-release closure effort are also pending. I cannot support a delivery date from these records. My next commitment is to return with the confirmed decision, estimates, and forecast basis after those checks.”

## Separate after-action review from J–N

| Observation supported by records | Possible cause to check, not a finding |
| --- | --- |
| Both week 6 updates say engineering work is largely complete and Product acceptance remains open (J, K). | Ask whether acceptance criteria or review timing delayed closure. |
| The PM status requires a customer-specific condition before external communication (J); the CTO update says support handover awaits final documentation (K). | Ask whether these were tracked as explicit closure gates. |
| Three actions were copied to two trackers; one lacks a confirmed owner (L). | Ask whether duplicate entry caused inconsistent follow-up. Hours wasted are unknown. |
| A Teams discussion says an access decision was verbal and asks for GitBook/GitHub updates (M). | Check whether the durable records were updated. |
| Support requested acceptance-criteria clarification after the planned handover meeting (N). | Ask what was missing at handover; the record does not establish who caused it. |

**Small pilot:** Build one checked fact sheet and draft two audience versions from it, preserving the customer-specific qualification from J. Measure total preparation and review minutes and corrections over two reporting cycles. Do not claim savings until measured.

| Candidate improvement | Frequency | Value | Effort | Error risk | Human verification |
| --- | --- | --- | --- | --- | --- |
| One checked fact sheet feeding two audience drafts (J, K) | Two week 6 updates are shown; ongoing frequency is unknown. | May reduce inconsistent facts; benefit is unmeasured. | Requires a source check and two reviews; minutes are unknown. | Customer-specific conditions could be dropped (J). | A PM compares both drafts with J and K before use. |
| One owner and one durable record for copied actions (L, M) | Three copied actions appear in L; future frequency is unknown. | May reduce missed follow-up; no outcome is measured. | Record reconciliation and owner confirmation are required. | An incorrect owner could be propagated twice. | The named owner and PM check the action record. |

The packet does not establish repeated time cost, a root cause for late acceptance or handover, or whether either improvement saves time. Those questions need team confirmation and two measured cycles.

**Questions for the team:** Which acceptance condition was still open? Were the verbal access decision and action owner later recorded? What information did Support need at handover?
