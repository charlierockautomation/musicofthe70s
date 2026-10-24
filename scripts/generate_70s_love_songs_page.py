#!/usr/bin/env python3
"""Fill the playable table on /blog/songs/70s-love-songs/ (6F Listening page #1).

The 30 songs are picked from data/radio/radio-songs.json (mood tag "romantic",
each with an embeddable YouTube ID). Year, year-end rank, YouTube ID and radio_id
are read from that file, never typed here. The "#1 Hit" flag and every weeks-at-#1
figure come from data/billboard/hot100_weekly.json. The one-line stories use only
facts already on this site's own Songs posts, that weekly file, or the Wikipedia
pages those posts cite. Year-end data gives ranks only, so peaks below #1 are
quoted from the site's own Songs posts (Wikipedia), never from year-end rank.

Run: python3 scripts/generate_70s_love_songs_page.py
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "blog/songs/70s-love-songs/index.html"

# (radio_id, #1 on the weekly Hot 100?, Songs post slug or None, one verified line)
PICKS = [
    ("1970-2-they-long-to-be-close-to-you", True, "close-to-you",
     "Richard Chamberlain, Dionne Warwick and Dusty Springfield cut it first, then the Carpenters took it to number one for four weeks in 1970."),
    ("1970-7-ill-be-there", True, "ill-be-there-jackson-5",
     "Five weeks at number one in 1970, the Jackson 5's fourth straight chart-topper that year."),
    ("1970-13-make-it-with-you", True, None,
     "Bread's first Hot 100 entry went straight to number one, for one week in August 1970."),
    ("1970-65-weve-only-just-begun", False, "weve-only-just-begun",
     "It began as music for a bank commercial and stopped at number two on the Hot 100."),
    ("1971-3-its-too-late-i-feel-the-earth-move", True, "carole-king-its-too-late",
     "Five weeks at number one, with breakup lyrics a poet Carole King barely knew wrote in a single day."),
    ("1971-12-tired-of-being-alone", False, "al-green-tired-of-being-alone",
     "It reached number 11 in 1971, after four earlier singles from the same album missed the pop chart's upper half."),
    ("1972-1-the-first-time-ever-i-saw-your-face", True, None,
     "Six weeks at number one, the longest unbroken run of 1972."),
    ("1972-11-lets-stay-together", True, "al-green-lets-stay-together",
     "One week on top of the pop chart and nine on the soul chart, after Al Green argued for two days before he would record it."),
    ("1973-3-killing-me-softly-with-his-song", True, None,
     "Five non-consecutive weeks at number one made it the longest-running number one of 1973."),
    ("1973-10-touch-me-in-the-morning", True, None,
     "Diana Ross's second solo number one, for one week in August 1973."),
    ("1973-4-lets-get-it-on", True, "marvin-gaye-lets-get-it-on",
     "It hit number one twice in September 1973, with Helen Reddy in between."),
    ("1973-19-you-are-the-sunshine-of-my-life", True, "you-are-the-sunshine-of-my-life",
     "Stevie Wonder recorded it the same summer his marriage to Syreeta Wright ended."),
    ("1973-49-midnight-train-to-georgia", True, "midnight-train-to-georgia",
     "It began life as Midnight Plane to Houston, with a one-take vocal, two weeks at number one and a Grammy."),
    ("1974-25-annies-song", True, "annies-song",
     "John Denver wrote it in about ten minutes on an Aspen ski lift, and it spent two weeks at number one."),
    ("1974-97-i-honestly-love-you", True, None,
     "Olivia Newton-John's first number one, for two weeks in October 1974."),
    ("1975-36-mandy", True, "mandy-barry-manilow",
     "A little-known 1972 song called Brandy became Barry Manilow's first number one, for one week in January 1975."),
    ("1975-13-best-of-my-love", True, "best-of-my-love",
     "The Eagles' first number one in 1975, a soft country ballad the band and their own label almost buried."),
    ("1975-14-lovin-you", True, None,
     "Minnie Riperton's one week at number one in April 1975 was the only Top 40 hit of her career."),
    ("1976-6-kiss-and-say-goodbye", True, None,
     "The Manhattans' first number one, for two weeks in July 1976."),
    ("1976-15-love-hangover", True, None,
     "Two weeks at number one, and Diana Ross's second number one of 1976."),
    ("1976-48-if-you-leave-me-now", True, "if-you-leave-me-now",
     "Chicago's first number one, for two weeks in October 1976."),
    ("1977-4-evergreen-love-theme-from-a-star-is-born", True, None,
     "The love theme from A Star Is Born spent three weeks at number one in 1977."),
    ("1977-24-when-i-need-you", True, None,
     "Leo Sayer's second number one of 1977, for one week in May."),
    ("1977-2-i-just-want-to-be-your-everything", True, None,
     "Andy Gibb's first number one and four weeks on top in 1977."),
    ("1978-6-how-deep-is-your-love", True, "how-deep-is-your-love",
     "The Bee Gees wrote it with Yvonne Elliman in mind, and it reached number one on Christmas Eve 1977."),
    ("1978-3-you-light-up-my-life", True, None,
     "Ten straight weeks at number one starting in October 1977, the longest run of the decade."),
    ("1978-10-three-times-a-lady", True, None,
     "The Commodores' first number one, for two weeks in August 1978."),
    ("1978-35-hopelessly-devoted-to-you", False, "hopelessly-devoted-to-you",
     "John Farrar wrote it mid-shoot for Grease, and it peaked at number three and lost the Oscar."),
    ("1979-11-too-much-heaven", True, "too-much-heaven",
     "It knocked Le Freak off number one twice in January 1979, and the Bee Gees gave all of the proceeds to UNICEF."),
    ("1979-5-reunited", True, None,
     "Peaches & Herb's first number one, for four straight weeks in May 1979."),
]

# Longest runs at #1 on the list; weeks_at_number_one per hot100_weekly.json, runs stated unambiguously.
LONG_RUNS = [
    ("You Light Up My Life", 10),
    ("The First Time Ever I Saw Your Face", 6),
    ("I'll Be There", 5),
    ("It's Too Late", 5),
    ("Killing Me Softly with His Song", 5),
    ("I Just Want to Be Your Everything", 4),
    ("Reunited", 4),
    ("(They Long to Be) Close to You", 4),
]


def load_songs():
    radio = {s["radio_id"]: s for s in json.loads((ROOT / "data/radio/radio-songs.json").read_text())}
    songs = []
    for rid, n1, slug, story in PICKS:
        r = radio[rid]
        songs.append({"radio_id": rid, "title": r["title"], "artist": r["artist"], "year": r["year"],
                      "rank": r["rank"], "yt": r["youtube_id"], "n1": n1, "slug": slug, "story": story})
    return songs


SONGS = load_songs()


def esc(s):
    return html.escape(s, quote=True)


def artist_slug(artist, slugs):
    def norm(x):
        return re.sub(r"[^a-z0-9]+", "", x.lower().replace("&", "and"))
    a = norm(artist.replace("The ", "", 1) if artist.startswith("The ") else artist)
    for sl in slugs:
        s = norm(sl)
        if s == a or s.startswith(a) and s[len(a):] in ("songs", "theband", "bandsongs", "andthesunshineband"):
            return sl
    return None


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


START, END = "<!-- LOVE-START -->", "<!-- LOVE-END -->"


def main():
    n1 = sum(s["n1"] for s in SONGS)
    assert len(SONGS) == 30 and n1 == 27, (len(SONGS), n1)
    page = PAGE.read_text(encoding="utf-8")
    if START not in page or END not in page:
        raise SystemExit(f"markers missing in {PAGE}")
    new = re.sub(re.escape(START) + ".*?" + re.escape(END),
                 lambda _: START + "\n" + table_rows() + "\n              " + END, page, flags=re.S)
    PAGE.write_text(new, encoding="utf-8")
    print(f"{len(SONGS)} songs, {n1} number ones")


if __name__ == "__main__":
    main()
