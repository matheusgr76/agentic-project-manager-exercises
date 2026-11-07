# Runnable Chapter 10 project history

From the repository root, with Python 3.10 or newer:

~~~powershell
python chapters/10-project-that-remembers/example/knowledge_base.py --scenario a
python chapters/10-project-that-remembers/example/knowledge_base.py --scenario b --as-of 2026-11-12
python chapters/10-project-that-remembers/example/knowledge_base.py --scenario b
python chapters/10-project-that-remembers/example/knowledge_base.py --scenario c
python -m unittest discover -s chapters/10-project-that-remembers/example/tests -v
~~~

Each run writes `chapters/10-project-that-remembers/example/outputs/<scenario>/knowledge.json`, replacing the previous local answer for that scenario. Run the earlier-date B query before default B so the retained B file shows the November 15 approval; inspect the earlier answer before the second command. The output directory is ignored by Git. The records file links to repository sources; the invented [approval addendum](fixtures/approval-addendum.md) and [conflicting export](fixtures/conflicting-decision-export.md) are separate from the shared practice packet.

| Scenario | As-of date | What to inspect |
| --- | --- | --- |
| A | November 12 | DEC-12/v2 pending; GH-41 undated context; R1 risk a hypothesis |
| B | November 15 | Invented approval supersedes pending DEC-12/v2; GH-41 remains undated; risk needs revalidation |
| B with earlier `--as-of` | November 12 | The later approval is invisible to the earlier answer |
| C | November 15 | Two active decision sources conflict and both are cited |

Read the [memory policy](memory-policy.md), [sample answer](sample-answer.md), and [expected results](expected-results.md). The [memory prompt](memory-prompt.md) is for an optional model-assisted variation. The runnable code uses explicit local rules and no credentials, network calls, or model dependencies.
