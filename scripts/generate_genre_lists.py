#!/usr/bin/env python3
"""Playable song lists for the genre pages that had none: folk rock, soft rock,
glam rock, progressive rock. Rows come from data/radio/radio-songs.json (songs on a
Year-End Hot 100, filtered by genre/subgenre tag, only rows with a YouTube ID) plus
data/billboard/hot100_weekly.json for the "#1 Hit" flag. Year-End Rank is the
year-end rank, never a peak. Same pattern and classes as generate_disco_table.py
(js/table-player.js, .ohw-*). Also applies the list-page layout rule (jump button,
collapsible TOC). Run generate_beyond_year_end.py after this one.

Run: python3 scripts/generate_genre_lists.py
"""
import html
import json

from genre_page_common import ROOT, norm, read, write, ensure_jump, ensure_toc_details, toc_set, put_block, \
    song_post_slug, play_button, ensure_scripts

START, END = "<!-- GENRE-LIST-START -->", "<!-- GENRE-LIST-END -->"


def sg(s):
    return (s.get("subgenre") or "").lower().replace("-", " ")


PAGES = {
    "blog/genres/70s-folk-rock/": dict(
        id="folk-rock-song-list", name="Folk Rock in the 70s", first_h2="what-counts",
        tag="folk rock or folk", pick=lambda s: sg(s) in ("folk rock", "folk"), label="folk rock", kw="folk rock in the 70s"),
    "blog/genres/70s-soft-rock/": dict(
        id="soft-rock-song-list", name="70s Soft Rock", first_h2="defining-the-sound",
        tag="soft rock", pick=lambda s: s["genre"] == "soft-rock", label="soft rock", kw="70s soft rock"),
    "blog/genres/glam-rock-in-the-70s/": dict(
        id="glam-rock-song-list", name="Glam Rock in the 70s", first_h2="what-counts",
        tag="glam rock", pick=lambda s: "glam" in sg(s), label="glam rock", kw="glam rock in the 70s"),
    "blog/genres/70s-progressive-rock/": dict(
        id="prog-rock-song-list", name="70s Progressive Rock", first_h2="what-counts",
        tag="progressive rock", pick=lambda s: s["genre"] == "prog-rock", label="progressive rock", kw="70s progressive rock"),
    "blog/genres/pop-songs-of-70s/": dict(
        id="pop-song-list", name="Pop Songs of 70s", first_h2="what-counts",
        tag="pop", pick=lambda s: s["genre"] == "pop", label="pop", kw="pop songs of 70s"),
    "blog/genres/70s-funk/": dict(
        id="funk-song-list", name="70s Funk", first_h2="what-counts",
        tag="funk", pick=lambda s: s["genre"] == "funk", label="funk", kw="70s funk"),
}


def main():
    radio = json.loads(read(ROOT / "data/radio/radio-songs.json"))
    weekly = json.loads(read(ROOT / "data/billboard/hot100_weekly.json"))
    number_ones = {(norm(w["title"]), norm(w["artist"])) for wk in weekly.values() for w in wk}
    song_slugs = {p.parent.name for p in (ROOT / "blog/songs").glob("*/index.html")}
    artist_slugs = {p.parent.name for p in (ROOT / "blog/artists").glob("*/index.html")}

    for rel, cfg in PAGES.items():
        songs = sorted((s for s in radio if cfg["pick"](s)), key=lambda s: (s["year"], s["rank"]))
        shown = [s for s in songs if s.get("youtube_id")]
        skipped = len(songs) - len(shown)
        rows, n1 = [], 0
        for s in shown:
            t, a = html.escape(s["title"]), html.escape(s["artist"])
            sslug = song_post_slug(s["title"], s["artist"], song_slugs)
            aslug = next((sl for sl in artist_slugs if norm(sl) == norm(s["artist"])), None)
            song_cell = f'<a href="/blog/songs/{sslug}/">{t}</a>' if sslug else t
            artist_cell = f'<a href="/blog/artists/{aslug}/">{a}</a>' if aslug else a
            is1 = (norm(s["title"]), norm(s["artist"])) in number_ones
            n1 += is1
            rows.append(f'              <tr><td class="ohw-listen">{play_button(s["youtube_id"], s["title"], s["artist"])}</td>'
                        f'<td class="ohw-song">{song_cell}</td><td class="ohw-artist">{artist_cell}</td>'
                        f'<td>{s["year"]}</td><td>{s["rank"]}</td><td>{"Yes" if is1 else ""}</td></tr>')
        years = f'{shown[0]["year"]} to {shown[-1]["year"]}'
        cap = (f'{len(shown)} {cfg["label"]} songs of the 70s, by year and Billboard Year-End Hot 100 rank, '
               'with weekly number ones marked')
        block = f'''        <h2 id="{cfg["id"]}">{cfg["name"]}: Play the Songs</h2>
        <p>Here are {len(shown)} {cfg["kw"]} songs from this site's Year-End Hot 100 data, from {years}.</p>
        <p>Each is tagged {cfg["tag"]}. Press Play on any row to watch it here, and tap a heading to sort.</p>

        <div class="data-table-wrap scroll-list">
          <table class="data-table sortable-table" id="{cfg["id"].replace("-song-list", "")}SongsTable" data-inline-player>
            <caption>{cap}</caption>
            <thead>
              <tr>
                <th><span class="visually-hidden">Play</span></th>
                <th><button type="button" data-col="1" data-type="text">Song</button></th>
                <th><button type="button" data-col="2" data-type="text">Artist</button></th>
                <th aria-sort="ascending"><button type="button" data-col="3" data-type="num">Year</button></th>
                <th><button type="button" data-col="4" data-type="num">Year-End Rank</button></th>
                <th><button type="button" data-col="5" data-type="text">#1 Hit</button></th>
              </tr>
            </thead>
            <tbody>
{chr(10).join(rows)}
            </tbody>
          </table>
        </div>
        <p>Year-End Rank is the song's spot on that year's Billboard Year-End Hot 100.</p>
        <p>That list keeps only the top 100 songs of each year.</p>
        <p>The #1 Hit column marks songs that also reached number one on the weekly chart.</p>'''
        path = ROOT / rel / "index.html"
        page = read(path)
        page = ensure_jump(page, "#" + cfg["id"])
        page = ensure_toc_details(page)
        page = toc_set(page, cfg["id"], f'{cfg["name"]}: Play the Songs')
        page = put_block(page, START, END, block, f'<h2 id="{cfg["first_h2"]}">')
        page = ensure_scripts(page)
        write(path, page)
        print(f"{rel}: {len(shown)} rows ({skipped} without a video skipped), {n1} #1 hits")


if __name__ == "__main__":
    main()
