# Runnable Chapter 12 run gate

From the repository root, with Python 3.10 or newer:

~~~powershell
python chapters/12-when-the-agent-breaks/example/health_monitor.py --case a
python chapters/12-when-the-agent-breaks/example/health_monitor.py --case a
python chapters/12-when-the-agent-breaks/example/health_monitor.py --case b
python chapters/12-when-the-agent-breaks/example/health_monitor.py --case b_recovered
python chapters/12-when-the-agent-breaks/example/health_monitor.py --case c
python -m unittest discover -s chapters/12-when-the-agent-breaks/example/tests -v
~~~

The commands read the committed [Chapter 11 Scenario A view model](fixtures/view-model-a.json), [fictional cases](cases.csv), and [policy values](config.json). Inspect `outputs/<case>/health.json`, `outputs/ledger.json`, and `outputs/attempts.jsonl`. `outputs` is ignored by Git. To reset the sequence, delete only that generated Chapter 12 `outputs` directory, then rerun. The ledger contains successful review-ready run IDs, not approvals or publications.

To regenerate the view model from the previous chapter, run Chapter 11 Scenario A first, then add `--from-prior-outputs` to a Chapter 12 command. The [run policy](run-policy.md) explains the gates; [expected results](expected-results.md) shows the exact sequence. Use the [failure prompt](failure-prompt.md) to draft a source-backed human review note.

The program simulates a partial retrieval with a case field. It has no live connector, scheduler, automatic retry, or network timeout. A real deployment would need those controls at the external call boundary.
