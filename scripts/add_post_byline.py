#!/usr/bin/env python3
"""Insert visible byline/dates under H1 and sync Article schema author url.

Single source of truth for the byline block across every blog post. Run with
--apply to write changes; without it, prints a diff-style report only.
"""
import re
import sys
from datetime import datetime
from pathlib import Path

BLOG_DIR = Path(__file__).resolve().parent.parent / "blog"
AUTHOR_URL = "https://musicofthe70s.net/about/author/"
OLD_AUTHOR_URL_LINE = '      "url": "https://musicofthe70s.net/pages/about"'
NEW_AUTHOR_URL_LINE = f'      "url": "{AUTHOR_URL}"'

DATE_PUBLISHED_RE = re.compile(r'"datePublished":\s*"(\d{4}-\d{2}-\d{2})"')
DATE_MODIFIED_RE = re.compile(r'"dateModified":\s*"(\d{4}-\d{2}-\d{2})"')
H1_RE = re.compile(r'(        <h1>.*?</h1>\n)')
BYLINE_RE = re.compile(r'        <p class="post-byline">.*?</p>\n')


def fmt(date_str):
    d = datetime.strptime(date_str, "%Y-%m-%d")
    return f"{d.strftime('%B')} {d.day}, {d.year}"


def find_posts():
    return sorted(
        p for p in BLOG_DIR.glob("*/*/index.html")
        if "archive" not in p.parts
    )


def build_byline(pub, mod):
    pub_fmt = fmt(pub)
    byline = f'By <a href="{AUTHOR_URL}">Charlie</a> &middot; Published {pub_fmt}'
    if mod != pub:
        byline += f' &middot; Updated {fmt(mod)}'
    return f'        <p class="post-byline">{byline}</p>\n'


def process(path, apply_changes):
    text = path.read_text()

    pub_match = DATE_PUBLISHED_RE.search(text)
    mod_match = DATE_MODIFIED_RE.search(text)
    if not pub_match or not mod_match:
        print(f"SKIP (no schema dates): {path}")
        return

    pub, mod = pub_match.group(1), mod_match.group(1)
    byline_html = build_byline(pub, mod)

    new_text = text
    if BYLINE_RE.search(new_text):
        new_text = BYLINE_RE.sub(byline_html, new_text, count=1)
    else:
        h1_match = H1_RE.search(new_text)
        if not h1_match:
            print(f"SKIP (no h1 match): {path}")
            return
        new_text = H1_RE.sub(lambda m: m.group(1) + "\n" + byline_html, new_text, count=1)

    new_text = new_text.replace(OLD_AUTHOR_URL_LINE, NEW_AUTHOR_URL_LINE)

    if new_text == text:
        return

    if apply_changes:
        path.write_text(new_text)
    print(f"UPDATED: {path}")


def main():
    apply_changes = "--apply" in sys.argv
    only = None
    for arg in sys.argv[1:]:
        if arg != "--apply":
            only = arg

    posts = find_posts()
    if only:
        posts = [p for p in posts if only in str(p)]

    for p in posts:
        process(p, apply_changes)


if __name__ == "__main__":
    main()
