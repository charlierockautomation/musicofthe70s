#!/usr/bin/env python3
"""
Build the "every number one" table on /blog/songs/70s-number-one-hits/
from data/billboard/hot100_weekly.json, the same way the other
generators work: the data on disk is the source of truth.

One row per song (253), in order of its first week at number one.
Weeks at #1 are counted from the weekly rows, NOT the file's
weeks_at_number_one field: that field disagrees with the rows for 9
songs (e.g. Superstition says 2, the chart shows 1 week).

Each row links to the song's Listen Now tile when the song is in
data/radio/radio-songs.json, and to its Songs post when one exists
(found through the /radio/?play=<radio_id> link every Songs post carries).

Rewrites the block between <!-- NUMBER-ONES-START --> and
<!-- NUMBER-ONES-END --> in the page.

Run: python3 scripts/generate_number_one_table.py
"""
import html
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "blog/songs/70s-number-one-hits/index.html"
START, END = "<!-- NUMBER-ONES-START -->", "<!-- NUMBER-ONES-END -->"


def norm(s):
    s = s.lower().replace("&", "and")
    s = re.sub(r"\(.*?\)", "", s)
    return re.sub(r"[^a-z0-9]+", "", s)


def main():
    weekly = json.loads((ROOT / "data/billboard/hot100_weekly.json").read_text())
    rows = [r for y in sorted(weekly) for r in weekly[y]]

    radio = json.loads((ROOT / "data/radio/radio-songs.json").read_text())
    radio_by_song = {}
    for s in radio:
        radio_by_song.setdefault((norm(s["title"]), norm(s["artist"])), s["radio_id"])
        radio_by_song.setdefault((norm(s["title"]), ""), s["radio_id"])

    # A Songs post counts as "the" post for a song only when its slug
    # contains the song title, so roundups like Best Songs of the 70s
    # (which also carry play links) don't get linked from every row.
    post_by_radio = {}
    for post in (ROOT / "blog/songs").glob("*/index.html"):
        for rid in set(re.findall(r'href="/radio/\?play=([^"]+)"', post.read_text(encoding="utf-8"))):
            post_by_radio.setdefault(rid, []).append(post.parent.name)

    song_slugs = sorted(p.parent.name for p in (ROOT / "blog/songs").glob("*/index.html")
                        if p.parent.name != PAGE.parent.name)
    # Each post's title, meta description and intro, normalised, to confirm the artist matches too
    # (two different songs called Best of My Love were number ones).
    post_titles = {}
    for sl in song_slugs:
        page_html = (ROOT / "blog/songs" / sl / "index.html").read_text(encoding="utf-8")
        head = re.search(r"<title>([^<]*)</title>", page_html)
        desc = re.search(r'<meta name="description" content="([^"]*)"', page_html)
        intro = re.findall(r'<p class="post-intro">(.*?)</p>', page_html)
        post_titles[sl] = norm(html.unescape(" ".join(
            [head.group(1) if head else "", desc.group(1) if desc else ""] + intro)))

    songs = {}
    for r in rows:
        k = (r["title"].strip(), r["artist"].strip())
        if k not in songs:
            songs[k] = {"first": r["week_start"], "weeks": 0}
        songs[k]["weeks"] += 1

    title_count = {}
    for (t, _a) in songs:
        title_count[norm(t.split(" / ")[0])] = title_count.get(norm(t.split(" / ")[0]), 0) + 1

    out, n_radio, n_post = [], 0, 0
    for (title, artist), info in sorted(songs.items(), key=lambda kv: kv[1]["first"]):
        d = date.fromisoformat(info["first"])
        rid = radio_by_song.get((norm(title), norm(artist))) or radio_by_song.get((norm(title), ""))
        # Only trust a title-only match when the artist also lines up loosely.
        if rid and (norm(title), norm(artist)) not in radio_by_song:
            match = next(s for s in radio if s["radio_id"] == rid)
            if norm(artist)[:5] not in norm(match["artist"]) and norm(match["artist"])[:5] not in norm(artist):
                rid = None
        # Double A-sides ("American Woman / No Sugar Tonight") match on the A-side.
        nt = norm(title.split(" / ")[0])
        by_artist = lambda sl: norm(artist).split("and")[0][:5] in post_titles[sl]
        slug = next((sl for sl in post_by_radio.get(rid, [])
                     if nt in norm(sl) and sl in post_titles and by_artist(sl)), None)
        if not slug:
            # Songs posts without a play link, or linked to another radio slot.
            slug = next((sl for sl in song_slugs if (norm(sl) == nt or (len(nt) >= 8 and nt in norm(sl)))
                         and by_artist(sl)), None)
        if not slug and title_count[nt] == 1:
            # A title only one number one ever had can match its slug exactly.
            slug = next((sl for sl in song_slugs if norm(sl) == nt), None)
        post = f"/blog/songs/{slug}/" if slug else None
        t = html.escape(title)
        song_cell = f'<a href="{post}">{t}</a>' if post else t
        play_cell = f'<a href="/radio/?play={rid}" aria-label="Play {t} on Listen Now">Play</a>' if rid else ""
        n_radio += bool(rid)
        n_post += bool(post)
        out.append(
            f'<tr><td data-sort="{info["first"]}">{d.strftime("%b")} {d.day}, {d.year}</td>'
            f"<td>{song_cell}</td><td>{html.escape(artist)}</td>"
            f'<td data-sort="{info["weeks"]}">{info["weeks"]}</td><td>{play_cell}</td></tr>'
        )

    page = PAGE.read_text(encoding="utf-8")
    if START not in page or END not in page:
        sys.exit(f"markers missing in {PAGE}")
    body = "\n".join("              " + line for line in out)
    new = re.sub(re.escape(START) + ".*?" + re.escape(END), START + "\n" + body + "\n              " + END, page, flags=re.S)
    PAGE.write_text(new, encoding="utf-8")
    print(f"{len(out)} songs, {n_radio} with Listen Now links, {n_post} with Songs posts")


if __name__ == "__main__":
    main()
