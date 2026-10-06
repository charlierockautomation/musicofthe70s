#!/usr/bin/env python3
"""Build the playable year-end list on each /blog/years/top-songs-of-YYYY/ page
from data/billboard/year_end_hot100.json (all 100 songs), joined to
data/radio/radio-songs.json on (year, rank) for the YouTube ID.

Same pattern as generate_best_songs_table.py (js/table-player.js, .ohw-* classes).
"#1 Hit" is "Yes" only when the song reached number one on the weekly Hot 100
per data/billboard/hot100_weekly.json (title + artist match, any year). The rank
column is the Year-End Hot 100 position, NOT a weekly peak.

A row with no verified video ID gets no Play button and is reported; IDs are
never guessed. Rewrites the block between <!-- YEAR-LIST-START --> and
<!-- YEAR-LIST-END -->.

Run: python3 scripts/generate_year_table.py [YYYY ...]   (default: all ten years)
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
START, END = "<!-- YEAR-LIST-START -->", "<!-- YEAR-LIST-END -->"


def norm(s):
    s = s.lower().replace("&", "and")
    s = re.sub(r"\(.*?\)", "", s)
    return re.sub(r"[^a-z0-9]+", "", s)


def title_parts(t):
    return {norm(x) for x in re.split(r"\s/\s", t) if norm(x)}


def artist_tokens(a):
    stop = {"the", "and", "featuring", "band", "a", "of"}
    return {x for x in re.split(r"[^a-z0-9]+", a.lower().replace("&", " ")) if x and x not in stop}


def main():
    years = sys.argv[1:] or [str(y) for y in range(1970, 1980)]
    ye = json.loads((ROOT / "data/billboard/year_end_hot100.json").read_text())
    radio = json.loads((ROOT / "data/radio/radio-songs.json").read_text())
    by_rank = {(str(s["year"]), s["rank"]): s for s in radio}
    weekly = json.loads((ROOT / "data/billboard/hot100_weekly.json").read_text())
    number_ones = {(w["title"], w["artist"]) for wk in weekly.values() for w in wk}

    def reached_number_one(title, artist):
        tp, at = title_parts(title), artist_tokens(artist)
        return any(tp & title_parts(t) and at & artist_tokens(a) for t, a in number_ones)

    song_slugs = {p.parent.name for p in (ROOT / "blog/songs").glob("*/index.html")}
    artist_slugs = {p.parent.name for p in (ROOT / "blog/artists").glob("*/index.html")}

    for year in years:
        rows, out, n_play, n_no1, missing = ye[year], [], 0, 0, []
        for r in sorted(rows, key=lambda r: r["rank"]):
            s = by_rank[(year, r["rank"])]
            if norm(s["title"]) != norm(r["title"]) or norm(s["artist"]) != norm(r["artist"]):
                sys.exit(f"{year} #{r['rank']}: radio-songs row does not match year-end row: {s['title']} / {r['title']}")
            t, a = html.escape(r["title"]), html.escape(r["artist"])
            yt = s.get("youtube_id")
            if yt:
                play = (f'<button type="button" class="ohw-play" data-yt="{yt}" data-title="{t} by {a}" '
                        f'aria-label="Play {t} by {a} here">&#9654; Play</button>')
                n_play += 1
            else:
                play = ""
                missing.append(f"#{r['rank']} {r['title']} - {r['artist']}")
            sslug = next((sl for sl in song_slugs if norm(sl) in (norm(r["title"]), norm(r["artist"] + r["title"]),
                                                                   norm(r["title"] + r["artist"]))), None)
            song_cell = f'<a href="/blog/songs/{sslug}/">{t}</a>' if sslug else t
            aslug = next((sl for sl in artist_slugs if norm(sl) == norm(r["artist"])), None)
            artist_cell = f'<a href="/blog/artists/{aslug}/">{a}</a>' if aslug else a
            is1 = reached_number_one(r["title"], r["artist"])
            n_no1 += is1
            out.append(f'<tr><td class="ohw-listen">{play}</td><td class="ohw-song">{song_cell}</td>'
                       f'<td class="ohw-artist">{artist_cell}</td><td>{r["rank"]}</td><td>{"Yes" if is1 else ""}</td></tr>')
        page_path = ROOT / f"blog/years/top-songs-of-{year}/index.html"
        page = page_path.read_text(encoding="utf-8")
        if START not in page or END not in page:
            sys.exit(f"markers missing in {page_path}")
        body = "\n".join("              " + line for line in out)
        new = re.sub(re.escape(START) + ".*?" + re.escape(END),
                     lambda m: START + "\n" + body + "\n              " + END, page, flags=re.S)
        page_path.write_text(new, encoding="utf-8")
        print(f"{year}: {len(out)} songs, {n_play} with Play, {n_no1} reached #1" + (f"; NO PLAY: {missing}" if missing else ""))


if __name__ == "__main__":
    main()
