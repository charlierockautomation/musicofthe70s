#!/usr/bin/env python3
"""Build /blog/trivia/november-19-in-music-history/ (6G Freshness track, post 18).

For each year 1970-1979 the post takes the weekly Hot 100 number one for the chart week that
contains November 19, straight from data/billboard/hot100_weekly.json. The chart week, the
song's total weeks at number one and the week of its run that November 19 fell in are all
computed from that file. YouTube ID and radio_id come from data/radio/radio-songs.json, or
data/radio/number-one-videos.json for the two songs not in the radio file. The one-line story
for each song is a fact read off its Wikipedia page (see SOURCES in the template), never
typed from memory.

Date rule (Charlie 2026-11-08): a This Week in Music History post covers the real week it
publishes, and lists every number one from that week. Songs are never dropped or swapped
because they appear on another date post. Seven of these ten are also on the November 12
page, and four are also on the November 28 page.

Run: python3 scripts/generate_this_week_nov_19_page.py
"""
import html
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "blog/trivia/november-19-in-music-history/index.html"
DATE_LONG = "November 19, 2026"
DATE_ISO = "2026-11-19"
MONTH_DAY = "-11-19"

# year -> (radio_id or None, one-line story fact, Wikipedia-verified 2026-11-08).
# Each line is a different fact from the ones already used on other date pages.
PICKS = {
    1970: ("1970-7-ill-be-there", "Michael Jackson turned 12 the day after Motown released it, and it was the group's last Hot 100 number one."),
    1971: ("1971-39-gypsys-tramps-thieves", "It was Cher's first single in four years to chart higher than number 84, and her album was renamed after it."),
    1972: ("1972-47-i-can-see-clearly-now", "Francis Monkman played the instrumental break on a Moog synthesizer."),
    1973: ("1973-35-keep-on-truckin", "Leonard Caston and Frank Wilson produced it, and the album version runs eight minutes."),
    1974: (None, "Elton John played piano and sang harmony on it, and he bet Lennon it would reach number one."),
    1975: ("1976-65-island-girl", "Elton John sang uncredited on \"Bad Blood,\" the Neil Sedaka hit it replaced at number one."),
    1976: ("1977-1-tonights-the-night-gonna-be-alright", "It held number one for eight weeks, the longest US run for a single since \"Hey Jude\" in 1968."),
    1977: ("1978-3-you-light-up-my-life", "It topped Record World's singles chart for 13 weeks, three more than its Hot 100 run."),
    1978: ("1979-12-macarthur-park", "Giorgio Moroder recorded his own voice to make the choir heard behind Summer on the chorus."),
    1979: (None, "It was the Commodores' last number one in the United States, with \"Such a Woman\" on the B-side."),
}

# Runs that were broken up by another song (checked against the weekly file): none this week.
SPLIT = set()
# weeks_at_number_one in the weekly file disagrees with its own rows here; the rows (8) match
# Wikipedia's "eight consecutive weeks", so the rows stay the source of truth.
JSON_WEEKS_WRONG = {"Tonight's the Night (Gonna Be Alright)": 7}

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
    ("What was the number one song on November 19 in music history in the 1970s?",
     "The Hot 100 number one for the week that includes November 19 changed every year. "
     "From 1970 to 1974 it was \"I'll Be There,\" \"Gypsys, Tramps & Thieves,\" \"I Can See Clearly Now,\" "
     "\"Keep on Truckin'\" and \"Whatever Gets You thru the Night.\" "
     "From 1975 to 1979 it was \"Island Girl,\" \"Tonight's the Night,\" \"You Light Up My Life,\" "
     "\"MacArthur Park\" and \"Still.\""),
    ("Which song was number one the week of November 19, 1976?",
     "Rod Stewart's \"Tonight's the Night (Gonna Be Alright)\" was number one for the Hot 100 chart week that began "
     "November 13, 1976. "
     "That was the first of its eight weeks on top, and it stayed there until the chart week of January 1, 1977, "
     "according to this site's weekly Hot 100 data."),
    ("What was John Lennon's only solo number one in his lifetime?",
     "\"Whatever Gets You thru the Night\" was John Lennon's only solo number one single in the United States during "
     "his lifetime, according to Wikipedia. "
     "It held the top spot for one week, the chart week of November 16, 1974, which contains November 19."),
    ("How can I find the number one song from my own birthday?",
     "You can find the number one song from your birthday with the Birthday #1 Song Finder on this site. "
     "Enter a birthday from the 1970s and it shows the song that topped the Billboard Hot 100 that week, "
     "using the same weekly chart data as the ten songs on this page."),
    ("Why are so many of these songs also on the November 12 list?",
     "November 12 and November 19 are one week apart, and long runs at number one often carried a song across both "
     "chart weeks. "
     "Seven songs appear on both lists. "
     "Only 1974, 1976 and 1979 had a new number one by November 19."),
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
    # Rows in the weekly file are the source of truth; weeks_at_number_one only disagrees where listed.
    for s in SONGS:
        if s["title"] in JSON_WEEKS_WRONG:
            assert (s["json_weeks"], s["total"]) == (JSON_WEEKS_WRONG[s["title"]], 8), s["title"]
        else:
            assert s["json_weeks"] == s["total"], ("weeks_at_number_one disagrees with run length", s["title"])
    assert TOTAL_WEEKS == 39, TOTAL_WEEKS
    assert (len(FIRST), len(MID), len(LAST)) == (3, 3, 4), (len(FIRST), len(MID), len(LAST))
    assert [s["title"] for s in FIRST] == ["Whatever Gets You thru the Night", "Tonight's the Night (Gonna Be Alright)", "Still"]
    assert [s["title"] for s in MID] == ["I Can See Clearly Now", "You Light Up My Life", "MacArthur Park"]
    assert [s["title"] for s in LAST] == ["I'll Be There", "Gypsys, Tramps & Thieves", "Keep on Truckin'", "Island Girl"]
    assert [s["total"] for s in LONGEST] == [10, 8, 5, 4, 3, 3, 2, 2, 1, 1]
    assert all(s["offs"] == list(range(s["total"])) for s in SONGS), "unexpected split run"
    assert [s["week_start"] for s in SONGS] == [
        "1970-11-14", "1971-11-13", "1972-11-18", "1973-11-17", "1974-11-16",
        "1975-11-15", "1976-11-13", "1977-11-19", "1978-11-18", "1979-11-17"]
    assert [s["pos"] for s in SONGS] == [5, 2, 3, 2, 1, 3, 1, 6, 2, 1]
    assert BY[1970]["run_first"] == "1970-10-17" and BY[1970]["run_last"] == "1970-11-14"
    assert BY[1971]["run_first"] == "1971-11-06" and BY[1971]["run_last"] == "1971-11-13"
    assert BY[1972]["run_first"] == "1972-11-04" and BY[1972]["run_last"] == "1972-11-25"
    assert BY[1973]["run_first"] == "1973-11-10" and BY[1973]["run_last"] == "1973-11-17"
    assert BY[1975]["run_first"] == "1975-11-01" and BY[1975]["run_last"] == "1975-11-15"
    assert BY[1976]["run_first"] == "1976-11-13" and BY[1976]["run_last"] == "1977-01-01"
    assert BY[1977]["run_first"] == "1977-10-15" and BY[1977]["run_last"] == "1977-12-17"
    assert BY[1978]["run_first"] == "1978-11-11" and BY[1978]["run_last"] == "1978-11-25"
    # Neighbours named in the prose, read off the weekly file.
    nb = {r["week_start"]: r["title"] for r in SEQ}
    assert nb["1970-10-10"] == "Cracklin' Rosie" and nb["1970-11-21"] == "I Think I Love You"
    assert nb["1971-10-30"].startswith("Maggie May") and nb["1971-11-20"] == "Theme from Shaft"
    assert nb["1972-10-28"] == "My Ding-a-Ling" and nb["1972-12-02"] == "Papa Was a Rollin' Stone"
    assert nb["1973-11-03"] == "Midnight Train to Georgia" and nb["1973-11-24"] == "Photograph"
    assert nb["1974-11-09"] == "You Ain't Seen Nothing Yet" and nb["1974-11-23"] == "I Can Help"
    assert nb["1975-10-25"] == "Bad Blood" and nb["1975-11-22"] == "That's the Way (I Like It)"
    assert nb["1976-11-06"] == "Rock'n Me" and nb["1977-01-08"] == "You Don't Have to Be a Star (To Be in My Show)"
    assert nb["1977-10-08"] == "Star Wars Theme/Cantina Band" and nb["1977-12-24"] == "How Deep Is Your Love"
    assert nb["1978-11-04"] == "You Needed Me" and nb["1978-12-02"] == "You Don't Bring Me Flowers"
    assert nb["1979-11-10"] == "Heartache Tonight" and nb["1979-11-24"] == "No More Tears (Enough Is Enough)"
    assert [s["ye_rank"] for s in SONGS] == [7, 39, 47, 35, None, 65, 1, 3, 12, None]
    assert [s["ye_year"] for s in SONGS] == [1970, 1971, 1972, 1973, None, 1976, 1977, 1978, 1979, None]
    page = (ROOT / "scripts/this_week_nov_19_template.tpl").read_text(encoding="utf-8")
    rep = {
        "{{ROWS}}": table_rows(), "{{LONG_ROWS}}": long_rows(), "{{DATE_LIST}}": date_list(),
        "{{FAQ_SCHEMA}}": faq_schema(), "{{FAQ_HTML}}": faq_html(),
        "{{TOTAL_WEEKS}}": str(TOTAL_WEEKS), "{{N_FIRST}}": str(len(FIRST)), "{{N_MID}}": str(len(MID)),
        "{{N_LAST}}": str(len(LAST)), "{{DATE_LONG}}": DATE_LONG, "{{DATE_ISO}}": DATE_ISO,
    }
    for k, v in rep.items():
        page = page.replace(k, v)
    assert "{{" not in page, "unfilled placeholder"
    PAGE.parent.mkdir(parents=True, exist_ok=True)
    PAGE.write_text(page, encoding="utf-8")
    print(f"10 songs, {TOTAL_WEEKS} weeks at #1, first-week {len(FIRST)}, mid-run {len(MID)}, last-week {len(LAST)}")


if __name__ == "__main__":
    main()
