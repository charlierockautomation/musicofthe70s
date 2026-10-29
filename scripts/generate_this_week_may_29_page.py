#!/usr/bin/env python3
"""Build /blog/trivia/may-29-in-music-history/ (6G Freshness track, post 9).

For each year 1970-1979 the post takes the weekly Hot 100 number one for the chart week that
contains May 29, straight from data/billboard/hot100_weekly.json. The chart week, the
song's total weeks at number one and the week of its run that May 29 fell in are all
computed from that file. YouTube ID and radio_id come from data/radio/radio-songs.json. The
one-line story for each song is a fact read off its Wikipedia page (see SOURCES in the
template), never typed from memory.

Run: python3 scripts/generate_this_week_may_29_page.py
"""
import html
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "blog/trivia/may-29-in-music-history/index.html"
DATE_LONG = "May 29, 2027"
DATE_ISO = "2027-05-29"
MONTH_DAY = "-05-29"

# year -> (radio_id, one-line story fact, Wikipedia-verified 2026-10-28)
PICKS = {
    1970: ("1970-3-american-woman", "The music and lyrics were improvised on stage during a concert in Southern Ontario, and the band asked a kid with a cassette recorder for his bootleg tape."),
    1971: ("1971-16-brown-sugar", "Mick Jagger wrote it during the filming of Ned Kelly in 1969, and the Stones recorded it over three days at Muscle Shoals Sound Studio in Alabama."),
    1972: ("1972-13-oh-girl", "Eugene Record wrote it, sang lead and produced it, and a harmonica carries the song."),
    1973: ("1973-16-frankenstein", "Drummer Chuck Ruff named it after the massive editing of the original studio recording, which was spliced together from many sections."),
    1974: ("1974-8-the-streak", "Ray Stevens got the idea from a news magazine item about streaking that he read on an airplane."),
    1975: ("1975-7-shining-star", "Maurice White got the idea while strolling at night and looking up at the starry sky during the That's the Way of the World sessions."),
    1976: ("1976-15-love-hangover", "Producer Hal Davis had a strobe light installed so that Diana Ross could get into a disco mindset, and it gave her a fourth number one."),
    1977: ("1977-18-sir-duke", "Stevie Wonder wrote it as a tribute to Duke Ellington, who had died in 1974."),
    1978: ("1978-18-with-a-little-luck", "Paul McCartney wrote it in Scotland, and Wings recorded it aboard a boat in the Virgin Islands that had been fitted with a 24-track studio."),
    1979: ("1979-5-reunited", "Dino Fekaris and Freddie Perren wrote it as a sequel to the duo's 1968 hit \"(We'll Be) United.\""),
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
    ("What was the number one song on May 29 in music history in the 1970s?",
     "The number one song for the Hot 100 chart week that includes May 29 changed every year. "
     "It was \"American Woman\" in 1970, \"Brown Sugar\" in 1971, \"Oh Girl\" in 1972, "
     "\"Frankenstein\" in 1973 and \"The Streak\" in 1974. Five more follow, ending with \"Reunited\" in 1979."),
    ("Which 70s number one song stayed on top the longest around May 29?",
     "Peaches & Herb's \"Reunited\" held the longest run of the ten songs, with four weeks, according to this site's weekly Hot 100 data. "
     "It ran from May 5 to May 26, 1979. The Guess Who's \"American Woman,\" Ray Stevens' \"The Streak\" and Stevie Wonder's \"Sir Duke\" tie for second with three weeks each."),
    ("What was the number one song on May 29, 1971?",
     "The Rolling Stones' \"Brown Sugar\" was number one for the Hot 100 chart week that began May 29, 1971. "
     "It was the first of its two weeks at number one, according to this site's weekly Hot 100 data. "
     "Billboard ranked it number 16 for 1971, which matches the 1971 year-end Hot 100 in this site's data."),
    ("How can I find the number one song from my own birthday?",
     "You can find the number one song from your birthday with the Birthday #1 Song Finder on this site. "
     "Enter a birthday from the 1970s and it shows the song that topped the Billboard Hot 100 that week, "
     "using the same weekly chart data as the ten songs on this page."),
    ("Why does the chart week change from year to year?",
     "This site's weekly Hot 100 file dates each chart week from a Saturday, and that date moves each year. "
     "The week containing May 29 began May 29 in 1971 and 1976, May 28 in 1977, May 27 in 1972 and 1978, "
     "May 26 in 1973 and 1979, May 25 in 1974, May 24 in 1975 and May 23 in 1970."),
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
    assert TOTAL_WEEKS == 22, TOTAL_WEEKS
    assert (len(FIRST), len(MID), len(LAST)) == (5, 2, 3), (len(FIRST), len(MID), len(LAST))
    assert [s["title"] for s in LONGEST[:4]] == ["Reunited", "American Woman / No Sugar Tonight", "The Streak", "Sir Duke"]
    assert [s["total"] for s in LONGEST[:4]] == [4, 3, 3, 3]
    assert BY[1979]["run_first"] == "1979-05-05" and BY[1979]["run_last"] == "1979-05-26" and BY[1979]["pos"] == 4
    assert BY[1971]["run_first"] == "1971-05-29" and BY[1971]["run_last"] == "1971-06-05" and BY[1971]["pos"] == 1
    assert BY[1970]["pos"] == 3 == BY[1970]["total"] and BY[1977]["pos"] == 2 and BY[1977]["total"] == 3
    assert sum(1 for s in SONGS if s["total"] == 1) == 3
    assert [s["week_start"] for s in SONGS] == [
        "1970-05-23", "1971-05-29", "1972-05-27", "1973-05-26", "1974-05-25",
        "1975-05-24", "1976-05-29", "1977-05-28", "1978-05-27", "1979-05-26"]
    page = (ROOT / "scripts/this_week_may_29_template.tpl").read_text(encoding="utf-8")
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
