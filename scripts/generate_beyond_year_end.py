#!/usr/bin/env python3
"""Build the "Beyond the year-end list" section on each genre page from
data/billboard/beyond_year_end.json: songs that charted on the weekly Hot 100 but are
not on any 1970-1979 Year-End Hot 100. Peaks are WEEKLY peaks from Wikipedia (linked
per row); they are never shown as year-end ranks and the column is "Weekly Peak".
Rewrites the block between <!-- BEYOND-START --> and <!-- BEYOND-END -->, adds the TOC
entry, and loads the in-page player. Run generate_genre_lists.py first (it places the
full list ahead of this block).

Run: python3 scripts/generate_beyond_year_end.py
"""
import html
import json

from genre_page_common import ROOT, read, write, toc_set, put_block, play_button, ensure_scripts, ensure_toc_details, ensure_jump

START, END = "<!-- BEYOND-START -->", "<!-- BEYOND-END -->"
ID = "beyond-year-end"

# page -> (label used in text, page focus keyword, H2 id the block goes before,
#          TOC entry the new entry follows (None = first))
PAGES = {
    "blog/genres/70s-folk-rock/": ("folk rock", "Folk Rock in the 70s", "what-counts", "folk-rock-song-list"),
    "blog/genres/70s-soft-rock/": ("soft rock", "70s Soft Rock", "defining-the-sound", "soft-rock-song-list"),
    "blog/genres/glam-rock-in-the-70s/": ("glam rock", "Glam Rock in the 70s", "what-counts", "glam-rock-song-list"),
    "blog/genres/70s-progressive-rock/": ("progressive rock", "70s Progressive Rock", "what-counts", "prog-rock-song-list"),
    "blog/genres/70s-punk-rock/": ("punk and new wave", "70s Punk Rock", "what-counts", None),
    "blog/genres/disco-music-of-the-70s/": ("disco", "70s Disco Music", "short-answer", "disco-song-list"),
    "blog/genres/70s-soul-music/": ("soul", "70s Soul Music", "short-answer", "soul-song-list"),
}


def main():
    doc = json.loads(read(ROOT / "data/billboard/beyond_year_end.json"))
    for rel, (label, kw, anchor, after) in PAGES.items():
        songs = sorted((s for s in doc["songs"] if s["page"] == rel), key=lambda s: (s["released"], s["weekly_peak"]))
        has_style = any("tag" in s for s in songs)
        rows = []
        for s in songs:
            t, a = html.escape(s["title"]), html.escape(s["artist"])
            style = f'<td>{s["tag"]}</td>' if has_style else ""
            rows.append(f'              <tr><td class="ohw-listen">{play_button(s["youtube_id"], s["title"], s["artist"])}</td>'
                        f'<td class="ohw-song">{t}</td><td class="ohw-artist">{a}</td><td>{s["released"]}</td>'
                        f'<td>{s["weekly_peak"]}</td>{style}'
                        f'<td><a href="{s["wikipedia_url"]}" rel="noopener">Wikipedia</a></td></tr>')
        style_th = '<th><button type="button" data-col="5" data-type="text">Style</button></th>\n                ' if has_style else ""
        n = len(songs)
        block = f'''        <h2 id="{ID}">Beyond the Year-End List: {kw} Hits the Top 100 Left Out</h2>
        <p>The Year-End Hot 100 keeps only each year's 100 biggest songs.</p>
        <p>Plenty of weekly Hot 100 hits never made it onto that list, including these {n} picks for {kw.lower()}.</p>
        <p>None is on any 1970 to 1979 year-end top 100, and all {n} charted weekly.</p>

        <div class="data-table-wrap scroll-list">
          <table class="data-table sortable-table" id="beyondYearEndTable" data-inline-player>
            <caption>{n} {label} songs that charted weekly but missed the year-end top 100, by release year and weekly Hot 100 peak</caption>
            <thead>
              <tr>
                <th><span class="visually-hidden">Play</span></th>
                <th><button type="button" data-col="1" data-type="text">Song</button></th>
                <th><button type="button" data-col="2" data-type="text">Artist</button></th>
                <th aria-sort="ascending"><button type="button" data-col="3" data-type="num">Released</button></th>
                <th><button type="button" data-col="4" data-type="num">Weekly Peak</button></th>
                {style_th}<th>Source</th>
              </tr>
            </thead>
            <tbody>
{chr(10).join(rows)}
            </tbody>
          </table>
        </div>
        <p>Weekly Peak is each song's best spot on the weekly Billboard Hot 100.</p>
        <p>Each peak comes from the song's own linked Wikipedia article.</p>
        <p>None of these songs is ranked on a year-end list, so the table shows no Year-End Rank.</p>'''
        path = ROOT / rel / "index.html"
        page = read(path)
        if after is None:
            page = ensure_jump(page, "#" + ID)
            page = ensure_toc_details(page)
        page = toc_set(page, ID, f'Beyond the Year-End List: {kw} Hits the Top 100 Left Out', after_id=after)
        page = put_block(page, START, END, block, f'<h2 id="{anchor}">')
        page = ensure_scripts(page)
        write(path, page)
        print(f"{rel}: {n} beyond-year-end rows")


if __name__ == "__main__":
    main()
