#!/usr/bin/env python3
"""Generate _routes.json so functions/_middleware.js only runs on private paths.

Without _routes.json, Cloudflare Pages invokes the middleware on EVERY request
(HTML, images, CSS, JS), and each one counts against the free-plan limit of
100k Workers requests a day. The middleware only has to block internal working
files, so route just those paths to it; everything else is served as a static
asset with no Function invocation.

Re-run after adding any new tracked .md file or private root file:
    python3 scripts/build_routes_json.py
"""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Keep in sync with BLOCKED_PREFIXES / BLOCKED_ROOT_FILES in functions/_middleware.js
PREFIXES = ["/.claude/*", "/scripts/*", "/sources/*", "/functions/*", "/.git/*", "/.gitignore"]
ROOT_FILES = ["/QUICK_START.docx", "/QUICK_START.pdf", "/musicofthe70s_fixes.tar.gz"]
COVERED_DIRS = ("/.claude/", "/scripts/", "/sources/", "/functions/")

tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True,
                         text=True, check=True).stdout.splitlines()
md = sorted("/" + f for f in tracked if f.lower().endswith(".md"))
md = [p for p in md if not p.startswith(COVERED_DIRS)]

include = []
for p in PREFIXES + ROOT_FILES + md:
    for v in (p, p.lower()):
        if v not in include:
            include.append(v)

if len(include) > 100:
    raise SystemExit(f"{len(include)} rules exceeds the Cloudflare limit of 100")

(ROOT / "_routes.json").write_text(json.dumps(
    {"version": 1, "include": include, "exclude": []}, indent=2) + "\n")
print(f"wrote _routes.json with {len(include)} include rules")
