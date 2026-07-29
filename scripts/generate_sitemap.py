#!/usr/bin/env python3
"""
Generate sitemap.xml from the actual pages present on disk.

Source of truth is the filesystem, not CONTENT-INDEX.md, so the sitemap
can never drift from what Cloudflare Pages is actually serving. lastmod
dates come from git history of each file so they reflect real edits, not
a manually typed date.

Run manually with: python3 scripts/generate_sitemap.py
Also run automatically on every push to main via
.github/workflows/update-sitemap.yml — this script should not need to be
run by hand as part of normal publishing, but it's safe to.
"""
import subprocess
import sys
from pathlib import Path
from xml.sax.saxutils import escape

REPO_ROOT = Path(__file__).resolve().parent.parent
SITE = "https://musicofthe70s.net"

# Pages tier: (filename without .html) -> (priority, changefreq)
ABOUT_STYLE_PAGES = {"about", "privacy-policy"}


def git_lastmod(path: Path) -> str:
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%ad", "--date=short", "--", str(path)],
            cwd=REPO_ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
        if out:
            return out
    except subprocess.CalledProcessError:
        pass
    # Uncommitted new file (e.g. generated in the same session as the push
    # that adds it) — fall back to today so the entry is still valid.
    import datetime
    return datetime.date.today().isoformat()


def collect_urls():
    urls = []

    # Homepage
    urls.append({
        "loc": f"{SITE}/",
        "lastmod": git_lastmod(REPO_ROOT / "index.html"),
        "changefreq": "monthly",
        "priority": "1.0",
    })

    # Core tool/info pages: /pages/*.html -> /pages/<name> (Cloudflare
    # Pages strips .html and does not add a trailing slash for these)
    pages_dir = REPO_ROOT / "pages"
    for f in sorted(pages_dir.glob("*.html")):
        name = f.stem
        priority = "0.5" if name in ABOUT_STYLE_PAGES else "0.8"
        changefreq = "yearly" if name in ABOUT_STYLE_PAGES else "monthly"
        urls.append({
            "loc": f"{SITE}/pages/{name}",
            "lastmod": git_lastmod(f),
            "changefreq": changefreq,
            "priority": priority,
        })

    # Blog hub: /blog/index.html -> /blog/ (Cloudflare Pages strips
    # index.html and keeps the trailing slash for directory-index files)
    blog_dir = REPO_ROOT / "blog"
    hub = blog_dir / "index.html"
    if hub.exists():
        urls.append({
            "loc": f"{SITE}/blog/",
            "lastmod": git_lastmod(hub),
            "changefreq": "weekly",
            "priority": "0.7",
        })

    # Category pages: /blog/<category>/index.html -> /blog/<category>/
    for cat_dir in sorted(p for p in blog_dir.iterdir() if p.is_dir()):
        cat_index = cat_dir / "index.html"
        if cat_index.exists():
            urls.append({
                "loc": f"{SITE}/blog/{cat_dir.name}/",
                "lastmod": git_lastmod(cat_index),
                "changefreq": "monthly",
                "priority": "0.6",
            })

        # Post pages: /blog/<category>/<slug>/index.html -> /blog/<category>/<slug>/
        for post_dir in sorted(p for p in cat_dir.iterdir() if p.is_dir()):
            post_index = post_dir / "index.html"
            if post_index.exists():
                urls.append({
                    "loc": f"{SITE}/blog/{cat_dir.name}/{post_dir.name}/",
                    "lastmod": git_lastmod(post_index),
                    "changefreq": "monthly",
                    "priority": "0.6",
                })

    return urls


def render(urls) -> str:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{escape(u['loc'])}</loc>")
        lines.append(f"    <lastmod>{u['lastmod']}</lastmod>")
        lines.append(f"    <changefreq>{u['changefreq']}</changefreq>")
        lines.append(f"    <priority>{u['priority']}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main():
    urls = collect_urls()
    xml = render(urls)
    out_path = REPO_ROOT / "sitemap.xml"
    existing = out_path.read_text() if out_path.exists() else None
    out_path.write_text(xml)

    print(f"sitemap.xml written with {len(urls)} URLs")
    for u in urls:
        print(f"  {u['loc']}")

    if existing == xml:
        print("No changes.")
        return 0
    print("sitemap.xml changed." if existing is not None else "sitemap.xml created.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
