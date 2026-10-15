#!/usr/bin/env python3
"""
PUBLISH GATE check: fail if any <img src>, <source srcset>/<img srcset> on a
built HTML page points to a local file that does not exist on disk.

Usage: python3 scripts/check_image_files.py
Exits 1 and prints every missing file (with page) if any found, else PASS.
"""
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", ".serena", "node_modules", "video_site_logo", ".claude"}
IMG_TAG = re.compile(r"<(?:img|source)\b[^>]*>", re.I | re.S)
SRC = re.compile(r'\b(?:src|srcset)\s*=\s*"([^"]*)"', re.I)


def local_path(url, page):
    url = url.strip()
    if not url or url.startswith(("data:", "#")):
        return None
    p = urlparse(url)
    if p.scheme in ("http", "https"):
        if p.netloc not in ("musicofthe70s.net", "www.musicofthe70s.net"):
            return None
        path = p.path
    elif p.scheme or p.netloc:
        return None
    else:
        path = p.path
    path = unquote(path)
    if not path:
        return None
    return ROOT / path.lstrip("/") if path.startswith("/") else page.parent / path


def main():
    missing = []
    for page in sorted(ROOT.rglob("*.html")):
        if SKIP_DIRS & set(page.relative_to(ROOT).parts):
            continue
        text = page.read_text(encoding="utf-8", errors="ignore")
        for tag in IMG_TAG.finditer(text):
            for attr in SRC.finditer(tag.group(0)):
                val = attr.group(1)
                # srcset: comma-separated "url descriptor" entries
                cands = [c.strip().split()[0] for c in val.split(",") if c.strip()] \
                    if "srcset" in attr.group(0).lower()[:7] else [val]
                for c in cands:
                    f = local_path(c, page)
                    if f is not None and not f.is_file():
                        line = text.count("\n", 0, tag.start()) + 1
                        missing.append(f"{page.relative_to(ROOT)}:{line} -> {c}")
    if missing:
        print(f"FAIL: {len(missing)} image reference(s) point to missing files")
        for m in missing:
            print("  " + m)
        sys.exit(1)
    print("PASS: every img src/srcset on built pages exists on disk")


if __name__ == "__main__":
    main()
