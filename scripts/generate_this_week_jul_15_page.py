#!/usr/bin/env python3
"""Build /blog/trivia/july-15-in-music-history/ (6G Freshness track, post 11).

For each year 1970-1979 the post takes the weekly Hot 100 number one for the chart week that
contains July 15, straight from data/billboard/hot100_weekly.json. The chart week, the
song's total weeks at number one and the week of its run that July 15 fell in are all
computed from that file. YouTube ID and radio_id come from data/radio/radio-songs.json. The
one-line story for each song is a fact read off its Wikipedia page (see SOURCES in the
template), never typed from memory.

Run: python3 scripts/generate_this_week_jul_15_page.py
"""
import html
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "blog/trivia/july-15-in-music-history/index.html"
DATE_LONG = "July 15, 2027"
DATE_ISO = "2027-07-15"
MONTH_DAY = "-07-15"

# year -> (radio_id, one-line story fact, Wikipedia-verified 2026-11-03)
PICKS = {
    1970: ("1970-11-mama-told-me-not-to-come", "Randy Newman wrote it in 1966 for Eric Burdon's first solo album, and Three Dog Night's cover took it to number one."),
    1971: ("1971-3-its-too-late-i-feel-the-earth-move", "Toni Stern wrote the lyrics and Carole King the music, and Stern later said she wrote the words in a single day after her relationship with James Taylor ended."),
    1972: ("1972-7-lean-on-me", "Bill Withers wrote it after moving to Los Angeles and missing the community ethic of his hometown, the coal mining town of Slab Fork, West Virginia."),
    1973: ("1973-8-will-it-go-round-in-circles", "Billy Preston and Bruce Fisher wrote it, and it came from Preston's 1972 album Music Is My Life."),
    1974: ("1974-38-rock-your-baby", "The backing track was recorded in 45 minutes as a demo, and George McCrae was in the studio and added his falsetto vocals."),
    1975: ("1975-1-love-will-keep-us-together", "Neil Sedaka and Howard Greenfield wrote it, and Sedaka admitted borrowing the main chord progression from the Beach Boys' \"Do It Again.\""),
    1976: ("1976-12-afternoon-delight", "Bill Danoff wrote it after seeing a happy hour menu at Clyde's in Georgetown, Washington, D.C., that was titled \"Afternoon Delights.\""),
    1977: ("1977-9-undercover-angel", "Alan O'Day called it a \"nocturnal novelette,\" and it reached number one before an album to support it was released."),
    1978: ("1978-1-shadow-dancing", "Andy Gibb wrote it with his brothers Barry, Robin and Maurice, and Albhy Galuten co-wrote and produced it."),
    1979: ("1979-2-bad-girls", "The idea came after one of Donna Summer's assistants was insulted by a police officer who thought she was a prostitute."),
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
    ("What was the number one song on July 15 in music history in the 1970s?",
     "The number one song for the Hot 100 chart week that includes July 15 changed every year. "
     "It was \"Mama Told Me (Not to Come)\" in 1970, \"It's Too Late\" in 1971, \"Lean on Me\" in 1972, "
     "\"Will It Go Round in Circles\" in 1973 and \"Rock Your Baby\" in 1974. Five more follow, ending with \"Bad Girls\" in 1979."),
    ("Which 70s number one song stayed on top the longest around July 15?",
     "Andy Gibb's \"Shadow Dancing\" had the most weeks at number one of the ten songs, with seven in a row, according to this site's weekly Hot 100 data. "
     "Carole King's \"It's Too Late\" and Donna Summer's \"Bad Girls\" were next with five weeks each, and Captain & Tennille's \"Love Will Keep Us Together\" had four."),
    ("What was the number one song on July 15, 1978?",
     "Andy Gibb's \"Shadow Dancing\" was number one for the Hot 100 chart week that began July 15, 1978. "
     "It was the fifth of its seven straight weeks at number one, according to this site's weekly Hot 100 data. "
     "It is also number one on the 1978 year-end Hot 100 in this site's data."),
    ("How can I find the number one song from my own birthday?",
     "You can find the number one song from your birthday with the Birthday #1 Song Finder on this site. "
     "Enter a birthday from the 1970s and it shows the song that topped the Billboard Hot 100 that week, "
     "using the same weekly chart data as the ten songs on this page."),
    ("Why does the chart week change from year to year?",
     "This site's weekly Hot 100 file dates each chart week from a Saturday, and that date moves each year. "
     "The week containing July 15 began July 15 in 1972 and 1978, July 14 in 1973 and 1979, July 13 in 1974, "
     "July 12 in 1975, July 11 in 1970, July 10 in 1971 and 1976 and July 9 in 1977."),
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
    assert TOTAL_WEEKS == 33, TOTAL_WEEKS
    assert (len(FIRST), len(MID), len(LAST)) == (5, 3, 2), (len(FIRST), len(MID), len(LAST))
    assert [s["title"] for s in LONGEST[:5]] == ["Shadow Dancing", "It's Too Late / I Feel the Earth Move", "Bad Girls", "Love Will Keep Us Together", "Lean on Me"]
    assert [s["total"] for s in LONGEST[:5]] == [7, 5, 5, 4, 3]
    assert BY[1978]["run_first"] == "1978-06-17" and BY[1978]["run_last"] == "1978-07-29" and BY[1978]["pos"] == 5
    assert BY[1971]["run_first"] == "1971-06-19" and BY[1971]["run_last"] == "1971-07-17" and BY[1971]["pos"] == 4
    assert BY[1979]["run_first"] == "1979-07-14" and BY[1979]["run_last"] == "1979-08-11" and BY[1979]["pos"] == 1
    assert BY[1975]["pos"] == 4 == BY[1975]["total"] and BY[1975]["run_first"] == "1975-06-21"
    assert sum(1 for s in SONGS if s["total"] == 1) == 1
    assert all(s["offs"] == list(range(s["total"])) for s in SONGS), "unbroken runs expected"
    assert [s["week_start"] for s in SONGS] == [
        "1970-07-11", "1971-07-10", "1972-07-15", "1973-07-14", "1974-07-13",
        "1975-07-12", "1976-07-10", "1977-07-09", "1978-07-15", "1979-07-14"]
    page = (ROOT / "scripts/this_week_jul_15_template.tpl").read_text(encoding="utf-8")
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
