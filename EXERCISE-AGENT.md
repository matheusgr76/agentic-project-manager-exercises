# Revision A exercise agent

`exercise_agent.py` checks all 15 chapters of the Revision A manuscript against the fictional Acme companion repository. It runs the existing offline programs for Chapters 4–15, then asks the installed Codex CLI to assess the repository exercise using the manuscript, chapter guide, source records, command log, and generated outputs. Chapters 1–3 are written exercises only.

Run it from a PowerShell terminal with Python 3.10 or newer and an authenticated Codex CLI:

```powershell
python exercise_agent.py --manuscript "C:\Users\mathe\Documents\ChatGPT\New Book\The Agentic Project Manager - Rev A corrected v2.docx" --output "C:\Users\mathe\Documents\ChatGPT\New Book\exercise-run-new"
```

The output folder must not already exist. The agent copies the repository there before running any exercise. No program connects to a company system, changes GitHub records, sends a message, or publishes a report. The Codex process runs with a read-only sandbox. The exercise programs write only to the isolated repository copy.

Results appear in `summary.md` and `results.json`. Every chapter also has an `answer.md`. `execution_status` is `SUCCESS` when all example commands and chapter behavior tests exit successfully and required output files exist. `validation_status` also requires a `PASS` verdict from the source-backed Codex review. Command failures and review findings remain separate in `results.json`. The written verdict is an agent evidence review, so its reasoning and source references remain visible for audit.

The run continues after a chapter failure so the log covers all 15 chapters. The CLI exits with status 1 if any chapter fails validation. Use `--repo` to point to another checkout, `--codex` to set the Codex executable, and `--timeout` to change the per-command timeout in seconds. The chapter command inventory and representative required artifacts are in `exercise_manifest.json`.
