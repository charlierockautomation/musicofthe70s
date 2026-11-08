#!/usr/bin/env python3
"""Build /blog/trivia/november-12-in-music-history/ (6G Freshness track, post 17).

For each year 1970-1979 the post takes the weekly Hot 100 number one for the chart week that
contains November 12, straight from data/billboard/hot100_weekly.json. The chart week, the
song's total weeks at number one and the week of its run that November 12 fell in are all
computed from that file. YouTube ID and radio_id come from data/radio/radio-songs.json, or
data/radio/number-one-videos.json for the two songs not in the radio file. The one-line story
for each song is a fact read off its Wikipedia page (see SOURCES in the template), never
typed from memory.

Date rule (Charlie 2026-11-08): a This Week in Music History post covers the real week it
publishes, and lists every number one from that week. Songs are never dropped or swapped
because they appear on another date post. Six of these ten are also on the November 7 page.

Run: python3 scripts/generate_this_week_nov_12_page.py
"""
import html
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "blog/trivia/november-12-in-music-history/index.html"
DATE_LONG = "November 12, 2026"
DATE_ISO = "2026-11-12"
MONTH_DAY = "-11-12"

# year -> (radio_id or None, one-line story fact, Wikipedia-verified 2026-11-08)
PICKS = {
    1970: ("1970-7-ill-be-there", "Recorded in June 1970 at Hitsville West in Los Angeles, it also topped the soul singles chart for six weeks."),
    1971: ("1971-39-gypsys-tramps-thieves", "Wrecking Crew session players backed Cher, and it was MCA's biggest-selling single at the time."),
    1972: ("1972-47-i-can-see-clearly-now", "Wikipedia says its arrangement and style are heavily laced with reggae influences."),
    1973: ("1973-35-keep-on-truckin", "It was Eddie Kendricks' only number one solo hit, two years after he left the Temptations."),
    1974: ("1975-98-you-aint-seen-nothing-yet", "Randy Bachman sang it with a stutter as a joke for his brother Gary, who had a stutter."),
    1975: ("1976-65-island-girl", "It entered the Hot 100 at number 49 on October 11, 1975, and reached the top in four weeks."),
    1976: (None, "Steve Miller recorded it at CBS studios in San Francisco, and it went to number one in Canada too."),
    1977: ("1978-3-you-light-up-my-life", "Debby Boone sang her vocal over an instrumental track already made for the film's soundtrack."),
    1978: ("1979-12-macarthur-park", "It came from Donna Summer's live double album Live and More, and it was her first Hot 100 number one."),
    1979: (None, "Bob Seger and JD Souther wrote it with Don Henley and Glenn Frey, and Frey sang lead."),
}

# Runs that were broken up by another song (checked against the weekly file): none this week.
SPLIT = set()

RADIO = {s["radio_id"]: s for s in json.loads((ROOT / "data/radio/radio-songs.json").read_text())}
NONES = {(v["title"], v["artist"]): v for v in json.loads((ROOT / "data/radio/number-one-videos.json").read_text())["videos"]}
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
        if rid:
            radio = RADIO[rid]
            assert radio["title"] == r["title"], (radio["title"], r["title"])
        else:
            radio = {"youtube_id": NONES[(r["title"], r["artist"])]["youtube_id"], "rank": None, "year": None}
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
    ("What was the number one song on November 12 in music history in the 1970s?",
     "The number one song for the Hot 100 chart week that includes November 12 changed every year. "
     "It was \"I'll Be There\" in 1970, \"Gypsys, Tramps & Thieves\" in 1971, \"I Can See Clearly Now\" in 1972, "
     "\"Keep on Truckin'\" in 1973 and \"You Ain't Seen Nothing Yet\" in 1974. "
     "The list ends with \"Island Girl,\" \"Rock'n Me,\" \"You Light Up My Life,\" \"MacArthur Park\" and \"Heartache Tonight.\""),
    ("Which 70s number one song stayed on top the longest around November 12?",
     "Debby Boone's \"You Light Up My Life\" stayed on top the longest, with ten weeks at number one from "
     "October 15 to December 17, 1977, according to this site's weekly Hot 100 data. "
     "The chart week that contains November 12 was the fifth of those ten weeks."),
    ("What was the number one song on November 12, 1978?",
     "Donna Summer's \"MacArthur Park\" was number one for the Hot 100 chart week that began November 11, 1978. "
     "It was the first of its three weeks on top, and Wikipedia calls it her first Hot 100 number one. "
     "Anne Murray's \"You Needed Me\" was on top the week before."),
    ("How can I find the number one song from my own birthday?",
     "You can find the number one song from your birthday with the Birthday #1 Song Finder on this site. "
     "Enter a birthday from the 1970s and it shows the song that topped the Billboard Hot 100 that week, "
     "using the same weekly chart data as the ten songs on this page."),
    ("Why are some of these songs also on the November 7 list?",
     "November 7 and November 12 are only five days apart, so in some years they fall in the same chart week. "
     "In other years a long run carried a song across both weeks. "
     "Six songs appear on both lists, and four are different."),
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
    assert (len(FIRST), len(MID), len(LAST)) == (6, 4, 0), (len(FIRST), len(MID), len(LAST))
    assert [s["title"] for s in FIRST] == ["Gypsys, Tramps & Thieves", "Keep on Truckin'", "You Ain't Seen Nothing Yet",
                                           "Rock'n Me", "MacArthur Park", "Heartache Tonight"]
    assert [s["title"] for s in MID] == ["I'll Be There", "I Can See Clearly Now", "Island Girl", "You Light Up My Life"]
    assert [s["total"] for s in LONGEST] == [10, 5, 4, 3, 3, 2, 2, 1, 1, 1]
    assert all(s["offs"] == list(range(s["total"])) for s in SONGS), "unexpected split run"
    assert [s["week_start"] for s in SONGS] == [
        "1970-11-07", "1971-11-06", "1972-11-11", "1973-11-10", "1974-11-09",
        "1975-11-08", "1976-11-06", "1977-11-12", "1978-11-11", "1979-11-10"]
    assert [s["pos"] for s in SONGS] == [4, 1, 2, 1, 1, 2, 1, 5, 1, 1]
    assert BY[1970]["run_first"] == "1970-10-17" and BY[1970]["run_last"] == "1970-11-14"
    assert BY[1972]["run_first"] == "1972-11-04" and BY[1972]["run_last"] == "1972-11-25"
    assert BY[1975]["run_first"] == "1975-11-01" and BY[1975]["run_last"] == "1975-11-15"
    assert BY[1977]["run_first"] == "1977-10-15" and BY[1977]["run_last"] == "1977-12-17"
    assert BY[1978]["run_first"] == "1978-11-11" and BY[1978]["run_last"] == "1978-11-25"
    # Neighbours named in the prose, read off the weekly file.
    nb = {r["week_start"]: r["title"] for r in SEQ}
    assert nb["1970-10-10"] == "Cracklin' Rosie" and nb["1970-11-21"] == "I Think I Love You"
    assert nb["1971-10-30"].startswith("Maggie May") and nb["1971-11-20"] == "Theme from Shaft"
    assert nb["1972-10-28"] == "My Ding-a-Ling" and nb["1972-12-02"] == "Papa Was a Rollin' Stone"
    assert nb["1973-11-03"] == "Midnight Train to Georgia" and nb["1973-11-24"] == "Photograph"
    assert nb["1974-11-02"] == "You Haven't Done Nothin'" and nb["1974-11-16"] == "Whatever Gets You thru the Night"
    assert nb["1975-10-25"] == "Bad Blood" and nb["1975-11-22"] == "That's the Way (I Like It)"
    assert nb["1976-10-30"] == "If You Leave Me Now" and nb["1976-11-13"].startswith("Tonight's the Night")
    assert nb["1977-10-08"] == "Star Wars Theme/Cantina Band" and nb["1977-12-24"] == "How Deep Is Your Love"
    assert nb["1978-11-04"] == "You Needed Me" and nb["1978-12-02"] == "You Don't Bring Me Flowers"
    assert nb["1979-11-03"] == "Pop Muzik" and nb["1979-11-17"] == "Still"
    assert [s["ye_rank"] for s in SONGS] == [7, 39, 47, 35, 98, 65, None, 3, 12, None]
    assert [s["ye_year"] for s in SONGS] == [1970, 1971, 1972, 1973, 1975, 1976, None, 1978, 1979, None]
    page = (ROOT / "scripts/this_week_nov_12_template.tpl").read_text(encoding="utf-8")
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
