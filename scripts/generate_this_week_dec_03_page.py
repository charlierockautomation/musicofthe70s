#!/usr/bin/env python3
"""Build /blog/trivia/december-3-in-music-history/ (6G Freshness track, post 19).

For each year 1970-1979 the post takes the weekly Hot 100 number one for the chart week that
contains December 3, straight from data/billboard/hot100_weekly.json. The chart week, the
song's total weeks at number one and the week of its run that December 3 fell in are all
computed from that file. YouTube ID and radio_id come from data/radio/radio-songs.json, or
data/radio/number-one-videos.json for the two songs not in the radio file. The one-line story
for each song is a fact read off its Wikipedia page (see SOURCES in the template), never
typed from memory.

Date rule (Charlie 2026-11-08): a This Week in Music History post covers the real week it
publishes, and lists every number one from that week. November 26 was skipped because its ten
songs are exactly the November 28 page's ten (Charlie's call, 2026-11-08), so this is the next
real week. Six of these ten are also on the November 28 page, and four on the December 12 page.

Run: python3 scripts/generate_this_week_dec_03_page.py
"""
import html
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "blog/trivia/december-3-in-music-history/index.html"
DATE_LONG = "December 3, 2026"
DATE_ISO = "2026-12-03"
MONTH_DAY = "-12-03"

# year -> (radio_id or None, one-line story fact, Wikipedia-verified 2026-11-08).
# Each line is a different fact from the ones already used on other date pages.
PICKS = {
    1970: (None, "It was cut at United Western Recorders in Hollywood, with Hal Blaine on drums and Wes Farrell producing."),
    1971: ("1971-89-theme-from-shaft", "Isaac Hayes recorded the rhythm parts first, scored the rest of the film, then came back to finish the theme."),
    1972: ("1973-100-papa-was-a-rollin-stone", "The Undisputed Truth released it first, in May 1972, months before the Temptations' version."),
    1973: ("1974-39-top-of-the-world", "Lynn Anderson's cover reached number 2 on the country chart before the Carpenters put out their own single."),
    1974: ("1975-44-i-can-help", "Billy Swan played the organ part on a portable Farfisa that belonged to Memphis session player Bobby Emmons."),
    1975: ("1976-14-fly-robin-fly", "Sylvester Levay and Stephan Prager wrote it, and it won the Grammy for Best R&B Instrumental Performance."),
    1976: ("1977-1-tonights-the-night-gonna-be-alright", "Tom Dowd produced it, and it was recorded at Muscle Shoals Sound Studio in Alabama."),
    1977: ("1978-3-you-light-up-my-life", "Kasey Cisyk recorded it first, for the soundtrack album of the 1977 film of the same title."),
    1978: ("1979-21-you-dont-bring-me-flowers", "Louisville radio programmer Gary Guthrie spliced Diamond's and Streisand's solo recordings into a duet before they cut one together."),
    1979: (None, "Gary Klein and Giorgio Moroder produced it, and the 12-inch version runs 11 minutes 43 seconds."),
}

# Runs that were broken up by another song (checked against the weekly file): "Le Freak" took
# the chart week of December 9, 1978 between this song's two weeks.
SPLIT = {"You Don't Bring Me Flowers"}
# weeks_at_number_one in the weekly file disagrees with its own rows here; the rows (8) match
# Wikipedia's "eight consecutive weeks", so the rows stay the source of truth.
JSON_WEEKS_WRONG = {"Tonight's the Night (Gonna Be Alright)": 7}

RADIO = {s["radio_id"]: s for s in json.loads((ROOT / "data/radio/radio-songs.json").read_text())}
NONES = {(v["title"], v["artist"]): v for v in json.loads((ROOT / "data/radio/number-one-videos.json").read_text())["videos"]}
WEEKLY = json.loads((ROOT / "data/billboard/hot100_weekly.json").read_text())
SEQ = sorted((r for y in WEEKLY.values() for r in y), key=lambda r: r["week_start"])


def esc(s):
    return html.escape(s, quote=True)


def long_date(iso):
    d = date.fromisoformat(iso)
    return f"{d.strftime('%B')} {d.day}, {d.year}"


def short_date(iso):
    d = date.fromisoformat(iso)
    return f"{d.strftime('%b')} {d.day}"


def load():
    out = []
    for year, (rid, line) in PICKS.items():
        i = next(k for k, r in enumerate(SEQ) if r["week_start"] <= f"{year}{MONTH_DAY}" <= r["week_end"])
        r = SEQ[i]
        idx = [k for k, x in enumerate(SEQ) if x["title"] == r["title"] and x["artist"] == r["artist"]]
        a, b = idx[0], idx[-1]
        assert b - a + 1 == len(idx) or r["title"] in SPLIT, r["title"]
        if rid:
            radio = RADIO[rid]
            assert radio["title"] == r["title"], (radio["title"], r["title"])
        else:
            radio = {"youtube_id": NONES[(r["title"], r["artist"])]["youtube_id"], "rank": None, "year": None}
        out.append({
            "year": year, "title": r["title"], "artist": r["artist"], "yt": radio["youtube_id"],
            "rid": rid, "ye_rank": radio["rank"], "ye_year": radio["year"], "line": line,
            "week_start": r["week_start"], "week_end": r["week_end"],
            "pos": idx.index(i) + 1, "total": len(idx),
            "offs": [k - a for k in idx], "run_first": SEQ[a]["week_start"], "run_last": SEQ[b]["week_start"],
            "json_weeks": r["weeks_at_number_one"],
        })
    return out


SONGS = load()
BY = {s["year"]: s for s in SONGS}
TOTAL_WEEKS = sum(s["total"] for s in SONGS)
FIRST = [s for s in SONGS if s["pos"] == 1]
MID = [s for s in SONGS if 1 < s["pos"] < s["total"]]
LAST = [s for s in SONGS if s["pos"] == s["total"] and s["total"] > 1]
LONGEST = sorted(SONGS, key=lambda s: (-s["total"], s["year"]))


def table_rows():
    out = []
    for s in SONGS:
        t, a = esc(s["title"]), esc(s["artist"])
        play = (f'<button type="button" class="ohw-play" data-yt="{s["yt"]}" data-title="{t} by {a}" '
                f'aria-label="Play {t} by {a} here">&#9654; Play</button>')
        wk = f'{short_date(s["week_start"])} to {short_date(s["week_end"])}'
        out.append(
            f'<tr><td class="ohw-listen">{play}</td><td class="ohw-song">{t}</td>'
            f'<td class="ohw-artist">{a}</td><td data-sort="{s["year"]}">{s["year"]}</td>'
            f'<td data-sort="{s["week_start"]}">{wk}</td>'
            f'<td data-sort="{s["pos"]}">{s["pos"]} of {s["total"]}</td>'
            f'<td data-sort="{s["total"]}">{s["total"]}</td>'
            f'<td class="love-story">{esc(s["line"])}</td></tr>')
    return "\n".join("              " + r for r in out)


def long_rows():
    rows = []
    for i, s in enumerate(LONGEST):
        cls = ' class="row-highlight"' if i == 0 else ""
        rows.append(f'              <tr{cls}><td>{esc(s["title"])}</td><td>{esc(s["artist"])}</td>'
                    f'<td>{s["year"]}</td><td>{s["total"]}</td>'
                    f'<td>{long_date(s["run_first"])}</td><td>{long_date(s["run_last"])}</td></tr>')
    return "\n".join(rows)


def date_list():
    items = []
    for s in SONGS:
        items.append(f'          <li>{s["year"]}: the chart week of {long_date(s["week_start"])}, with '
                     f'"{esc(s["title"])}" by {esc(s["artist"])} on top.</li>')
    return "\n".join(items)


FAQ = [
    ("What was the number one song on December 3 in music history in the 1970s?",
     "The Hot 100 number one for the week that includes December 3 changed every year. "
     "From 1970 to 1974 it was \"I Think I Love You,\" \"Theme from Shaft,\" \"Papa Was a Rollin' Stone,\" "
     "\"Top of the World\" and \"I Can Help.\" "
     "From 1975 to 1979 it was \"Fly, Robin, Fly,\" \"Tonight's the Night,\" \"You Light Up My Life,\" "
     "\"You Don't Bring Me Flowers\" and \"No More Tears.\""),
    ("Which song was number one the week of December 3, 1977?",
     "Debby Boone's \"You Light Up My Life\" was number one for the Hot 100 chart week that began "
     "December 3, 1977. "
     "That was the eighth of its ten weeks on top, a run that started October 15 and ended December 17, 1977, "
     "according to this site's weekly Hot 100 data."),
    ("How did Barbra Streisand and Neil Diamond end up singing \"You Don't Bring Me Flowers\" together?",
     "Both had recorded \"You Don't Bring Me Flowers\" as a solo song. "
     "Wikipedia says Louisville radio programmer Gary Guthrie spliced the two solo recordings into a duet, "
     "and Columbia then had the pair record a new studio version together, released October 17, 1978. "
     "Their duet reached number one for the chart week of December 2, 1978."),
    ("How can I find the number one song from my own birthday?",
     "You can find the number one song from your birthday with the Birthday #1 Song Finder on this site. "
     "Enter a birthday from the 1970s and it shows the song that topped the Billboard Hot 100 that week, "
     "using the same weekly chart data as the ten songs on this page."),
    ("Why are so many of these songs also on the November 28 list?",
     "November 28 and December 3 are five days apart, and in 1970, 1971 and 1976 they fall in the same "
     "Hot 100 chart week. "
     "Six songs appear on both lists. "
     "Only 1972, 1973, 1975 and 1978 had a new number one by December 3."),
]


def faq_schema():
    items = []
    for q, a in FAQ:
        items.append('      {\n        "@type": "Question",\n        "name": %s,\n        "acceptedAnswer": {\n'
                     '          "@type": "Answer",\n          "text": %s\n        }\n      }'
                     % (json.dumps(q, ensure_ascii=False), json.dumps(a, ensure_ascii=False)))
    return ",\n".join(items)


def faq_html():
    out = []
    for q, a in FAQ:
        out.append(f'          <div class="faq-item">\n            <h3>{html.escape(q, quote=False)}</h3>\n'
                   f'            <p>{html.escape(a, quote=False)}</p>\n          </div>')
    return "\n".join(out)


def main():
    assert len(SONGS) == 10 and len({s["title"] for s in SONGS}) == 10
    # Rows in the weekly file are the source of truth; weeks_at_number_one only disagrees where listed.
    for s in SONGS:
        if s["title"] in JSON_WEEKS_WRONG:
            assert (s["json_weeks"], s["total"]) == (JSON_WEEKS_WRONG[s["title"]], 8), s["title"]
        else:
            assert s["json_weeks"] == s["total"], ("weeks_at_number_one disagrees with run length", s["title"])
    for faq_q, faq_a in FAQ:
        assert 40 <= len(faq_a.split()) <= 70, (faq_q, len(faq_a.split()))
    assert TOTAL_WEEKS == 35, TOTAL_WEEKS
    assert (len(FIRST), len(MID), len(LAST)) == (4, 3, 3), (len(FIRST), len(MID), len(LAST))
    assert [s["title"] for s in FIRST] == ["Papa Was a Rollin' Stone", "Top of the World", "Fly, Robin, Fly", "You Don't Bring Me Flowers"]
    assert [s["title"] for s in MID] == ["I Think I Love You", "Tonight's the Night (Gonna Be Alright)", "You Light Up My Life"]
    assert [s["title"] for s in LAST] == ["Theme from Shaft", "I Can Help", "No More Tears (Enough Is Enough)"]
    assert [s["total"] for s in LONGEST] == [10, 8, 3, 3, 2, 2, 2, 2, 2, 1]
    assert all(s["offs"] == list(range(s["total"])) for s in SONGS if s["title"] not in SPLIT), "unexpected split run"
    assert BY[1978]["offs"] == [0, 2] and BY[1978]["pos"] == 1
    assert [s["week_start"] for s in SONGS] == [
        "1970-11-28", "1971-11-27", "1972-12-02", "1973-12-01", "1974-11-30",
        "1975-11-29", "1976-11-27", "1977-12-03", "1978-12-02", "1979-12-01"]
    assert [s["pos"] for s in SONGS] == [2, 2, 1, 1, 2, 1, 3, 8, 1, 2]
    assert BY[1970]["run_first"] == "1970-11-21" and BY[1970]["run_last"] == "1970-12-05"
    assert BY[1971]["run_first"] == "1971-11-20" and BY[1971]["run_last"] == "1971-11-27"
    assert BY[1973]["run_first"] == "1973-12-01" and BY[1973]["run_last"] == "1973-12-08"
    assert BY[1974]["run_first"] == "1974-11-23" and BY[1974]["run_last"] == "1974-11-30"
    assert BY[1975]["run_first"] == "1975-11-29" and BY[1975]["run_last"] == "1975-12-13"
    assert BY[1976]["run_first"] == "1976-11-13" and BY[1976]["run_last"] == "1977-01-01"
    assert BY[1977]["run_first"] == "1977-10-15" and BY[1977]["run_last"] == "1977-12-17"
    assert BY[1978]["run_first"] == "1978-12-02" and BY[1978]["run_last"] == "1978-12-16"
    assert BY[1979]["run_first"] == "1979-11-24" and BY[1979]["run_last"] == "1979-12-01"
    # Neighbours named in the prose, read off the weekly file.
    nb = {r["week_start"]: (r["title"], r["artist"]) for r in SEQ}
    assert nb["1970-11-14"][0] == "I'll Be There" and nb["1970-12-12"][0] == "The Tears of a Clown"
    assert nb["1971-11-13"][0] == "Gypsys, Tramps & Thieves" and nb["1971-12-04"][0] == "Family Affair"
    assert nb["1972-11-25"][0] == "I Can See Clearly Now" and nb["1972-12-09"][0] == "I Am Woman"
    assert nb["1973-11-24"][0] == "Photograph" and nb["1973-12-15"][0] == "The Most Beautiful Girl"
    assert nb["1974-11-16"][0] == "Whatever Gets You thru the Night" and nb["1974-12-07"][0] == "Kung Fu Fighting"
    assert nb["1975-11-22"][0] == "That's the Way (I Like It)" and nb["1975-12-20"][0] == "That's the Way (I Like It)"
    assert nb["1976-11-06"][0] == "Rock'n Me" and nb["1977-01-08"][0] == "You Don't Have to Be a Star (To Be in My Show)"
    assert nb["1977-10-08"][0] == "Star Wars Theme/Cantina Band" and nb["1977-12-24"][0] == "How Deep Is Your Love"
    assert nb["1978-11-25"][0] == "MacArthur Park" and nb["1978-12-09"][0] == "Le Freak" and nb["1978-12-23"][0] == "Le Freak"
    assert nb["1979-11-17"][0] == "Still" and nb["1979-12-08"][0] == "Babe"
    assert [s["ye_rank"] for s in SONGS] == [None, 89, 100, 39, 44, 14, 1, 3, 21, None]
    assert [s["ye_year"] for s in SONGS] == [None, 1971, 1973, 1974, 1975, 1976, 1977, 1978, 1979, None]
    page = (ROOT / "scripts/this_week_dec_03_template.tpl").read_text(encoding="utf-8")
    rep = {
        "{{ROWS}}": table_rows(), "{{LONG_ROWS}}": long_rows(), "{{DATE_LIST}}": date_list(),
        "{{FAQ_SCHEMA}}": faq_schema(), "{{FAQ_HTML}}": faq_html(),
        "{{TOTAL_WEEKS}}": str(TOTAL_WEEKS), "{{N_FIRST}}": str(len(FIRST)), "{{N_MID}}": str(len(MID)),
        "{{N_LAST}}": str(len(LAST)), "{{DATE_LONG}}": DATE_LONG, "{{DATE_ISO}}": DATE_ISO,
    }
    for k, v in rep.items():
        page = page.replace(k, v)
    assert "{{" not in page, "unfilled placeholder"
    PAGE.parent.mkdir(parents=True, exist_ok=True)
    PAGE.write_text(page, encoding="utf-8")
    print(f"10 songs, {TOTAL_WEEKS} weeks at #1, first-week {len(FIRST)}, mid-run {len(MID)}, last-week {len(LAST)}")


if __name__ == "__main__":
    main()
