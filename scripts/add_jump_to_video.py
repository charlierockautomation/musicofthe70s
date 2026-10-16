#!/usr/bin/env python3
"""Add a "Jump to the video" button under the byline of single-song Songs posts.

Skips posts that already have a jump-to-list button (the playable-list pages) and posts
without exactly one video-embed div. Idempotent: re-running changes nothing.

Run: python3 scripts/add_jump_to_video.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BTN = ('        <p class="jump-to-list"><a class="btn-primary jump-btn" '
       'href="#song-video">&#9654; Jump to the video</a></p>\n')
BYLINE = re.compile(r'(        <p class="post-byline">.*?</p>\n)', re.S)

changed, skipped = [], []
for f in sorted((ROOT / "blog/songs").glob("*/index.html")):
    s = f.read_text(encoding="utf-8")
    if "jump-to-list" in s or s.count('<div class="video-embed">') != 1 or len(BYLINE.findall(s)) != 1:
        skipped.append(f.parent.name)
        continue
    s = BYLINE.sub(lambda m: m.group(1) + "\n" + BTN, s, count=1)
    s = s.replace('<div class="video-embed">', '<div class="video-embed" id="song-video">', 1)
    f.write_text(s, encoding="utf-8")
    changed.append(f.parent.name)
print(f"changed {len(changed)}, skipped {len(skipped)}: {skipped}")
