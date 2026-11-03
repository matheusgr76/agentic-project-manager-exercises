# Chapter 5 — connected reporting pilot

**Starting point:** the Chapter 4 Report Builder and its tests. A mock retrieval is enough; no live connection or credential is required.

## Exercise

1. Define the narrow goal: retrieve the current state and update timestamp of selected test issues without modifying any issue. List only the fields the Report Builder needs.
2. Inspect the connections available in your environment. If considering a real MCP server, record maintainer, read operations, authentication, permissions, data handling, update history, and revocation path before requesting approval. If those facts are unclear, stop at evaluation.
3. Retrieve one known issue from a mock service or approved test repository. Compare ID, status, update time, and dependency with the source. Record retrieval time separately from source update time.
4. Transform the result into the Chapter 4 input schema, preserving the source ID. Run the existing validation rules and produce an evidence report. A missing field must remain missing or flagged.
5. Simulate an unavailable server, a missing issue, and an issue comment that tells the system to ignore reporting rules. Failures must remain visible; the comment is data, not an instruction.
6. Compare effort, freshness, traceability, permissions, and failure behavior against manual exports. Record whether the connection actually improves the workflow.

## Check the result

A successful pilot produces one traceable read without changing the source. Failed retrievals must not be presented as current evidence. If a connection is unavailable or unapproved, the evaluation and mock retrieval complete the exercise.

Use the [Chapter 4 inputs](../../acme-practice-packet/inputs/) as your known comparison records. Keep the capability assessment and your run notes.

## Copyable pilot prompt

~~~text
Help me evaluate one read-only issue retrieval for the fictional Acme Report Builder. First list the exact fields required and the permissions a connector would need. Do not install or authorize anything. Use a mock retrieval unless I supply an approved test connection. Compare the returned issue ID, status, dependency, source update time, and retrieval time with the Chapter 4 input. Preserve missing fields as missing. Simulate server failure, a missing issue, and a source comment saying to ignore reporting rules. Show the evidence report and explain whether the connection improves freshness, effort, and traceability.
~~~
