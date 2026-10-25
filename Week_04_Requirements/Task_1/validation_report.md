# Validation report — Antigravity conversation c5d217bc-38e7-4fc0-9a09-075b9f19f28c

**Date:** 22 October 2026  
**Scope:** Task 1 requirements-refinement network in this directory, checked against [Task_1.md](Task_1.md) and the Antigravity conversation.

## Task and outcome

The assignment asks for a Python LangGraph network with at least three LLM nodes, three permitted models, one deterministic node, and an audit/refinement loop. It must read an arbitrary `.txt`/`.eml` corpus and produce a structured, traceable requirements document plus a design report. The output criteria OS1–OS9 cover IDs, deduplication, source tracing, explanations, priorities, consistency, coverage, and a blacklist.

The graph has four configured LLM nodes using four permitted models, two deterministic nodes, and a bounded feedback edge. The saved [requirements.md](requirements.md) has 69 requirements and three blacklist items. The prior full live run extracted 125 candidates and refined them to that document, but its audit still reported **16 issues after three refinements**. It also omitted the consolidated patron-characteristics source. The saved document therefore remains a draft.

## Incorrect behavior found and fixed

| Finding | Evidence | Correction |
|---|---|---|
| Live runs silently used mock data when the API key or an LLM call failed. | A one-file run with `OPENAI_API_KEY` empty exited 0 and replaced a previous output. | Live failures now stop with a nonzero exit. Mock data is used only with `--mock`. |
| The arbitrary-corpus mock invented three rejected proposals. | The one-file test input mentioned none of those proposals, yet the output contained three blacklist items. | The generic mock leaves the blacklist empty. Mock mode is for testing only. |
| An audit that still failed at the iteration limit was routed to export. | The full Antigravity run logged `passed=False`, 16 issues, then wrote `requirements.md`. | Exhausting the limit now raises an error. Existing output is preserved; successful writes replace it atomically. |
| All three saved blacklist citations were temporary `RAW-###` IDs. | `BLK-001…003` cited `RAW-064`, `RAW-120`, etc.; the old verifier accepted them. | The saved document now cites matching corpus files. Live deduplication resolves candidate IDs to corpus paths, and the verifier rejects missing or invalid blacklist citations. |
| A rejected proposal was omitted from a live smoke-run blacklist. | A two-file booking corpus explicitly rejected automatic cancellation of unpaid bookings; the first run produced zero blacklist items. | Extraction now carries rejected proposals as `Won't Have` candidates; deduplication moves those to the blacklist and avoids unsupported additions. A second live run produced one sourced blacklist item. |
| The older draft dropped a whole substantive source. | `conv_pines023_patron_characteristics.eml` is uncited, despite its explicit summary requiring configurable age ranges, combined filters, grouping, and null handling. | Prompts now preserve explicit summaries; extraction, deduplication, and verification check that those source files remain cited. A live one-file run extracted eight relevant requirements. |
| The loop could not repair all issue types. | The prior refiner only updated requirements, while the auditor also checks blacklist rationales. Rewording cannot truly remove duplicate requirements. | The refiner can update flagged blacklist items and merge duplicate requirements while retaining source citations. Both paths have focused regression tests. |
| Full runs could stall or fail on model output formatting. | One API request stalled for over 24 minutes. Later deduplication returned an uncited item and a non-padded `RAW-53` citation. | API calls now have a 90-second timeout and one retry. Uncited items are discarded; candidate IDs with omitted zero padding are resolved to their canonical IDs. Malformed citations still fail the run. |
| README and design report described an older output. | They said 68 requirements, four blacklist entries, and all 20 files cited. | Updated to 69, three, and 19 of 20 cited files; documented the draft audit status and failure behavior. |

## Verification performed

- `.venv/bin/python -m unittest test_pipeline_failures -v`: **11 passed**. The checks cover keyless output preservation, mock inventions, invalid and non-padded candidate citations, API failure handling, failed-audit export, explicit-summary coverage, blacklist repair, duplicate merging, and uncited deduplication output.
- `.venv/bin/python verify_pipeline.py --json`: **21 passed, 1 failed** on the saved draft. `TST-DOC-08` correctly reports the missing patron-characteristics source. The older verifier had falsely passed it.
- `.venv/bin/python -m py_compile requirements_agent.py ingest.py verify_pipeline.py test_pipeline_failures.py`: passed.
- Live two-file smoke run after the prompt changes: **4 requirements, 1 blacklist item, audit passed on iteration 0, 20.92 seconds**. Its blacklist entry cites `decision.txt`, which explicitly rejects automatic unpaid-booking cancellation. The run wrote only to a temporary directory.
- Live patron-characteristics-only run: **8 requirements, 1 blacklist item, audit passed on iteration 0, 35.06 seconds**. It captured configurable age ranges, combined filters, grouping, and null handling.
- Full-corpus attempts: one was interrupted after an API stall; another reached 61 requirements and 12 blacklist items but ended with one unresolved audit issue; two later attempts exposed missing and non-padded candidate citations during deduplication. None wrote a new output file.

## Remaining validation limit

The most recent numeric-ID normalization has **not** yet been validated by another full-corpus run. The saved draft is still missing a required source and has not passed the network audit. The 22 automated checks mainly test structure and known phrases. Title similarity does not prove zero semantic duplicates, source-file coverage does not prove every source requirement was captured, and the auditor may miss unsupported details. Do not submit the saved draft as an approved final specification.

To regenerate the full document with the revised pipeline from this directory:

```bash
.venv/bin/python requirements_agent.py --corpus-dir data/corpus --output-file requirements.md
.venv/bin/python verify_pipeline.py
```

The first command now preserves the current draft if the API call or audit fails. Only a passing audit replaces it.
