#!/usr/bin/env python3
"""PreToolUse hook: block Claude from modifying the protected project skeleton.

Covers file tools (Edit/Write/NotebookEdit) by path, and Bash commands that would write to a
protected file (redirects, sed -i, mv, rm, cp, tee, ...). Read-only commands (cat, grep) pass.
To change a protected file, edit it yourself or remove it from PROTECTED below.
"""

import json
import os
import re
import sys

PROTECTED = [
    "mise.toml",
    "pyproject.toml",
    "uv.lock",
    ".env.example",
    ".gitignore",
    "README.md",
    "CLAUDE.md",
    "scripts/fetch_clawbio.sh",
    "scripts/check_env.py",
]
PROTECTED_DIRS = [".claude/"]

WRITE_VERBS = re.compile(
    r"\b(sed\s+(-\S*\s+)*-i|perl\s+(-\S*\s+)*-i|tee|mv|rm|cp|truncate|ln|chmod|touch|dd|"
    r"git\s+(checkout|restore|rm|mv)|open\(|write_text|write_bytes|unlink|rename)\b"
)

root = os.path.realpath(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())


def deny(target: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"{target} is part of the protected project skeleton (see CLAUDE.md). "
                "Do not modify it or work around this block; ask the user to make the change."
            ),
        }
    }))
    sys.exit(0)


def is_protected(path: str) -> bool:
    full = os.path.realpath(path if os.path.isabs(path) else os.path.join(root, path))
    rel = os.path.relpath(full, root)
    return rel in PROTECTED or any(rel + "/" == d or rel.startswith(d) for d in PROTECTED_DIRS)


def path_pattern(p: str) -> str:
    # Match p as a whole path token at the project root: bare, ./p, or /abs/root/p.
    prefix = rf"(?:\./|{re.escape(root)}/)?"
    tail = "" if p.endswith("/") else r"(?=$|[\s'\";|&)])"
    return rf"(?:^|(?<=[\s'\"=(]))" + prefix + re.escape(p) + tail


data = json.load(sys.stdin)
tool, inp = data.get("tool_name", ""), data.get("tool_input", {})

if tool == "Bash":
    cmd = inp.get("command", "")
    for p in PROTECTED + PROTECTED_DIRS:
        pat = path_pattern(p)
        redirect = rf">{{1,2}}\s*['\"]?(?:\./|{re.escape(root)}/)?{re.escape(p)}"
        if re.search(redirect, cmd) or (re.search(pat, cmd) and WRITE_VERBS.search(cmd)):
            deny(p)
else:
    target = inp.get("file_path") or inp.get("notebook_path")
    if target and is_protected(target):
        deny(os.path.relpath(os.path.realpath(os.path.join(root, target)), root))

sys.exit(0)
