# Chapter 1 — worked example

This is one defensible response to the [five fictional source records](source-records.csv), before the Step 5 variation. It illustrates the form of an answer; a reader's wording can differ if the same evidence boundaries are preserved. The weekday labels are relative to the exercise, not calendar dates.

## Confirmed from the packet

| Statement | Source |
| --- | --- |
| The forecasting data definition is open; Product must confirm treatment of missing values. | C1-1, Monday, Alpha lead |
| Bravo cannot finish full integration sizing until Alpha's definition is stable. Independent interface work can be estimated. | C1-2, Tuesday, Bravo lead |
| Customer access rules await Product approval. No delivery date has been committed. | C1-3, Wednesday, Charlie lead |
| Team allocations are provisional and due for review. | C1-4, previous Friday, capacity snapshot |
| Acme aims for a 25% forecasting improvement, but its baseline and measurement method are not agreed. | C1-5, management note |

## Unknowns and management judgment

The records do not establish the final data definition, approved access rules, confirmed capacity, a measurable improvement result, or a delivery date. A sensible interpretation is that these gaps prevent a credible commitment. That is a management assessment, not an additional source fact.

| Decision or check | Proposed next contact | Why |
| --- | --- | --- |
| Confirm missing-value handling and the stable definition | Product with Alpha | Bravo's full sizing depends on it (C1-1, C1-2). |
| Confirm access rules | Product with Charlie | Charlie reports that approval is pending (C1-3). |
| Refresh allocations | Capacity owner or relevant team leads | The only snapshot is provisional (C1-4). |
| Agree the baseline and measurement method | Management, Product, and the measurement owner | The 25% figure is still a target (C1-5). |

The proposed contacts are suggestions, not a claim that formal decision ownership has been assigned.

## Example weekly status draft

Alpha's forecasting data definition remains open, including the treatment of missing values (C1-1). Bravo cannot finish full integration sizing until that definition is stable, although it can estimate independent interface work (C1-2). Charlie is waiting for Product approval of customer access rules, and no delivery date has been committed (C1-3). The available capacity snapshot is provisional and due for review (C1-4). The initiative aims for a 25% forecasting improvement, but the baseline and measurement method still need agreement (C1-5). Before the next status review, the PM should confirm the definition, access decision, updated allocations, and how improvement will be measured. These records do not support a delivery commitment.

**Before sending:** Check whether newer records supersede C1-1 through C1-4, confirm decisions with their owners, and verify the audience and wording.

## Step 5 variation

If C1-1 is replaced with “The data definition was approved Wednesday, but Bravo has not acknowledged the new version,” the next draft may report that **Alpha says** approval occurred. It must still ask which version was approved and whether Bravo has received it and assessed the effect on its estimate. Approval alone does not prove Bravo's blocker is cleared. Keep the original and variation outputs separate.

**Example revised status draft:** Alpha reports that the data definition was approved Wednesday, but Bravo has not acknowledged the new version (revised C1-1). Bravo's earlier note said full integration sizing needed a stable definition and that independent interface work could be estimated (C1-2). The PM should confirm the approved version and ask Bravo whether it has received it and can revise the estimate. Customer access approval remains pending and no delivery date is committed (C1-3). Allocations remain provisional (C1-4). The 25% improvement is still a target without an agreed baseline or method (C1-5). The available records do not justify declaring the integration dependency resolved.
