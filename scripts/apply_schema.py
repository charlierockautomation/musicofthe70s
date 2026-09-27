#!/usr/bin/env python3
"""Single source of truth for the sitewide JSON-LD nodes (Organization,
WebSite, author Person reference, publisher reference with logo).

- Home page: writes one WebSite + Organization @graph block (stable @ids
  from schema_common.py) between SCHEMA-START/END markers in <head>.
- Every blog post: rewrites the Article block's author and publisher to
  the shared references (@id + inline name/url, publisher gains logo).
  Nothing else in the Article block, and no other block, is touched.
- /about/methodology/: same author/publisher references on AboutPage.

Hubs are handled by generate_category_cards.py and
generate_blog_hub_cards.py, which write their CollectionPage schema from
the same post list they render.

Safe to re-run. Without --apply, reports what would change and writes
nothing. Run with: python3 scripts/apply_schema.py [--apply]
"""
import json
import sys
from pathlib import Path

from schema_common import (
    AUTHOR_REF, LD_RE, ORG_ID, PUBLISHER_REF, SITE, SITE_NAME, LOGO,
    WEBSITE_ID, dump_block, upsert_head_schema,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
BLOG_DIR = REPO_ROOT / "blog"
HOME = REPO_ROOT / "index.html"
METHODOLOGY = REPO_ROOT / "about" / "methodology" / "index.html"

SITE_GRAPH = {
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "WebSite",
            "@id": WEBSITE_ID,
            "name": SITE_NAME,
            "url": f"{SITE}/",
            "publisher": {"@id": ORG_ID},
        },
        {
            "@type": "Organization",
            "@id": ORG_ID,
            "name": SITE_NAME,
            "url": f"{SITE}/",
            "logo": LOGO,
        },
    ],
}


def set_refs(page, target_type):
    """Point author/publisher of the one block of target_type at the
    shared references. Returns (new_page, found)."""
    found = False

    def repl(m):
        nonlocal found
        data = json.loads(m.group(2))
        if data.get("@type") != target_type:
            return m.group(0)
        found = True
        data["author"] = AUTHOR_REF
        data["publisher"] = PUBLISHER_REF
        return m.group(1) + dump_block(data) + m.group(3)

    return LD_RE.sub(repl, page), found


def main():
    apply = "--apply" in sys.argv
    targets = [(p, "Article") for p in sorted(BLOG_DIR.glob("*/*/index.html"))]
    targets.append((METHODOLOGY, "AboutPage"))

    changed, errors = [], []
    for path, target_type in targets:
        page = path.read_text(encoding="utf-8")
        new, found = set_refs(page, target_type)
        if not found:
            errors.append(f"no {target_type} block in {path.relative_to(REPO_ROOT)}")
            continue
        if new != page:
            changed.append((path, new))

    home = HOME.read_text(encoding="utf-8")
    new_home = upsert_head_schema(home, "scripts/apply_schema.py", [SITE_GRAPH])
    if new_home != home:
        changed.append((HOME, new_home))

    for err in errors:
        print(f"ERROR: {err}", file=sys.stderr)
    for path, new in changed:
        print(f"{'WROTE' if apply else 'WOULD CHANGE'} {path.relative_to(REPO_ROOT)}")
        if apply:
            path.write_text(new, encoding="utf-8")
    print(f"\n{len(changed)} file(s) {'changed' if apply else 'to change'}, {len(errors)} error(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
