#!/usr/bin/env python3
"""Build the playable 1970s pop songs list on /blog/genres/pop-songs-of-70s/.

Rows: every song tagged genre "pop" in data/radio/radio-songs.json (each one is a
Billboard Year-End Hot 100 entry, 1970 to 1979). A song on two year-end lists gets one
row, at its first year, with both ranks shown.

Play IDs come only from data/official-videos.json (Article Standard L3): official artist,
label or VEVO uploads, or a label-delivered Topic upload under the 2026-11-09 Topic
exception. A row with no recorded official ID has no Play button. No radio-ID fallback.

Weeks at No. 1 are counted from data/billboard/hot100_weekly.json (WEEKLY_CREDIT maps a
year-end credit to the weekly chart credit where the two differ, e.g. Dawn).
Song titles link to the song story on this site when one exists (SONG_STORIES).
Artist cells are plain text (each internal link appears once on the page).

Rewrites the block between <!-- POP-START --> and <!-- POP-END -->.

Run: python3 scripts/generate_pop_table.py
"""
import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "blog/genres/pop-songs-of-70s/index.html"
START, END = "<!-- POP-START -->", "<!-- POP-END -->"

# (title, artist) -> song story slug; explicit so a same-name story about another act never links
SONG_STORIES = {
    ("(They Long to Be) Close to You", "The Carpenters"): "close-to-you",
    ("We've Only Just Begun", "The Carpenters"): "weve-only-just-begun",
    ("Bad, Bad Leroy Brown", "Jim Croce"): "bad-bad-leroy-brown",
    ("Waterloo", "ABBA"): "abba-waterloo",
    ("Knowing Me, Knowing You", "ABBA"): "abba-knowing-me-knowing-you",
    ("Take a Chance on Me", "ABBA"): "take-a-chance-on-me",
    ("The Name of the Game", "ABBA"): "the-name-of-the-game-abba",
    ("Hopelessly Devoted to You", "Olivia Newton-John"): "hopelessly-devoted-to-you",
    ("You're the One That I Want", "John Travolta & Olivia Newton-John"): "youre-the-one-that-i-want",
}

# chart credit -> credit used in data/official-videos.json, where the two differ
ARTIST_ALIAS = {}

# (title, year-end credit) -> credit on the weekly Hot 100 in data/billboard/hot100_weekly.json
WEEKLY_CREDIT = {
    ("Knock Three Times", "Tony Orlando and Dawn"): "Dawn",
    ("Tie a Yellow Ribbon Round the Ole Oak Tree", "Tony Orlando and Dawn"): "Dawn featuring Tony Orlando",
    ("(You're) Having My Baby", "Paul Anka"): "Paul Anka and Odia Coates",
    ("Philadelphia Freedom", "Elton John"): "Elton John Band",
}


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


# Songs whose original recording has no official, label or label-delivered Topic upload anywhere on
# YouTube (step 4.8 searches, 2026-11-10) are swapped for a year-end hit of the same year and the same
# No. 1 status from another radio bucket that does play (Charlie, 2026-11-10: every row must play).
SWAP = {
    "Hitchin' a Ride": ("O-o-h Child", "Five Stairsteps"),
    "My Baby Loves Lovin'": ("Hey There Lonely Girl", "Eddie Holman"),
    "For the Love of Him": ("Band of Gold", "Freda Payne"),
    "Lay a Little Lovin' on Me": ("Give Me Just a Little More Time", "Chairmen of the Board"),
    "Chick-A-Boom (Don't Ya Jes' Love It)": ("Take Me Home, Country Roads", "John Denver"),
    "Chirpy Chirpy Cheep Cheep": ("Treat Her Like a Lady", "Cornelius Brothers & Sister Rose"),
    "The Candy Man": ("Brandy (You're a Fine Girl)", "Looking Glass"),
    "The Lion Sleeps Tonight": ("Betcha by Golly, Wow", "The Stylistics"),
    "Don't Say You Don't Remember": ("Everybody Plays the Fool", "The Main Ingredient"),
    "The Twelfth of Never": ("Daddy's Home", "Jermaine Jackson"),
    "Rock Me Gently": ("Seasons in the Sun", "Terry Jacks"),
    "Feelings": ("I'm Not in Love", "10cc"),
    "Don't Call Us, We'll Call You": ("When Will I See You Again", "The Three Degrees"),
    "The Rockford Files Theme": ("You Are So Beautiful", "Joe Cocker"),
    "Let Her In": ("Right Back Where We Started From", "Maxine Nightingale"),
    "I Like Dreamin'": ("Angel in Your Arms", "Hot"),
    "Do You Wanna Make Love": ("Easy", "Commodores"),
    "Swayin' to the Music (Slow Dancing)": ("I've Got Love on My Mind", "Natalie Cole"),
    "After the Lovin'": ("So in to You", "Atlanta Rhythm Section"),
    "Love's Grown Deep": ("Telephone Line", "Electric Light Orchestra"),
    "Don't Worry Baby": ("Hot Line", "The Sylvers"),
    "Star Wars (Main Title)": ("Float On", "The Floaters"),
    "My Angel Baby": ("Love Is in the Air", "John Paul Young"),
}


def rows():
    radio = json.loads((ROOT / "data/radio/radio-songs.json").read_text())
    sub = {(t, a): x for x in radio for (t, a) in SWAP.values() if x["title"] == t and x["artist"] == a}
    assert len(sub) == len(SWAP), sorted(set(SWAP.values()) - set(sub))
    songs = [sub[SWAP[s["title"]]] if s["title"] in SWAP else s for s in radio if s["genre"] == "pop"]
    songs = sorted(songs, key=lambda s: (s["year"], s["rank"]))
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
        kw = (norm(s["title"]), norm(WEEKLY_CREDIT.get((s["title"], s["artist"]), "")))
        vid = (s["radio_id"] if s["radio_id"] in vids and vids[s["radio_id"]].get("official")
               else by_key.get(k) or by_key.get(ka) or by_key.get(kw))
        s["vid"] = vid
        t, a = html.escape(s["title"]), html.escape(s["artist"])
        play = (f'<button type="button" class="ohw-play" data-yt="{vid}" data-title="{t} by {a}" '
                f'aria-label="Play {t} by {a} here">&#9654; Play</button>') if vid else ""
        n_play += bool(vid)
        slug = SONG_STORIES.get((s["title"], s["artist"]))
        song_cell = f'<a href="/blog/songs/{slug}/">{t}</a>' if slug else t
        rank_cell = ", ".join(f"{r} ({y})" for y, r in s["ranks"]) if len(s["ranks"]) > 1 else str(s["rank"])
        w = wk.get(k, 0) or wk.get(kw, 0)
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
