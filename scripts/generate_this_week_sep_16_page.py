#!/usr/bin/env python3
"""Build /blog/trivia/september-16-in-music-history/ (6G Freshness track, post 13).

For each year 1970-1979 the post takes the weekly Hot 100 number one for the chart week that
contains September 16, straight from data/billboard/hot100_weekly.json. The chart week, the
song's total weeks at number one and the week of its run that September 16 fell in are all
computed from that file. YouTube ID and radio_id come from data/radio/radio-songs.json. The
one-line story for each song is a fact read off its Wikipedia page (see SOURCES in the
template), never typed from memory.

Run: python3 scripts/generate_this_week_sep_16_page.py
"""
import html
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "blog/trivia/september-16-in-music-history/index.html"
DATE_LONG = "September 16, 2027"
DATE_ISO = "2027-09-16"
MONTH_DAY = "-09-16"

# year -> (radio_id, one-line story fact, Wikipedia-verified 2026-11-06)
PICKS = {
    1970: ("1970-5-war", "Motown held back the Temptations' version as a single, so Edwin Starr re-recorded it, and it became his only number one."),
    1971: ("1971-7-go-away-little-girl", "Bobby Vee recorded it first in 1962, and Wikipedia calls it the first song to reach number one by two different artists."),
    1972: ("1972-63-black-and-white", "Pete Seeger made the first recording in 1956, and the Supreme Court's Brown v. Board of Education decision inspired the song."),
    1973: ("1973-14-delta-dawn", "Alex Harvey wrote it about his mother, and producer Tom Catalano offered the vocal to Barbra Streisand before Helen Reddy."),
    1974: ("1974-76-i-shot-the-sheriff", "Bob Marley wrote it for the Wailers, and Clapton's cover is his only number one on the Hot 100."),
    1975: ("1975-2-rhinestone-cowboy", "The week of September 13 it topped the country chart and the Hot 100 at once, a first since \"Big Bad John\" in 1961."),
    1976: ("1976-26-shake-shake-shake-shake-your-booty", "Its B-side, \"Boogie Shoes,\" became a hit on its own after it appeared on the Saturday Night Fever soundtrack."),
    1977: ("1977-3-best-of-my-love", "Maurice White and Al McKay of Earth, Wind & Fire wrote it, and it won a Grammy at the 20th Annual Grammy Awards."),
    1978: ("1978-9-boogie-oogie-oogie", "It was the first certified Platinum single in Capitol Records history, and Janice-Marie Johnson sang lead while playing slap bass."),
    1979: ("1979-1-my-sharona", "Doug Fieger met 17-year-old Sharona Alperin, who inspired the song, and he said he wrote it in 15 minutes."),
}

# Runs that were broken up by another song (checked against Wikipedia and the weekly file)
SPLIT = {"Best of My Love"}

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
    ("What was the number one song on September 16 in music history in the 1970s?",
     "The number one song for the Hot 100 chart week that includes September 16 changed every year. "
     "It was \"War\" in 1970, \"Go Away Little Girl\" in 1971, \"Black and White\" in 1972, "
     "\"Delta Dawn\" in 1973 and \"I Shot the Sheriff\" in 1974. Five more follow, ending with \"My Sharona\" in 1979."),
    ("Which 70s number one song stayed on top the longest around September 16?",
     "The Knack's \"My Sharona\" had the most weeks at number one of the ten songs, with six, according to this site's weekly Hot 100 data. "
     "They ran from August 25 to September 29, 1979. The Emotions' \"Best of My Love\" had five weeks, split by one week of Andy Gibb's \"I Just Want to Be Your Everything.\""),
    ("What was the number one song on September 16, 1972?",
     "Three Dog Night's \"Black and White\" was number one for the Hot 100 chart week that began September 16, 1972. "
     "It was the first and only week of its run at number one, according to this site's weekly Hot 100 data. "
     "It is number 63 on the 1972 year-end Hot 100 in this site's data."),
    ("How can I find the number one song from my own birthday?",
     "You can find the number one song from your birthday with the Birthday #1 Song Finder on this site. "
     "Enter a birthday from the 1970s and it shows the song that topped the Billboard Hot 100 that week, "
     "using the same weekly chart data as the ten songs on this page."),
    ("Why does the chart week change from year to year?",
     "This site's weekly Hot 100 file dates each chart week from a Saturday, and that date moves each year. "
     "The week containing September 16 began September 16 in 1972 and 1978, September 15 in 1973 and 1979, September 14 in 1974, "
     "September 13 in 1975, September 12 in 1970, September 11 in 1971 and 1976 and September 10 in 1977."),
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
    assert TOTAL_WEEKS == 26, TOTAL_WEEKS
    assert (len(FIRST), len(MID), len(LAST)) == (5, 3, 2), (len(FIRST), len(MID), len(LAST))
    assert [s["title"] for s in LONGEST[:3]] == ["My Sharona", "Best of My Love", "War"]
    assert [s["total"] for s in LONGEST] == [6, 5, 3, 3, 3, 2, 1, 1, 1, 1]
    assert BY[1979]["run_first"] == "1979-08-25" and BY[1979]["run_last"] == "1979-09-29" and BY[1979]["pos"] == 4
    assert BY[1977]["run_first"] == "1977-08-20" and BY[1977]["run_last"] == "1977-09-24" and BY[1977]["pos"] == 4
    assert BY[1970]["pos"] == 3 == BY[1970]["total"] and BY[1971]["pos"] == 1 and BY[1978]["pos"] == 2
    assert BY[1975]["pos"] == 2 == BY[1975]["total"]
    assert sum(1 for s in SONGS if s["total"] == 1) == 4
    assert [s["title"] for s in SONGS if s["offs"] != list(range(s["total"]))] == ["Best of My Love"]
    assert [s["week_start"] for s in SONGS] == [
        "1970-09-12", "1971-09-11", "1972-09-16", "1973-09-15", "1974-09-14",
        "1975-09-13", "1976-09-11", "1977-09-10", "1978-09-16", "1979-09-15"]
    assert [s["ye_rank"] for s in SONGS] == [5, 7, 63, 14, 76, 2, 26, 3, 9, 1]
    page = (ROOT / "scripts/this_week_sep_16_template.tpl").read_text(encoding="utf-8")
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
