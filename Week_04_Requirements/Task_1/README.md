# Requirements Refinement Agentic Network

A [LangGraph](https://langchain-ai.github.io/langgraph/) pipeline that reads a folder of messy project documents (emails, meeting minutes, interviews, surveys, draft specs) and produces one structured requirements document.

Course task: AI4SE Labs 2026, Week 04. See [Task_1.md](Task_1.md) for the assignment.

## How it works (in 30 seconds)

```mermaid
flowchart LR
    I["ingest<br/>(Python)"] --> E["extract<br/>(LLM)"] --> D["deduplicate &<br/>resolve conflicts<br/>(LLM)"] --> A["audit<br/>(LLM)"]
    A -- "defects" --> R["refine<br/>(LLM)"] --> A
    A -- "passed" --> X["export<br/>(Python)"]
    A -- "limit reached with defects" --> F["fail; keep prior output"]
```

1. **Ingest:** read all `.txt` / `.eml` files and remember where each came from.
2. **Extract:** an LLM pulls out candidate requirements.
3. **Deduplicate:** another LLM merges duplicates, unifies wording, assigns IDs, and moves rejected ideas to a blacklist.
4. **Audit / refine loop:** a third LLM checks quality; a fourth fixes whatever it flags. Repeats until it passes or hits the limit (default 3).
5. **Export:** write `requirements.md` only after the audit passes. An API error or unresolved audit leaves an existing output file intact.

More detail and diagrams: [docs/workflow.md](docs/workflow.md).

## Models

| Node | Model |
|---|---|
| extract | `gpt-5-mini` |
| deduplicate | `gpt-5.4-nano` |
| audit | `gpt-6-luna` |
| refine | `gpt-5.6-luna` |

## Setup

Requires Python 3.12.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # then put your OPENAI_API_KEY in .env
```

`.env` is git-ignored. Never commit your key.

## Run

```bash
python requirements_agent.py --corpus-dir data/corpus --output-file requirements.md
```

| Flag | Meaning | Default |
|---|---|---|
| `--corpus-dir` | Folder with the input documents (searched recursively) | `data/corpus` |
| `--output-file` | Where to write the Markdown result | `requirements.md` |
| `--max-iterations` | Max audit/refine cycles (≥ 1) | `3` |
| `--mock` | Offline mode, no API calls (for testing only) | off |
| `-v` | Verbose logging | off |

The live pipeline accepts any `.txt` / `.eml` corpus directory. `OPENAI_API_KEY` is required unless `--mock` is set.

## Verify

```bash
python verify_pipeline.py          # 22 checks: ingestion, graph shape, output document
pytest verify_pipeline.py -v       # same checks via pytest
```

## Files and responsibilities

| File or directory | Responsibility | Role in the submission |
|---|---|---|
| [requirements_agent.py](requirements_agent.py) | Main CLI entry point and LangGraph workflow: extraction, deduplication, audit/refinement loop, and Markdown export. | Required script |
| [ingest.py](ingest.py) | Parses the input `.txt` and `.eml` files and retains source paths for traceability; also has a standalone inspection CLI. | Required supporting script |
| [data/corpus/](data/corpus/) | Example input documents read by the pipeline; these are not generated output. | Include when the submission must be reproducible and the corpus is not supplied separately |
| [requirements.md](requirements.md) | Generated requirements specification, including priorities, source citations, and a blacklist. | Required system output after a successful live run |
| [Task_1_Report.md](Task_1_Report.md) | Design report explaining node responsibilities, model choices, feedback loop, and assignment coverage. | Required report |
| [README.md](README.md) | Project overview, setup, run instructions, and this file map. | Include with the report and scripts |
| [requirements.txt](requirements.txt) | Python package dependencies; despite its name, it is not the generated requirements specification. | Include so the scripts can run |
| [docs/workflow.md](docs/workflow.md) | Detailed workflow diagrams and execution walkthrough. | Optional supporting documentation |
| [verify_pipeline.py](verify_pipeline.py), [test_pipeline_failures.py](test_pipeline_failures.py) | Structural verification and regression tests; neither runs as part of normal generation. | Optional verification material |
| [.env.example](.env.example) | Template showing the required environment variable. | Optional setup aid |
| [Task_1.md](Task_1.md) | Original assignment statement. | Reference, not a deliverable |
| [requirements_mock.md](requirements_mock.md) | Saved output from an offline mock run. | Test artifact, not the live system output |
| [validation_report.md](validation_report.md) | Record of the review, fixes, checks, and remaining limitations. | Review artifact, not the architecture report |
| `.env`, `.venv/`, `__pycache__/`, `.pytest_cache/` | Local credentials, environment, and caches. | Do not submit; `.env` may contain an API key |

The current [requirements.md](requirements.md) is a previous live draft with 69 requirements and 3 blacklisted proposals. Its audit did not pass, and it omits the patron-characteristics source. Regenerate and verify it before treating it as the final deliverable; a failed run preserves the existing file.

## Good to know

- `verify_pipeline.py` checks **structure** (IDs, traces, priority scale, graph shape). It cannot judge whether the requirements are semantically correct or complete, so review the output yourself.
- `--mock` uses test data for the example corpus. It is for testing, and a live run never silently switches to it.
