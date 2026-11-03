# Acme workshop — Chapters 4–6

This is the known-good local example behind the [beginner route](../START-HERE.md). It lets a reader run the same fictional reporting problem through three chapters before writing code. It uses only Python's standard library and makes no network calls.

| Module | Job | Main output |
| --- | --- | --- |
| report_builder.py | Validate Chapter 4 CSV records and draft a status report | outputs/ch4/evidence.json and weekly-status.md |
| connected_pilot.py | Substitute one mock issue retrieval, including failure cases | outputs/ch5/case-name/retrieval.json |
| scheduled_run.py | Apply Chapter 6's four fixed policy cases | outputs/ch6/case-name/run.json; case C also creates exception.json |

The [Chapter 7 example](../chapters/07-dependency-agent/example/README.md) accepts case C's exception file. It uses a separate Markdown scenario matching the exception and performs its own bounded investigation. The handoff validates the issue and decision states before the agent runs.

Run all commands from the repository root as shown in START-HERE.md. Test the workshop with:

~~~text
python -m unittest discover -s workshop/tests -v
~~~

The workshop is a reference implementation, not a required solution. Make your own assessment first; then compare source references, failure behavior, and approval boundaries. Outputs are local drafts and are ignored by Git.
