# Runnable Chapter 8 example

This offline Python example extends the Chapter 7 investigation into cross-team risk discovery. It uses only fictional records and standard-library modules. No account, API key, network call, or Office installation is needed.

From the repository root, first run Chapter 7 Scenario A, then Chapter 8:

~~~powershell
python chapters/07-dependency-agent/example/agent.py --scenario a
python chapters/08-risk-analyst/example/risk_analyst.py --scenario a --investigation chapters/07-dependency-agent/example/outputs/a/investigation.json
python chapters/08-risk-analyst/example/risk_analyst.py --scenario b
python chapters/08-risk-analyst/example/risk_analyst.py --scenario c
python -m unittest discover -s chapters/08-risk-analyst/example/tests -v
~~~

Open `chapters/08-risk-analyst/example/outputs/a/analysis.json`. The program writes only this local artifact for each scenario. The `outputs` folder should stay untracked. The handoff is optional for studying Chapter 8 alone; when supplied, the program checks that it is an unresolved GH-41 investigation and records its references as context. The Chapter 8 signals remain separate evidence.

| Scenario | Fictional change | Expected result |
| --- | --- | --- |
| A | Alpha's contract moves, Bravo's window narrows, Charlie's environment is late | Emerging risk for PM review |
| B | Alpha and Charlie records are resolved | Insufficient evidence |
| C | Alpha record is older than the seven-day window | Insufficient evidence |

The seven-day window and three-team threshold are educational policy choices, not calibrated predictive statistics. A different project would need its own rule and retrospective validation. Read [risk_policy.md](risk_policy.md), [risk_prompt.md](risk_prompt.md), [sample-analysis.md](sample-analysis.md), and [expected-results.md](expected-results.md) before changing the rule. The runtime uses explicit deterministic rules; the prompt is for a separate model-assisted exercise.
