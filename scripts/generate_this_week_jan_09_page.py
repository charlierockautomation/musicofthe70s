#!/usr/bin/env python3
"""Build /blog/trivia/january-9-in-music-history/ (6G Freshness track, post 5).

For each year 1970-1979 the post takes the weekly Hot 100 number one for the chart week that
contains January 9, straight from data/billboard/hot100_weekly.json. The chart week, the
song's total weeks at number one and the week of its run that January 9 fell in are all
computed from that file. YouTube ID and radio_id come from data/radio/radio-songs.json. The
one-line story for each song is a fact read off its Wikipedia page (see SOURCES in the
template), never typed from memory.

Run: python3 scripts/generate_this_week_jan_09_page.py
"""
import html
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "blog/trivia/january-9-in-music-history/index.html"
DATE_LONG = "January 9, 2027"
DATE_ISO = "2027-01-09"
MONTH_DAY = "-01-09"

# year -> (radio_id, one-line story fact, Wikipedia-verified 2026-10-26)
PICKS = {
    1970: ("1970-4-raindrops-keep-fallin-on-my-head", "Burt Bacharach and Hal David wrote it for Butch Cassidy and the Sundance Kid, and it won the Academy Award for Best Original Song."),
    1971: ("1971-31-my-sweet-lord-isnt-it-a-pity", "In the US it was paired with \"Isn't It a Pity\" as a double A-side, and a court later found Harrison had subconsciously copied \"He's So Fine.\""),
    1972: ("1972-9-brand-new-key", "It is sung by a girl on roller skates trying to catch a boy's eye, and some radio stations banned it."),
    1973: ("1973-9-youre-so-vain", "Mick Jagger sang uncredited backing vocals, and Carly Simon has said the song is about three men, naming only Warren Beatty."),
    1974: ("1974-24-time-in-a-bottle", "Croce wrote the lyrics after his wife told him she was pregnant, and the single came out two months after his death in a plane crash."),
    1975: ("1975-35-lucy-in-the-sky-with-diamonds", "John Lennon sang backing vocals and played guitar on it, credited as Dr. Winston O'Boogie."),
    1976: ("1976-64-saturday-night", "It did not chart in the UK in 1973, and the US release came in August 1975, with the word Saturday spelled out in a chant."),
    1977: ("1977-27-you-dont-have-to-be-a-star-to-be-in-my-show", "It won the married duo the 1977 Grammy for Best R&B Performance by a Duo or Group with Vocals."),
    1978: ("1978-6-how-deep-is-your-love", "It won the Grammy for Best Pop Performance by a Group at the 20th Grammy Awards."),
    1979: ("1979-11-too-much-heaven", "The Bee Gees gave it to Music for UNICEF and performed it at the benefit concert on January 9, 1979."),
}

# Runs that were broken up by another song (checked against Wikipedia)
SPLIT = set()

RADIO = {s["radio_id"]: s for s in json.loads((ROOT / "data/radio/radio-songs.json").read_text())}
NONES = {(v["title"], v["artist"]): v for v in json.loads((ROOT / "data/radio/number-one-videos.json").read_text())["videos"]}
WEEKLY = json.loads((ROOT / "data/billboard/hot100_weekly.json").read_text())
SEQ = sorted((r for y in WEEKLY.values() for r in y), key=lambda r: r["week_start"])
NUM = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten"}


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
        radio = RADIO[rid] if rid else {"youtube_id": NONES[(r["title"], r["artist"])]["youtube_id"], "rank": None, "year": None}
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
    ("What was the number one song on January 9 in music history in the 1970s?",
     "The number one song for the Hot 100 chart week that includes January 9 changed every year. "
     "It was \"Raindrops Keep Fallin' on My Head\" in 1970, \"My Sweet Lord\" in 1971, \"Brand New Key\" in 1972, "
     "\"You're So Vain\" in 1973 and \"Time in a Bottle\" in 1974. The list ends with five more, up to \"Too Much Heaven\" in 1979."),
    ("Which 70s number one song stayed on top the longest around January 9?",
     "Two songs tie, with four weeks each, according to this site's weekly Hot 100 data. "
     "B. J. Thomas's \"Raindrops Keep Fallin' on My Head\" ran from January 3 to January 24, 1970. "
     "George Harrison's \"My Sweet Lord\" ran from December 26, 1970 to January 16, 1971."),
    ("What was the number one song on January 9, 1979?",
     "The Bee Gees' \"Too Much Heaven\" was number one for the Hot 100 chart week of January 6 to 12, 1979. "
     "It was the first of its two weeks at number one, according to this site's weekly Hot 100 data. "
     "The group performed it at the Music for UNICEF Concert on January 9, 1979, according to Wikipedia."),
    ("How can I find the number one song from my own birthday?",
     "You can find the number one song from your birthday with the Birthday #1 Song Finder on this site. "
     "Enter a birthday from the 1970s and it shows the song that topped the Billboard Hot 100 that week, "
     "using the same weekly chart data as the ten songs on this page."),
    ("Why does the chart week change from year to year?",
     "This site's weekly Hot 100 file dates each chart week from a Saturday, and that date moves each year. "
     "The week containing January 9 began January 9 in 1971, January 8 in 1972 and 1977, January 7 in 1978, "
     "January 6 in 1973 and 1979, January 5 in 1974, January 4 in 1975 and January 3 in 1970 and 1976."),
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
    # Rows in the weekly file are the source of truth. weeks_at_number_one disagrees with the row count for
    # "Brand New Key" (2 vs 3), "Time in a Bottle" (1 vs 2; Wikipedia says a two-week run) and
    # "How Deep Is Your Love" (1 vs 3), so those three use the row count.
    assert all(s["json_weeks"] == s["total"] for s in SONGS if s["year"] not in (1972, 1974, 1978)), "weeks_at_number_one disagrees with run length"
    assert (BY[1972]["json_weeks"], BY[1972]["total"]) == (2, 3)
    assert (BY[1974]["json_weeks"], BY[1974]["total"]) == (1, 2)
    assert (BY[1978]["json_weeks"], BY[1978]["total"]) == (1, 3)
    assert TOTAL_WEEKS == 25, TOTAL_WEEKS
    assert (len(FIRST), len(MID), len(LAST)) == (6, 1, 3), (len(FIRST), len(MID), len(LAST))
    assert [s["title"] for s in LONGEST[:2]] == ["Raindrops Keep Fallin' on My Head", "My Sweet Lord / Isn't It a Pity"]
    assert LONGEST[0]["total"] == LONGEST[1]["total"] == 4
    assert BY[1970]["run_first"] == "1970-01-03" and BY[1970]["run_last"] == "1970-01-24" and BY[1970]["pos"] == 1
    assert BY[1971]["run_first"] == "1970-12-26" and BY[1971]["run_last"] == "1971-01-16" and BY[1971]["pos"] == 3
    assert BY[1979]["run_first"] == "1979-01-06" and BY[1979]["run_last"] == "1979-01-13" and BY[1979]["pos"] == 1
    assert [s["week_start"] for s in SONGS] == [
        "1970-01-03", "1971-01-09", "1972-01-08", "1973-01-06", "1974-01-05",
        "1975-01-04", "1976-01-03", "1977-01-08", "1978-01-07", "1979-01-06"]
    page = (ROOT / "scripts/this_week_jan_09_template.tpl").read_text(encoding="utf-8")
    rep = {
        "{{ROWS}}": table_rows(), "{{LONG_ROWS}}": long_rows(), "{{DATE_LIST}}": date_list(),
        "{{FAQ_SCHEMA}}": faq_schema(), "{{FAQ_HTML}}": faq_html(),
        "{{TOTAL_WEEKS}}": str(TOTAL_WEEKS), "{{N_FIRST}}": str(len(FIRST)), "{{N_MID}}": str(len(MID)),
        "{{N_LAST}}": str(len(LAST)),
        "{{DATE_LONG}}": DATE_LONG, "{{DATE_ISO}}": DATE_ISO,
    }
    for k, v in rep.items():
        page = page.replace(k, v)
    assert "{{" not in page, "unfilled placeholder"
    PAGE.parent.mkdir(parents=True, exist_ok=True)
    PAGE.write_text(page, encoding="utf-8")
    print(f"10 songs, {TOTAL_WEEKS} weeks at #1, first-week {len(FIRST)}, mid-run {len(MID)}, last-week {len(LAST)}")


if __name__ == "__main__":
    main()
