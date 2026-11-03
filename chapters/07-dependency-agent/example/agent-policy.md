# Acme Dependency Agent — example policy

ID: POLICY-1
Goal: Investigate a dependency exception using fictional approved records.
Max retrievals: 6

Permitted: Read local issue, decision, and update records; update the local exception register; draft a recommendation.

Prohibited: Change source records, close issues, approve decisions, send messages, publish reports, or make delivery commitments.

Stop: Evidence is insufficient, retrieval limit is reached, or a consequential action requires human approval.

The Python tool layer implements these boundaries. This policy is a readable record of them; changing the prose alone does not grant a new tool permission.
