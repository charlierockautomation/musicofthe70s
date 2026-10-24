#!/usr/bin/env python3
"""Build /blog/songs/70s-party-songs/ (6F Listening page #2).

The 30 songs are picked from data/radio/radio-songs.json (vibe tag "party" or "dance",
each with an embeddable YouTube ID). Year, year-end rank, genre, YouTube ID and radio_id
are read from that file, never typed here. The "#1 Hit" flag and every weeks-at-#1 figure
and chart date come from data/billboard/hot100_weekly.json (asserted below). The story
lines use only that weekly file or facts already on this site's own Songs posts.
Year-end data gives ranks only, so peaks below #1 are quoted from the site's own Songs
posts (Wikipedia-credited), never from year-end rank.

Run: python3 scripts/generate_70s_party_songs_page.py
"""
import html
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_70s_love_songs_page import artist_slug  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "blog/songs/70s-party-songs/index.html"
SLUG = "70s-party-songs"
DATE_LONG = "October 24, 2026"
DATE_ISO = "2026-10-24"

# (radio_id, #1 on the weekly Hot 100?, Songs post slug or None, weekly-file title or None, one verified line)
PICKS = [
    ("1970-15-abc", True, None, "ABC",
     "Two weeks at number one from April 25, 1970, taking the top spot from The Beatles' \"Let It Be.\""),
    ("1970-11-mama-told-me-not-to-come", True, None, "Mama Told Me (Not to Come)",
     "Two weeks at number one in July 1970, between The Jackson 5's \"The Love You Save\" and The Carpenters' \"(They Long to Be) Close to You.\""),
    ("1971-10-knock-three-times", True, None, "Knock Three Times",
     "Three weeks at number one from January 23, 1971, right after George Harrison's \"My Sweet Lord.\""),
    ("1971-1-joy-to-the-world", True, "joy-to-the-world-three-dog-night", "Joy to the World",
     "Six weeks at number one in spring 1971, and Billboard's top single of the year."),
    ("1973-7-crocodile-rock", True, None, "Crocodile Rock",
     "Three weeks at number one from February 3, 1973, taking over from Stevie Wonder's \"Superstition.\""),
    ("1973-32-love-train", True, None, "Love Train",
     "One week at number one on March 24, 1973, a pause in the run of \"Killing Me Softly with His Song.\""),
    ("1973-26-superstition", True, "superstition-stevie-wonder", "Superstition",
     "Wonder wrote it as part of a deal with Jeff Beck, and his own version reached number one for one week on January 27, 1973."),
    ("1973-35-keep-on-truckin", True, None, "Keep on Truckin'",
     "Eddie Kendricks' two weeks at number one began November 10, 1973, right after \"Midnight Train to Georgia.\""),
    ("1974-20-hooked-on-a-feeling", True, None, "Hooked on a Feeling",
     "Blue Swede's one week at number one, April 6, 1974, sat between \"Sunshine on My Shoulders\" and \"Bennie and the Jets.\""),
    ("1974-7-tsop-the-sound-of-philadelphia", True, None, "TSOP (The Sound of Philadelphia)",
     "Two weeks at number one from April 20, 1974, right after Elton John's \"Bennie and the Jets.\""),
    ("1974-6-the-loco-motion", True, None, "The Loco-Motion",
     "Two weeks at number one from May 4, 1974, taking over directly from \"TSOP.\""),
    ("1974-43-rock-the-boat", True, None, "Rock the Boat",
     "One week at number one on July 6, 1974, and \"Rock Your Baby\" took the top spot the next week."),
    ("1974-38-rock-your-baby", True, None, "Rock Your Baby",
     "Two weeks at number one from July 13, 1974, directly after \"Rock the Boat.\""),
    ("1975-15-kung-fu-fighting", True, None, "Kung Fu Fighting",
     "Two weeks at number one from December 7, 1974, which is why it sits on the 1975 year-end list."),
    ("1975-23-lady-marmalade", True, None, "Lady Marmalade",
     "One week at number one on March 29, 1975, followed by Minnie Riperton's \"Lovin' You.\""),
    ("1975-22-the-hustle", True, None, "The Hustle",
     "One week at number one on July 26, 1975, between Wings' \"Listen to What the Man Said\" and the Eagles' \"One of These Nights.\""),
    ("1975-65-get-down-tonight", True, None, "Get Down Tonight",
     "One week at number one on August 30, 1975, ahead of Glen Campbell's \"Rhinestone Cowboy.\""),
    ("1976-14-fly-robin-fly", True, None, "Fly, Robin, Fly",
     "Three weeks at number one from November 29, 1975, split between KC and the Sunshine Band's two weeks of \"That's the Way (I Like It).\""),
    ("1976-3-disco-lady", True, None, "Disco Lady",
     "Four weeks at number one from April 3, 1976, taking over from \"December, 1963 (Oh, What a Night).\""),
    ("1976-5-play-that-funky-music", True, None, "Play That Funky Music",
     "Three weeks at number one from September 18, 1976, right after KC and the Sunshine Band's \"(Shake, Shake, Shake) Shake Your Booty.\""),
    ("1976-10-a-fifth-of-beethoven", True, None, "A Fifth of Beethoven",
     "One week at number one on October 9, 1976, between \"Play That Funky Music\" and \"Disco Duck.\""),
    ("1977-13-you-make-me-feel-like-dancing", True, None, "You Make Me Feel Like Dancing",
     "The first of Leo Sayer's two number ones in 1977, for one week from January 15."),
    ("1977-26-car-wash", True, None, "Car Wash",
     "One week at number one on January 29, 1977, right after Stevie Wonder's \"I Wish.\""),
    ("1978-4-stayin-alive", True, "stayin-alive", "Stayin' Alive",
     "Four straight weeks at number one from February 4, 1978, and the Bee Gees wrote it before Saturday Night Fever had a finished script."),
    ("1978-9-boogie-oogie-oogie", True, None, "Boogie Oogie Oogie",
     "A Taste of Honey's three weeks at number one from September 9, 1978, right after Frankie Valli's \"Grease.\""),
    ("1978-34-last-dance", False, "last-dance", None,
     "It reached number three on the Hot 100 in August 1978 and won the Academy Award for Best Original Song."),
    ("1979-3-le-freak", True, None, "Le Freak",
     "Six weeks at number one in three separate stretches between December 9, 1978, and February 3, 1979."),
    ("1979-6-i-will-survive", True, "i-will-survive", "I Will Survive",
     "Three weeks at number one in March 1979, after Gloria Gaynor carried copies to Studio 54 herself and asked the DJ to play it."),
    ("1979-8-ymca", False, "song-ymca", None,
     "Released October 9, 1978, it stalled at number two on the weekly Hot 100 in early 1979."),
    ("1979-78-september", False, "september-earth-wind-and-fire", None,
     "Never got higher than number eight on the Hot 100, and it came out on November 18, 1978."),
]

WEEKLY = json.loads((ROOT / "data/billboard/hot100_weekly.json").read_text())
WEEKS = Counter(r["title"] for y in WEEKLY.values() for r in y)


def load_songs():
    radio = {s["radio_id"]: s for s in json.loads((ROOT / "data/radio/radio-songs.json").read_text())}
    songs = []
    for rid, n1, slug, wtitle, story in PICKS:
        r = radio[rid]
        weeks = WEEKS.get(wtitle, 0) if wtitle else 0
        assert (weeks > 0) == n1, (rid, weeks, n1)
        songs.append({"radio_id": rid, "title": r["title"], "artist": r["artist"], "year": r["year"],
                      "rank": r["rank"], "yt": r["youtube_id"], "genre": r["genre"], "n1": n1,
                      "slug": slug, "weeks": weeks, "story": story})
    return songs


SONGS = load_songs()
LONG_RUNS = sorted(((s["title"], s["weeks"]) for s in SONGS if s["weeks"] >= 3),
                   key=lambda r: (-r[1], r[0]))
N = len(SONGS)
N1 = sum(s["n1"] for s in SONGS)
POOL = sum(1 for s in json.loads((ROOT / "data/radio/radio-songs.json").read_text())
           if s.get("youtube_id") and ({"party", "dance"} & set(s.get("vibe", []))))
GENRE_LABEL = {"disco": "Disco", "funk": "Funk", "soul": "Soul", "pop": "Pop", "classic-rock": "Classic rock"}
GENRES = Counter(s["genre"] for s in SONGS)
YEARS = Counter(s["year"] for s in SONGS)
YEAR_N1 = Counter(s["year"] for s in SONGS if s["n1"])


def esc(s):
    return html.escape(s, quote=True)


def table_rows():
    slugs = [p.parent.name for p in (ROOT / "blog/artists").glob("*/index.html")]
    out = []
    for s in SONGS:
        t, a = esc(s["title"]), esc(s["artist"])
        play = (f'<button type="button" class="ohw-play" data-yt="{s["yt"]}" data-title="{t} by {a}" '
                f'aria-label="Play {t} by {a} here">&#9654; Play</button>')
        song_cell = f'<a href="/blog/songs/{s["slug"]}/">{t}</a>' if s["slug"] else t
        asl = artist_slug(s["artist"], slugs)
        artist_cell = f'<a href="/blog/artists/{asl}/">{a}</a>' if asl else a
        out.append(
            f'<tr><td class="ohw-listen">{play}</td><td class="ohw-song">{song_cell}</td>'
            f'<td class="ohw-artist">{artist_cell}</td><td data-sort="{s["year"]}">{s["year"]}</td>'
            f'<td data-sort="{s["rank"]}">{s["rank"]}</td><td>{"Yes" if s["n1"] else "No"}</td>'
            f'<td class="love-story">{esc(s["story"])}</td></tr>')
    return "\n".join("              " + r for r in out)


def long_run_rows():
    rows = []
    for i, (t, w) in enumerate(LONG_RUNS):
        s = next(x for x in SONGS if x["title"] == t)
        cls = ' class="row-highlight"' if i < 2 else ""
        rows.append(f'              <tr{cls}><td>{esc(t)}</td><td>{esc(s["artist"])}</td><td>{w}</td><td>{s["year"]}</td></tr>')
    return "\n".join(rows)


def genre_rows():
    rows = []
    for g, c in GENRES.most_common():
        n1 = sum(1 for s in SONGS if s["genre"] == g and s["n1"])
        rows.append(f'              <tr><td>{GENRE_LABEL.get(g, g)}</td><td>{c}</td><td>{n1}</td></tr>')
    return "\n".join(rows)


def year_rows():
    top = max(YEARS.values())
    rows = []
    for y in range(1970, 1980):
        cls = ' class="row-highlight"' if YEARS.get(y, 0) == top else ""
        rows.append(f'              <tr{cls}><td>{y}</td><td>{YEARS.get(y, 0)}</td><td>{YEAR_N1.get(y, 0)}</td></tr>')
    return "\n".join(rows)


def main():
    assert N == 30 and N1 == 27, (N, N1)
    top_year = max(YEARS, key=lambda y: (YEARS[y], -y))
    top_n = YEARS[top_year]
    peak_years = sorted(y for y in YEARS if YEARS[y] == top_n)
    longest = LONG_RUNS[0][1]
    page = (ROOT / "scripts/party_songs_template.tpl").read_text(encoding="utf-8")
    rep = {
        "{{ROWS}}": table_rows(), "{{LONG_ROWS}}": long_run_rows(), "{{GENRE_ROWS}}": genre_rows(),
        "{{YEAR_ROWS}}": year_rows(), "{{POOL}}": str(POOL), "{{N}}": str(N), "{{N1}}": str(N1),
        "{{NOT_N1}}": str(N - N1), "{{DATE_LONG}}": DATE_LONG, "{{DATE_ISO}}": DATE_ISO,
        "{{TOP_YEAR}}": str(top_year), "{{TOP_N}}": str(top_n),
        "{{N_LONG}}": str(len(LONG_RUNS)), "{{LONGEST}}": str(longest),
        "{{GENRE_DISCO}}": str(GENRES["disco"]),
    }
    for k, v in rep.items():
        page = page.replace(k, v)
    assert "{{" not in page, "unfilled placeholder"
    PAGE.parent.mkdir(parents=True, exist_ok=True)
    PAGE.write_text(page, encoding="utf-8")
    print(f"{N} songs, {N1} number ones, pool {POOL}, top year {peak_years} ({top_n}), long runs {len(LONG_RUNS)}")


if __name__ == "__main__":
    main()
