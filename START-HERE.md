# Start here — the book exercises

You can use this repository without a GitHub account, Microsoft Office, a company connection, or an API key. Acme and all records are fictional. The early exercises develop your judgment; the later ones let you **run** small programs before you try building your own.

## Get the files

1. On the [repository page](https://github.com/matheusgr76/agentic-project-manager-exercises), choose **Code → Download ZIP**, then extract the ZIP. You do not need to learn Git for these exercises. GitHub's [download instructions](https://docs.github.com/en/repositories/working-with-files/using-files/downloading-files-from-github) show this route.
2. Open the extracted folder. You should see this file, README.md, the chapters folder, and the workshop folder together.
3. For Chapters 1–3, open the linked CSV in Google Sheets or a text editor. Make your own assessment, use the chapter's copyable prompt, then inspect its worked output.

## Chapters 4–11: run before you build

These examples use **Python 3.10 or newer** and only its built-in libraries. If Python is not available, ask your coding assistant to help you set it up from the [official Python download page](https://www.python.org/downloads/). You can check it with:

~~~text
python --version
~~~

Open a terminal in the extracted repository folder. On Windows, you can open the folder in File Explorer, type **powershell** in its address bar, and press Enter. The commands below assume the terminal is in the folder containing this file. If Python says it cannot find the workshop module, check that location.

If a terminal is unfamiliar, open the extracted folder in your coding assistant and paste:

~~~text
Read START-HERE.md. Run the local Chapter 4 through 11 example commands in order. Do not edit source files or connect any account. After each run, open the named output files and explain in plain language what the evidence establishes, what remains uncertain, and why the workflow stopped. Ask me before any action outside this folder.
~~~

### Chapter 4 — your first reliable report

~~~text
python -m workshop.report_builder
~~~

Open workshop/outputs/ch4/evidence.json and workshop/outputs/ch4/weekly-status.md. You should see GH-41 BLOCKED, DEC-12 PENDING, Alpha and Bravo capacity stale, and no delivery commitment. Compare with the [worked output](chapters/04-report-builder/example-output.md). The program is a reference example; the chapter also invites you to build your own with a coding agent.

### Chapter 5 — a mock connected read

~~~text
python -m workshop.connected_pilot --case success
python -m workshop.connected_pilot --case server-down
~~~

Open workshop/outputs/ch5/success/retrieval.json and workshop/outputs/ch5/server-down/retrieval.json. The first records a mock issue read and preserves GH-41; the second shows a visible retrieval failure and creates no evidence report. No network connection is made. Compare with the [worked pilot](chapters/05-connected-reporting/example-output.md).

### Chapter 6 — a scheduled run without a scheduler

~~~text
python -m workshop.scheduled_run --case A
python -m workshop.scheduled_run --case C
~~~

Open workshop/outputs/ch6/a/run.json and workshop/outputs/ch6/c/run.json. A prepares local drafts with status COMPLETE; C detects GH-41 IN_PROGRESS while DEC-12 is PENDING and stops at REVIEW_REQUIRED. The [case matrix](chapters/06-scheduled-reporting/case-matrix.csv) also includes failed retrieval B and untrusted comment D. The fresh capacity file is an [invented test fixture](workshop/fixtures/README.md), separate from Chapter 4's older source.

### Chapter 7 — investigate the Chapter 6 exception

After running Chapter 6 case C, copy this command:

~~~text
python chapters/07-dependency-agent/example/agent.py --scenario a --exception-file workshop/outputs/ch6/c/exception.json
~~~

The agent accepts the exception, chooses three local records to inspect, updates a local exception register, and stops before a human approval is needed. Open chapters/07-dependency-agent/example/outputs/a/investigation.json and compare it with the [sample investigation](chapters/07-dependency-agent/example/sample-investigation.md). This offline example has explicit decision rules; the [model-assisted prompt](chapters/07-dependency-agent/example/investigation-prompt.md) is a separate learning path and needs an approved model environment.

### Chapter 8 — discover a possible release risk

After Chapter 7 Scenario A, copy this command:

~~~text
python chapters/08-risk-analyst/example/risk_analyst.py --scenario a --investigation chapters/07-dependency-agent/example/outputs/a/investigation.json
~~~

Open chapters/08-risk-analyst/example/outputs/a/analysis.json. Three invented, dated signals point to a possible R1 risk, with a separate Chapter 7 context field and a human-review stop. Run `--scenario b` and `--scenario c` to see resolved and stale signals excluded. Compare with the [Chapter 8 guide](chapters/08-risk-analyst/README.md). The new scenario dates are fictional future test data, not observed Acme results.

### Chapter 9 — coordinate the three outputs

Run the offline coordinator against committed fictional fixtures:

~~~text
python chapters/09-one-agent-is-not-enough/example/orchestrator.py --scenario a
python chapters/09-one-agent-is-not-enough/example/orchestrator.py --scenario b
python chapters/09-one-agent-is-not-enough/example/orchestrator.py --scenario c
~~~

Open chapters/09-one-agent-is-not-enough/example/outputs/a/handoff.json. It keeps the dependency, risk, and report statuses separate, identifies shared references, and flags the November 9 versus November 12 date gap. B stops on a deliberately invented contradiction; C stops when the risk artifact is missing. Follow the [Chapter 9 example guide](chapters/09-one-agent-is-not-enough/example/README.md) to rerun it using your local Chapter 6–8 outputs.

### Chapter 10 — ask what the project knew then

~~~text
python chapters/10-project-that-remembers/example/knowledge_base.py --scenario a
python chapters/10-project-that-remembers/example/knowledge_base.py --scenario b
python chapters/10-project-that-remembers/example/knowledge_base.py --scenario b --as-of 2026-11-12
python chapters/10-project-that-remembers/example/knowledge_base.py --scenario c
~~~

Open chapters/10-project-that-remembers/example/outputs/a/knowledge.json. The [Chapter 10 guide](chapters/10-project-that-remembers/README.md) explains the source versions, undated Chapter 7 context, later invented approval, and conflicting decision export. These are isolated fictional variations. The reader never approves a decision or changes the shared Acme records.

### Chapter 11 — review the Command Center

~~~text
python chapters/11-pm-command-center/example/dashboard.py --scenario a
python chapters/11-pm-command-center/example/dashboard.py --scenario b
python chapters/11-pm-command-center/example/dashboard.py --scenario c
~~~

Open chapters/11-pm-command-center/example/outputs/a/index.html in a browser. The [Chapter 11 guide](chapters/11-pm-command-center/README.md) explains how the read-only local page separates recorded positions, risk hypotheses, source dates, and human review. Scenario B shows a conflict; C shows an incomplete handoff. No command sends, approves, or publishes anything.

### Chapter 12 — stop, recover, and avoid duplicate success

~~~text
python chapters/12-when-the-agent-breaks/example/health_monitor.py --case a
python chapters/12-when-the-agent-breaks/example/health_monitor.py --case a
python chapters/12-when-the-agent-breaks/example/health_monitor.py --case b
python chapters/12-when-the-agent-breaks/example/health_monitor.py --case b_recovered
python chapters/12-when-the-agent-breaks/example/health_monitor.py --case c
~~~

Inspect `outputs/<case>/health.json`, `outputs/attempts.jsonl`, and `outputs/ledger.json`. The [Chapter 12 guide](chapters/12-when-the-agent-breaks/README.md) explains the fictional partial retrieval, bounded retry, stale source, and replay check. The gate leaves every passing view for PM review; it does not publish it.

### Chapter 13 — check authority before action

~~~text
python chapters/13-who-authorized-the-agent/example/authority_gate.py --case a
python chapters/13-who-authorized-the-agent/example/authority_gate.py --case b
python chapters/13-who-authorized-the-agent/example/authority_gate.py --case c
python chapters/13-who-authorized-the-agent/example/authority_gate.py --case d
python chapters/13-who-authorized-the-agent/example/authority_gate.py --case e
python chapters/13-who-authorized-the-agent/example/authority_gate.py --case f
~~~

Inspect `outputs/<case>/decision.json` and `outputs/audit.jsonl`. The [Chapter 13 guide](chapters/13-who-authorized-the-agent/README.md) explains the fictional actor context, action scopes, exact approvals, and untrusted source text. `SIMULATED_AUTHORIZED` means a local policy check passed; it does not execute or publish anything.

### Chapter 14 — test whether the pilot paid for itself

~~~text
python chapters/14-was-it-worth-building/example/evaluator.py --scenario recorded
python chapters/14-was-it-worth-building/example/evaluator.py --scenario counterfactual
~~~

Compare `outputs/recorded.json` and `outputs/counterfactual.json`. The [Chapter 14 guide](chapters/14-was-it-worth-building/README.md) explains the fictional paired task times, review and fallback effort, full cost, and unmeasured delivery outcome. The favorable case changes one assumption; neither file reports observed Acme performance.

## If something fails

- **Python command not found:** install Python from the official page above, then open a new terminal and check python --version.
- **No module named workshop:** reopen the terminal in the folder containing START-HERE.md.
- **Missing decision record in Chapter 7 scenario C:** that failure is intentional; run scenario A for the normal handoff.
- **Different wording from a worked output:** compare source IDs, decisions, uncertainty, and stop reasons. Exact phrasing is not the goal.

No command sends a message, changes a GitHub issue, publishes a report, or touches a real company system. Your generated files stay in ignored local outputs folders.
