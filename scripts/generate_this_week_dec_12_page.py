#!/usr/bin/env python3
"""Build /blog/trivia/december-12-in-music-history/ (6G Freshness track, post 4).

For each year 1970-1979 the post takes the weekly Hot 100 number one for the chart week that
contains December 12, straight from data/billboard/hot100_weekly.json. The chart week, the
song's total weeks at number one and the week of its run that December 12 fell in are all
computed from that file. YouTube ID and radio_id come from data/radio/radio-songs.json. The
one-line story for each song is a fact read off its Wikipedia page (see SOURCES in the
template), never typed from memory.

Run: python3 scripts/generate_this_week_dec_12_page.py
"""
import html
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "blog/trivia/december-12-in-music-history/index.html"
DATE_LONG = "December 12, 2026"
DATE_ISO = "2026-12-12"
MONTH_DAY = "-12-12"

# year -> (radio_id, one-line story fact, Wikipedia-verified 2026-10-26)
PICKS = {
    1970: (None, "Stevie Wonder wrote the music and Smokey Robinson the lyrics, and a bassoon is one of its few pop-hit sounds."),
    1971: ("1972-79-family-affair", "Sly Stone's drum-machine groove was later reused by the Temptations and Stevie Wonder."),
    1972: (None, "Helen Reddy and Ray Burton wrote it, and it was the first Australian-penned song to win a Grammy."),
    1973: ("1974-39-top-of-the-world", "Karen Carpenter re-recorded her lead vocal for the single because she was not satisfied with the original."),
    1974: ("1975-15-kung-fu-fighting", "It began as a B-side, recorded in two takes in the last ten minutes of a three-hour session."),
    1975: ("1976-14-fly-robin-fly", "Silver Convention became the second German act to top the US charts, after Bert Kaempfert."),
    1976: ("1977-1-tonights-the-night-gonna-be-alright", "Jerry Jumonville played the saxophone solo, and the BBC originally banned the song."),
    1977: ("1978-3-you-light-up-my-life", "Joseph Brooks wrote it, and it won him the Academy Award for Best Original Song."),
    1978: ("1979-3-le-freak", "Nile Rodgers says it grew out of being refused entry to Studio 54 around New Year's Eve 1977."),
    1979: (None, "Dennis DeYoung wrote it as a birthday present for his wife, Suzanne."),
}

# Runs that were broken up by another song (checked against Wikipedia)
SPLIT = {"Le Freak"}

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
    ("What was the number one song on December 12 in music history in the 1970s?",
     "The number one song for the Hot 100 chart week that includes December 12 changed every year. "
     "It was \"The Tears of a Clown\" in 1970, \"Family Affair\" in 1971, \"I Am Woman\" in 1972, "
     "\"Top of the World\" in 1973 and \"Kung Fu Fighting\" in 1974. The list ends with five more, up to \"Babe\" in 1979."),
    ("Which 70s number one song stayed on top the longest around December 12?",
     "Debby Boone's \"You Light Up My Life\" stayed on top the longest, with ten weeks at number one from "
     "October 15 to December 17, 1977, according to this site's weekly Hot 100 data. The chart week that "
     "contains December 12 was the ninth of those ten weeks."),
    ("What was the number one song on December 12, 1978?",
     "Chic's \"Le Freak\" was number one for the Hot 100 chart week of December 9 to 15, 1978. "
     "Barbra Streisand and Neil Diamond's \"You Don't Bring Me Flowers\" took the top spot the next week, "
     "and \"Le Freak\" came back for two weeks starting December 23 and three more starting January 20, 1979, "
     "six weeks in all, according to this site's weekly Hot 100 data."),
    ("How can I find the number one song from my own birthday?",
     "You can find the number one song from your birthday with the Birthday #1 Song Finder on this site. "
     "Enter a birthday from the 1970s and it shows the song that topped the Billboard Hot 100 that week, "
     "using the same weekly chart data as the ten songs on this page."),
    ("Why does the chart week change from year to year?",
     "This site's weekly Hot 100 file dates each chart week from a Saturday, and that date moves each year. "
     "The week containing December 12 began December 12 in 1970, December 11 in 1971 and 1976, December 10 in 1977, "
     "December 9 in 1972 and 1978, December 8 in 1973 and 1979, December 7 in 1974 and December 6 in 1975."),
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
    # Rows in the weekly file are the source of truth. "Le Freak" has 6 chart rows in three separate runs
    # (Dec 9; Dec 23-30; Jan 20-Feb 3) but weeks_at_number_one says 3; Wikipedia says six non-consecutive weeks
    # (that line carries a citation-needed tag there). "Tonight's the Night" is 8 rows, JSON says 7.
    assert all(s["json_weeks"] == s["total"] for s in SONGS if s["year"] not in (1976, 1978)), "weeks_at_number_one disagrees with run length"
    assert BY[1976]["json_weeks"] == 7 and BY[1976]["total"] == 8
    assert BY[1978]["json_weeks"] == 3 and BY[1978]["total"] == 6 and BY[1978]["offs"] == [0, 2, 3, 6, 7, 8]
    assert TOTAL_WEEKS == 39, TOTAL_WEEKS
    assert (len(FIRST), len(MID), len(LAST)) == (5, 4, 1), (len(FIRST), len(MID), len(LAST))
    assert LONGEST[0]["title"] == "You Light Up My Life" and LONGEST[0]["total"] == 10
    assert LONGEST[1]["title"].startswith("Tonight's the Night") and LONGEST[1]["total"] == 8
    assert LONGEST[2]["title"] == "Le Freak" and LONGEST[2]["total"] == 6
    assert BY[1977]["run_first"] == "1977-10-15" and BY[1977]["run_last"] == "1977-12-17" and BY[1977]["pos"] == 9
    assert BY[1976]["run_first"] == "1976-11-13" and BY[1976]["run_last"] == "1977-01-01" and BY[1976]["pos"] == 5
    assert BY[1978]["run_first"] == "1978-12-09" and BY[1978]["run_last"] == "1979-02-03"
    assert [s["week_start"] for s in SONGS] == [
        "1970-12-12", "1971-12-11", "1972-12-09", "1973-12-08", "1974-12-07",
        "1975-12-06", "1976-12-11", "1977-12-10", "1978-12-09", "1979-12-08"]
    page = (ROOT / "scripts/this_week_dec_12_template.tpl").read_text(encoding="utf-8")
    rep = {
        "{{ROWS}}": table_rows(), "{{LONG_ROWS}}": long_rows(), "{{DATE_LIST}}": date_list(),
        "{{FAQ_SCHEMA}}": faq_schema(), "{{FAQ_HTML}}": faq_html(),
        "{{TOTAL_WEEKS}}": str(TOTAL_WEEKS), "{{N_FIRST}}": str(len(FIRST)), "{{N_MID}}": str(len(MID)),
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
