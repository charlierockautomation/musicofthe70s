#!/usr/bin/env python3
"""
Build the sortable ranking on /blog/artists/70s-bands/ from
data/billboard/year_end_hot100.json and data/billboard/hot100_weekly.json,
the same way generate_70s_singers_table.py builds the singers page.

Who counts: groups and duos only (the companion 70s Singers page covers
solo voices). BANDS below is the hand-checked list of every group act
with 3 or more year-end credits on the 1970-1979 Billboard Hot 100 in
this site's data, after merging spelling/credit variants of the same act
(counting call stated on the page too):

- "Wings" / "Paul McCartney & Wings" / "Paul McCartney and Wings" are one
  act, merged here as Wings. "Paul & Linda McCartney" (a 1971 duo credit
  that predates the Wings name) is NOT merged in and doesn't reach the
  3-hit threshold on its own.
- "Dr. Hook" / "Dr. Hook & the Medicine Show" / "Dr. Hook & The Medicine
  Show" are one act that dropped part of its name in 1976, merged here
  as Dr. Hook.
- Duo acts that charted only as one-off pairings of two already-ranked
  solo singers (the 70s Singers page's own "Duets" table) are not
  counted here even if they'd clear the 3-hit bar alone; none currently do.

Ranking: year-end entries, ties broken by chart points (101 minus
year-end rank, summed over every entry) -- same method as the singers page.

Each row's biggest hit gets a Play button only when an official artist or
label upload is recorded in data/official-videos.json ("song": "Title - Artist",
Article Standard L3). No radio-songs.json fallback: a song with no official
upload stays in the ranking without a button (js/table-player.js skips it).
Band names are plain text: the page's genre directory carries the act links.

Rewrites the block between <!-- BANDS-START --> and <!-- BANDS-END -->.

Run: python3 scripts/generate_70s_bands_table.py [--stats]
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "blog/artists/70s-bands/index.html"
START, END = "<!-- BANDS-START -->", "<!-- BANDS-END -->"

BANDS = [
    "Bee Gees", "The Carpenters", "Wings", "Chicago", "Electric Light Orchestra",
    "Earth, Wind & Fire", "Gladys Knight & the Pips", "The Jackson 5",
    "Three Dog Night", "War", "Dr. Hook", "The O'Jays", "ABBA", "Eagles",
    "Fleetwood Mac", "KC and the Sunshine Band", "Queen", "Steely Dan",
    "The Spinners", "The Temptations", "Bob Seger & The Silver Bullet Band",
    "Bread", "Captain & Tennille", "Chic", "Commodores", "Foreigner",
    "Ohio Players", "Steve Miller Band", "Sweet", "The Stylistics",
    "Tony Orlando and Dawn", "America", "Bay City Rollers",
    "Creedence Clearwater Revival", "Grand Funk Railroad", "Heatwave",
    "Little River Band", "Rare Earth", "Sly & the Family Stone", "Styx",
    "The Beatles", "The Doobie Brothers", "The Hollies", "The Isley Brothers",
    "The Osmonds", "The Rolling Stones", "The Sylvers",
]
# year-end and weekly credit strings that mean the same merged act
ALIAS = {
    "Paul McCartney & Wings": "Wings",
    "Paul McCartney and Wings": "Wings",
    "Dr. Hook & the Medicine Show": "Dr. Hook",
    "Dr. Hook & The Medicine Show": "Dr. Hook",
    # same act under the credit each chart week or year used (added 2026-11-09)
    "Dawn": "Tony Orlando and Dawn",
    "Dawn featuring Tony Orlando": "Tony Orlando and Dawn",
    "Grand Funk": "Grand Funk Railroad",
    "Sly and the Family Stone": "Sly & the Family Stone",
}
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
    rows = {b: {"band": b, "hits": [], "ones": {}} for b in BANDS}
    for year, recs in ye.items():
        for r in recs:
            a = ALIAS.get(r["artist"], r["artist"])
            if a in rows and (a, r["title"]) not in EXCLUDE:
                rows[a]["hits"].append((int(year), r["rank"], r["title"]))
    for year, recs in wk.items():
        for r in recs:
            a = ALIAS.get(r["artist"], r["artist"])
            if a in rows:
                rows[a]["ones"][r["title"]] = rows[a]["ones"].get(r["title"], 0) + 1
    out = []
    for b, x in rows.items():
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
            print(x["rank"], x["band"], x["count"], x["points"], x["best"], x["years"],
                  x["n_ones"], x["weeks"], sorted(x["ones"]))
        return

    radio_yt = {}
    official = json.loads((ROOT / "data/official-videos.json").read_text())["videos"]
    for vid, rec in official.items():
        if rec.get("official") and " - " in rec.get("song", ""):
            t, a = rec["song"].rsplit(" - ", 1)
            radio_yt[(norm(t), norm(a))] = vid

    song_slugs = {p.parent.name for p in (ROOT / "blog/songs").glob("*/index.html")}

    out = []
    for x in data:
        b = x["band"]
        year, rank, title = x["best"]
        yt = radio_yt.get((norm(title), norm(b)))
        t = html.escape(title)
        slug = next((sl for sl in song_slugs if norm(sl) == norm(title)
                     or norm(sl) == norm(b + title) or norm(sl) == norm(title + b)), None)
        song_cell = f'<a href="/blog/songs/{slug}/">{t}</a>' if slug else t
        band_cell = html.escape(b)
        if yt:
            play = (f'<button type="button" class="ohw-play" data-yt="{yt}" data-title="{t} by {html.escape(b)}" '
                    f'aria-label="Play {t} by {html.escape(b)} here">&#9654; Play</button>')
        else:
            play = ""
        out.append(
            f'<tr><td class="ohw-listen">{play}</td>'
            f'<td data-sort="{x["rank"]}">{x["rank"]}</td>'
            f'<td class="ohw-artist">{band_cell}</td>'
            f'<td data-sort="{x["count"]}">{x["count"]}</td>'
            f'<td data-sort="{x["n_ones"]}">{x["n_ones"]}</td>'
            f'<td data-sort="{x["weeks"]}">{x["weeks"]}</td>'
            f'<td class="ohw-song">{song_cell} <span class="table-note">({year}, year-end #{rank})</span></td></tr>'
        )

    page = PAGE.read_text(encoding="utf-8")
    if START not in page or END not in page:
        sys.exit(f"markers missing in {PAGE}")
    body = "\n".join("              " + line for line in out)
    new = re.sub(re.escape(START) + ".*?" + re.escape(END),
                 lambda m: START + "\n" + body + "\n              " + END, page, flags=re.S)
    PAGE.write_text(new, encoding="utf-8")
    print(f"{len(out)} bands, {sum('ohw-play' in r for r in out)} with in-page play")


if __name__ == "__main__":
    main()
