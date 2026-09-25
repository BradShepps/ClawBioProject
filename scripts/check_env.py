"""Sanity check: confirm key packages import and report which API keys are set."""

import importlib
import os
import sys

from dotenv import load_dotenv

load_dotenv()

PACKAGES = [
    "clawbio", "anthropic", "claude_agent_sdk", "openai", "pydantic",
    "httpx", "pymupdf", "pymupdf4llm", "Bio", "pandas", "polars", "duckdb",
]
KEYS = ["ANTHROPIC_API_KEY", "OPENAI_API_KEY", "NCBI_API_KEY", "NCBI_EMAIL",
        "SEMANTIC_SCHOLAR_API_KEY"]

print(f"Python {sys.version.split()[0]} at {sys.executable}")

failed = []
for name in PACKAGES:
    try:
        importlib.import_module(name)
    except Exception as e:  # noqa: BLE001
        failed.append(f"{name}: {e}")
print(f"Imports: {len(PACKAGES) - len(failed)}/{len(PACKAGES)} OK")
for f in failed:
    print(f"  FAIL {f}")

print("API keys:")
for key in KEYS:
    print(f"  {'set    ' if os.getenv(key) else 'missing'}  {key}")
if not (os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY")):
    print("\nAdd at least one of ANTHROPIC_API_KEY / OPENAI_API_KEY to .env")

sys.exit(1 if failed else 0)
