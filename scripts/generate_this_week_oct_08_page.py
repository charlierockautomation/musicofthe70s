#!/usr/bin/env python3
"""Build /blog/trivia/october-8-in-music-history/ (6G Freshness track, post 15).

For each year 1970-1979 the post takes the weekly Hot 100 number one for the chart week that
contains October 8, straight from data/billboard/hot100_weekly.json. The chart week, the
song's total weeks at number one and the week of its run that October 8 fell in are all
computed from that file. YouTube ID and radio_id come from data/radio/radio-songs.json. The
one-line story for each song is a fact read off its Wikipedia page (see SOURCES in the
template), never typed from memory.

Repeat note: after posts 1-14 no calendar date had fewer than two repeats. "Maggie May"
(1971) and "Kiss You All Over" (1978) are also on the October 24 page. Charlie chose
October 8 with two repeats on 2026-11-07; both are named on the page.

Run: python3 scripts/generate_this_week_oct_08_page.py
"""
import html
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "blog/trivia/october-8-in-music-history/index.html"
DATE_LONG = "October 8, 2027"
DATE_ISO = "2027-10-08"
MONTH_DAY = "-10-08"

# year -> (radio_id, one-line story fact, Wikipedia-verified 2026-11-07)
PICKS = {
    1970: ("1970-6-aint-no-mountain-high-enough", "Ashford and Simpson had Ross re-record the 1967 Marvin Gaye and Tammi Terrell duet, and it became her first solo number one."),
    1971: ("1971-2-maggie-may-reason-to-believe", "Ray Jackson of Lindisfarne played the mandolin, and the album credited him only as \"the mandolin player in Lindisfarne.\""),
    1972: ("1972-8-baby-dont-get-hooked-on-me", "Davis wrote it when the record company demanded he write a tune with a \"hook.\""),
    1973: ("1973-20-half-breed", "Cher recorded it on May 21, 1973, with Wrecking Crew session players, and it became her second solo US number one."),
    1974: ("1974-97-i-honestly-love-you", "Jeff Barry and Peter Allen wrote it, and it won Record of the Year at the 17th Grammy Awards."),
    1975: ("1975-8-fame", "John Lennon came up with the hook by singing \"aim\" over Carlos Alomar's guitar riff, and Bowie turned it into \"Fame.\""),
    1976: ("1976-5-play-that-funky-music", "Rob Parissi wrote it in about five minutes, after a club patron asked the rock band to play some funky music."),
    1977: ("1977-71-star-wars-theme-cantina-band", "It was one of two Star Wars hits, with John Williams's own \"Star Wars (Main Title)\" in the Top 10 at the same time."),
    1978: ("1978-5-kiss-you-all-over", "Casey Kasem reported that writer Mike Chapman named Barry White's \"It's Ecstasy When You Lay Down Next to Me\" as his inspiration."),
    1979: ("1979-10-sad-eyes", "It ended the six-week reign of The Knack's \"My Sharona\" at number one."),
}

# Runs that were broken up by another song (checked against Wikipedia and the weekly file)
SPLIT = {"Fame"}

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
    ("What was the number one song on October 8 in music history in the 1970s?",
     "The number one song for the Hot 100 chart week that includes October 8 changed every year. "
     "It was \"Ain't No Mountain High Enough\" in 1970, \"Maggie May\" in 1971, \"Baby, Don't Get Hooked on Me\" in 1972, "
     "\"Half-Breed\" in 1973 and \"I Honestly Love You\" in 1974. Five more follow, ending with \"Sad Eyes\" in 1979."),
    ("Which 70s number one song stayed on top the longest around October 8?",
     "Rod Stewart's \"Maggie May\" had the most weeks at number one of the ten songs, with five, according to this site's weekly Hot 100 data. "
     "They ran from October 2 to October 30, 1971. "
     "Exile's \"Kiss You All Over\" was next with four weeks, from September 30 to October 21, 1978."),
    ("What was the number one song on October 8, 1977?",
     "Meco's \"Star Wars Theme/Cantina Band\" was number one for the Hot 100 chart week that began October 8, 1977. "
     "It was the second and last week of its run at number one, according to this site's weekly Hot 100 data. "
     "It is number 71 on the 1977 year-end Hot 100 in this site's data."),
    ("How can I find the number one song from my own birthday?",
     "You can find the number one song from your birthday with the Birthday #1 Song Finder on this site. "
     "Enter a birthday from the 1970s and it shows the song that topped the Billboard Hot 100 that week, "
     "using the same weekly chart data as the ten songs on this page."),
    ("Why does the chart week change from year to year?",
     "This site's weekly Hot 100 file dates each chart week from a Saturday, and that date moves each year. "
     "The week containing October 8 began October 8 in 1977, October 7 in 1972 and 1978, October 6 in 1973 and 1979, "
     "October 5 in 1974, October 4 in 1975, October 3 in 1970 and October 2 in 1971 and 1976."),
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
    # Rows in the weekly file are the source of truth; here weeks_at_number_one agrees with the rows for all ten.
    assert all(s["json_weeks"] == s["total"] for s in SONGS), "weeks_at_number_one disagrees with run length"
    assert TOTAL_WEEKS == 27, TOTAL_WEEKS
    assert (len(FIRST), len(MID), len(LAST)) == (4, 1, 5), (len(FIRST), len(MID), len(LAST))
    assert [s["title"] for s in FIRST] == ["Maggie May / Reason to Believe", "Half-Breed", "I Honestly Love You", "Sad Eyes"]
    assert [s["title"] for s in LONGEST[:2]] == ["Maggie May / Reason to Believe", "Kiss You All Over"]
    assert [s["total"] for s in LONGEST] == [5, 4, 3, 3, 3, 2, 2, 2, 2, 1]
    # "Fame": Wikipedia says it displaced "Rhinestone Cowboy" the week of September 20, 1975, dropped behind
    # John Denver's "I'm Sorry" for a week, then returned for one final week before "Bad Blood".
    assert BY[1975]["offs"] == [0, 2] and BY[1975]["pos"] == 2
    assert BY[1975]["run_first"] == "1975-09-20" and BY[1975]["run_last"] == "1975-10-04"
    assert [r["title"] for r in SEQ if r["week_start"] == "1975-09-27"] == ["I'm Sorry"]
    assert [s["title"] for s in SONGS if s["offs"] != list(range(s["total"]))] == ["Fame"]
    assert BY[1971]["run_first"] == "1971-10-02" and BY[1971]["run_last"] == "1971-10-30" and BY[1971]["pos"] == 1
    assert BY[1978]["run_first"] == "1978-09-30" and BY[1978]["run_last"] == "1978-10-21" and BY[1978]["pos"] == 2
    assert BY[1970]["run_first"] == "1970-09-19" and BY[1970]["pos"] == 3
    assert BY[1972]["run_first"] == "1972-09-23" and BY[1972]["pos"] == 3
    assert BY[1976]["run_first"] == "1976-09-18" and BY[1976]["pos"] == 3
    assert BY[1977]["run_first"] == "1977-10-01" and BY[1977]["pos"] == 2
    # "Sad Eyes" ended the six-week run of "My Sharona" (Wikipedia); the weekly file agrees.
    assert [r["title"] for r in SEQ if r["week_start"] == "1979-09-29"] == ["My Sharona"]
    assert sum(1 for r in SEQ if r["title"] == "My Sharona") == 6
    assert [s["week_start"] for s in SONGS] == [
        "1970-10-03", "1971-10-02", "1972-10-07", "1973-10-06", "1974-10-05",
        "1975-10-04", "1976-10-02", "1977-10-08", "1978-10-07", "1979-10-06"]
    assert [s["ye_rank"] for s in SONGS] == [6, 2, 8, 20, 97, 8, 5, 71, 5, 10]
    page = (ROOT / "scripts/this_week_oct_08_template.tpl").read_text(encoding="utf-8")
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
