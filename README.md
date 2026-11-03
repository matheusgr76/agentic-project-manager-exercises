# The Agentic Project Manager — exercises through Chapter 14

**New reader? [Start here](START-HERE.md).** The guide shows how to download the files and run Chapters 4–14 without writing code or connecting a company account.

These exercises accompany the manuscript through Chapter 14. Acme and every record here are fictional. Start with the chapter you are reading. Chapters 1–3 need only a document or spreadsheet and a chatbot. Chapters 4–14 progressively build a local Report Builder, dependency agent, Risk Analyst, coordinator, project history, read-only Command Center, run gate, authority check, and pilot evaluator; no live company connection is required.

The CSV inputs are UTF-8 text and can be opened in Google Sheets or a text editor. Each worked output identifies its source records and marks added test assumptions, so readers can compare reasoning as well as formatting.

| Chapter | Exercise | Starting point | Worked output |
| --- | --- | --- | --- |
| 1 | [First management brief](chapters/01-first-management-brief/README.md) | [Five records in CSV](chapters/01-first-management-brief/source-records.csv) | [Example brief](chapters/01-first-management-brief/example-output.md) |
| 2 | [Initial assessment and after-action review](chapters/02-initial-assessment/README.md) | [Records A–N in CSV](chapters/02-initial-assessment/source-records.csv) | [Example assessment](chapters/02-initial-assessment/example-output.md) |
| 3 | [Information flow and two reports](chapters/03-information-flow/README.md) | [Records 1–6 in CSV](chapters/03-information-flow/source-records.csv) | [Example map and reports](chapters/03-information-flow/example-output.md) |
| 4 | [Local Report Builder](chapters/04-report-builder/README.md) | [CSV and update files](acme-practice-packet/inputs/) | [Example evidence sheet](chapters/04-report-builder/example-output.md) |
| 5 | [Connected reporting pilot](chapters/05-connected-reporting/README.md) | [Mock retrieval in CSV](chapters/05-connected-reporting/mock-issue-retrieval.csv) | [Example pilot result](chapters/05-connected-reporting/example-output.md) |
| 6 | [Scheduled reporting](chapters/06-scheduled-reporting/README.md) | [Case matrix in CSV](chapters/06-scheduled-reporting/case-matrix.csv) | [Example run log](chapters/06-scheduled-reporting/example-output.md) |
| 7 | [Dependency agent](chapters/07-dependency-agent/README.md) | [Markdown scenarios](chapters/07-dependency-agent/example/README.md) | [Sample investigation](chapters/07-dependency-agent/example/sample-investigation.md) |
| 8 | [Risk Analyst](chapters/08-risk-analyst/README.md) | [Fictional dated signals](chapters/08-risk-analyst/example/signals.csv) | [Sample analysis](chapters/08-risk-analyst/example/sample-analysis.md) |
| 9 | [Coordinator](chapters/09-one-agent-is-not-enough/README.md) | [Three fictional specialist outputs](chapters/09-one-agent-is-not-enough/example/fixtures/) | [Sample handoff](chapters/09-one-agent-is-not-enough/example/sample-handoff.md) |
| 10 | [Project history](chapters/10-project-that-remembers/README.md) | [Versioned fictional records](chapters/10-project-that-remembers/example/records.csv) | [Sample answer](chapters/10-project-that-remembers/example/sample-answer.md) |
| 11 | [PM Command Center](chapters/11-pm-command-center/README.md) | [Fictional handoff and knowledge fixtures](chapters/11-pm-command-center/example/fixtures/) | [Sample screen](chapters/11-pm-command-center/example/sample-screen.md) |
| 12 | [When the Agent Breaks at 2 A.M.](chapters/12-when-the-agent-breaks/README.md) | [Fictional run cases and Chapter 11 view model](chapters/12-when-the-agent-breaks/example/) | [Expected run states](chapters/12-when-the-agent-breaks/example/expected-results.md) |
| 13 | [Who Authorized the Agent?](chapters/13-who-authorized-the-agent/README.md) | [Fictional requests, actor context, approvals, and Chapter 12 health](chapters/13-who-authorized-the-agent/example/fixtures/) | [Expected authority decisions](chapters/13-who-authorized-the-agent/example/expected-results.md) |
| 14 | [Was It Worth Building?](chapters/14-was-it-worth-building/README.md) | [Fictional paired task and cost assumptions](chapters/14-was-it-worth-building/example/) | [Expected evaluation results](chapters/14-was-it-worth-building/example/expected-results.md) |

The [practice packet](acme-practice-packet/README.md) holds the shared source records and [illustrative reporting samples](acme-practice-packet/reporting-samples.md). The samples are examples to inspect, not answers to copy without checking the evidence. Each chapter guide has a copyable starter prompt. Chapters 7–14 include runnable Python examples and behavior tests.

Use only fictional or otherwise approved information in an AI tool. Keep generated reports local until a person checks and approves them. The exercises do not require credentials, automatic messages, or live GitHub access.

## How to use this repository

1. Read the relevant chapter and its exercise README.
2. Make your own assessment before using an assistant.
3. Use the linked packet snapshot. Do not combine records from different snapshots as though they were simultaneous.
4. Compare the result with the chapter's checks and the source references.
5. Save your prompt, output, corrections, and time spent for later comparison.

The manuscript is the full explanation. These files provide reusable inputs and compact instructions.
