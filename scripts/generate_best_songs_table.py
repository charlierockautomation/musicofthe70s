#!/usr/bin/env python3
"""Build the 100-song sortable ranking on /blog/songs/best-songs-of-the-70s/
from data/billboard/year_end_hot100.json, the same way the other table
generators work: the data on disk is the source of truth.

Selection: the top 10 songs of each year-end Hot 100, 1970-1979 (ranks 1-10),
100 songs total. Chart position decides the list, not critic opinion --
the site's point of difference from the opinion-ranking lists (Paste,
Forbes, Ultimate Classic Rock) that already rank for this keyword.

Default order is chronological (year ascending, then rank ascending within
year), matching the era-by-era narrative already on the page.

Each row gets a Play button when the song is in data/radio/radio-songs.json
with a YouTube ID (js/table-player.js, .ohw-* classes, same script already
used on the Artists flagship pages), and links to its Songs/Artists post
when one exists.

Rewrites the block between <!-- BEST100-START --> and <!-- BEST100-END -->.

Run: python3 scripts/generate_best_songs_table.py
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "blog/songs/best-songs-of-the-70s/index.html"
START, END = "<!-- BEST100-START -->", "<!-- BEST100-END -->"


def norm(s):
    s = s.lower().replace("&", "and")
    s = re.sub(r"\(.*?\)", "", s)
    return re.sub(r"[^a-z0-9]+", "", s)


def main():
    ye = json.loads((ROOT / "data/billboard/year_end_hot100.json").read_text())
    radio = json.loads((ROOT / "data/radio/radio-songs.json").read_text())
    radio_yt = {}
    for s in radio:
        radio_yt.setdefault((norm(s["title"]), norm(s["artist"])), s.get("youtube_id"))

    song_slugs = {p.parent.name for p in (ROOT / "blog/songs").glob("*/index.html")}
    artist_slugs = {p.parent.name for p in (ROOT / "blog/artists").glob("*/index.html")}

    rows = []
    for year in sorted(ye):
        for r in sorted(ye[year], key=lambda r: r["rank"]):
            if r["rank"] <= 10:
                rows.append({"year": int(year), "rank": r["rank"], "title": r["title"], "artist": r["artist"]})

    out, n_play, n_song_post, n_artist_post = [], 0, 0, 0
    for r in rows:
        t, a = html.escape(r["title"]), html.escape(r["artist"])
        yt = radio_yt.get((norm(r["title"]), norm(r["artist"])))
        if yt:
            play = (f'<button type="button" class="ohw-play" data-yt="{yt}" data-title="{t} by {a}" '
                    f'aria-label="Play {t} by {a} here">&#9654; Play</button>')
            n_play += 1
        else:
            play = ""
        sslug = next((sl for sl in song_slugs if norm(sl) == norm(r["title"])
                      or norm(sl) == norm(r["artist"] + r["title"]) or norm(sl) == norm(r["title"] + r["artist"])), None)
        song_cell = f'<a href="/blog/songs/{sslug}/">{t}</a>' if sslug else t
        n_song_post += bool(sslug)
        aslug = next((sl for sl in artist_slugs if norm(sl) == norm(r["artist"])), None)
        artist_cell = f'<a href="/blog/artists/{aslug}/">{a}</a>' if aslug else a
        n_artist_post += bool(aslug)
        out.append(
            f'<tr><td class="ohw-listen">{play}</td>'
            f'<td class="ohw-song">{song_cell}</td><td class="ohw-artist">{artist_cell}</td>'
            f'<td>{r["year"]}</td><td>{r["rank"]}</td></tr>'
        )

    page = PAGE.read_text(encoding="utf-8")
    if START not in page or END not in page:
        sys.exit(f"markers missing in {PAGE}")
    body = "\n".join("              " + line for line in out)
    new = re.sub(re.escape(START) + ".*?" + re.escape(END), START + "\n" + body + "\n              " + END, page, flags=re.S)
    PAGE.write_text(new, encoding="utf-8")
    print(f"{len(out)} songs, {n_play} with play links, {n_song_post} with Songs posts, {n_artist_post} with Artists posts")


if __name__ == "__main__":
    main()
