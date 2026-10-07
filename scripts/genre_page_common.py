"""Shared helpers for the genre-page list generators (generate_genre_lists.py,
generate_beyond_year_end.py). Idempotent: every block lives between a pair of
HTML comment markers and is replaced in place on re-run."""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOC_SCRIPT = ('<script>if(window.matchMedia("(max-width: 699px)").matches)'
              '{document.querySelector(".toc-details").open=false;}</script>')


def norm(s):
    s = s.lower().replace("&", "and")
    s = re.sub(r"\(.*?\)", "", s)
    return re.sub(r"[^a-z0-9]+", "", s)


def read(path):
    return Path(path).read_text(encoding="utf-8")


def write(path, text):
    Path(path).write_text(text, encoding="utf-8")


def ensure_jump(page, href):
    """Jump button right under the byline (list-page layout rule 6b)."""
    if 'class="jump-to-list"' in page:
        return re.sub(r'(<p class="jump-to-list"><a class="btn-primary jump-btn" href=")[^"]*(")',
                      lambda m: m.group(1) + href + m.group(2), page, count=1)
    btn = (f'\n        <p class="jump-to-list"><a class="btn-primary jump-btn" href="{href}">'
           '&#9654; Jump to the playable list</a></p>')
    return re.sub(r'(<p class="post-byline">.*?</p>)', lambda m: m.group(1) + btn, page, count=1, flags=re.S)


def ensure_toc_details(page):
    """Turn <nav class="toc-block"><h2>Table of Contents</h2><ol>..</ol></nav> into the
    collapsible <details class="toc-details"> form (open on desktop, closed under 700px)."""
    if "toc-details" in page:
        return page
    m = re.search(r'(<nav class="toc-block"[^>]*>)\s*<h2>Table of Contents</h2>\s*(<ol>.*?</ol>)\s*</nav>', page, re.S)
    if not m:
        sys.exit("TOC block not found")
    new = (f'{m.group(1)}\n          <details class="toc-details" open>\n            <summary>Table of Contents</summary>\n'
           f'            {m.group(2)}\n          </details>\n        </nav>\n        {TOC_SCRIPT}')
    return page[:m.start()] + new + page[m.end():]


def toc_set(page, anchor_id, text, after_id=None):
    """Add or update a TOC entry. after_id=None puts it first."""
    li = f'<li><a href="#{anchor_id}">{text}</a></li>'
    pat = re.compile(r'<li><a href="#' + re.escape(anchor_id) + r'">.*?</a></li>')
    if pat.search(page):
        return pat.sub(lambda m: li, page, count=1)
    if after_id is None:
        return re.sub(r'(<nav class="toc-block".*?<ol>\s*)', lambda m: m.group(1) + li + "\n            ", page, count=1, flags=re.S)
    return re.sub(r'(<li><a href="#' + re.escape(after_id) + r'">.*?</a></li>)',
                  lambda m: m.group(1) + "\n            " + li, page, count=1)


def put_block(page, start, end, block, before):
    """Replace the block between markers, or insert it (with markers) before `before`."""
    full = f"{start}\n{block}\n        {end}\n\n        "
    pat = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"\n\n        ", re.S)
    if pat.search(page):
        return pat.sub(lambda m: full, page, count=1)
    i = page.find(before)
    if i < 0:
        sys.exit(f"anchor not found: {before}")
    return page[:i] + full + page[i:]


def song_post_slug(title, artist, song_slugs):
    return next((sl for sl in song_slugs if norm(sl) in (norm(title), norm(artist + title), norm(title + artist))), None)


def play_button(yt, title, artist):
    t, a = html.escape(title), html.escape(artist)
    return (f'<button type="button" class="ohw-play" data-yt="{yt}" data-title="{t} by {a}" '
            f'aria-label="Play {t} by {a} here">&#9654; Play</button>')


def ensure_scripts(page):
    """Load the sortable-table and in-page player scripts once."""
    for js in ("sortable-table.js", "table-player.js"):
        if f'/js/{js}' not in page:
            page = page.replace('<script src="/js/main.js"></script>',
                                f'<script src="/js/main.js"></script>\n  <script src="/js/{js}"></script>', 1)
    return page
