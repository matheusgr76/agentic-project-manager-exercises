# Chapter 4 — build the local Acme Report Builder

**Tools:** a local folder, Python or another language you can run, and a coding agent such as Codex. This chapter asks you to build the program; the packet supplies the starter data rather than a completed implementation.

## Starter inputs

Create `acme-report-builder/inputs/` and copy the four files from the [shared inputs](../../acme-practice-packet/inputs/): `issues.csv`, `decisions.csv`, `capacity.csv`, and `updates.md`. Use **2026-11-06** as the fixed reporting date and **seven calendar days** as the maximum age for a capacity snapshot. Do not connect to a live system.

## Exercise

Ask your coding agent to read the files and implement the one-page specification in Chapter 4. Have it show a plan first, use a simple local design, document how to run it, and add behavior tests. Inspect the proposed rules and outputs before accepting them.

The result should retain source IDs and generate an evidence report. It should flag missing approval information, stale capacity, and unsupported delivery claims. Ask for a test proving that UP-1's “Option B looks good” never establishes formal approval. As a second test, change DEC-12 to `APPROVED` while leaving `approver` blank; this must be flagged as incomplete approval evidence. Restore the original file afterward.

## Check the result

- DEC-12 remains `PENDING`; GH-41 remains `BLOCKED` in this snapshot.
- GH-42 is independent work in progress, not completed integration.
- Alpha and Bravo capacity is provisional and stale under the exercise rule.
- No delivery date or achieved 25% improvement is invented.
- The agent can explain the program entry point, validation rules, test command, and effect of a new capacity column.

Keep the program folder and tests for Chapters 5–7. The [sample evidence sheet](../../acme-practice-packet/reporting-samples.md#evidence-sheet) is an inspection aid, not a required byte-for-byte output.
