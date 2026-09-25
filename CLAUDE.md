# Genomic Equity Agent

Hackathon project: A pipeline that computes polygenic risk scores from a genotype file and a PGS Catalog score ID, then audits whether the resulting percentile is actually interpretable for that individual. It cross-references the sample's genetic ancestry against the populations the score was developed and evaluated in, and applies a deterministic gate that returns one of three outcomes: report the percentile, report the raw score only, or abstain entirely. The goal is to make a PRS say nothing rather than say something confidently wrong for people outside its reference population.

## Protected skeleton — do not modify

These files form the project skeleton and must not be edited, overwritten, moved, or deleted
without explicit approval from the user in the current conversation:

- `mise.toml`, `pyproject.toml`, `uv.lock`
- `.env.example`, `.gitignore`
- `README.md`, `CLAUDE.md`
- `scripts/fetch_clawbio.sh`, `scripts/check_env.py`
- everything under `.claude/`

A hook (`.claude/hooks/protect_skeleton.py`) blocks edits to these files. If a task seems to need
one changed, stop and ask the user instead of working around the hook.

## Environment

- Python 3.13 in `.venv`, managed by uv; tools pinned by mise.
- Run Python through the venv: `uv run python ...` (or plain `python` when mise is active).
- API keys live in `.env` (gitignored, loaded by mise and `python-dotenv`). Read keys from
  environment variables; never hardcode, print, or commit them.
- Adding a dependency: `uv add <pkg>` (requires user approval). Never use `pip install`.

## Commands

- `mise run setup`: full setup (clone ClawBio, `uv sync`, create `.env`)
- `mise run sync`: reinstall after dependency changes
- `mise run check`: verify imports and show which API keys are set
- `mise run demo`: run ClawBio's equity-scorer demo
- `mise run notebook`: JupyterLab

## Layout

- `vendor/ClawBio/`: upstream ClawBio (gitignored). Treat as read-only reference; ask before
  editing it. Useful skills: `skills/equity-scorer` (HEIM equity score), `skills/lit-synthesizer`,
  `skills/pubmed-summariser`. Each skill's `SKILL.md` documents its inputs and usage.
- `data/raw/`: local input data (gitignored)
- `outputs/`: generated results (gitignored)
- Application code: put it in new files/directories (e.g. `src/`, `notebooks/`, `tests/`),
  not in the skeleton files above.

## Available libraries

LLMs: `anthropic`, `claude-agent-sdk`, `openai`, `pydantic`, `tenacity`.
Papers: `httpx`, `pymupdf`, `pymupdf4llm`, `lxml`, `biopython` (Entrez/PubMed).
Data: `pandas`, `polars`, `pyarrow`, `duckdb`, `numpy`, `scipy`, `scikit-learn`, `matplotlib`, `seaborn`.
Dev: `pytest`, `ruff`, `jupyterlab`.
