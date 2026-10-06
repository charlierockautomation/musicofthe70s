#!/usr/bin/env python3
"""
Build the sortable ranking on /blog/artists/70s-singers/ from
data/billboard/year_end_hot100.json and data/billboard/hot100_weekly.json,
the same way the other generators work: the data on disk is the source
of truth.

Who counts: solo singers only (groups are a separate page). SINGERS
below is the hand-checked list of every individual act with 3 or more
solo credits on the 1970-1979 year-end Hot 100 in this site's data.

Counting call (stated on the page too):
- Only credits under the singer's own name count toward the ranking.
- Duets with another named singer ("Elton John & Kiki Dee") are shown
  in their own table on the page, not counted.
- Singer-plus-band credits ("Paul McCartney & Wings", "Gladys Knight &
  the Pips") are group records and are not counted.
- Alice Cooper was a band name until 1975; "School's Out" (1972) is the
  band's record and is not counted, the four 1975-1979 solo hits are.
- "Elton John Band" on the weekly #1 file ("Philadelphia Freedom") is
  counted as Elton John, matching the year-end file's own credit.

Ranking: solo year-end entries, ties broken by chart points (101 minus
year-end rank, summed over every entry).

Each row's biggest hit gets a Play button when the song is in
data/radio/radio-songs.json with a YouTube ID (js/table-player.js opens
the video under the row, checking data/youtube-status.json first).

Rewrites the block between <!-- SINGERS-START --> and <!-- SINGERS-END -->.

Run: python3 scripts/generate_70s_singers_table.py [--stats]
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "blog/artists/70s-singers/index.html"
START, END = "<!-- SINGERS-START -->", "<!-- SINGERS-END -->"

SINGERS = [
    "Elton John", "Stevie Wonder", "Barry Manilow", "Olivia Newton-John",
    "Helen Reddy", "Anne Murray", "John Denver", "Al Green", "Diana Ross",
    "Aretha Franklin", "Cher", "Ringo Starr", "Carly Simon", "Paul Simon",
    "Linda Ronstadt", "Donna Summer", "Andy Gibb", "Alice Cooper",
    "B.J. Thomas", "James Taylor", "Glen Campbell", "Rod Stewart",
    "Donny Osmond", "Marvin Gaye", "Jim Croce", "Barbra Streisand",
    "Leo Sayer", "Ray Stevens", "Neil Diamond", "Elvis Presley",
    "Bill Withers", "Cat Stevens", "Roberta Flack", "Gilbert O'Sullivan",
    "Michael Jackson", "Billy Preston", "Joe Simon", "Barry White",
    "Eddie Kendricks", "Charlie Rich", "David Bowie", "Jim Stafford",
    "Eric Clapton", "Frankie Valli", "Neil Sedaka", "Peter Frampton",
    "Kenny Rogers", "Shaun Cassidy",
]
# weekly-file spellings that mean the same solo credit
WEEKLY_ALIAS = {"Elton John Band": "Elton John", "B. J. Thomas": "B.J. Thomas"}
# year-end entries that are not the solo singer's own record
EXCLUDE = {("Alice Cooper", "School's Out")}

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
            a = WEEKLY_ALIAS.get(r["artist"], r["artist"])
            if a in rows:
                rows[a]["ones"][r["title"]] = rows[a]["ones"].get(r["title"], 0) + 1
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


def duets(singers):
    ye = json.loads((ROOT / "data/billboard/year_end_hot100.json").read_text())
    res = []
    for year, recs in ye.items():
        for r in recs:
            a = r["artist"]
            if a in singers:
                continue
            if any(s in a for s in singers) and re.search(r" & | and ", a):
                res.append((int(year), r["rank"], r["title"], a))
    return sorted(res)


def main():
    data = build()
    if "--stats" in sys.argv:
        for x in data:
            print(x["rank"], x["singer"], x["count"], x["points"], x["best"], x["years"],
                  x["n_ones"], x["weeks"], sorted(x["ones"]))
        for d in duets(set(SINGERS)):
            print("DUET", d)
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
            f'<td class="ohw-song">{song_cell} <span class="table-note">({year}, year-end #{rank})</span></td></tr>'
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
