#!/usr/bin/env python3
"""Build /blog/trivia/november-7-in-music-history/ (6G Freshness track, post 2).

For each year 1970-1979 the post takes the weekly Hot 100 number one for the chart week that
contains November 7, straight from data/billboard/hot100_weekly.json. The chart week, the
song's total weeks at number one and the week of its run that November 7 fell in are all
computed from that file. YouTube ID and radio_id come from data/radio/radio-songs.json. The
one-line story for each song is a fact read off its Wikipedia page (see SOURCES in the
template), never typed from memory.

Run: python3 scripts/generate_this_week_nov_07_page.py
"""
import html
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "blog/trivia/november-7-in-music-history/index.html"
DATE_LONG = "November 7, 2026"
DATE_ISO = "2026-11-07"
MONTH_DAY = "-11-07"

# year -> (radio_id, one-line story fact, Wikipedia-verified 2026-11-07)
PICKS = {
    1970: ("1970-7-ill-be-there", "Four number ones in a row for the Jackson 5, written by Berry Gordy, Hal Davis, Bob West and Willie Hutch."),
    1971: ("1971-39-gypsys-tramps-thieves", "Cher's first solo number one in the United States and Canada, written by Bob Stone."),
    1972: ("1972-47-i-can-see-clearly-now", "Johnny Nash recorded it in London with members of the Fabulous Five Inc."),
    1973: ("1973-49-midnight-train-to-georgia", "Jim Weatherly first recorded it as \"Midnight Plane to Houston.\""),
    1974: (None, "The Jackson 5 sing background vocals, and the single came out the day before Nixon announced his resignation."),
    1975: ("1976-65-island-girl", "The first single from Rock of the Westies."),
    1976: (None, "The second single from Fly Like an Eagle, with an intro Miller called a nod to Free."),
    1977: ("1978-3-you-light-up-my-life", "Ten weeks at the top, a Hot 100 record at the time."),
    1978: ("1978-63-you-needed-me", "Randy Goodrum wrote it, and it won Anne Murray a Grammy, the first for a Canadian artist."),
    1979: (None, "Robin Scott wrote and produced it and sang lead as M."),
}

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
        assert b - a + 1 == len(idx), r["title"]
        radio = RADIO[rid] if rid else {"youtube_id": NONES[(r["title"], r["artist"])]["youtube_id"], "rank": None, "year": None}
        out.append({
            "year": year, "title": r["title"], "artist": r["artist"], "yt": radio["youtube_id"],
            "rid": rid, "ye_rank": radio["rank"], "ye_year": radio["year"], "line": line,
            "week_start": r["week_start"], "week_end": r["week_end"],
            "pos": i - a + 1, "total": len(idx),
            "run_first": SEQ[a]["week_start"], "run_last": SEQ[b]["week_start"],
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
    ("What was the number one song on November 7 in music history in the 1970s?",
     "The number one song for the Hot 100 chart week that includes November 7 changed every year. "
     "It was \"I'll Be There\" in 1970, \"Gypsys, Tramps & Thieves\" in 1971, \"I Can See Clearly Now\" in 1972, "
     "\"Midnight Train to Georgia\" in 1973 and \"You Haven't Done Nothin'\" in 1974. The list ends with \"Island Girl,\" "
     "\"Rock'n Me,\" \"You Light Up My Life,\" \"You Needed Me\" and \"Pop Muzik.\""),
    ("Which 70s number one song stayed on top the longest around November 7?",
     "Debby Boone's \"You Light Up My Life\" stayed on top the longest, with ten weeks at number one from "
     "October 15 to December 17, 1977, according to this site's weekly Hot 100 data. The chart week that "
     "contains November 7 was the fourth of those ten weeks."),
    ("What was the number one song on November 7, 1973?",
     "Gladys Knight & the Pips' \"Midnight Train to Georgia\" was number one for the Hot 100 chart week of "
     "November 3 to 9, 1973. It was the second and last of its two weeks at the top, after a first week "
     "starting October 27. Jim Weatherly wrote the song and first recorded it as \"Midnight Plane to Houston.\""),
    ("How can I find the number one song from my own birthday?",
     "You can find the number one song from your birthday with the Birthday #1 Song Finder on this site. "
     "Enter a birthday from the 1970s and it shows the song that topped the Billboard Hot 100 that week, "
     "using the same weekly chart data as the ten songs on this page."),
    ("Why does the chart week change from year to year?",
     "This site's weekly Hot 100 file dates each chart week from a Saturday, and that date moves each year. "
     "The week containing November 7 began November 7 in 1970, November 6 in 1971 and 1976, November 5 in 1977, "
     "November 4 in 1972 and 1978, November 3 in 1973 and 1979, November 2 in 1974 and November 1 in 1975."),
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
    assert all(s["json_weeks"] == s["total"] for s in SONGS), "weeks_at_number_one disagrees with run length"
    assert TOTAL_WEEKS == 30, TOTAL_WEEKS
    assert (len(FIRST), len(MID), len(LAST)) == (7, 2, 1), (len(FIRST), len(MID), len(LAST))
    assert LONGEST[0]["title"] == "You Light Up My Life" and LONGEST[0]["total"] == 10
    assert BY[1977]["run_first"] == "1977-10-15" and BY[1977]["run_last"] == "1977-12-17" and BY[1977]["pos"] == 4
    assert BY[1970]["run_first"] == "1970-10-17" and BY[1970]["run_last"] == "1970-11-14" and BY[1970]["pos"] == 4
    assert BY[1973]["run_first"] == "1973-10-27" and BY[1973]["pos"] == 2 and BY[1973]["total"] == 2
    assert BY[1972]["run_last"] == "1972-11-25" and BY[1975]["run_last"] == "1975-11-15"
    assert [s["week_start"] for s in SONGS] == [
        "1970-11-07", "1971-11-06", "1972-11-04", "1973-11-03", "1974-11-02",
        "1975-11-01", "1976-11-06", "1977-11-05", "1978-11-04", "1979-11-03"]
    page = (ROOT / "scripts/this_week_nov_07_template.tpl").read_text(encoding="utf-8")
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
