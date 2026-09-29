#!/usr/bin/env python3
"""Build the sortable ranking on /blog/artists/70s-female-singers/ from
data/billboard/year_end_hot100.json and data/billboard/hot100_weekly.json,
the same way generate_70s_singers_table.py and generate_70s_bands_table.py
build their pages.

Who counts: solo women credited under their own name, with 2 or more
year-end Hot 100 hits from 1970-1979 in this site's data. The bar is lower
than the 3-hit bar used on the 70s Singers page because only 11 women clear
that bar; dropping to 2 keeps the ranking a real list instead of a top-11
curiosity, and is stated as the counting call on the page itself.

Women who charted only as part of a group credit (Karen Carpenter via The
Carpenters, Gladys Knight via Gladys Knight & the Pips, Stevie Nicks and
Christine McVie via Fleetwood Mac) are on the 70s Bands page instead, not
double-counted here. Shared solo+solo credits ("John Travolta & Olivia
Newton-John") are shown in a separate Duets table on the page, not counted
in this ranking.

Ranking: solo year-end entries, ties broken by chart points (101 minus
year-end rank, summed over every entry) -- same method as the other two
Artists flagship pages.

Each row's biggest hit gets a Play button when the song is in
data/radio/radio-songs.json with a YouTube ID (js/table-player.js).

Rewrites the block between <!-- FEMALE-SINGERS-START --> and
<!-- FEMALE-SINGERS-END -->.

Run: python3 scripts/generate_70s_female_singers_table.py [--stats]
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "blog/artists/70s-female-singers/index.html"
START, END = "<!-- FEMALE-SINGERS-START -->", "<!-- FEMALE-SINGERS-END -->"

SINGERS = [
    "Olivia Newton-John", "Helen Reddy", "Anne Murray", "Donna Summer",
    "Diana Ross", "Cher", "Carly Simon", "Aretha Franklin", "Linda Ronstadt",
    "Barbra Streisand", "Roberta Flack", "Melanie", "Maxine Nightingale",
    "Freda Payne", "Gloria Gaynor", "Natalie Cole", "Melissa Manchester",
    "Rita Coolidge", "Dionne Warwick", "Donna Fargo", "Bette Midler",
    "Alicia Bridges",
]
EXCLUDE = set()

# Songs posts whose slug doesn't contain the title, keyed by (artist, title)
POSTS = {}


def norm(s):
    s = s.lower().replace("&", "and")
    s = re.sub(r"\(.*?\)", "", s)
    return re.sub(r"[^a-z0-9]+", "", s)


def build():
    ye = json.loads((ROOT / "data/billboard/year_end_hot100.json").read_text())
    wk = json.loads((ROOT / "data/billboard/hot100_weekly.json").read_text())
    rows = {s: {"singer": s, "hits": [], "ones": {}} for s in SINGERS}
    for year, recs in ye.items():
        for r in recs:
            if r["artist"] in rows and (r["artist"], r["title"]) not in EXCLUDE:
                rows[r["artist"]]["hits"].append((int(year), r["rank"], r["title"]))
    for year, recs in wk.items():
        for r in recs:
            if r["artist"] in rows:
                rows[r["artist"]]["ones"][r["title"]] = rows[r["artist"]]["ones"].get(r["title"], 0) + 1
    out = []
    for s, x in rows.items():
        hits = sorted(x["hits"], key=lambda h: (h[1], h[0]))
        x["count"] = len(hits)
        x["points"] = sum(101 - h[1] for h in hits)
        x["best"] = hits[0] if hits else None
        x["years"] = (min(h[0] for h in hits), max(h[0] for h in hits)) if hits else None
        x["n_ones"] = len(x["ones"])
        x["weeks"] = sum(x["ones"].values())
        out.append(x)
    out.sort(key=lambda x: (-x["count"], -x["points"]))
    for i, x in enumerate(out, 1):
        x["rank"] = i
    return out


def main():
    data = build()
    if "--stats" in sys.argv:
        for x in data:
            print(x["rank"], x["singer"], x["count"], x["points"], x["best"], x["years"],
                  x["n_ones"], x["weeks"], sorted(x["ones"]))
        return

    radio = json.loads((ROOT / "data/radio/radio-songs.json").read_text())
    radio_yt = {}
    for s in radio:
        radio_yt.setdefault((norm(s["title"]), norm(s["artist"])), (s["radio_id"], s.get("youtube_id")))

    song_slugs = {p.parent.name for p in (ROOT / "blog/songs").glob("*/index.html")}
    artist_slugs = {p.parent.name for p in (ROOT / "blog/artists").glob("*/index.html")}

    out = []
    for x in data:
        s = x["singer"]
        year, rank, title = x["best"]
        rid, yt = radio_yt.get((norm(title), norm(s)), (None, None))
        t = html.escape(title)
        slug = next((sl for sl in song_slugs if norm(sl) == norm(title)
                     or norm(sl) == norm(s + title) or norm(sl) == norm(title + s)), None)
        song_cell = f'<a href="/blog/songs/{slug}/">{t}</a>' if slug else t
        aslug = next((sl for sl in artist_slugs if norm(sl) == norm(s)), None)
        singer_cell = f'<a href="/blog/artists/{aslug}/">{html.escape(s)}</a>' if aslug else html.escape(s)
        if yt:
            play = (f'<button type="button" class="ohw-play" data-yt="{yt}" data-title="{t} by {html.escape(s)}" '
                    f'aria-label="Play {t} by {html.escape(s)} here">&#9654; Play</button>')
        elif rid:
            play = f'<a href="/radio/?play={rid}" aria-label="Find {t} on Listen Now">Listen Now</a>'
        else:
            play = ""
        out.append(
            f'<tr><td class="ohw-listen">{play}</td>'
            f'<td data-sort="{x["rank"]}">{x["rank"]}</td>'
            f'<td class="ohw-artist">{singer_cell}</td>'
            f'<td data-sort="{x["count"]}">{x["count"]}</td>'
            f'<td data-sort="{x["n_ones"]}">{x["n_ones"]}</td>'
            f'<td data-sort="{x["weeks"]}">{x["weeks"]}</td>'
            f'<td class="ohw-song">{song_cell} <span class="table-note">({year}, No. {rank})</span></td></tr>'
        )

    page = PAGE.read_text(encoding="utf-8")
    if START not in page or END not in page:
        sys.exit(f"markers missing in {PAGE}")
    body = "\n".join("              " + line for line in out)
    new = re.sub(re.escape(START) + ".*?" + re.escape(END),
                 lambda m: START + "\n" + body + "\n              " + END, page, flags=re.S)
    PAGE.write_text(new, encoding="utf-8")
    print(f"{len(out)} singers, {sum('ohw-play' in r for r in out)} with in-page play")


if __name__ == "__main__":
    main()
