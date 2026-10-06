#!/usr/bin/env python3
"""Pre-push gate: a year-end rank must never be written as a chart peak.

Year-end data (data/billboard/year_end_hot100.json) has RANKS only. Peaks and
weeks at #1 come from data/billboard/hot100_weekly.json (number ones only) or
an outside source such as Wikipedia, and the page must credit it that way.

Fails (exit 1) when a sentence/list item/table row names a song and states
"number N", "#N" or "No. N" where N equals that song's year-end rank, unless
the text says it is a year-end figure (year-end, ranked, rank, finished,
database, billboard_peak, closed out ...) or N is 1 and the song really hit #1
in the weekly file. Also fails on "year-end ... confirms ... peak/weeks at".
Skips /blog/years/ (year-end lists by design) and table rows (each column has a
header; label the column "Year-End Rank" or "Weekly peak", never plain "Peak").
"""
import glob, html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
norm = lambda s: re.sub(r"[^a-z0-9]", "", re.sub(r"\(.*?\)", "", s.lower().replace("&", "and")))
ye = json.loads((ROOT / "data/billboard/year_end_hot100.json").read_text())
weekly = json.loads((ROOT / "data/billboard/hot100_weekly.json").read_text())
songs = [(int(y), r["rank"], r["title"], norm(r["title"])) for y, l in ye.items() for r in l]
no1 = {norm(w["title"]) for wk in weekly.values() for w in wk}
NUM = re.compile(r"(?:number|no\.|#)\s*(\d{1,3})\b", re.I)
OK = re.compile(r"year-end|year end|ranked|rank|ranking|finished|finishing|billboard_peak|database|countdown|closed out|for the year|of the year|for 19\d\d|not #\d+|turn up at", re.I)
BAD_ATTR = re.compile(r"year-end[^.]{0,80}confirm[^.]{0,80}(peak|weeks? at|three-week|two-week|run at)", re.I)
SKIP = ("/blog/years/", "/.claude/", "/video_site_logo/", "/sources/")
bad = []
for f in sorted(glob.glob(str(ROOT / "**/*.html"), recursive=True)):
    if any(k in f.replace(str(ROOT), "") + "/" for k in SKIP) or "/blog/years/" in f:
        continue
    s = Path(f).read_text(encoding="utf-8")
    for u in re.findall(r"<(?:li|p|h2|h3)[^>]*>(.*?)</(?:li|p|h2|h3)>", s[s.find("<body"):], re.S):
        t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", u))).strip()
        if len(t) > 500:
            continue
        if BAD_ATTR.search(t):
            bad.append((f, "year-end data credited for peak/weeks", t[:150])); continue
        if OK.search(t):
            continue
        tn = norm(t)
        for m in NUM.finditer(t):
            n = int(m.group(1))
            hit = [x for x in songs if x[1] == n and len(x[3]) >= 4 and x[3] in tn]
            if hit and not (n == 1 and hit[0][3] in no1):
                bad.append((f, f"{hit[0][2]} ({hit[0][0]}) year-end rank {n} written as a chart number", t[:150])); break
if bad:
    for f, why, t in bad:
        print(f"FAIL {f.replace(str(ROOT)+'/', '')}: {why}\n     {t}")
    print(f"{len(bad)} problem(s). Year-end data = ranks only; peaks/weeks at #1 come from hot100_weekly.json or Wikipedia and must be credited that way.")
    sys.exit(1)
print("PASS: no year-end rank written as a peak, and no peak/weeks credited to year-end data.")
