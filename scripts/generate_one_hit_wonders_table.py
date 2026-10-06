#!/usr/bin/env python3
"""
Build the sortable table on /blog/songs/70s-one-hit-wonders/ from
data/billboard/one_hit_wonders_70s.json, the same way the other
generators work: the data on disk is the source of truth.

That JSON file is itself derived data (see its _methodology field):
every act with exactly one entry in data/billboard/year_end_hot100.json
for 1970-1979, cross-checked against Wikipedia's "List of one-hit
wonders in the United States" (1970s section), then individually
verified against each act's full Billboard Hot 100 chart history
(any other Hot 100 entry peaking 1-40, any year, disqualifies).

Each row gets a Play button when the song is in
data/radio/radio-songs.json with a YouTube ID (js/one-hit-wonder-player.js
opens the video under the row, checking data/youtube-status.json first),
and links to its Songs post when one exists.

Rewrites the block between <!-- OHW-START --> and <!-- OHW-END --> in
the page.

Run: python3 scripts/generate_one_hit_wonders_table.py
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "blog/songs/70s-one-hit-wonders/index.html"
START, END = "<!-- OHW-START -->", "<!-- OHW-END -->"


def norm(s):
    s = s.lower().replace("&", "and")
    s = re.sub(r"\(.*?\)", "", s)
    return re.sub(r"[^a-z0-9]+", "", s)


def main():
    data = json.loads((ROOT / "data/billboard/one_hit_wonders_70s.json").read_text())
    acts = data["acts"]

    radio = json.loads((ROOT / "data/radio/radio-songs.json").read_text())
    radio_by_song = {}
    radio_yt = {x["radio_id"]: x.get("youtube_id") for x in radio}
    for s in radio:
        radio_by_song.setdefault((norm(s["title"]), norm(s["artist"])), s["radio_id"])
        radio_by_song.setdefault((norm(s["title"]), ""), s["radio_id"])

    song_slugs = sorted(p.parent.name for p in (ROOT / "blog/songs").glob("*/index.html")
                        if p.parent.name != PAGE.parent.name)
    post_titles = {}
    for sl in song_slugs:
        page_html = (ROOT / "blog/songs" / sl / "index.html").read_text(encoding="utf-8")
        head = re.search(r"<title>([^<]*)</title>", page_html)
        desc = re.search(r'<meta name="description" content="([^"]*)"', page_html)
        intro = re.findall(r'<p class="post-intro">(.*?)</p>', page_html)
        post_titles[sl] = norm(html.unescape(" ".join(
            [head.group(1) if head else "", desc.group(1) if desc else ""] + intro)))

    out, n_radio, n_play, n_post = [], 0, 0, 0
    for a in acts:
        artist, title = a["artist"], a["song"]
        key = (norm(title), norm(artist))
        rid = radio_by_song.get(key) or radio_by_song.get((norm(title), ""))
        if rid and key not in radio_by_song:
            match = next(s for s in radio if s["radio_id"] == rid)
            if norm(artist)[:5] not in norm(match["artist"]) and norm(match["artist"])[:5] not in norm(artist):
                rid = None
        nt = norm(title.split(" / ")[0])
        by_artist = lambda sl: norm(artist).split("and")[0][:5] in post_titles[sl]
        slug = next((sl for sl in song_slugs if (norm(sl) == nt or (len(nt) >= 8 and nt in norm(sl)))
                     and by_artist(sl)), None)
        post = f"/blog/songs/{slug}/" if slug else None
        t = html.escape(title)
        song_cell = f'<a href="{post}">{t}</a>' if post else t
        yt = radio_yt.get(rid) if rid else None
        if yt:
            play_cell = (f'<button type="button" class="ohw-play" data-yt="{yt}" '
                         f'aria-label="Play {t} here">&#9654; Play</button>')
        elif rid:
            play_cell = f'<a href="/radio/?play={rid}" aria-label="Find {t} on Listen Now">Listen Now</a>'
        else:
            play_cell = ""
        n_radio += bool(rid)
        n_play += bool(yt)
        n_post += bool(post)
        artist_esc = html.escape(artist)
        out.append(
            f'<tr><td class="ohw-listen">{play_cell}</td>'
            f'<td class="ohw-song">{song_cell}</td><td class="ohw-artist">{artist_esc}</td>'
            f'<td data-sort="{a["year_end_year"]}">{a["year_end_year"]}</td>'
            f'<td data-sort="{a["year_end_rank"]}">{a["year_end_rank"]}</td></tr>'
        )

    page = PAGE.read_text(encoding="utf-8")
    if START not in page or END not in page:
        sys.exit(f"markers missing in {PAGE}")
    body = "\n".join("              " + line for line in out)
    new = re.sub(re.escape(START) + ".*?" + re.escape(END), START + "\n" + body + "\n              " + END, page, flags=re.S)
    PAGE.write_text(new, encoding="utf-8")
    print(f"{len(out)} acts, {n_play} with Play buttons, {n_post} with Songs posts")


if __name__ == "__main__":
    main()
