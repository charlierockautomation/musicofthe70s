#!/usr/bin/env python3
"""Build /blog/trivia/august-19-in-music-history/ (6G Freshness track, post 12).

For each year 1970-1979 the post takes the weekly Hot 100 number one for the chart week that
contains August 19, straight from data/billboard/hot100_weekly.json. The chart week, the
song's total weeks at number one and the week of its run that August 19 fell in are all
computed from that file. YouTube ID and radio_id come from data/radio/radio-songs.json. The
one-line story for each song is a fact read off its Wikipedia page (see SOURCES in the
template), never typed from memory.

Run: python3 scripts/generate_this_week_aug_19_page.py
"""
import html
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "blog/trivia/august-19-in-music-history/index.html"
DATE_LONG = "August 19, 2027"
DATE_ISO = "2027-08-19"
MONTH_DAY = "-08-19"

# year -> (radio_id, one-line story fact, Wikipedia-verified 2026-11-06)
PICKS = {
    1970: ("1970-2-they-long-to-be-close-to-you", "Herb Alpert recorded it but never released his version, and Richard Carpenter added the parentheses to the title because he thought the original was too long."),
    1971: ("1971-5-how-can-you-mend-a-broken-heart", "Barry and Robin Gibb wrote it in August 1970 after the brothers reunited, and Robin said the song took about an hour to complete."),
    1972: ("1972-2-alone-again-naturally", "Biz Markie's unauthorized sample of it led to the 1991 case Grand Upright Music v. Warner Bros. Records, which affected how hip-hop producers handle samples."),
    1973: ("1973-10-touch-me-in-the-morning", "Ron Miller and Michael Masser wrote it, and Wikipedia calls it Diana Ross's second solo number one on the Hot 100."),
    1974: ("1974-47-the-night-chicago-died", "The writers said they had never been to Chicago and based the shoot-out on gangster films, and Mayor Richard Daley disliked the record."),
    1975: ("1975-12-jive-talkin", "The working title was \"Drive Talking,\" and the beat was modeled on the sound of their car crossing the Julia Tuttle Causeway on the way to the studio."),
    1976: ("1976-2-dont-go-breaking-my-heart", "Elton John and Bernie Taupin wrote it under the pseudonyms \"Ann Orson\" and \"Carte Blanche\" and first offered it to Dusty Springfield."),
    1977: ("1977-2-i-just-want-to-be-your-everything", "Barry Gibb wrote it, and The Emotions' \"Best of My Love\" interrupted its run, so its four weeks at number one came in two stretches."),
    1978: ("1978-10-three-times-a-lady", "Lionel Richie wrote it after a toast his father gave at his parents' 37th anniversary party, and he imagined Frank Sinatra singing it."),
    1979: ("1979-20-good-times", "Its bassline was recreated in \"Rapper's Delight,\" and the threat of legal action ended in a settlement and co-writer credits for Rodgers and Edwards."),
}

# Runs that were broken up by another song (checked against Wikipedia and the weekly file)
SPLIT = {"Alone Again (Naturally)", "I Just Want to Be Your Everything"}

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
    ("What was the number one song on August 19 in music history in the 1970s?",
     "The number one song for the Hot 100 chart week that includes August 19 changed every year. "
     "It was \"(They Long to Be) Close to You\" in 1970, \"How Can You Mend a Broken Heart\" in 1971, \"Alone Again (Naturally)\" in 1972, "
     "\"Touch Me in the Morning\" in 1973 and \"The Night Chicago Died\" in 1974. Five more follow, ending with \"Good Times\" in 1979."),
    ("Which 70s number one song stayed on top the longest around August 19?",
     "Gilbert O'Sullivan's \"Alone Again (Naturally)\" had the most weeks at number one of the ten songs, with six, according to this site's weekly Hot 100 data. "
     "They were split by one week of Looking Glass's \"Brandy (You're a Fine Girl).\" Four songs had four weeks each, including \"Close to You\" and \"Don't Go Breaking My Heart.\""),
    ("What was the number one song on August 19, 1978?",
     "The Commodores' \"Three Times a Lady\" was number one for the Hot 100 chart week that began August 19, 1978. "
     "It was the second and last of its two weeks at number one, according to this site's weekly Hot 100 data. "
     "It is number 10 on the 1978 year-end Hot 100 in this site's data."),
    ("How can I find the number one song from my own birthday?",
     "You can find the number one song from your birthday with the Birthday #1 Song Finder on this site. "
     "Enter a birthday from the 1970s and it shows the song that topped the Billboard Hot 100 that week, "
     "using the same weekly chart data as the ten songs on this page."),
    ("Why does the chart week change from year to year?",
     "This site's weekly Hot 100 file dates each chart week from a Saturday, and that date moves each year. "
     "The week containing August 19 began August 19 in 1972 and 1978, August 18 in 1973 and 1979, August 17 in 1974, "
     "August 16 in 1975, August 15 in 1970, August 14 in 1971 and 1976 and August 13 in 1977."),
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
    assert TOTAL_WEEKS == 29, TOTAL_WEEKS
    assert (len(FIRST), len(MID), len(LAST)) == (3, 4, 3), (len(FIRST), len(MID), len(LAST))
    assert [s["title"] for s in LONGEST[:5]] == ["Alone Again (Naturally)", "(They Long to Be) Close to You", "How Can You Mend a Broken Heart", "Don't Go Breaking My Heart", "I Just Want to Be Your Everything"]
    assert [s["total"] for s in LONGEST[:5]] == [6, 4, 4, 4, 4]
    assert BY[1972]["run_first"] == "1972-07-29" and BY[1972]["run_last"] == "1972-09-09" and BY[1972]["pos"] == 4
    assert BY[1977]["run_first"] == "1977-07-30" and BY[1977]["run_last"] == "1977-09-17" and BY[1977]["pos"] == 3
    assert BY[1970]["pos"] == 4 == BY[1970]["total"] and BY[1970]["run_first"] == "1970-07-25"
    assert BY[1971]["pos"] == 2 and BY[1976]["pos"] == 2 and BY[1978]["pos"] == 2 == BY[1978]["total"]
    assert sum(1 for s in SONGS if s["total"] == 1) == 3
    assert [s["title"] for s in SONGS if s["offs"] != list(range(s["total"]))] == ["Alone Again (Naturally)", "I Just Want to Be Your Everything"]
    assert [s["week_start"] for s in SONGS] == [
        "1970-08-15", "1971-08-14", "1972-08-19", "1973-08-18", "1974-08-17",
        "1975-08-16", "1976-08-14", "1977-08-13", "1978-08-19", "1979-08-18"]
    page = (ROOT / "scripts/this_week_aug_19_template.tpl").read_text(encoding="utf-8")
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
