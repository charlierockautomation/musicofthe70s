#!/usr/bin/env python3
"""Rock hub additions for /blog/genres/70s-rock/ (additive, existing copy untouched):
a subgenre guide linking every rock list page, a short playable teaser (18 songs from
data/radio/radio-songs.json: rock-tagged songs with a YouTube ID, one per artist, best
weekly peak first, pop-leaning subgenre tags skipped), and a Sources block.
Peak comes from the radio data's billboard_peak; Year-End Rank is the year-end rank only.

Run: python3 scripts/generate_rock_hub.py   (then generate_beyond_year_end.py)
"""
import html
import json

from genre_page_common import ROOT, norm, read, write, ensure_jump, toc_set, put_block, song_post_slug, play_button, ensure_scripts

REL = "blog/genres/70s-rock/"
SUB_START, SUB_END = "<!-- ROCK-SUBGENRES-START -->", "<!-- ROCK-SUBGENRES-END -->"
LIST_START, LIST_END = "<!-- ROCK-TEASER-START -->", "<!-- ROCK-TEASER-END -->"
SRC_START, SRC_END = "<!-- ROCK-SOURCES-START -->", "<!-- ROCK-SOURCES-END -->"
SKIP = {"pop", "ballad", "pop-rock", "pop rock", "power-pop", "power pop", "soft rock", "soft-rock", "blue-eyed-soul",
        "baroque pop", "comedy rock", "rnb-rock", "soul rock", "progressive-pop"}
N = 18

SUBS = [  # slug, label, one-line description, genre tags counted for the song total
    ("70s-hard-rock", "Hard Rock", "Heavy riffs and loud guitars: Grand Funk Railroad, Edgar Winter, Sweet."),
    ("70s-progressive-rock", "Progressive Rock", "Long forms and studio ambition: Queen, Supertramp, ELO."),
    ("70s-soft-rock", "Soft Rock", "Melody, harmony and acoustic color that ruled mid-70s radio."),
    ("glam-rock-in-the-70s", "Glam Rock", "Costume, swagger and hooks: Sweet, David Essex, Elton John."),
    ("70s-punk-rock", "Punk Rock", "The stripped-down reaction that closed out the decade."),
    ("70s-folk-rock", "Folk Rock", "Acoustic roots plugged in, from Don McLean to Rod Stewart."),
    ("70s-country-rock", "Country Rock", "Where Nashville met the Sunset Strip: Eagles, Linda Ronstadt."),
]
SOURCES = [
    ("https://en.wikipedia.org/wiki/Rock_music", "Wikipedia: Rock music", "for the overall history of the genre."),
    ("https://en.wikipedia.org/wiki/Hard_rock", "Wikipedia: Hard rock", "for the heavier side of 70s rock."),
    ("https://en.wikipedia.org/wiki/Progressive_rock", "Wikipedia: Progressive rock", "for the prog movement and its major acts."),
    ("https://en.wikipedia.org/wiki/Punk_rock", "Wikipedia: Punk rock", "for the punk breakout of 1976 and 1977."),
]


def main():
    radio = json.loads(read(ROOT / "data/radio/radio-songs.json"))
    weekly = json.loads(read(ROOT / "data/billboard/hot100_weekly.json"))
    number_ones = {(norm(w["title"]), norm(w["artist"])) for wk in weekly.values() for w in wk}
    song_slugs = {p.parent.name for p in (ROOT / "blog/songs").glob("*/index.html")}
    artist_slugs = {p.parent.name for p in (ROOT / "blog/artists").glob("*/index.html")}

    pool = [s for s in radio if s["genre"] in ("classic-rock", "hard-rock", "prog-rock") and s.get("youtube_id")
            and (s.get("subgenre") or "") not in SKIP]
    pool.sort(key=lambda s: (s["billboard_peak"], s["rank"]))
    seen, pick = set(), []
    for s in pool:
        if s["artist"] not in seen:
            seen.add(s["artist"])
            pick.append(s)
    pick = sorted(pick[:N], key=lambda s: (s["year"], s["rank"]))

    rows = []
    for s in pick:
        t, a = html.escape(s["title"]), html.escape(s["artist"])
        sslug = song_post_slug(s["title"], s["artist"], song_slugs)
        aslug = next((sl for sl in artist_slugs if norm(sl) == norm(s["artist"])), None)
        song_cell = f'<a href="/blog/songs/{sslug}/">{t}</a>' if sslug else t
        artist_cell = f'<a href="/blog/artists/{aslug}/">{a}</a>' if aslug else a
        is1 = (norm(s["title"]), norm(s["artist"])) in number_ones
        rows.append(f'              <tr><td class="ohw-listen">{play_button(s["youtube_id"], s["title"], s["artist"])}</td>'
                    f'<td class="ohw-song">{song_cell}</td><td class="ohw-artist">{artist_cell}</td>'
                    f'<td>{s["year"]}</td><td>{s["rank"]}</td><td>{"Yes" if is1 else ""}</td></tr>')

    sub_rows = "\n".join(
        f'              <tr><td><a href="/blog/genres/{slug}/">{label}</a></td><td>{desc}</td></tr>' for slug, label, desc in SUBS)
    sub_block = f'''        <h2 id="rock-subgenres">Every 70s Rock Subgenre, Page by Page</h2>
        <p>Each sound above has its own page with a full playable song list.</p>
        <div class="data-table-wrap">
          <table class="data-table">
            <caption>The seven 70s rock subgenre pages on this site</caption>
            <thead>
              <tr><th>Subgenre page</th><th>What you will find</th></tr>
            </thead>
            <tbody>
{sub_rows}
            </tbody>
          </table>
        </div>
        <p>Start with the one that matches the sound you want to hear.</p>'''

    list_block = f'''        <h2 id="rock-song-teaser">Play 70s Rock: {len(pick)} Songs to Start With</h2>
        <p>These {len(pick)} rock songs come from this site's Year-End Hot 100 data, one per artist.</p>
        <p>They are the rock-tagged songs with the best weekly Hot 100 peaks, shown in year order.</p>
        <p>Press Play on any row to watch it here, and tap a heading to sort.</p>
        <div class="data-table-wrap scroll-list">
          <table class="data-table sortable-table" id="rockTeaserTable" data-inline-player>
            <caption>{len(pick)} rock songs of the 70s, by year and Billboard Year-End Hot 100 rank, with weekly number ones marked</caption>
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
        <p>The #1 Hit column marks songs that also reached number one on the weekly chart.</p>
        <p>For longer lists, use the subgenre pages in the guide above.</p>'''

    src_items = "\n".join(f'          <li><a href="{u}" rel="noopener">{t}</a> {d}</li>' for u, t, d in SOURCES)
    src_block = f'''        <h2 id="sources">Sources</h2>
        <p>The chart counts and ranks come from this site's own Billboard data, described on the <a href="/about/methodology/">methodology page</a>.</p>
        <p>Background on the genre can be checked against these outside sources:</p>
        <ul>
{src_items}
        </ul>'''

    path = ROOT / REL / "index.html"
    page = read(path)
    page = ensure_jump(page, "#rock-song-teaser")
    page = put_block(page, SUB_START, SUB_END, sub_block, '<section class="faq-block" id="faq">')
    page = put_block(page, LIST_START, LIST_END, list_block, '<section class="faq-block" id="faq">')
    page = put_block(page, SRC_START, SRC_END, src_block, '<section class="faq-block" id="faq">')
    page = toc_set(page, "rock-subgenres", "Every 70s Rock Subgenre, Page by Page", after_id="great-schism")
    page = toc_set(page, "rock-song-teaser", f"Play 70s Rock: {len(pick)} Songs to Start With", after_id="rock-subgenres")
    page = toc_set(page, "sources", "Sources", after_id="rock-song-teaser")
    page = ensure_scripts(page)
    write(path, page)
    print(f"{REL}: {len(pick)} teaser rows, {sum('Yes</td>' in r for r in rows)} #1 hits")
    for s in pick:
        print(" ", s["year"], s["rank"], s["billboard_peak"], s["title"], "-", s["artist"])


if __name__ == "__main__":
    main()
