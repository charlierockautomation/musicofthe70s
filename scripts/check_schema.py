#!/usr/bin/env python3
"""
PUBLISH GATE pre-commit check for JSON-LD, alongside check_clean_urls.py.
Fails (exit 1) if any built HTML page has:

- a JSON-LD block that isn't valid JSON
- a node missing the properties this site requires for its @type
  (Article, FAQPage, BreadcrumbList, CollectionPage/ItemList, WebSite,
  Organization, ProfilePage/Person, AboutPage, WebApplication)
- more than one Article/BlogPosting block, or both types on one page
- Article dates that don't match the visible byline, a mainEntityOfPage
  or CollectionPage url that isn't the canonical, an image/logo whose
  file isn't in the repo, or an author/publisher @id that isn't the
  shared one from schema_common.py
- a hub ItemList entry that isn't a real post and linked on the page
- an @id reference that no page on the site defines
- no schema at all on a page that must have it (home, posts, hubs,
  /about/*, /radio/)

Usage: python3 scripts/check_schema.py
Prints every problem as file: message and exits 1, or prints PASS.
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

from schema_common import AUTHOR_ID, LD_RE, ORG_ID, SITE, WEBSITE_ID

REPO_ROOT = Path(__file__).resolve().parent.parent

MUST_HAVE_SCHEMA = re.compile(r"^(index\.html|blog/.+/index\.html|blog/index\.html|about/[^/]+/index\.html|radio/index\.html)$")
POST_PATH = re.compile(r"^blog/[^/]+/[^/]+/index\.html$")
HUB_PATH = re.compile(r"^blog/(?:[^/]+/)?index\.html$")
BYLINE_RE = re.compile(r'<p class="post-byline">(.*?)</p>', re.S)
CANONICAL_RE = re.compile(r'<link rel="canonical" href="([^"]*)"')

REQUIRED = {
    "Article": ["headline", "image", "datePublished", "dateModified", "author", "publisher", "mainEntityOfPage"],
    "BlogPosting": ["headline", "image", "datePublished", "dateModified", "author", "publisher", "mainEntityOfPage"],
    "FAQPage": ["mainEntity"],
    "BreadcrumbList": ["itemListElement"],
    "CollectionPage": ["@id", "url", "name", "mainEntity"],
    "ItemList": ["itemListElement"],
    "WebSite": ["@id", "name", "url"],
    "Organization": ["name", "url"],
    "ProfilePage": ["mainEntity"],
    "Person": ["name"],
    "AboutPage": ["name", "url"],
    "WebApplication": ["name", "url", "applicationCategory"],
}


def local_path(url):
    """Map a site URL to the file Cloudflare Pages would serve, or None
    for off-site URLs."""
    if not url.startswith(SITE + "/"):
        return None
    path = url[len(SITE) + 1:].split("#")[0].split("?")[0]
    if path == "" or path.endswith("/"):
        return REPO_ROOT / path / "index.html"
    candidate = REPO_ROOT / path
    return candidate if candidate.suffix else candidate.with_suffix(".html")


def walk(node):
    """Yield every dict node in a JSON-LD tree."""
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from walk(v)
    elif isinstance(node, list):
        for v in node:
            yield from walk(v)


def byline_dates(page):
    m = BYLINE_RE.search(page)
    if not m:
        return None, None
    text = re.sub(r"<[^>]+>", "", m.group(1))
    def iso(label):
        d = re.search(label + r" ([A-Z][a-z]+ \d{1,2}, \d{4})", text)
        return datetime.strptime(d.group(1), "%B %d, %Y").strftime("%Y-%m-%d") if d else None
    return iso("Published"), iso("Updated")


def check_file_exists(url, what, err):
    target = local_path(url) if isinstance(url, str) else None
    if target is None or not target.is_file():
        err(f"{what} {url!r} is not a file in this repo")


def check_node(node, rel, page, canonical, err):
    t = node.get("@type")
    for prop in REQUIRED.get(t, []):
        if node.get(prop) in (None, "", [], {}):
            err(f"{t} missing required '{prop}'")

    if t in ("Article", "BlogPosting"):
        if node.get("mainEntityOfPage") != canonical:
            err(f"{t} mainEntityOfPage {node.get('mainEntityOfPage')!r} != canonical {canonical!r}")
        check_file_exists(node.get("image"), f"{t} image", err)
        author = node.get("author") or {}
        if author.get("@id") != AUTHOR_ID or not author.get("name") or not author.get("url"):
            err(f"{t} author must carry @id {AUTHOR_ID} plus name and url")
        pub = node.get("publisher") or {}
        if pub.get("@id") != ORG_ID or not pub.get("name") or not (pub.get("logo") or {}).get("url"):
            err(f"{t} publisher must carry @id {ORG_ID} plus name and logo.url")
        published, updated = byline_dates(page)
        if published is None:
            err("post has no visible byline with a Published date")
        else:
            if node.get("datePublished") != published:
                err(f"datePublished {node.get('datePublished')} != byline {published}")
            if node.get("dateModified") != (updated or published):
                err(f"dateModified {node.get('dateModified')} != byline {updated or published}")

    if t == "Organization" and node.get("logo"):
        logo = node["logo"]
        check_file_exists(logo.get("url") if isinstance(logo, dict) else logo, "Organization logo", err)

    if t == "FAQPage":
        for q in node.get("mainEntity") or []:
            if not q.get("name") or not (q.get("acceptedAnswer") or {}).get("text"):
                err("FAQPage Question missing name or acceptedAnswer.text")

    if t == "BreadcrumbList":
        items = node.get("itemListElement") or []
        if [i.get("position") for i in items] != list(range(1, len(items) + 1)):
            err("BreadcrumbList positions are not 1..n in order")
        for i in items:
            if not i.get("name") or not i.get("item"):
                err("BreadcrumbList ListItem missing name or item")
        if items and items[-1].get("item") != canonical:
            err(f"BreadcrumbList last item {items[-1].get('item')!r} != canonical {canonical!r}")

    if t == "CollectionPage" and node.get("url") != canonical:
        err(f"CollectionPage url {node.get('url')!r} != canonical {canonical!r}")

    if t == "ItemList":
        items = node.get("itemListElement") or []
        if [i.get("position") for i in items] != list(range(1, len(items) + 1)):
            err("ItemList positions are not 1..n in order")
        if node.get("numberOfItems") not in (None, len(items)):
            err(f"ItemList numberOfItems {node.get('numberOfItems')} != {len(items)} entries")
        for i in items:
            url = i.get("url") or ""
            target = local_path(url)
            if target is None or not target.is_file():
                err(f"ItemList url {url!r} is not a page on this site")
            elif f'href="{url[len(SITE):]}"' not in page and f'href="{url}"' not in page:
                err(f"ItemList url {url!r} is not linked on the page")


def main():
    problems = []
    defined_ids, referenced_ids = set(), []

    for f in sorted(REPO_ROOT.rglob("*.html")):
        if ".git" in f.parts:
            continue
        rel = f.relative_to(REPO_ROOT).as_posix()
        page = f.read_text(encoding="utf-8")
        canonical = (CANONICAL_RE.search(page) or [None, None])[1]
        err = lambda msg, rel=rel: problems.append(f"{rel}: {msg}")

        blocks = []
        for m in LD_RE.finditer(page):
            try:
                blocks.append(json.loads(m.group(2)))
            except json.JSONDecodeError as e:
                err(f"invalid JSON-LD: {e}")

        if not blocks and MUST_HAVE_SCHEMA.match(rel) and rel != "404.html":
            err("page has no JSON-LD")
            continue

        types = [n.get("@type") for b in blocks for n in walk(b) if n.get("@type")]
        articles = [t for t in types if t in ("Article", "BlogPosting")]
        if len(articles) > 1:
            err(f"conflicting article types on one page: {articles}")
        if POST_PATH.match(rel) and articles != ["Article"]:
            err("post must have exactly one Article block")
        if POST_PATH.match(rel) and "BreadcrumbList" not in types:
            err("post has no BreadcrumbList")
        if HUB_PATH.match(rel) and not {"CollectionPage", "ItemList", "BreadcrumbList"} <= set(types):
            err("hub must have CollectionPage + ItemList + BreadcrumbList")

        for block in blocks:
            for node in walk(block):
                node_id = node.get("@id")
                if node_id:
                    # A page defines an @id only when the @id points at that
                    # page (home defines /#organization, the author page
                    # defines /about/author/); anywhere else it's a reference.
                    if len(node) > 1 and node_id.split("#")[0] == canonical:
                        defined_ids.add(node_id)
                    referenced_ids.append((rel, node_id))
                check_node(node, rel, page, canonical, err)

    for required_id in (ORG_ID, WEBSITE_ID, AUTHOR_ID):
        if required_id not in defined_ids:
            problems.append(f"sitewide: {required_id} is not defined (Organization/WebSite on index.html, Person on about/author/)")
    for rel, ref in referenced_ids:
        if ref not in defined_ids:
            problems.append(f"{rel}: @id reference {ref!r} is not defined anywhere on the site")

    if problems:
        print(f"FAIL: {len(problems)} schema problem(s)")
        for p in problems:
            print(f"  {p}")
        return 1
    print("PASS: all JSON-LD valid, required properties present, @ids resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
