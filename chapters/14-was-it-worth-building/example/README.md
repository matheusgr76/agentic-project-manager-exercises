# Runnable Chapter 14 pilot evaluator

From the repository root, with Python 3.10 or newer:

~~~powershell
python chapters/14-was-it-worth-building/example/evaluator.py --scenario recorded
python chapters/14-was-it-worth-building/example/evaluator.py --scenario counterfactual
python -m unittest discover -s chapters/14-was-it-worth-building/example/tests -v
~~~

Inspect `outputs/recorded.json` and `outputs/counterfactual.json`. The ignored files show every task's baseline, assisted, fallback, and net minutes. The evaluator reads [fictional paired tasks](work-samples.csv) and [fictional cost assumptions](cost-assumptions.json); it does not read a live company system or make an external call.

Read the [measurement policy](measurement-policy.md) before interpreting the result. [Expected results](expected-results.md) gives the arithmetic and the important sensitivity: one rejected output requires a manual fallback. The [evaluation prompt](evaluation-prompt.md) asks for a PM recommendation that distinguishes calculated effort from unmeasured delivery outcomes.

`counterfactual` changes only the acceptance of F-03. It is a test of how the conclusion depends on that assumption, not another observed run. Costs are in fictional USD and the six rows are invented. Do not reuse the return figure as a forecast for your organization.
