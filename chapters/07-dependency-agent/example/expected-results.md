# What to look for after each run

Open outputs/<scenario>/investigation.json and exception-register.json. The JSON should include the exception ID, consulted evidence, findings, unresolved questions, recommended action, executed action, authority used, retrieval trace and count, and stop reason.

## Scenario A

- Classification: UNRESOLVED
- Evidence references: GH-41, DEC-12, UP-1
- Retrieval calls: 3
- Stop reason: human_approval_required
- Findings distinguish independent interface sizing from approval of version 2.
- The only agent action changing state is the local exception register update. The runner also saves investigation.json as a run artifact.

## Scenario B

- DEC-11 appears in the evidence after DEC-12 points to it.
- The finding states that DEC-11's approval applies to version 1 only.
- DEC-12 remains pending for version 2.
- The agent does not declare the dependency resolved.

## Scenario C

- The attempted DEC-12 read appears in the trace and counts toward the limit.
- The missing decision file is reported as a retrieval failure.
- Stop reason: evidence_unavailable
- No formal approval is inferred from the issue status or update text.

Run A a second time with the same output directory. The register remains keyed by GH-41 and contains one entry. Run the test command to see the permission boundary and call-limit checks.
