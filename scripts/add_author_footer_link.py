#!/usr/bin/env python3
"""Add the 'About the Author' footer link site-wide.

Single source of truth for the shared footer block. Run with --apply to
write changes; without it, prints which files would change.
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

FOOTER_TEMPLATE = '''  <footer class="site-footer">
    <p>{copy} 2026 Music of the 70s |
      <a href="/pages/privacy-policy">Privacy Policy</a> |
      <a href="/pages/terms-of-use">Terms of Use</a> |
      <a href="/pages/contact">Contact</a> |
      <a href="/pages/about">About</a>{author_link}
    </p>
  </footer>'''

VARIANTS = [
    (FOOTER_TEMPLATE.format(copy="©", author_link=""),
     FOOTER_TEMPLATE.format(copy="©", author_link=' |\n      <a href="/about/author/">About the Author</a>')),
    (FOOTER_TEMPLATE.format(copy="&copy;", author_link=""),
     FOOTER_TEMPLATE.format(copy="&copy;", author_link=' |\n      <a href="/about/author/">About the Author</a>')),
]


def main():
    apply_changes = "--apply" in sys.argv
    files = sorted(REPO_ROOT.rglob("*.html"))

    changed = 0
    for f in files:
        text = f.read_text()
        for old, new in VARIANTS:
            if old in text:
                changed += 1
                if apply_changes:
                    f.write_text(text.replace(old, new))
                print(f"UPDATED: {f.relative_to(REPO_ROOT)}")
                break

    print(f"\n{changed} files {'updated' if apply_changes else 'would be updated'}")


if __name__ == "__main__":
    main()
