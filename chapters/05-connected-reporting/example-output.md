# Chapter 5 — worked connected-retrieval pilot

The [mock retrieval CSV](mock-issue-retrieval.csv) copies GH-41's source fields from the Chapter 4 issues file. The retrieval timestamp **2026-11-06T09:00:00Z** is invented test metadata for this exercise; it is not a time supplied by the manuscript or by a live GitHub service. The source gives an update **date only**, so do not claim an hour-level age.

## Example capability decision

**Required read:** one selected issue's ID, title, status, owner, update date, and dependency reference. **Permission:** read access to an approved test source only. A real connector's maintainer, permissions, authentication, data handling, update history, and revocation method would need review before use. This mock requires no authorization or network call.

## Example retrieval record

| Check | Observation |
| --- | --- |
| Source ID | GH-41 |
| Source state | BLOCKED, owner Bravo, dependency DEC-12 |
| Source update date | 2026-11-05 |
| Mock retrieval time | 2026-11-06T09:00:00Z |
| Comparison with Chapter 4 input | ID, title, status, owner, update date, and dependency match the issues.csv row. |
| What remains unknown | The exact source update hour and whether any later live change exists. |

**Mapping to Report Builder:** Pass the six source fields through unchanged, preserving GH-41 and DEC-12. Store retrieval time separately as provenance. Run the Chapter 4 validation rules: DEC-12 is still pending in the local decision file, and this issue read does not settle it.

## Failure examples

| Test | Example result | Required behavior |
| --- | --- | --- |
| Server unavailable | No issue record returned | Show retrieval failure; do not present the old CSV as a fresh connected read. |
| Issue missing | GH-41 cannot be found | Mark the source missing and retain the unresolved dependency. |
| Source comment says to ignore reporting rules | Comment text returned with the issue | Treat the text as data, not an instruction to change validation or publish. |

## Pilot decision

The mock proves that the field mapping and failure checks can be exercised locally. It does **not** prove that a real MCP server is safe, available, faster, or fresher than exports. Those claims require an approved connection and measured runs. A reader without one can stop at this documented evaluation and mock retrieval.
