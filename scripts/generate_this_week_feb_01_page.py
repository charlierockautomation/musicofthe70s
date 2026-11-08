#!/usr/bin/env python3
"""Build /blog/trivia/february-1-in-music-history/ (6G Freshness track, post 14).

For each year 1970-1979 the post takes the weekly Hot 100 number one for the chart week that
contains February 1, straight from data/billboard/hot100_weekly.json. The chart week, the
song's total weeks at number one and the week of its run that February 1 fell in are all
computed from that file. YouTube ID and radio_id come from data/radio/radio-songs.json. The
one-line story for each song is a fact read off its Wikipedia page (see SOURCES in the
template), never typed from memory.

Repeat note: "Le Freak" (1979 slot here) is also on the December 12 page (1978 slot there).
Charlie said to build post 14 on 2026-11-07; the repeat is flagged for him at review.

Run: python3 scripts/generate_this_week_feb_01_page.py
"""
import html
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "blog/trivia/february-1-in-music-history/index.html"
DATE_LONG = "February 1, 2027"
DATE_ISO = "2027-02-01"
MONTH_DAY = "-02-01"

# year -> (radio_id, one-line story fact, Wikipedia-verified 2026-11-07)
PICKS = {
    1970: ("1970-28-i-want-you-back", "It was first considered for Gladys Knight & the Pips and later Diana Ross, and an 11-year-old Michael Jackson sang lead."),
    1971: ("1971-10-knock-three-times", "Tony Orlando sang lead, but the record was credited simply to Dawn, a name taken from a Bell Records executive's daughter."),
    1972: ("1972-3-american-pie", "At 8 minutes and 42 seconds, it held the record for almost 50 years as the longest song to reach number one."),
    1973: ("1973-26-superstition", "Jeff Beck came up with the opening drum beat, and Wonder played the riff on a Hohner Clavinet."),
    1974: ("1974-31-youre-sixteen", "The Sherman Brothers wrote it, and Paul McCartney sang a \"kazoo\" vocal solo on Ringo Starr's version."),
    1975: ("1975-9-laughter-in-the-rain", "It came out in the US on Elton John's Rocket label and was Sedaka's first Hot 100 number one since 1962."),
    1976: ("1976-30-love-rollercoaster", "An urban legend says a scream on the record was a real murder, but a band member credits the screech to Billy Beck."),
    1977: ("1977-26-car-wash", "Norman Whitfield got the idea watching basketball and wrote the first draft on a paper bag from a fried chicken place."),
    1978: ("1978-7-baby-come-back", "Peter Beckett and J. C. Crowley wrote it after two of the band members had broken up with their girlfriends."),
    1979: ("1979-3-le-freak", "Wikipedia says it was the first song to reach number one on the Hot 100 three separate times."),
}

# Runs that were broken up by another song (checked against Wikipedia and the weekly file)
SPLIT = {"Le Freak"}

RADIO = {s["radio_id"]: s for s in json.loads((ROOT / "data/radio/radio-songs.json").read_text())}
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
        radio = RADIO[rid]
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
    ("What was the number one song on February 1 in music history in the 1970s?",
     "The number one song for the Hot 100 chart week that includes February 1 changed every year. "
     "It was \"I Want You Back\" in 1970, \"Knock Three Times\" in 1971, \"American Pie\" in 1972, "
     "\"Superstition\" in 1973 and \"You're Sixteen\" in 1974. Five more follow, ending with \"Le Freak\" in 1979."),
    ("Which 70s number one song stayed on top the longest around February 1?",
     "Chic's \"Le Freak\" had the most weeks at number one of the ten songs, with six, according to this site's weekly Hot 100 data. "
     "They came in three separate runs between December 9, 1978 and February 3, 1979. "
     "Don McLean's \"American Pie\" had four weeks in a row, from January 15 to February 5, 1972."),
    ("What was the number one song on February 1, 1975?",
     "Neil Sedaka's \"Laughter in the Rain\" was number one for the Hot 100 chart week that began February 1, 1975. "
     "It was the first and only week of its run at number one, according to this site's weekly Hot 100 data. "
     "It is number 9 on the 1975 year-end Hot 100 in this site's data."),
    ("How can I find the number one song from my own birthday?",
     "You can find the number one song from your birthday with the Birthday #1 Song Finder on this site. "
     "Enter a birthday from the 1970s and it shows the song that topped the Billboard Hot 100 that week, "
     "using the same weekly chart data as the ten songs on this page."),
    ("Why does the chart week change from year to year?",
     "This site's weekly Hot 100 file dates each chart week from a Saturday, and that date moves each year. "
     "The week containing February 1 began February 1 in 1975, January 31 in 1970 and 1976, January 30 in 1971, "
     "January 29 in 1972 and 1977, January 28 in 1978, January 27 in 1973 and 1979 and January 26 in 1974."),
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
    # Rows in the weekly file are the source of truth. "Le Freak" has 6 rows in three runs but
    # weeks_at_number_one says 3 (same as on the December 12 page). "Superstition" has 1 row but
    # weeks_at_number_one says 2; Wikipedia's 1973 number-ones list shows one week (January 27 issue).
    assert all(s["json_weeks"] == s["total"] for s in SONGS if s["year"] not in (1973, 1979)), "weeks_at_number_one disagrees with run length"
    assert BY[1973]["json_weeks"] == 2 and BY[1973]["total"] == 1
    assert BY[1979]["json_weeks"] == 3 and BY[1979]["total"] == 6 and BY[1979]["offs"] == [0, 2, 3, 6, 7, 8]
    assert TOTAL_WEEKS == 22, TOTAL_WEEKS
    assert (len(FIRST), len(MID), len(LAST)) == (6, 3, 1), (len(FIRST), len(MID), len(LAST))
    assert all(s["total"] == 1 for s in FIRST)
    assert [s["title"] for s in LONGEST[:4]] == ["Le Freak", "American Pie", "Knock Three Times", "Baby Come Back"]
    assert [s["total"] for s in LONGEST] == [6, 4, 3, 3, 1, 1, 1, 1, 1, 1]
    assert BY[1979]["run_first"] == "1978-12-09" and BY[1979]["run_last"] == "1979-02-03" and BY[1979]["pos"] == 5
    assert BY[1972]["run_first"] == "1972-01-15" and BY[1972]["run_last"] == "1972-02-05" and BY[1972]["pos"] == 3
    assert BY[1971]["run_first"] == "1971-01-23" and BY[1971]["run_last"] == "1971-02-06" and BY[1971]["pos"] == 2
    assert BY[1978]["run_first"] == "1978-01-14" and BY[1978]["run_last"] == "1978-01-28" and BY[1978]["pos"] == 3
    assert [s["title"] for s in SONGS if s["offs"] != list(range(s["total"]))] == ["Le Freak"]
    assert [s["week_start"] for s in SONGS] == [
        "1970-01-31", "1971-01-30", "1972-01-29", "1973-01-27", "1974-01-26",
        "1975-02-01", "1976-01-31", "1977-01-29", "1978-01-28", "1979-01-27"]
    assert [s["ye_rank"] for s in SONGS] == [28, 10, 3, 26, 31, 9, 30, 26, 7, 3]
    page = (ROOT / "scripts/this_week_feb_01_template.tpl").read_text(encoding="utf-8")
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
