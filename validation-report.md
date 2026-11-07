# Validation report - Revision A exercises (2026-11-07)

Scope: all 15 chapter exercises, local working tree of `feature/all-chapter-exercise-agent` (based on origin/main 935eed5, which already contains PRs #15 and #16), against `The Agentic Project Manager - Rev A corrected v11.docx`.
Environment: Linux VM on the author's machine, Python 3.10.12. NOT Windows. No Codex CLI.
Run folders: `exercise-run-final-verify` (before the Chapter 8 fix) and `exercise-run-final-verify-2` (after; the authoritative run).

## EXECUTED AND PASSED
| Check | Result |
| --- | --- |
| Chapter commands + unit tests, chapters 1-15 | 55/55 exit 0, 0 missing artifacts, in both runs (Chapters 1-3 have no commands) |
| 70 committed sample outputs vs freshly generated output (JSON compared by value) | 69 identical; Chapter 6 `run.json` x4 differ only by the documented random run ID |
| Chapter 12 digest `48e0f8dd...90bb89f0` | Equals the generated `model_sha256`; matches all 5 mentions in corrected v11 and all repo mentions. `--from-prior-outputs` and default path give the same digest |
| Chapter 12 fixture | Byte-identical to `sample-outputs/ch11/a/view-model.json` |
| Chapter 7 wording | Corrected v11 attributes independent sizing to the issue's Latest update |
| Chapter 10 | E-02 cites `sample-outputs/ch07/a/investigation.json` (exists); B as of 2026-11-12 still returns DEC-12 PENDING from E-01 |
| Chapters 9-11 content, 18 programmatic checks against each chapter's expected-results.md | Statuses, references, dates, publication none, no external requests all agree |
| Manuscript links and paths | 73 repository links and 51 repository paths in corrected v11 all exist in the local tree |

## EXECUTED AND FAILED (found, then fixed)
| Finding | Fix |
| --- | --- |
| `sample-outputs/ch08/a/analysis.json` was stale: it lacked `evidence_signals` that `risk_analyst.py` now writes | Sample regenerated with the documented command; new test `test_committed_samples_match_current_output` (Chapter 8, 6 tests now) fails on the old sample and passes on the new one |

## NOT EXECUTED / NOT ESTABLISHED
- **No model-written content review in this session.** The Codex reviewer was unavailable. Chapters 9-11 content was checked by scripted comparison to each chapter's own expected results, plus my reading of the guides; Chapters 1-3, 5, 6, 8, 13-15 carry only their earlier v11/v12 reviewer verdicts (v11: 1-3, 5, 6, 8, 13-15 PASS; v12: 1-4 PASS). Chapters 4, 7, 12 failed v11 review; their fixes were re-verified mechanically here, not re-reviewed by Codex. Treat this as **no final clean 15/15 reviewed run**.
- Windows execution (this was Linux). A real Windows run of `python -m unittest discover` per chapter is still needed.
- Chapters 1-3 reader writing/chatbot work, live connectors, human approvals, real time savings.
- Layout of the corrected DOCX against official Rev A (prose, figures, layout); only selective page inspection exists from before. No text diff was run in this session.
- Fresh-checkout test of the publishable branch.
- The 15 local changes are uncommitted and unpushed; buyers still see the old remote material. Not buyer-ready until published.

## Local state
- Changed this session: `chapters/08-risk-analyst/example/tests/test_risk_analyst.py`, `sample-outputs/ch08/a/analysis.json`, this report. No commit, push or merge.
- Git could not delete lock files; one stale `.git/objects/stale-maintenance-lock-claude-20261107` (a renamed lock left by my `git fetch`) is harmless and safe to delete.
- Official Rev A untouched.

## Addendum (same day, after commit 240156c)
- Fresh checkout: `git clone` of branch `feature/all-chapter-exercise-agent` at 240156c, run in an isolated workspace: 15 chapters, 55/55 commands exit 0.
- Corrected v11 DOCX vs the sandbox copy of Rev A (the file delivered as "Rev A"; the author's Documents copy was not compared): 196 headings, 94 tables (0 cell changes), 94 images and 74 hyperlinks all identical; 20 of 1453 paragraphs changed, all tied to the code fixes above (Chapters 4, 6-12, 14, 15); 2 images differ (media rId424, rId427; not visually inspected here). Saved unchanged as `The Agentic Project Manager - Rev B.docx`; `Rev B.pdf` is the 179-page Word render made after that DOCX.
- Commit author is "Claude" because no git identity is configured here. Not pushed.

## Windows result (author's machine, 2026-11-07, Python 3.14.2, PowerShell; reported by the author, output pasted in chat)
- `commands_only_check.py`: 15 chapters, 55/55 commands and unit tests exit 0, no missing artifacts.
- Direct runs: workshop tests 15 OK; Chapter 7 model-agent tests 31 OK with 1 skipped (the real-SDK unreachable-API test, because `anthropic` was not installed); Chapter 12 tests 6 OK; `python -m workshop.report_builder` printed `GH-41: BLOCKED; DEC-12: PENDING`.
- The earlier Windows failure (Chapter 12 test reading UTF-8 without an encoding) does not recur.
- Still not run on Windows: the real-SDK test with `anthropic` installed, and the Codex content review.
