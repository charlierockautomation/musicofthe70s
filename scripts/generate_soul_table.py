#!/usr/bin/env python3
"""Build the playable soul song list on /blog/genres/70s-soul-music/
from data/radio/radio-songs.json (every song tagged genre "soul" that has
a YouTube ID) plus data/billboard/hot100_weekly.json for the "#1" flag.

Same pattern as generate_best_songs_table.py (js/table-player.js, .ohw-*
classes). Rewrites the block between <!-- SOUL-START --> and <!-- SOUL-END -->.

Run: python3 scripts/generate_disco_table.py
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "blog/genres/70s-soul-music/index.html"
START, END = "<!-- SOUL-START -->", "<!-- SOUL-END -->"


def norm(s):
    s = s.lower().replace("&", "and")
    s = re.sub(r"\(.*?\)", "", s)
    return re.sub(r"[^a-z0-9]+", "", s)


SONG_POSTS = {  # (title, artist) -> live /blog/songs/ slug; artist is checked so covers never link
    (norm(t), norm(a)): sl for t, a, sl in [
        ("Tired of Being Alone", "Al Green", "al-green-tired-of-being-alone"),
        ("Let's Stay Together", "Al Green", "al-green-lets-stay-together"),
        ("What's Going On", "Marvin Gaye", "whats-going-on-marvin-gaye"),
        ("Let's Get It On", "Marvin Gaye", "marvin-gaye-lets-get-it-on"),
        ("You Are the Sunshine of My Life", "Stevie Wonder", "you-are-the-sunshine-of-my-life"),
        ("Living for the City", "Stevie Wonder", "living-for-the-city"),
        ("Sir Duke", "Stevie Wonder", "sir-duke-stevie-wonder"),
    ]}


def main():
    radio = json.loads((ROOT / "data/radio/radio-songs.json").read_text())
    weekly = json.loads((ROOT / "data/billboard/hot100_weekly.json").read_text())
    number_ones = {(norm(w["title"]), norm(w["artist"])) for wk in weekly.values() for w in wk}
    songs = sorted((s for s in radio if s["genre"] == "soul" and s.get("youtube_id")), key=lambda s: (s["year"], s["rank"]))
    song_slugs = {p.parent.name for p in (ROOT / "blog/songs").glob("*/index.html")}
    artist_slugs = {p.parent.name for p in (ROOT / "blog/artists").glob("*/index.html")}

    out, n_play, n_no1 = [], 0, 0
    for s in songs:
        t, a = html.escape(s["title"]), html.escape(s["artist"])
        play = (f'<button type="button" class="ohw-play" data-yt="{s["youtube_id"]}" data-title="{t} by {a}" '
                f'aria-label="Play {t} by {a} here">&#9654; Play</button>')
        n_play += 1
        sslug = SONG_POSTS.get((norm(s["title"]), norm(s["artist"])))
        if sslug and sslug not in song_slugs:
            sys.exit(f"song post missing: {sslug}")
        song_cell = f'<a href="/blog/songs/{sslug}/">{t}</a>' if sslug else t
        aslug = next((sl for sl in artist_slugs if norm(sl) == norm(s["artist"])), None)
        artist_cell = f'<a href="/blog/artists/{aslug}/">{a}</a>' if aslug else a
        is1 = (norm(s["title"]), norm(s["artist"])) in number_ones
        n_no1 += is1
        out.append(
            f'<tr><td class="ohw-listen">{play}</td><td class="ohw-song">{song_cell}</td>'
            f'<td class="ohw-artist">{artist_cell}</td><td>{s["year"]}</td><td>{s["rank"]}</td>'
            f'<td>{"Yes" if is1 else ""}</td></tr>'
        )

    page = PAGE.read_text(encoding="utf-8")
    if START not in page or END not in page:
        sys.exit(f"markers missing in {PAGE}")
    body = "\n".join("              " + line for line in out)
    new = re.sub(re.escape(START) + ".*?" + re.escape(END), lambda m: START + "\n" + body + "\n              " + END, page, flags=re.S)
    PAGE.write_text(new, encoding="utf-8")
    print(f"{len(out)} songs, {n_play} with play links, {n_no1} reached #1")


if __name__ == "__main__":
    main()
