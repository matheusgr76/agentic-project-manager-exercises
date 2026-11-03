# Chapter 4 — worked Report Builder output

This is an illustrative result for the [four Chapter 4 input files](../../acme-practice-packet/inputs/) using the manuscript's fixed reporting date of **2026-11-06** and seven-calendar-day capacity freshness limit. It shows the expected behavior of a reader-built program; it is not output from a completed Report Builder supplied in this repository.

## Example evidence sheet

| Finding | Source | Validation |
| --- | --- | --- |
| Bravo's full integration sizing is blocked by the missing-value decision. | GH-41 has status BLOCKED and dependency DEC-12; UP-2 says the data contract still blocks the full estimate. | Keep the dependency open. |
| Independent interface sizing is in progress. | GH-42 is IN_PROGRESS; UP-2 says Bravo can size independent interfaces. | Do not report the full integration estimate as complete. |
| Alpha's data contract work is in progress. | GH-43 is IN_PROGRESS and references DEC-12. | In-progress work is not decision approval. |
| DEC-12 is not formally approved. | DEC-12 is PENDING, version v2, with no approver or effective date. UP-1 says option B looks good. | Treat UP-1 as discussion, not approval. |
| Proof-of-concept scope has an approved record. | DEC-13 is APPROVED for v1, Product Manager, effective 2026-11-04. | Do not use DEC-13 to approve DEC-12. |
| Alpha and Bravo capacity figures are stale and provisional. | Both snapshots are PROVISIONAL and dated 2026-10-23. | They are 14 calendar days old on 2026-11-06, beyond the seven-day limit. |
| Charlie has one confirmed allocation in the packet. | Charlie row is CONFIRMED, dated 2026-11-05. | This says nothing about Alpha or Bravo availability. |
| New allocations are not yet confirmed. | UP-3, CTO, 2026-11-05. | Ask for a refreshed capacity record. |

## Example weekly status draft

Bravo's full integration sizing remains blocked on pending decision DEC-12 (GH-41, DEC-12, UP-2). Independent interface sizing is in progress (GH-42, UP-2). Alpha's data contract issue remains in progress (GH-43). DEC-13 records approval of proof-of-concept scope, but it does not settle the missing-value definition (DEC-13, DEC-12). Alpha and Bravo capacity snapshots are provisional and 14 days old at the fixed reporting date; the CTO says new allocations are not confirmed (capacity.csv, UP-3). The PM should seek formal approval of DEC-12 and refreshed capacity before stating a delivery forecast. The supplied inputs do not establish a delivery date or an achieved 25% improvement.

**Review status:** Draft for PM inspection. Nothing is published or sent.

## Incomplete approval variation

In a **test copy only**, change DEC-12 from PENDING to APPROVED while leaving approver and effective date empty. The expected output is an exception such as: “DEC-12 is marked APPROVED but lacks an approver and effective date; do not treat it as verified approval.” The program should preserve the record ID and avoid clearing GH-41's dependency automatically. Restore the original input after the test.
