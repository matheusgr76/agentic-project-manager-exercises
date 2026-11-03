# Chapter 3 — worked example

This example uses only [Records 1–6](source-records.csv). Source dates are weekday labels from the exercise, not calendar dates. The freshness rules and contacts below are proposed workflow choices, not additional source facts.

## Information-flow map

| Information needed | Source and apparent contact | Confirmed statement | Gap or conflict | Verification question and reporting consequence |
| --- | --- | --- | --- | --- |
| Progress | GitHub, Thursday 09:00 (1); Bravo is named in the record | Independent interface sizing is in progress. | Completion and full estimate are not established. | Ask Bravo what is done; report progress without calling integration complete. |
| Product decisions | GitBook, Monday 16:00 (2); Teams, Wednesday 14:00 (3); Product approval is referenced in 2 | Two definitions are candidates; approval was pending in 2. Teams says option B looks good. | 3 does not identify formal approval, version, or approver. | Ask Product for the decision record; report approval as unverified. |
| Dependencies | GitHub, Thursday 09:00 (1) | The data contract blocks Bravo's full integration sizing. | No verified decision clears the blocker. | Ask Bravo and the decision owner what is needed; retain the dependency. |
| Capacity | Excel, previous Friday (4); CTO email, Thursday 11:00 (5) | Two Bravo engineers were provisionally allocated; closure is using capacity; updates are due Friday. | Current confirmed availability is unknown. | Ask the CTO for refreshed allocations; do not state two engineers are available. |
| Customer commitments | Sales update, Thursday 12:00 (6) | The 25% target was discussed with customers; no release date was committed. | The target is not a measured outcome or delivery promise. | Confirm approved customer language with Sales/Product before external use. |

**Suggested freshness rule:** Review issue state on reporting day; check decision records after any new discussion; refresh capacity before a forecast; confirm customer wording before external communication. These are proposed controls, not facts supplied by Records 1–6.

## Verified fact sheet example

GitHub reports that Bravo's integration sizing remains blocked by the data contract while independent interface sizing is in progress (1). GitBook lists two candidate missing-value definitions and Product approval pending as of Monday (2). A Wednesday Teams message says option B looks good (3), but the packet contains no formal approval record. The prior-Friday Excel allocation of two Bravo engineers is provisional (4). The CTO says previous-release closure is using engineering capacity and updated allocations will be confirmed Friday (5). Sales says the 25% improvement target has been discussed with customers and no release date has been committed (6). Before a credible full estimate or external statement, the PM needs the formal data decision, refreshed capacity, and approved wording.

## Management update example

Bravo's full integration sizing remains blocked by the data contract, though independent interface sizing is in progress (1). Product approval was pending in GitBook (2), and the later Teams message does not establish formal approval (3). The prior-Friday allocation is provisional, while previous-release closure is using capacity; the CTO expects updated allocations Friday (4, 5). Sales has discussed the 25% target with customers but has not committed a release date (6). The PM should seek the formal data decision and refreshed capacity before presenting a reliable forecast.

## Engineering coordination update example

Continue the independent interface sizing already in progress, while keeping full integration sizing blocked on the data contract (1). GitBook recorded two candidate definitions with Product approval pending (2); the Teams comment about option B should be checked against a formal decision record (3). The two-engineer Bravo allocation in the prior-Friday sheet is provisional, and the CTO says closure work is using capacity (4, 5). Confirm the applicable data version and updated allocations before revising the estimate.

The reports change emphasis but do not disagree. Record 6 appears only in the management version because it concerns customer language; it is not contradicted in the engineering version. Both drafts remain subject to PM review.
