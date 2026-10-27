#!/usr/bin/env python3
"""Build /blog/trivia/march-20-in-music-history/ (6G Freshness track, post 7).

For each year 1970-1979 the post takes the weekly Hot 100 number one for the chart week that
contains March 20, straight from data/billboard/hot100_weekly.json. The chart week, the
song's total weeks at number one and the week of its run that March 20 fell in are all
computed from that file. YouTube ID and radio_id come from data/radio/radio-songs.json. The
one-line story for each song is a fact read off its Wikipedia page (see SOURCES in the
template), never typed from memory.

Run: python3 scripts/generate_this_week_mar_20_page.py
"""
import html
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "blog/trivia/march-20-in-music-history/index.html"
DATE_LONG = "March 20, 2027"
DATE_ISO = "2027-03-20"
MONTH_DAY = "-03-20"

# year -> (radio_id, one-line story fact, Wikipedia-verified 2026-10-26)
PICKS = {
    1970: (None, "Paul Simon wrote it, Art Garfunkel sang lead, and it won Record of the Year and Song of the Year at the 1971 Grammys."),
    1971: ("1971-11-me-and-bobby-mcgee", "Kris Kristofferson wrote it, and Wikipedia calls Janis Joplin's version the second posthumously released number one single in US chart history."),
    1972: ("1972-17-heart-of-gold", "Neil Young recorded it in Nashville with James Taylor and Linda Ronstadt on backing vocals, and Wikipedia calls it his only US number one."),
    1973: ("1973-3-killing-me-softly-with-his-song", "Charles Fox and Norman Gimbel wrote it, and Wikipedia says Lori Lieberman was inspired by a Don McLean performance in late 1971."),
    1974: ("1974-2-seasons-in-the-sun", "Rod McKuen wrote the English lyrics in 1963 for Jacques Brel's 1961 Belgian song \"Le Moribond.\""),
    1975: ("1975-16-black-water", "Patrick Simmons wrote it and sings lead, and Wikipedia calls it the first of the Doobie Brothers' two number one singles."),
    1976: ("1976-4-december-1963-oh-what-a-night", "Its first lyrics were about the 1933 repeal of Prohibition, and drummer Gerry Polci sings lead on the verses."),
    1977: ("1977-4-evergreen-love-theme-from-a-star-is-born", "Barbra Streisand wrote the music and Paul Williams the lyrics, and it won the Academy Award for Best Original Song."),
    1978: ("1978-2-night-fever", "The Bee Gees had already written it when asked for a song called \"Saturday Night,\" and they persuaded Robert Stigwood to rename the film Saturday Night Fever."),
    1979: ("1979-6-i-will-survive", "Freddie Perren and Dino Fekaris wrote it, and it was first released as the B-side of \"Substitute.\""),
}

# Runs that were broken up by another song (checked against Wikipedia)
SPLIT = {"Killing Me Softly with His Song", "I Will Survive"}

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
    ("What was the number one song on March 20 in music history in the 1970s?",
     "The number one song for the Hot 100 chart week that includes March 20 changed every year. "
     "It was \"Bridge over Troubled Water\" in 1970, \"Me and Bobby McGee\" in 1971, \"Heart of Gold\" in 1972, "
     "\"Killing Me Softly with His Song\" in 1973 and \"Seasons in the Sun\" in 1974. Five more follow, ending with \"I Will Survive\" in 1979."),
    ("Which 70s number one song stayed on top the longest around March 20?",
     "The Bee Gees' \"Night Fever\" held the longest run of the ten songs, with eight weeks, according to this site's weekly Hot 100 data. "
     "It ran from March 18 to May 6, 1978. Simon & Garfunkel's \"Bridge over Troubled Water\" is second with six weeks, and Roberta Flack's \"Killing Me Softly with His Song\" is third with five."),
    ("What was the number one song on March 20, 1971?",
     "Janis Joplin's \"Me and Bobby McGee\" was number one for the Hot 100 chart week that began March 20, 1971. "
     "It was the first of its two weeks at number one, according to this site's weekly Hot 100 data. "
     "Wikipedia calls it the second posthumously released number one single in US chart history, and it is number 11 on the 1971 year-end Hot 100."),
    ("How can I find the number one song from my own birthday?",
     "You can find the number one song from your birthday with the Birthday #1 Song Finder on this site. "
     "Enter a birthday from the 1970s and it shows the song that topped the Billboard Hot 100 that week, "
     "using the same weekly chart data as the ten songs on this page."),
    ("Why does the chart week change from year to year?",
     "This site's weekly Hot 100 file dates each chart week from a Saturday, and that date moves each year. "
     "The week containing March 20 began March 20 in 1971 and 1976, March 19 in 1977, March 18 in 1972 and 1978, "
     "March 17 in 1973 and 1979, March 16 in 1974, March 15 in 1975 and March 14 in 1970."),
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
    assert TOTAL_WEEKS == 35, TOTAL_WEEKS
    assert (len(FIRST), len(MID), len(LAST)) == (4, 4, 2), (len(FIRST), len(MID), len(LAST))
    assert [s["title"] for s in LONGEST[:3]] == ["Night Fever", "Bridge over Troubled Water", "Killing Me Softly with His Song"]
    assert [s["total"] for s in LONGEST[:3]] == [8, 6, 5]
    assert BY[1978]["run_first"] == "1978-03-18" and BY[1978]["run_last"] == "1978-05-06" and BY[1978]["pos"] == 1
    assert BY[1970]["run_first"] == "1970-02-28" and BY[1970]["pos"] == 3 and BY[1974]["pos"] == 3 == BY[1974]["total"]
    assert BY[1973]["offs"] == [0, 1, 2, 3, 5] and BY[1979]["offs"] == [0, 1, 4]
    assert sum(1 for s in SONGS if s["total"] == 1) == 2
    assert [s["week_start"] for s in SONGS] == [
        "1970-03-14", "1971-03-20", "1972-03-18", "1973-03-17", "1974-03-16",
        "1975-03-15", "1976-03-20", "1977-03-19", "1978-03-18", "1979-03-17"]
    page = (ROOT / "scripts/this_week_mar_20_template.tpl").read_text(encoding="utf-8")
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
