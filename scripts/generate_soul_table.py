#!/usr/bin/env python3
"""Build the playable 70s soul songs list on /blog/genres/70s-soul-music/.

Rows: every song tagged genre "soul" in data/radio/radio-songs.json (each one is a
Billboard Year-End Hot 100 entry, 1970 to 1979). A song on two year-end lists gets one
row, at its first year, with both ranks shown.

Play IDs come only from data/official-videos.json (Article Standard L3): official artist,
label or VEVO uploads, or a label-delivered Topic upload under the 2026-11-09 Topic
exception. A row with no recorded official ID has no Play button. No radio-ID fallback.

Weeks at No. 1 are counted from data/billboard/hot100_weekly.json.
Song titles link to the song story on this site when one exists (SONG_STORIES).
Artist cells are plain text (each internal link appears once on the page).

Rewrites the block between <!-- SOUL-START --> and <!-- SOUL-END -->.

Run: python3 scripts/generate_soul_table.py
"""
import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "blog/genres/70s-soul-music/index.html"
START, END = "<!-- SOUL-START -->", "<!-- SOUL-END -->"

# (title, artist) -> song story slug; explicit so a same-name story about another act never links
SONG_STORIES = {
    ("I Want You Back", "The Jackson 5"): "i-want-you-back",
    ("Ain't No Mountain High Enough", "Diana Ross"): "aint-no-mountain-high-enough",
    ("I'll Be There", "The Jackson 5"): "ill-be-there-jackson-5",
    ("Tired of Being Alone", "Al Green"): "al-green-tired-of-being-alone",
    ("What's Going On", "Marvin Gaye"): "whats-going-on-marvin-gaye",
    ("Let's Stay Together", "Al Green"): "al-green-lets-stay-together",
    ("You Are the Sunshine of My Life", "Stevie Wonder"): "you-are-the-sunshine-of-my-life",
    ("Let's Get It On", "Marvin Gaye"): "marvin-gaye-lets-get-it-on",
    ("Midnight Train to Georgia", "Gladys Knight & the Pips"): "midnight-train-to-georgia",
    ("Living for the City", "Stevie Wonder"): "living-for-the-city",
    ("Sir Duke", "Stevie Wonder"): "sir-duke-stevie-wonder",
}

# chart credit -> credit used in data/official-videos.json, where the two differ
ARTIST_ALIAS = {"Hall & Oates": "Daryl Hall and John Oates"}


def norm(s):
    s = s.lower().replace("&", "and")
    s = re.sub(r"\(.*?\)", "", s)
    return re.sub(r"[^a-z0-9]+", "", s)


def official_ids():
    vids = json.loads((ROOT / "data/official-videos.json").read_text())["videos"]
    by_key = {}
    for vid, rec in vids.items():
        if rec.get("official") and " - " in rec.get("song", ""):
            t, a = rec["song"].rsplit(" - ", 1)
            by_key.setdefault((norm(t), norm(a)), vid)
    return vids, by_key


def rows():
    radio = json.loads((ROOT / "data/radio/radio-songs.json").read_text())
    songs = sorted((s for s in radio if s["genre"] == "soul"), key=lambda s: (s["year"], s["rank"]))
    out, seen = [], {}
    for s in songs:
        k = (norm(s["title"]), norm(s["artist"]))
        if k in seen:
            seen[k]["ranks"].append((s["year"], s["rank"]))
            continue
        r = {"title": s["title"], "artist": s["artist"], "year": s["year"], "rank": s["rank"],
             "ranks": [(s["year"], s["rank"])], "radio_id": s.get("youtube_id")}
        seen[k] = r
        out.append(r)
    return out


def weeks_at_one():
    weekly = json.loads((ROOT / "data/billboard/hot100_weekly.json").read_text())
    c = Counter()
    for wk in weekly.values():
        for w in wk:
            c[(norm(w["title"]), norm(w["artist"]))] += 1
    return c


def build():
    vids, by_key = official_ids()
    wk = weeks_at_one()
    out, n_play, n_no1 = [], 0, 0
    data = rows()
    for s in data:
        k = (norm(s["title"]), norm(s["artist"]))
        ka = (norm(s["title"]), norm(ARTIST_ALIAS.get(s["artist"], s["artist"])))
        vid = s["radio_id"] if s["radio_id"] in vids and vids[s["radio_id"]].get("official") else by_key.get(k) or by_key.get(ka)
        s["vid"] = vid
        t, a = html.escape(s["title"]), html.escape(s["artist"])
        play = (f'<button type="button" class="ohw-play" data-yt="{vid}" data-title="{t} by {a}" '
                f'aria-label="Play {t} by {a} here">&#9654; Play</button>') if vid else ""
        n_play += bool(vid)
        slug = SONG_STORIES.get((s["title"], s["artist"]))
        song_cell = f'<a href="/blog/songs/{slug}/">{t}</a>' if slug else t
        rank_cell = ", ".join(f"{r} ({y})" for y, r in s["ranks"]) if len(s["ranks"]) > 1 else str(s["rank"])
        w = wk.get(k, 0)
        s["weeks"] = w
        n_no1 += bool(w)
        out.append(
            f'<tr><td class="ohw-listen">{play}</td><td class="ohw-song">{song_cell}</td>'
            f'<td class="ohw-artist">{a}</td><td data-sort="{s["year"]}">{s["year"]}</td>'
            f'<td data-sort="{min(r for _, r in s["ranks"])}">{rank_cell}</td>'
            f'<td data-sort="{w}">{w if w else ""}</td></tr>'
        )
    return data, out, n_play, n_no1


def main():
    data, out, n_play, n_no1 = build()
    page = PAGE.read_text(encoding="utf-8")
    if START not in page or END not in page:
        sys.exit(f"markers missing in {PAGE}")
    body = "\n".join("              " + line for line in out)
    new = re.sub(re.escape(START) + ".*?" + re.escape(END),
                 lambda m: START + "\n" + body + "\n              " + END, page, flags=re.S)
    PAGE.write_text(new, encoding="utf-8")
    print(f"{len(out)} songs, {n_play} with Play, {n_no1} reached No. 1")


if __name__ == "__main__":
    main()
