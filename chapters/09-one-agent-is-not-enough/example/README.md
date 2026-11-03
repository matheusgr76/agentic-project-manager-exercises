# Runnable Chapter 9 coordinator

From the repository root, with Python 3.10 or newer, run the committed fictional fixtures first:

~~~powershell
python chapters/09-one-agent-is-not-enough/example/orchestrator.py --scenario a
python chapters/09-one-agent-is-not-enough/example/orchestrator.py --scenario b
python chapters/09-one-agent-is-not-enough/example/orchestrator.py --scenario c
python -m unittest discover -s chapters/09-one-agent-is-not-enough/example/tests -v
~~~

The output is `chapters/09-one-agent-is-not-enough/example/outputs/<scenario>/handoff.json`. The folder is ignored by Git. The [sample handoff](sample-handoff.md) explains Scenario A; [expected results](expected-results.md) covers all three.

To use the actual local outputs from the earlier exercises, run these from the repository root:

~~~powershell
python -m workshop.scheduled_run --case C
python chapters/07-dependency-agent/example/agent.py --scenario a --exception-file workshop/outputs/ch6/c/exception.json
python chapters/08-risk-analyst/example/risk_analyst.py --scenario a --investigation chapters/07-dependency-agent/example/outputs/a/investigation.json
python chapters/09-one-agent-is-not-enough/example/orchestrator.py --scenario a --from-prior-outputs
~~~

The committed fixtures are copies of those deterministic local outputs, except Scenario B's explicitly invented contradictory dependency record. Scenario C points to a deliberately absent risk file. The coordinator does not invoke a model, agent tool, network service, or message system. It only reads JSON and writes the local handoff. The [coordination policy](coordination-policy.md) states the decision boundary; [coordination-prompt.md](coordination-prompt.md) is a separate model-assisted learning path.

The Chapter 8 risk assessment is dated November 9; the Chapter 6 case C report is dated November 12. This example preserves that order and asks for refreshed risk signals. It does not treat their source snapshots as simultaneous.
