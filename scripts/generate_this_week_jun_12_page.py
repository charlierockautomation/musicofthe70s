#!/usr/bin/env python3
"""Build /blog/trivia/june-12-in-music-history/ (6G Freshness track, post 10).

For each year 1970-1979 the post takes the weekly Hot 100 number one for the chart week that
contains June 12, straight from data/billboard/hot100_weekly.json. The chart week, the
song's total weeks at number one and the week of its run that June 12 fell in are all
computed from that file. YouTube ID and radio_id come from data/radio/radio-songs.json. The
one-line story for each song is a fact read off its Wikipedia page (see SOURCES in the
template), never typed from memory.

Run: python3 scripts/generate_this_week_jun_12_page.py
"""
import html
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "blog/trivia/june-12-in-music-history/index.html"
DATE_LONG = "June 12, 2027"
DATE_ISO = "2027-06-12"
MONTH_DAY = "-06-12"

# year -> (radio_id, one-line story fact, Wikipedia-verified 2026-10-31)
PICKS = {
    1970: ("1970-12-everything-is-beautiful", "Ray Stevens wrote and sang it, and the children who sing the opening hymn came from Oak Hill Elementary School in Nashville, including his daughters Suzi and Timi."),
    1971: ("1971-13-want-ads", "Barney Perkins suggested a song about want ads after reading a newspaper's classified section."),
    1972: ("1972-5-the-candy-man", "Sammy Davis Jr. reportedly recorded it in only two takes and told his manager it was \"horrible\" and \"white bread.\""),
    1973: (None, "Paul McCartney wrote it as a love song to his wife Linda, and guitarist Henry McCullough improvised the guitar solo."),
    1974: ("1974-22-band-on-the-run", "The first two sections were taped at EMI's studio in Lagos, Nigeria, and the third was recorded at AIR Studios in London in October 1973."),
    1975: ("1975-11-thank-god-im-a-country-boy", "John Sommers of Denver's backup band wrote it on New Year's Eve 1973 while driving from Aspen to Los Angeles."),
    1976: ("1976-1-silly-love-songs", "Paul and Linda McCartney wrote it as a rebuttal to critics who accused McCartney of writing \"sentimental slush,\" including John Lennon."),
    1977: ("1977-11-im-your-boogie-man", "Richard Finch said it was written about a Miami DJ who was the first to give airplay to the group's \"Get Down Tonight.\""),
    1978: (None, "John Farrar wrote it specifically for Olivia Newton-John's appearance in the film, and it was not in the original stage musical."),
    1979: ("1979-33-love-you-inside-out", "The Bee Gees sent manager Robert Stigwood a prank version with an altered lyric to see whether he was paying attention."),
}

# Runs that were broken up by another song (checked against Wikipedia)
SPLIT = {"Silly Love Songs"}

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
    ("What was the number one song on June 12 in music history in the 1970s?",
     "The number one song for the Hot 100 chart week that includes June 12 changed every year. "
     "It was \"Everything Is Beautiful\" in 1970, \"Want Ads\" in 1971, \"The Candy Man\" in 1972, "
     "\"My Love\" in 1973 and \"Band on the Run\" in 1974. Five more follow, ending with \"Love You Inside Out\" in 1979."),
    ("Which 70s number one song stayed on top the longest around June 12?",
     "Wings' \"Silly Love Songs\" had the most weeks at number one of the ten songs, with five, according to this site's weekly Hot 100 data. "
     "They were not in a row, because another song held the top spot for two weeks in the middle. "
     "Paul McCartney and Wings' \"My Love\" was next with four weeks, and Sammy Davis Jr.'s \"The Candy Man\" had three."),
    ("What was the number one song on June 12, 1976?",
     "Wings' \"Silly Love Songs\" was number one for the Hot 100 chart week that began June 12, 1976. "
     "It was the second of its five weeks at number one, after a gap of two weeks, according to this site's weekly Hot 100 data. "
     "Billboard ranked it number one for 1976, which matches the 1976 year-end Hot 100 in this site's data."),
    ("How can I find the number one song from my own birthday?",
     "You can find the number one song from your birthday with the Birthday #1 Song Finder on this site. "
     "Enter a birthday from the 1970s and it shows the song that topped the Billboard Hot 100 that week, "
     "using the same weekly chart data as the ten songs on this page."),
    ("Why does the chart week change from year to year?",
     "This site's weekly Hot 100 file dates each chart week from a Saturday, and that date moves each year. "
     "The week containing June 12 began June 12 in 1971 and 1976, June 11 in 1977, June 10 in 1972 and 1978, "
     "June 9 in 1973 and 1979, June 8 in 1974, June 7 in 1975 and June 6 in 1970."),
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
    # Rows in the weekly file are the source of truth; for these ten songs weeks_at_number_one matches the row count.
    assert all(s["json_weeks"] == s["total"] for s in SONGS), "weeks_at_number_one disagrees with run length"
    assert TOTAL_WEEKS == 20, TOTAL_WEEKS
    assert (len(FIRST), len(MID), len(LAST)) == (7, 2, 1), (len(FIRST), len(MID), len(LAST))
    assert [s["title"] for s in LONGEST[:4]] == ["Silly Love Songs", "My Love", "The Candy Man", "Everything Is Beautiful"]
    assert [s["total"] for s in LONGEST[:4]] == [5, 4, 3, 2]
    assert BY[1976]["run_first"] == "1976-05-22" and BY[1976]["run_last"] == "1976-07-03" and BY[1976]["pos"] == 2
    assert BY[1976]["offs"] == [0, 3, 4, 5, 6]
    assert BY[1973]["run_first"] == "1973-06-02" and BY[1973]["run_last"] == "1973-06-23" and BY[1973]["pos"] == 2
    assert BY[1972]["run_first"] == "1972-06-10" and BY[1972]["run_last"] == "1972-06-24" and BY[1972]["pos"] == 1
    assert BY[1970]["pos"] == 2 == BY[1970]["total"] and BY[1970]["run_first"] == "1970-05-30"
    assert sum(1 for s in SONGS if s["total"] == 1) == 6
    assert [s["week_start"] for s in SONGS] == [
        "1970-06-06", "1971-06-12", "1972-06-10", "1973-06-09", "1974-06-08",
        "1975-06-07", "1976-06-12", "1977-06-11", "1978-06-10", "1979-06-09"]
    page = (ROOT / "scripts/this_week_jun_12_template.tpl").read_text(encoding="utf-8")
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
