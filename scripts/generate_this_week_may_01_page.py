#!/usr/bin/env python3
"""Build /blog/trivia/may-1-in-music-history/ (6G Freshness track, post 16).

For each year 1970-1979 the post takes the weekly Hot 100 number one for the chart week that
contains May 1, straight from data/billboard/hot100_weekly.json. The chart week, the song's
total weeks at number one and the week of its run that May 1 fell in are all computed from
that file. YouTube ID and radio_id come from data/radio/radio-songs.json. The one-line story
for each song is a fact read off its Wikipedia page (see SOURCES in the template), never
typed from memory.

Repeat note: after posts 1-15 no calendar date had fewer than three repeats. "Joy to the
World" (1971), "The First Time Ever I Saw Your Face" (1972) and "Night Fever" (1978) are also
on the April 17 page, and "Night Fever" is on the March 20 page too. Charlie chose May 1 with
three repeats on 2026-11-07; all three are named on the page.

Run: python3 scripts/generate_this_week_may_01_page.py
"""
import html
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "blog/trivia/may-1-in-music-history/index.html"
DATE_LONG = "May 1, 2027"
DATE_ISO = "2027-05-01"
MONTH_DAY = "-05-01"

# year -> (radio_id, one-line story fact, Wikipedia-verified 2026-11-07)
PICKS = {
    1970: ("1970-15-abc", "Motown's writing and production team The Corporation wrote and produced it, and the session players went uncredited under Motown policy."),
    1971: ("1971-1-joy-to-the-world", "All seven members of Three Dog Night sang on it, not only the band's three lead singers."),
    1972: ("1972-1-the-first-time-ever-i-saw-your-face", "Flack recorded it in February 1969 for her debut album First Take, much slower than Peggy Seeger's original."),
    1973: ("1973-1-tie-a-yellow-ribbon-round-the-ole-oak-tree", "It sold 3 million records in the US in three weeks and was the top-selling single of 1973 in the US and UK."),
    1974: ("1974-7-tsop-the-sound-of-philadelphia", "Gamble and Huff wrote it as the theme for Soul Train, and it was the first TV theme song to reach number one on the Hot 100."),
    1975: ("1975-18-hey-wont-you-play-another-somebody-done-somebody-wrong-song", "It was the longest title of any single to top the Hot 100 up to that time."),
    1976: ("1976-36-let-your-love-flow", "It was the debut single by the Bellamy Brothers, and it also went to number one in Germany."),
    1977: ("1977-22-southern-nights", "Allen Toussaint wrote it from childhood memories of visiting relatives in the Louisiana backwoods."),
    1978: ("1978-2-night-fever", "Its string intro was inspired by Percy Faith's \"Theme from A Summer Place.\""),
    1979: ("1979-18-heart-of-glass", "Debbie Harry and Chris Stein wrote an early version called \"Once I Had a Love\" in 1974 and 1975."),
}

# Runs that were broken up by another song (checked against Wikipedia and the weekly file)
SPLIT = set()

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
    ("What was the number one song on May 1 in music history in the 1970s?",
     "The number one song for the Hot 100 chart week that includes May 1 changed every year. "
     "It was \"ABC\" in 1970, \"Joy to the World\" in 1971, \"The First Time Ever I Saw Your Face\" in 1972, "
     "\"Tie a Yellow Ribbon Round the Ole Oak Tree\" in 1973 and \"TSOP (The Sound of Philadelphia)\" in 1974. "
     "Five more follow, ending with \"Heart of Glass\" in 1979."),
    ("Which 70s number one song stayed on top the longest around May 1?",
     "The Bee Gees' \"Night Fever\" had the most weeks at number one of the ten songs, with eight, according to this site's weekly Hot 100 data. "
     "They ran from March 18 to May 6, 1978. "
     "\"Joy to the World\" in 1971 and \"The First Time Ever I Saw Your Face\" in 1972 were next, with six weeks each."),
    ("What was the number one song on May 1, 1976?",
     "The Bellamy Brothers' \"Let Your Love Flow\" was number one for the Hot 100 chart week that began May 1, 1976. "
     "It was the duo's debut single, and it held the top spot for that one week, according to this site's weekly Hot 100 data. "
     "John Sebastian's \"Welcome Back\" took over the next week."),
    ("How can I find the number one song from my own birthday?",
     "You can find the number one song from your birthday with the Birthday #1 Song Finder on this site. "
     "Enter a birthday from the 1970s and it shows the song that topped the Billboard Hot 100 that week, "
     "using the same weekly chart data as the ten songs on this page."),
    ("Why does the chart week change from year to year?",
     "This site's weekly Hot 100 file dates each chart week from a Saturday, and that date moves each year. "
     "The week containing May 1 began May 1 in 1971 and 1976, April 30 in 1977, April 29 in 1972 and 1978, "
     "April 28 in 1973 and 1979, April 27 in 1974, April 26 in 1975 and April 25 in 1970."),
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
    assert TOTAL_WEEKS == 32, TOTAL_WEEKS
    assert (len(FIRST), len(MID), len(LAST)) == (5, 4, 1), (len(FIRST), len(MID), len(LAST))
    assert [s["title"] for s in FIRST] == ["ABC", "(Hey Won't You Play) Another Somebody Done Somebody Wrong Song",
                                           "Let Your Love Flow", "Southern Nights", "Heart of Glass"]
    assert [s["title"] for s in MID] == ["Joy to the World", "The First Time Ever I Saw Your Face",
                                         "Tie a Yellow Ribbon Round the Ole Oak Tree", "Night Fever"]
    assert [s["title"] for s in LAST] == ["TSOP (The Sound of Philadelphia)"]
    assert [s["total"] for s in LONGEST] == [8, 6, 6, 4, 2, 2, 1, 1, 1, 1]
    assert [s["title"] for s in LONGEST[:3]] == ["Night Fever", "Joy to the World", "The First Time Ever I Saw Your Face"]
    assert all(s["offs"] == list(range(s["total"])) for s in SONGS), "unexpected split run"
    assert [s["week_start"] for s in SONGS] == [
        "1970-04-25", "1971-05-01", "1972-04-29", "1973-04-28", "1974-04-27",
        "1975-04-26", "1976-05-01", "1977-04-30", "1978-04-29", "1979-04-28"]
    assert [s["pos"] for s in SONGS] == [1, 3, 3, 2, 2, 1, 1, 1, 7, 1]
    assert BY[1970]["run_first"] == "1970-04-25" and BY[1970]["run_last"] == "1970-05-02"
    assert BY[1971]["run_first"] == "1971-04-17" and BY[1971]["run_last"] == "1971-05-22"
    assert BY[1972]["run_first"] == "1972-04-15" and BY[1972]["run_last"] == "1972-05-20"
    assert BY[1973]["run_first"] == "1973-04-21" and BY[1973]["run_last"] == "1973-05-12"
    assert BY[1974]["run_first"] == "1974-04-20" and BY[1974]["run_last"] == "1974-04-27"
    assert BY[1978]["run_first"] == "1978-03-18" and BY[1978]["run_last"] == "1978-05-06"
    # Neighbours named in the prose, read off the weekly file (Night Fever's also match Wikipedia).
    nb = {r["week_start"]: r["title"] for r in SEQ}
    assert nb["1970-04-18"] == "Let It Be" and nb["1970-05-09"].startswith("American Woman")
    assert nb["1974-04-13"] == "Bennie and the Jets" and nb["1974-05-04"] == "The Loco-Motion"
    assert nb["1975-04-19"] == "Philadelphia Freedom" and nb["1975-05-03"].startswith("He Don't Love You")
    assert nb["1976-04-24"] == "Disco Lady" and nb["1976-05-08"] == "Welcome Back"
    assert nb["1977-04-23"] == "Don't Leave Me This Way" and nb["1977-05-07"] == "Hotel California"
    assert nb["1978-03-11"] == "(Love Is) Thicker Than Water" and nb["1978-05-13"] == "If I Can't Have You"
    assert nb["1979-04-21"] == "Knock on Wood" and nb["1979-05-05"] == "Reunited"
    assert [s["ye_rank"] for s in SONGS] == [15, 1, 1, 1, 7, 18, 36, 22, 2, 18]
    assert [s["ye_year"] for s in SONGS] == list(range(1970, 1980))
    page = (ROOT / "scripts/this_week_may_01_template.tpl").read_text(encoding="utf-8")
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
