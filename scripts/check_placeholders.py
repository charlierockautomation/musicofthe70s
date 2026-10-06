#!/usr/bin/env python3
"""Fail (exit 1) if any built page shows unfinished filler text to readers.

Checks visible text (not scripts, styles or attributes) of every .html file
for: "Placeholder intro", "Lorem ipsum", "TBD", "TODO", "FIXME", "coming soon",
"your text here". The word "placeholder" alone is allowed (real stories use it).

Run: python3 scripts/check_placeholders.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".claude", ".serena", "sources", "video_site_logo", "node_modules", ".git", "scripts"}
PATTERN = re.compile(r"placeholder intro|lorem ipsum|\bTBD\b|\bTODO\b|\bFIXME\b|coming soon|your text here", re.I)


def visible_text(html):
    html = re.sub(r"(?is)<(script|style|noscript)\b.*?</\1>", " ", html)
    html = re.sub(r"(?s)<!--.*?-->", " ", html)
    return re.sub(r"<[^>]+>", " ", html)


def main():
    hits = []
    for f in sorted(ROOT.rglob("*.html")):
        if SKIP_DIRS & set(f.relative_to(ROOT).parts):
            continue
        for m in PATTERN.finditer(visible_text(f.read_text(encoding="utf-8", errors="ignore"))):
            hits.append(f"{f.relative_to(ROOT)}: {m.group(0)!r}")
    if hits:
        print("FAIL: placeholder text found:")
        print("\n".join(hits))
        sys.exit(1)
    print("PASS: no placeholder text found.")


if __name__ == "__main__":
    main()
