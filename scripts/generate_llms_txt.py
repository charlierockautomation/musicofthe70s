#!/usr/bin/env python3
"""
Generate root-level llms.txt from the pages actually on disk, same
philosophy as scripts/generate_sitemap.py and
scripts/generate_blog_hub_cards.py: the filesystem is the source of
truth, so this can never drift from CONTENT-INDEX.md.

Sections: Tools (6 permanent pillar pages, pages/*.html) then one
section per live blog category (Genres, Years, Artists, Songs, Trivia),
each entry sourced from that post's own Article schema headline +
datePublished + meta description. Categories with a real datePublished
sort newest-first; Tools have no publish date so they sort alphabetically
by title.

MAX_TOTAL_ENTRIES caps the combined post count (tools are never cut).
Not close to being hit at current post counts, but kept so this doesn't
silently blow past a sane ceiling if the site's content grows a lot.
Trims oldest-first from whichever blog category is currently largest.

Run manually with: python3 scripts/generate_llms_txt.py
Also runs automatically on every push to main via
.github/workflows/update-generated-files.yml, alongside the sitemap and
Blog Hub card generators.
"""
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SITE = "https://musicofthe70s.net"
BLOG_DIR = REPO_ROOT / "blog"
PAGES_DIR = REPO_ROOT / "pages"
LLMS_TXT = REPO_ROOT / "llms.txt"

MAX_TOTAL_ENTRIES = 200

# Tool pages to include, in the fixed set the site actually ships.
# rock-trivia-game.html exists on disk but was explicitly not shipped
# (content-build.md, 2026-08-27 call) so it's deliberately excluded here,
# same as it's excluded from the live tools grid.
TOOL_FILES = {
    "70s-decade-wheel.html",
    "70s-trivia-quiz.html",
    "birthday-number-one.html",
    "mood-song-matcher.html",
    "random-70s-song.html",
    "random-artist-picker.html",
}

CATEGORY_ORDER = ["genres", "years", "artists", "songs", "trivia"]
CATEGORY_LABELS = {
    "genres": "Genres",
    "years": "Years",
    "artists": "Artists",
    "songs": "Songs",
    "trivia": "Trivia",
}


def _extract(pattern, text, flags=0):
    m = re.search(pattern, text, flags)
    return m.group(1) if m else None


def find_tools():
    tools = []
    for fname in sorted(TOOL_FILES):
        f = PAGES_DIR / fname
        if not f.exists():
            print(f"WARNING: expected tool page missing: {f}", file=sys.stderr)
            continue
        html = f.read_text(encoding="utf-8")
        title = _extract(r"<title>([^<]*)</title>", html)
        description = _extract(r'<meta name="description" content="([^"]*)"', html)
        if not all([title, description]):
            print(f"WARNING: skipping {f}, missing title/description", file=sys.stderr)
            continue
        # Trim the " | Music of the 70s"-style suffix some titles carry,
        # keep the descriptive lead so entries read as tool names.
        title = title.split(" | ")[0].strip()
        tools.append({
            "title": title,
            "description": description,
            "url": f"{SITE}/pages/{f.stem}",
        })
    tools.sort(key=lambda t: t["title"])
    return tools


def find_posts_by_category():
    by_cat = {c: [] for c in CATEGORY_ORDER}
    for cat_dir in sorted(p for p in BLOG_DIR.iterdir() if p.is_dir()):
        if cat_dir.name not in by_cat:
            continue
        for post_dir in sorted(p for p in cat_dir.iterdir() if p.is_dir()):
            if post_dir.name == "archive":
                continue
            post_index = post_dir / "index.html"
            if not post_index.exists():
                continue
            html = post_index.read_text(encoding="utf-8")

            headline = _extract(r'"headline":\s*"([^"]*)"', html)
            date_published = _extract(r'"datePublished":\s*"([^"]*)"', html)
            description = _extract(r'<meta name="description" content="([^"]*)"', html)

            if not all([headline, date_published, description]):
                print(f"WARNING: skipping {post_index}, missing required field(s)", file=sys.stderr)
                continue

            by_cat[cat_dir.name].append({
                "headline": headline,
                "date": date_published,
                "description": description,
                "url": f"{SITE}/blog/{cat_dir.name}/{post_dir.name}/index.html",
            })
        by_cat[cat_dir.name].sort(key=lambda p: p["date"], reverse=True)
    return by_cat


def apply_cap(by_cat):
    """Trim oldest-first from whichever category is largest until the
    combined post count is at or under MAX_TOTAL_ENTRIES. Tools are not
    part of this count and are never trimmed."""
    total = sum(len(v) for v in by_cat.values())
    dropped = []
    while total > MAX_TOTAL_ENTRIES:
        largest = max(by_cat, key=lambda c: len(by_cat[c]))
        if not by_cat[largest]:
            break
        removed = by_cat[largest].pop()  # oldest, since each list is newest-first
        dropped.append((largest, removed))
        total -= 1
    return dropped


def render_section(label, posts):
    lines = [f"## {label}"]
    for p in posts:
        lines.append(f"- [{p['headline']}]({p['url']}): {p['description']}")
    return "\n".join(lines)


def render_tools_section(tools):
    lines = ["## Tools"]
    for t in tools:
        lines.append(f"- [{t['title']}]({t['url']}): {t['description']}")
    return "\n".join(lines)


def main():
    tools = find_tools()
    by_cat = find_posts_by_category()
    dropped = apply_cap(by_cat)

    parts = [
        "# Music of the 70s",
        "> Discover, Explore and Relive the Greatest Decade in Music",
        "",
        f"Sitemap: {SITE}/sitemap.xml",
        "",
        render_tools_section(tools),
        "",
    ]
    for cat in CATEGORY_ORDER:
        parts.append(render_section(CATEGORY_LABELS[cat], by_cat[cat]))
        parts.append("")

    content = "\n".join(parts).rstrip() + "\n"

    existing = LLMS_TXT.read_text(encoding="utf-8") if LLMS_TXT.exists() else None
    LLMS_TXT.write_text(content, encoding="utf-8")
    changed = existing != content

    total_posts = sum(len(v) for v in by_cat.values())
    print(f"Tools: {len(tools)}")
    for cat in CATEGORY_ORDER:
        print(f"{CATEGORY_LABELS[cat]}: {len(by_cat[cat])}")
    print(f"Total blog entries: {total_posts} (cap {MAX_TOTAL_ENTRIES})")
    for cat, p in dropped:
        print(f"  DROPPED (cap) {cat}: {p['date']}  {p['headline']}")
    print("llms.txt changed." if changed else "llms.txt unchanged.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
