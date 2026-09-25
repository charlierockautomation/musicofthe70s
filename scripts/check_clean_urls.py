#!/usr/bin/env python3
"""
PUBLISH GATE pre-commit check: fail if any built HTML file contains an
internal href, canonical, og:url, or JSON-LD url/@id/mainEntityOfPage/item
ending in ".html" or "index.html".

Cloudflare Pages 308-redirects /x.html -> /x and /x/index.html -> /x/, so
any internal link or URL field still pointing at the redirecting form
costs a hop and can dilute canonical signals. Run before every commit
that touches HTML.

Usage: python3 scripts/check_clean_urls.py
Exits 1 and prints every offending file:line if anything is found,
exits 0 with a PASS line otherwise.
"""
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# google51cd05767988751c.html and 404.html are real on-disk filenames,
# not clean-URL routed pages, so they're allowed to reference themselves
# but should still never be *linked to* with a redirecting internal URL
# elsewhere. No exclusion needed here since the check is on URL values,
# not filenames.
ATTR_PATTERN = re.compile(
    r'(?:href|content)="(/[^"]*\.html[^"]*|https://musicofthe70s\.net/[^"]*\.html[^"]*)"'
)
JSONLD_PATTERN = re.compile(
    r'"(?:url|@id|mainEntityOfPage|item)":\s*"(/[^"]*\.html[^"]*|https://musicofthe70s\.net/[^"]*\.html[^"]*)"'
)


def find_violations():
    violations = []
    for f in sorted(REPO_ROOT.rglob("*.html")):
        if ".git" in f.parts:
            continue
        rel = f.relative_to(REPO_ROOT)
        for lineno, line in enumerate(f.read_text(encoding="utf-8").splitlines(), start=1):
            for pattern in (ATTR_PATTERN, JSONLD_PATTERN):
                for m in pattern.finditer(line):
                    violations.append(f"{rel}:{lineno}: {m.group(0)}")
    return violations


def main():
    violations = find_violations()
    if violations:
        print(f"FAIL: {len(violations)} internal .html/index.html URL(s) found:", file=sys.stderr)
        for v in violations:
            print(f"  {v}", file=sys.stderr)
        return 1
    print("PASS: no internal .html or index.html URLs found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
