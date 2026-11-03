# Project-memory policy

All Acme examples are fictional. Scenario B's approval and Scenario C's conflicting export are isolated test variations. Neither modifies the shared decision log.

Store a claim with its key, value, source, authority, effective date, recorded date, optional review date, and explicit supersession link. Retain old records so an as-of question can be answered from what was knowable then. A later record can supersede only the same key. Undated evidence remains context and cannot establish an as-of state.

If no dated record is known, answer UNKNOWN or UNDATED_CONTEXT. If multiple active records disagree, answer CONFLICT with both sources. If a review date has passed, mark NEEDS_REVALIDATION without inventing a new value. A change to DEC-12 does not automatically change GH-41 or R1/risk.

The example may read local files and write one local answer. It has no tool to approve decisions, change issues, send messages, or publish a project statement. The PM and named approver own those decisions.
