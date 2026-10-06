#!/usr/bin/env python3
"""Audit every page for playable song lists (3+ Play buttons) and report
where the list starts at 390px and 1280px, whether it scrolls in its own
box, and how many rows have no Play button. Needs the site served on :8000."""
import glob, re, sys
from playwright.sync_api import sync_playwright
BASE = "http://localhost:8000/"
ALL = sorted(f for f in glob.glob("**/*.html", recursive=True) if not f.startswith((".claude", "video_site_logo", "sources")))
# Static pre-scan so only pages that can have a play list get rendered: 3+ Play buttons in
# the HTML, or a list built by JS (the radio jukebox).
PLAY_RE = re.compile(r'data-yt=|class="(?:n1|ohw)-play"')
files = [f for f in ALL if len(PLAY_RE.findall(open(f, encoding="utf-8").read())) >= 3 or f == "radio/index.html"]
single = [f for f in ALL if f not in files and "youtube.com/embed/" in open(f, encoding="utf-8").read()]
print(f"{len(ALL)} pages scanned: {len(files)} with a play list, {len(single)} with one single-song embed (not a list, skipped)")
JS = """() => {
  const btns=[...document.querySelectorAll('button[data-yt], button.ohw-play, button.n1-play, .jukebox-play, [data-play]')];
  const wrap=document.querySelector('.scroll-list');
  const tbl=document.querySelector('table[data-inline-player]');
  const el=wrap||tbl;
  const rows=tbl?[...tbl.tBodies[0].rows]:[];
  const miss=rows.filter(r=>!r.querySelector('button[data-yt]')).map(r=>r.innerText.replace(/\\s+/g,' ').trim().slice(0,90));
  return {plays:btns.length, top: el? Math.round(el.getBoundingClientRect().top+scrollY):null,
    scrolls: wrap? wrap.scrollHeight>wrap.clientHeight:false, rows:rows.length, miss}
}"""
out = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for f in files:
        url = BASE + re.sub(r"index\.html$", "", f)
        res = {}
        for w in (390, 1280):
            pg = b.new_page(viewport={"width": w, "height": 800})
            pg.goto(url); pg.wait_for_timeout(300)
            res[w] = pg.evaluate(JS); pg.close()
        if res[390]["plays"] >= 3 or res[390]["rows"]:
            out.append((f, res))
    b.close()
for f, r in out:
    a, c = r[390], r[1280]
    print(f"{f}: plays={a['plays']} rows={a['rows']} missing={len(a['miss'])} top390={a['top']} top1280={c['top']} scrolls={a['scrolls']}")
    for m in a["miss"]: print("    NO PLAY:", m)
if not out: print("no playable song lists found")
