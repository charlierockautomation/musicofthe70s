#!/usr/bin/env python3
"""Build /blog/songs/70s-road-trip-songs/ (6F Listening page, Road Trip Songs).

The 30 songs come from data/radio/radio-songs.json (vibe tag "drive", embeddable YouTube ID),
and none repeats on the 70s Party, Dance or Love Songs pages (asserted below). Year, year-end
rank, genre, YouTube ID and radio_id are read from that file, never typed here. Every
weeks-at-#1 figure, chart date and neighbouring number one is computed from
data/billboard/hot100_weekly.json. Songs that never reached #1 get their year-end rank (a
rank, never called a peak) with the two songs ranked either side of them that year.

Run: python3 scripts/generate_70s_road_trip_songs_page.py
"""
import html
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_70s_love_songs_page import artist_slug  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "blog/songs/70s-road-trip-songs/index.html"
DATE_LONG = "October 24, 2026"
DATE_ISO = "2026-10-24"

# (radio_id, Songs post slug or None); #1 status and story are computed from the data files
PICKS = [
    ("1970-89-travelin-band", None),
    ("1970-14-hitchin-a-ride", None),
    ("1970-85-vehicle", None),
    ("1971-8-take-me-home-country-roads", "take-me-home-country-roads"),
    ("1971-11-me-and-bobby-mcgee", None),
    ("1971-99-riders-on-the-storm", None),
    ("1972-27-a-horse-with-no-name", None),
    ("1972-45-city-of-new-orleans", None),
    ("1972-69-hot-rod-lincoln", None),
    ("1972-89-motorcycle-mama", None),
    ("1973-2-bad-bad-leroy-brown", "bad-bad-leroy-brown"),
    ("1973-41-long-train-runnin", None),
    ("1973-79-ramblin-man", None),
    ("1973-23-were-an-american-band", None),
    ("1974-64-radar-love", None),
    ("1974-22-band-on-the-run", None),
    ("1974-91-helen-wheels", None),
    ("1974-77-jet", None),
    ("1974-63-takin-care-of-business", None),
    ("1975-48-chevy-van", None),
    ("1975-85-the-rockford-files-theme", None),
    ("1976-57-convoy", None),
    ("1976-85-slow-ride", None),
    ("1977-62-jet-airliner", None),
    ("1977-52-dont-stop", None),
    ("1977-74-lido-shuffle", None),
    ("1978-82-running-on-empty", None),
    ("1978-26-baker-street", None),
    ("1979-61-sultans-of-swing", None),
    ("1979-50-the-devil-went-down-to-georgia", None),
]

RADIO = json.loads((ROOT / "data/radio/radio-songs.json").read_text())
RADIO_BY_ID = {s["radio_id"]: s for s in RADIO}
WEEKLY = json.loads((ROOT / "data/billboard/hot100_weekly.json").read_text())
SEQ = sorted((r for y in WEEKLY.values() for r in y), key=lambda r: r["week_start"])
GENRE_LABEL = {"classic-rock": "Classic rock", "soft-rock": "Soft rock", "hard-rock": "Hard rock",
               "country": "Country", "pop": "Pop", "soul": "Soul", "funk": "Funk", "disco": "Disco"}
NUM = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight"}


def long_date(iso):
    d = date.fromisoformat(iso)
    return f"{d.strftime('%B')} {d.day}, {d.year}"


def run_for(title, artist):
    first_word = artist.replace("&", "and").split()[0].lower()
    idx = [k for k, r in enumerate(SEQ) if r["title"].lower() == title.lower()
           and first_word in r["artist"].lower()]
    if not idx:
        return None
    a, b = idx[0], idx[-1]
    return {"weeks": len(idx), "first": SEQ[a]["week_start"], "contiguous": b - a + 1 == len(idx),
            "prev": SEQ[a - 1]["title"], "next": SEQ[b + 1]["title"]}


def year_end_neighbours(year, rank):
    by_rank = {s["rank"]: s["title"] for s in RADIO if s["year"] == year}
    return by_rank.get(rank - 1), by_rank.get(rank + 1)


def story(s):
    run = s["run"]
    if not run:
        up, down = year_end_neighbours(s["year"], s["rank"])
        base = f"Number {s['rank']} on the {s['year']} year-end Hot 100"
        if up and down:
            return f"{base}, between \"{up}\" at {s['rank'] - 1} and \"{down}\" at {s['rank'] + 1}."
        return f"{base}."
    w, d = run["weeks"], long_date(run["first"])
    wk = f"{NUM[w]} week{'s' if w > 1 else ''}"
    if not run["contiguous"]:
        return f"{wk} at number one in all, first reaching the top on {d}."
    if run["prev"] == run["next"]:
        return f"{wk} at number one from {d}, a short break inside the run of \"{run['prev']}.\""
    return f"{wk} at number one from {d}, after \"{run['prev']}\" and before \"{run['next']}.\""


def load_songs():
    songs = []
    for rid, slug in PICKS:
        r = RADIO_BY_ID[rid]
        run = run_for(r["title"], r["artist"])
        s = {"radio_id": rid, "title": r["title"], "artist": r["artist"], "year": r["year"],
             "rank": r["rank"], "yt": r["youtube_id"], "genre": r["genre"], "slug": slug,
             "run": run, "n1": bool(run), "weeks": run["weeks"] if run else 0}
        s["story"] = story(s)
        songs.append(s)
    return songs


SONGS = load_songs()
N = len(SONGS)
N1 = sum(s["n1"] for s in SONGS)
BY = {s["radio_id"]: s for s in SONGS}
N1_ROWS = sorted((s for s in SONGS if s["n1"]), key=lambda s: (-s["weeks"], s["run"]["first"]))
POOL = sum(1 for s in RADIO if s.get("youtube_id") and "drive" in s.get("vibe", []))
ERAS = [("1970 to 1973", 1970, 1973), ("1974 to 1976", 1974, 1976),
        ("1977 and 1978", 1977, 1978), ("1979", 1979, 1979)]
WORDS = [("Ride, Riders", r"\bride\b|\briders\b"), ("Run, Runnin', Running", r"\brun\b|runnin|running"),
         ("Road, Street, Highway", r"\broads?\b|\bstreet\b|highway"),
         ("Vehicles and wheels", r"\bvan\b|vehicle|wheels|lincoln|motorcycle|jet\b|airliner|train|convoy")]
GENRES = Counter(s["genre"] for s in SONGS)
GENRE_ORDER = sorted(GENRES, key=lambda g: (-GENRES[g], g))


def esc(s):
    return html.escape(s, quote=True)


def used_ids():
    out = set()
    for name in ("party", "dance", "love"):
        src = (ROOT / f"scripts/generate_70s_{name}_songs_page.py").read_text()
        out |= set(re.findall(r'^\s+\("(\d{4}-[^"]+)"', src, re.M))
    return out


def table_rows():
    slugs = [p.parent.name for p in (ROOT / "blog/artists").glob("*/index.html")]
    out = []
    for s in SONGS:
        t, a = esc(s["title"]), esc(s["artist"])
        play = (f'<button type="button" class="ohw-play" data-yt="{s["yt"]}" data-title="{t} by {a}" '
                f'aria-label="Play {t} by {a} here">&#9654; Play</button>')
        song_cell = f'<a href="/blog/songs/{s["slug"]}/">{t}</a>' if s["slug"] else t
        asl = artist_slug(s["artist"], slugs)
        artist_cell = f'<a href="/blog/artists/{asl}/">{a}</a>' if asl else a
        out.append(
            f'<tr><td class="ohw-listen">{play}</td><td class="ohw-song">{song_cell}</td>'
            f'<td class="ohw-artist">{artist_cell}</td><td data-sort="{s["year"]}">{s["year"]}</td>'
            f'<td data-sort="{s["rank"]}">{s["rank"]}</td><td>{"Yes" if s["n1"] else "No"}</td>'
            f'<td class="love-story">{esc(s["story"])}</td></tr>')
    return "\n".join("              " + r for r in out)


def long_rows():
    rows = []
    for i, s in enumerate(N1_ROWS):
        cls = ' class="row-highlight"' if i == 0 else ""
        rows.append(f'              <tr{cls}><td>{esc(s["title"])}</td><td>{esc(s["artist"])}</td>'
                    f'<td>{s["weeks"]}</td><td>{long_date(s["run"]["first"])}</td></tr>')
    return "\n".join(rows)


def word_rows():
    rows = []
    for label, pat in WORDS:
        hit = [s for s in SONGS if re.search(pat, s["title"], re.I)]
        names = ", ".join(f'"{esc(s["title"])}"' for s in hit)
        rows.append(f'              <tr><td>{label}</td><td>{len(hit)}</td><td>{names}</td></tr>')
    return "\n".join(rows)


def genre_rows():
    rows = []
    for i, g in enumerate(GENRE_ORDER):
        hit = [s for s in SONGS if s["genre"] == g]
        cls = ' class="row-highlight"' if i == 0 else ""
        rows.append(f'              <tr{cls}><td>{GENRE_LABEL[g]}</td><td>{len(hit)}</td>'
                    f'<td>{sum(s["n1"] for s in hit)}</td></tr>')
    return "\n".join(rows)


def era_rows():
    rows = []
    top = max(sum(1 for s in SONGS if a <= s["year"] <= b) for _, a, b in ERAS)
    for label, a, b in ERAS:
        hit = [s for s in SONGS if a <= s["year"] <= b]
        cls = ' class="row-highlight"' if len(hit) == top else ""
        rows.append(f'              <tr{cls}><td>{label}</td><td>{len(hit)}</td><td>{sum(s["n1"] for s in hit)}</td></tr>')
    return "\n".join(rows)


def not_n1_list():
    items = []
    for s in SONGS:
        if not s["n1"]:
            items.append(f'          <li>"{esc(s["title"])}" by {esc(s["artist"])}: number {s["rank"]} on the {s["year"]} year-end Hot 100.</li>')
    return "\n".join(items)


FAQ = [
    ("What are the best 70s road trip songs?",
     "The best 70s road trip songs on this list include John Denver's \"Take Me Home, Country Roads,\" Golden Earring's "
     "\"Radar Love,\" America's \"A Horse with No Name\" and Jackson Browne's \"Running on Empty.\" All {N} are checked "
     "against Billboard chart data, and every one can be played from the table at the top of the page, one after another."),
    ("What is the number one road trip song of the 70s?",
     "America's \"A Horse with No Name\" has the longest run at number one on this list, with three weeks from "
     "March 25, 1972. Six of the {N} songs reached number one on the weekly Billboard Hot 100 file on this site."),
    ("Do 70s road trip songs have to be about driving?",
     "No, this list mixes songs that name a road, a ride or a vehicle in the title with songs picked from the drive "
     "vibe tag in this site's song data. Only the title words are counted on this page, so no song's meaning is guessed."),
    ("Did every 70s road trip song on this list reach number one?",
     "No, {N1} of the {N} road trip songs on this list reached number one on the Billboard Hot 100. The other "
     "{NOT_N1} are year-end Hot 100 entries, including \"Take Me Home, Country Roads\" at number 8 for 1971 and "
     "\"Baker Street\" at number 26 for 1978."),
    ("Where can I listen to 70s road trip songs?",
     "You can play all {N} 70s road trip songs from the table at the top of this page, with no sign-in. Press Play on "
     "any row and the list continues song after song until you press Stop. You can also open the same songs on "
     "Listen Now, this site's 70s music player."),
]


def fill(text):
    for k, v in {"{N}": str(N), "{N1}": str(N1), "{NOT_N1}": str(N - N1)}.items():
        text = text.replace(k, v)
    return text


def faq_schema():
    items = []
    for q, a in FAQ:
        a = fill(a)
        items.append('      {\n        "@type": "Question",\n        "name": %s,\n        "acceptedAnswer": {\n'
                     '          "@type": "Answer",\n          "text": %s\n        }\n      }'
                     % (json.dumps(q, ensure_ascii=False), json.dumps(a, ensure_ascii=False)))
    return ",\n".join(items)


def faq_html():
    out = []
    for q, a in FAQ:
        out.append(f'          <div class="faq-item">\n            <h3>{html.escape(q, quote=False)}</h3>\n'
                   f'            <p>{html.escape(fill(a), quote=False)}</p>\n          </div>')
    return "\n".join(out)


def main():
    assert N == 30, N
    assert len({s["radio_id"] for s in SONGS}) == N
    assert not (used_ids() & {s["radio_id"] for s in SONGS}), "overlaps Party, Dance or Love Songs"
    assert all("drive" in RADIO_BY_ID[s["radio_id"]]["vibe"] for s in SONGS)
    assert BY["1972-27-a-horse-with-no-name"]["weeks"] == 3
    assert BY["1973-2-bad-bad-leroy-brown"]["weeks"] == 2
    assert BY["1974-22-band-on-the-run"]["n1"] and not BY["1971-8-take-me-home-country-roads"]["n1"]
    assert N1 == 6, N1
    assert Counter(x["year"] for x in SONGS).most_common(1) == [(1974, 5)]
    assert [BY[k]["rank"] for k in ("1974-22-band-on-the-run", "1974-77-jet", "1974-91-helen-wheels")] == [22, 77, 91]
    assert GENRES == {"classic-rock": 17, "country": 4, "pop": 4, "soft-rock": 3, "hard-rock": 2}
    page = (ROOT / "scripts/road_trip_songs_template.tpl").read_text(encoding="utf-8")
    top_era = max(ERAS, key=lambda e: sum(1 for s in SONGS if e[1] <= s["year"] <= e[2]))
    top_g = GENRE_ORDER[0]
    rep = {
        "{{ROWS}}": table_rows(), "{{LONG_ROWS}}": long_rows(), "{{WORD_ROWS}}": word_rows(),
        "{{GENRE_ROWS}}": genre_rows(), "{{ERA_ROWS}}": era_rows(), "{{NOT_N1_LIST}}": not_n1_list(),
        "{{FAQ_SCHEMA}}": faq_schema(), "{{FAQ_HTML}}": faq_html(),
        "{{POOL}}": str(POOL), "{{N}}": str(N), "{{N1}}": str(N1), "{{NOT_N1}}": str(N - N1),
        "{{DATE_LONG}}": DATE_LONG, "{{DATE_ISO}}": DATE_ISO,
        "{{TOP_GENRE}}": GENRE_LABEL[top_g].lower(), "{{TOP_GENRE_N}}": str(GENRES[top_g]),
        "{{TOP_ERA}}": top_era[0],
        "{{TOP_ERA_N}}": str(sum(1 for s in SONGS if top_era[1] <= s["year"] <= top_era[2])),
        "{{OVERLAP}}": str(sum(1 for s in RADIO if s.get("youtube_id") and "drive" in s.get("vibe", [])
                               and s["radio_id"] in used_ids())),
    }
    for k, v in rep.items():
        page = page.replace(k, v)
    assert "{{" not in page, "unfilled placeholder"
    PAGE.parent.mkdir(parents=True, exist_ok=True)
    PAGE.write_text(page, encoding="utf-8")
    print(f"{N} songs, {N1} number ones, pool {POOL}, top genre {top_g} {GENRES[top_g]}, top era {top_era[0]}")
    print(dict(GENRES))
    for label, pat in WORDS:
        print(label, [s["title"] for s in SONGS if re.search(pat, s["title"], re.I)])
    print({l: sum(1 for s in SONGS if a <= s["year"] <= b) for l, a, b in ERAS})


if __name__ == "__main__":
    main()
