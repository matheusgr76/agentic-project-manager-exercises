# Runnable Chapter 11 Command Center

From the repository root, with Python 3.10 or newer:

~~~powershell
python chapters/11-pm-command-center/example/dashboard.py --scenario a
python chapters/11-pm-command-center/example/dashboard.py --scenario b
python chapters/11-pm-command-center/example/dashboard.py --scenario c
python -m unittest discover -s chapters/11-pm-command-center/example/tests -v
~~~

Open `chapters/11-pm-command-center/example/outputs/a/index.html` in a browser. Inspect `view-model.json` beside it. The HTML is self-contained and read-only; no local server, JavaScript, account, or API key is needed. The `outputs` folder is ignored by Git.

To use the files produced by earlier exercises, first run Chapter 9 Scenario A and Chapter 10 Scenario A. Then run:

~~~powershell
python chapters/11-pm-command-center/example/dashboard.py --scenario a --from-prior-outputs
~~~

The committed [fixtures](fixtures/) are copies of those deterministic local outputs, plus the Chapter 9 conflict and missing-input cases. `--from-prior-outputs` is available for Scenario A only. The page does not claim the Chapter 9 handoff and Chapter 10 history were produced at the same time; it shows their source dates and the known freshness gap.

| Scenario | Page state | Required PM interpretation |
| --- | --- | --- |
| A | REVIEW_REQUIRED | Check sources and refresh older risk signals before deciding |
| B | CONFLICT | Reconcile the contradictory DEC-12 claim with its owner |
| C | INCOMPLETE | Re-run or retrieve the missing Risk Analyst output |

Read [view-policy.md](view-policy.md), [expected-results.md](expected-results.md), and [sample-screen.md](sample-screen.md). [view-prompt.md](view-prompt.md) gives a model-assisted variation; the runnable example itself uses fixed local rules.
