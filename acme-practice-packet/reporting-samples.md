# Illustrative reporting samples

These are **draft examples**, derived from the Chapter 4 snapshot with reporting date **2026-11-06**. They are not new source records, verified approvals, or publishable commitments. The seven-calendar-day freshness rule makes the 2026-10-23 Alpha and Bravo capacity snapshots stale.

## Evidence sheet

| Claim or question | Evidence | Assessment |
| --- | --- | --- |
| Bravo's full integration sizing is blocked | GH-41 `BLOCKED`; dependency DEC-12; UP-2 says the data contract still blocks the full estimate | Supported for this snapshot |
| Independent interface sizing can continue | GH-42 `IN_PROGRESS`; UP-2 | Supported as work in progress, not proof of completion |
| Missing-value definition is approved | DEC-12 `PENDING`, version v2, no approver or effective date; UP-1 expresses informal support | **Not established** |
| Alpha and Bravo have confirmed available capacity | Capacity snapshot 2026-10-23, both `PROVISIONAL`; UP-3 says new allocations are unconfirmed | **Not established; snapshot is stale** |
| Charlie has one confirmed allocation | Capacity snapshot 2026-11-05, `CONFIRMED` | Supported for this snapshot only |
| A delivery date or 25% result is committed | No such approval or measurement in the Chapter 4 inputs | **Not established** |

**Questions for owners:** Who will record the missing-value decision and its effective version? Can Bravo confirm what can be sized independently? When will the CTO confirm updated Alpha and Bravo capacity? What baseline and method would support the proposed 25% improvement target? The last question comes from the Chapter 1–2 packet, not the Chapter 4 CSV files.

## Weekly management status — draft

The data contract remains an open dependency for Bravo's full integration estimate (GH-41, DEC-12, UP-2). Independent interface sizing is in progress (GH-42, UP-2). Alpha's informal support for option B does not establish approval of DEC-12 (UP-1, DEC-12). Alpha and Bravo allocations are provisional and their 2026-10-23 snapshot is outside the seven-day freshness limit (capacity.csv); the CTO says new allocations are not yet confirmed (UP-3). The PM should obtain the formal decision and refreshed capacity before presenting a delivery forecast. No delivery date is established by these records.

**PM review before sending:** Check current issue and decision states, confirm source timestamps, ask owners about the unresolved decision and capacity, and ensure the audience has approved the wording.

## Engineering coordination update — draft

Bravo's full integration sizing remains blocked by DEC-12 (GH-41, UP-2). Independent interface sizing is in progress (GH-42, UP-2). DEC-12 is pending for version v2; UP-1 is not a formal decision. Alpha and Bravo capacity figures are provisional and stale under the exercise rule (capacity.csv). Confirm the data-definition decision and updated allocations before changing the full integration estimate. This is a coordination draft, not an issue update or commitment.

## Exception report — draft

| ID | Finding | Source | Next action | Publication status |
| --- | --- | --- | --- | --- |
| EX-1 | GH-41 depends on pending DEC-12 | GH-41, DEC-12, UP-2 | Ask the decision owner for formal status and version | Hold for PM review |
| EX-2 | Informal option B support could be mistaken for approval | UP-1, DEC-12 | Confirm approver and effective date | Hold for PM review |
| EX-3 | Alpha and Bravo capacity snapshots are stale and provisional | capacity.csv, UP-3 | Request refreshed allocations | Hold for PM review |

For Chapter 6's separate conflict case, GH-41 is changed to `IN_PROGRESS` while DEC-12 remains `PENDING`. That case should be `REVIEW_REQUIRED`; the system should investigate rather than silently replace this Chapter 4 snapshot.
