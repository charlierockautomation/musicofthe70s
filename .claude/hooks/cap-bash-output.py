#!/usr/bin/env python3
import json
import re
import sys
import shlex
import time
import os

NOISY_PATTERN = re.compile(
    r"(^|[;&|\s])git (log|diff)(\s|$)"
    r"|verify_post\.py"
    r"|generate_blog_hub_cards\.py"
    r"|(^|[;&|\s])(npm (run )?(test|build)|pytest|python3? -m pytest)(\s|$)"
)

LOG_DIR = ".claude/bash-logs"


def main():
    raw = sys.stdin.read()
    try:
        data = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        return

    cmd = (data.get("tool_input") or {}).get("command") or ""
    if not cmd or not NOISY_PATTERN.search(cmd):
        return

    log_file = os.path.join(LOG_DIR, f"{time.strftime('%Y%m%d-%H%M%S')}-{os.getpid()}.log")

    wrapped = (
        f"mkdir -p {shlex.quote(LOG_DIR)}; "
        f"{{ {cmd} ; }} > {shlex.quote(log_file)} 2>&1; "
        f"STATUS=$?; "
        f"LINES=$(wc -l < {shlex.quote(log_file)}); "
        f"echo \"[cap-bash-output: full output ($LINES lines) saved to {log_file}]\"; "
        f"tail -n 100 {shlex.quote(log_file)}; "
        f"exit $STATUS"
    )

    out = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": "Wrapped noisy command: full output logged to disk, tail(100) shown in context.",
            "updatedInput": {"command": wrapped},
        }
    }
    print(json.dumps(out))


if __name__ == "__main__":
    main()
