# Genomic Equity Agent

Hackathon project: an agent that evaluates genomics papers for population diversity and equity,
built on [ClawBio](https://github.com/ClawBio/ClawBio).

## Setup (one command)

### 1. Install and activate mise (once per machine)

Install mise:
```bash
curl https://mise.run | sh
```

Activate it in your shell so it loads automatically. Run the line for your shell:
```bash
# zsh (macOS default)
echo 'eval "$(~/.local/bin/mise activate zsh)"' >> ~/.zshrc

# bash
echo 'eval "$(~/.local/bin/mise activate bash)"' >> ~/.bashrc
```

Then open a new terminal and confirm it works with `mise --version`.

### 2. Set up the project

From the project folder, run:
```bash
mise trust && mise run setup
```

This installs Python 3.13 + uv, clones ClawBio into `vendor/ClawBio` (at the commit pinned in
`mise.toml`), creates `.venv` with all dependencies, and creates `.env` from `.env.example`.

Then **uncomment and fill in your API keys in `.env`** (Anthropic and/or OpenAI at minimum) and run `mise run check`.

With mise activated, `cd`-ing into the project auto-activates `.venv` and loads `.env`, so
`python`, `jupyter`, etc. just work.

## Everyday commands

| Command | What it does |
|---|---|
| `mise run sync` | Re-install after someone changes deps (run after `git pull`) |
| `mise run check` | Verify imports + show which API keys are set |
| `mise run demo` | Run ClawBio's equity-scorer demo |
| `mise run notebook` | Launch JupyterLab |
| `uv add <pkg>` | Add a dependency (commit `pyproject.toml` **and** `uv.lock`) |

## Relevant ClawBio skills

See `vendor/ClawBio/skills/`: `equity-scorer` (HEIM equity score), `lit-synthesizer`,
`pubmed-summariser`.

## Layout

```
mise.toml         tools, env, tasks
pyproject.toml    Python deps (uv.lock pins exact versions)
scripts/          setup helpers
vendor/ClawBio/   cloned by setup (gitignored)
data/raw/         local data (gitignored)
outputs/          generated results (gitignored)
```
