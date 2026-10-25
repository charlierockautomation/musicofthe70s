#!/usr/bin/env python3
"""Build /blog/trivia/this-week-in-music-history-october-24/ (6G Freshness track, post 1).

For each year 1970-1979 the post takes the weekly Hot 100 number one for the chart week that
contains October 24, straight from data/billboard/hot100_weekly.json. The chart week, the
song's total weeks at number one and the week of its run that October 24 fell in are all
computed from that file. YouTube ID and radio_id come from data/radio/radio-songs.json. The
one-line story for each song is a fact read off its Wikipedia page (see SOURCES in the
template), never typed from memory.

Run: python3 scripts/generate_this_week_oct_24_page.py
"""
import html
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "blog/trivia/this-week-in-music-history-october-24/index.html"
DATE_LONG = "October 24, 2026"
DATE_ISO = "2026-10-24"
MONTH_DAY = "-10-24"

# year -> (radio_id, one-line story fact, Wikipedia-verified 2026-10-24)
PICKS = {
    1970: ("1970-7-ill-be-there", "The Jackson 5's fourth number one in a row."),
    1971: ("1971-2-maggie-may-reason-to-believe", "The B-side of \"Reason to Believe\" that radio flipped."),
    1972: ("1972-15-my-ding-a-ling", "A live recording from Coventry, England, and Chuck Berry's only number one."),
    1973: ("1973-85-angie", "Lead single from Goats Head Soup, cut in Kingston, Jamaica."),
    1974: ("1974-37-nothing-from-nothing", "Billy Preston's second solo number one."),
    1975: ("1975-93-bad-blood", "Elton John sings backing vocals, uncredited."),
    1976: ("1976-48-if-you-leave-me-now", "Chicago's first number one, written and sung by Peter Cetera."),
    1977: ("1978-3-you-light-up-my-life", "Ten weeks at the top, a Hot 100 record at the time."),
    1978: ("1978-5-kiss-you-all-over", "The strings were played on a synthesizer."),
    1979: ("1979-80-rise", "An instrumental written by Herb Alpert's nephew Randy and Andy Armer."),
}

RADIO = {s["radio_id"]: s for s in json.loads((ROOT / "data/radio/radio-songs.json").read_text())}
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
        radio = RADIO[rid]
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
    ("What was the number one song this week in music history in the 1970s?",
     "The number one song for the Hot 100 chart week that includes October 24 was \"I'll Be There\" in 1970, "
     "\"Maggie May\" in 1971, \"My Ding-a-Ling\" in 1972, \"Angie\" in 1973 and \"Nothing From Nothing\" in 1974. "
     "It was \"Bad Blood\" in 1975, \"If You Leave Me Now\" in 1976, \"You Light Up My Life\" in 1977, "
     "\"Kiss You All Over\" in 1978 and \"Rise\" in 1979."),
    ("Which 70s number one song stayed on top the longest around October 24?",
     "Debby Boone's \"You Light Up My Life\" stayed on top the longest, with ten weeks at number one from "
     "October 15 to December 17, 1977, according to this site's weekly Hot 100 data. Wikipedia says that "
     "was a record for most weeks at number one on the Hot 100 at the time."),
    ("What was the number one song on October 24, 1975?",
     "Neil Sedaka's \"Bad Blood\" was number one for the Hot 100 chart week of October 18 to 24, 1975. "
     "It was the second of three weeks at the top. Elton John sang uncredited backing vocals on the "
     "record, which Neil Sedaka wrote with Phil Cody."),
    ("How can I find the number one song from my own birthday?",
     "You can find the number one song from your birthday with the Birthday #1 Song Finder on this site. "
     "Enter a birthday from the 1970s and it shows the song that topped the Billboard Hot 100 that week, "
     "using the same weekly chart data as the ten songs on this page."),
    ("Why does the chart week change from year to year?",
     "This site's weekly Hot 100 file dates each chart week from a Saturday, and that date moves each year. "
     "The week containing October 24 began October 24 in 1970, October 23 in 1971 and 1976, October 22 in 1977, "
     "October 21 in 1972 and 1978, October 20 in 1973 and 1979, October 19 in 1974 and October 18 in 1975."),
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
    assert TOTAL_WEEKS == 35, TOTAL_WEEKS
    assert (len(FIRST), len(MID), len(LAST)) == (5, 4, 1), (len(FIRST), len(MID), len(LAST))
    assert LONGEST[0]["title"] == "You Light Up My Life" and LONGEST[0]["total"] == 10
    assert BY[1977]["run_first"] == "1977-10-15" and BY[1977]["run_last"] == "1977-12-17"
    assert BY[1970]["run_first"] == "1970-10-17" and BY[1970]["run_last"] == "1970-11-14"
    assert BY[1976]["week_start"] == "1976-10-23" and BY[1978]["run_first"] == "1978-09-30"
    assert BY[1975]["week_start"] == "1975-10-18" and BY[1975]["week_end"] == "1975-10-24" and BY[1975]["pos"] == 2
    assert BY[1978]["pos"] == 4 and BY[1971]["pos"] == 4 and BY[1971]["total"] == 5
    assert BY[1977]["ye_year"] == 1978 and BY[1977]["ye_rank"] == 3
    assert BY[1978]["ye_rank"] == 5 and BY[1979]["ye_rank"] == 80
    assert [s["week_start"] for s in SONGS] == [
        "1970-10-24", "1971-10-23", "1972-10-21", "1973-10-20", "1974-10-19",
        "1975-10-18", "1976-10-23", "1977-10-22", "1978-10-21", "1979-10-20"]
    page = (ROOT / "scripts/this_week_oct_24_template.tpl").read_text(encoding="utf-8")
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
