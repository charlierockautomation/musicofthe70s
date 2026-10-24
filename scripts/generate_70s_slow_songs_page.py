#!/usr/bin/env python3
"""Build /blog/songs/70s-slow-songs/ (6F Listening page, Slow Songs).

The 30 songs are an editorial pick from data/radio/radio-songs.json (vibe tag "chill" or
"reflect", embeddable YouTube ID), three per year-end year, and none repeats on the 70s Party,
Dance, Love or Road Trip Songs pages (asserted below). Slow is a judgment call: the data holds
no tempo (BPM) field, and the page says so. Year, year-end
rank, genre, YouTube ID and radio_id are read from that file, never typed here. Every
weeks-at-#1 figure, chart date and neighbouring number one is computed from
data/billboard/hot100_weekly.json. Songs that never reached #1 get their year-end rank (a
rank, never called a peak) with the two songs ranked either side of them that year.

Run: python3 scripts/generate_70s_slow_songs_page.py
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
PAGE = ROOT / "blog/songs/70s-slow-songs/index.html"
DATE_LONG = "October 25, 2026"
DATE_ISO = "2026-10-25"

# (radio_id, Songs post slug or None); #1 status and story are computed from the data files
PICKS = [
    ("1970-1-bridge-over-troubled-water", "bridge-over-troubled-water"),
    ("1970-67-fire-and-rain", None),
    ("1970-37-rainy-night-in-georgia", None),
    ("1971-23-aint-no-sunshine", None),
    ("1971-17-youve-got-a-friend", None),
    ("1971-36-if-you-could-read-my-mind", None),
    ("1972-4-without-you", None),
    ("1972-17-heart-of-gold", None),
    ("1972-2-alone-again-naturally", None),
    ("1973-15-me-and-mrs-jones", None),
    ("1973-48-daniel", None),
    ("1973-70-yesterday-once-more", None),
    ("1974-24-time-in-a-bottle", None),
    ("1974-50-the-air-that-i-breathe", None),
    ("1974-1-the-way-we-were", None),
    ("1975-43-im-not-in-love", None),
    ("1975-20-at-seventeen", None),
    ("1975-67-you-are-so-beautiful", None),
    ("1976-40-all-by-myself", None),
    ("1976-11-sara-smile", None),
    ("1976-43-theme-from-mahogany-do-you-know-where-youre-going-to", None),
    ("1977-33-easy", None),
    ("1977-10-torn-between-two-lovers", None),
    ("1977-47-just-a-song-before-i-go", None),
    ("1978-39-dust-in-the-wind", None),
    ("1978-17-just-the-way-you-are", None),
    ("1978-38-the-closer-i-get-to-you", None),
    ("1979-26-dont-cry-out-loud", None),
    ("1979-10-sad-eyes", None),
    ("1979-29-just-when-i-needed-you-most", None),
]

RADIO = json.loads((ROOT / "data/radio/radio-songs.json").read_text())
RADIO_BY_ID = {s["radio_id"]: s for s in RADIO}
WEEKLY = json.loads((ROOT / "data/billboard/hot100_weekly.json").read_text())
SEQ = sorted((r for y in WEEKLY.values() for r in y), key=lambda r: r["week_start"])
GENRE_LABEL = {"classic-rock": "Classic rock", "soft-rock": "Soft rock", "hard-rock": "Hard rock",
               "country": "Country", "prog-rock": "Prog rock", "pop": "Pop", "soul": "Soul", "funk": "Funk", "disco": "Disco"}
NUM = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight"}


def long_date(iso):
    d = date.fromisoformat(iso)
    return f"{d.strftime('%B')} {d.day}, {d.year}"


def run_for(title, artist):
    first_word = {"Harry Nilsson": "nilsson"}.get(artist) or artist.replace("&", "and").split()[0].lower()
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
SLOW_VIBES = ("chill", "reflect")
POOL = sum(1 for s in RADIO if s.get("youtube_id") and set(s.get("vibe", [])) & set(SLOW_VIBES))
ERAS = [("1970 to 1972", 1970, 1972), ("1973 to 1975", 1973, 1975),
        ("1976 and 1977", 1976, 1977), ("1978 and 1979", 1978, 1979)]
MOOD_LABEL = {"melancholy": "Melancholy", "romantic": "Romantic", "nostalgic": "Nostalgic"}
for _s in SONGS:
    _s["mood"] = RADIO_BY_ID[_s["radio_id"]]["mood"][0]
MOODS = Counter(s["mood"] for s in SONGS)
MOOD_ORDER = sorted(MOODS, key=lambda m: (-MOODS[m], m))
GENRES = Counter(s["genre"] for s in SONGS)
GENRE_ORDER = sorted(GENRES, key=lambda g: (-GENRES[g], g))


def esc(s):
    return html.escape(s, quote=True)


def used_ids():
    out = set()
    for name in ("party", "dance", "love", "road_trip"):
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


def mood_rows():
    rows = []
    for i, m in enumerate(MOOD_ORDER):
        hit = [s for s in SONGS if s["mood"] == m]
        cls = ' class="row-highlight"' if i == 0 else ""
        names = ", ".join(f'"{esc(s["title"])}"' for s in hit) if len(hit) <= 5 else "See the list above"
        rows.append(f'              <tr{cls}><td>{MOOD_LABEL[m]}</td><td>{len(hit)}</td>'
                    f'<td>{sum(s["n1"] for s in hit)}</td><td>{names}</td></tr>')
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
    top = max(sum(s["n1"] for s in SONGS if a <= s["year"] <= b) for _, a, b in ERAS)
    for label, a, b in ERAS:
        hit = [s for s in SONGS if a <= s["year"] <= b]
        n1 = sum(s["n1"] for s in hit)
        cls = ' class="row-highlight"' if n1 == top else ""
        rows.append(f'              <tr{cls}><td>{label}</td><td>{len(hit)}</td><td>{n1}</td></tr>')
    return "\n".join(rows)


def not_n1_list():
    items = []
    for s in SONGS:
        if not s["n1"]:
            items.append(f'          <li>"{esc(s["title"])}" by {esc(s["artist"])}: number {s["rank"]} on the {s["year"]} year-end Hot 100.</li>')
    return "\n".join(items)


FAQ = [
    ("What are the best 70s slow songs?",
     "The best 70s slow songs on this list include Simon & Garfunkel's \"Bridge Over Troubled Water,\" Harry Nilsson's "
     "\"Without You,\" Jim Croce's \"Time in a Bottle\" and Kansas's \"Dust in the Wind.\" All {N} are checked "
     "against Billboard chart data, and every one can be played from the table at the top of the page, one after another."),
    ("What is the number one slow song of the 70s?",
     "Simon & Garfunkel's \"Bridge Over Troubled Water\" and Gilbert O'Sullivan's \"Alone Again (Naturally)\" share the "
     "longest runs at number one on this list, six weeks each. {N1} of the {N} slow songs reached number one on the "
     "weekly Billboard Hot 100 file on this site."),
    ("How do you decide what counts as a slow song?",
     "A slow song here is a ballad picked from the songs this site tags chill or reflect. The song data holds no tempo "
     "(BPM) field, so the choice is an editorial judgment, not a measurement. Chart facts beside each song, such as year-end "
     "rank and weeks at number one, are checked against Billboard data."),
    ("Are 70s slow songs the same as 70s love songs?",
     "No, slow songs and love songs are different lists. This list of 70s slow songs leans sad, with {MELANCHOLY} of the {N} songs "
     "carrying melancholy as their first mood tag and only {ROMANTIC} carrying romantic. None of the {N} also appears on this "
     "site's 70s love songs list."),
    ("Where can I listen to 70s slow songs?",
     "You can play all {N} songs from the table at the top of this page, with no sign-in. Press Play on any "
     "row and the list continues song after song until you press Stop. You can also open the same songs on Listen Now, "
     "this site's 70s music player."),
]


def fill(text):
    for k, v in {"{N}": str(N), "{N1}": str(N1), "{NOT_N1}": str(N - N1),
                 "{MELANCHOLY}": str(MOODS["melancholy"]), "{ROMANTIC}": str(MOODS["romantic"])}.items():
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
    assert not (used_ids() & {s["radio_id"] for s in SONGS}), "overlaps Party, Dance, Love or Road Trip Songs"
    assert all(set(RADIO_BY_ID[s["radio_id"]]["vibe"]) & set(SLOW_VIBES) for s in SONGS)
    assert Counter(s["year"] for s in SONGS) == {y: 3 for y in range(1970, 1980)}
    assert N1 == 11, N1
    assert BY["1970-1-bridge-over-troubled-water"]["weeks"] == 6
    assert BY["1972-2-alone-again-naturally"]["weeks"] == 6
    assert BY["1972-4-without-you"]["weeks"] == 4
    assert BY["1972-17-heart-of-gold"]["run"]["prev"] == "Without You"
    assert BY["1974-24-time-in-a-bottle"]["weeks"] == 2 and BY["1974-24-time-in-a-bottle"]["year"] == 1974
    assert BY["1973-15-me-and-mrs-jones"]["run"]["first"] < "1973-01-01" and BY["1973-15-me-and-mrs-jones"]["year"] == 1973
    assert BY["1978-39-dust-in-the-wind"]["rank"] == 39 and not BY["1978-39-dust-in-the-wind"]["n1"]
    assert GENRES == {"soft-rock": 18, "soul": 8, "pop": 3, "prog-rock": 1}, GENRES
    assert {g: sum(s["n1"] for s in SONGS if s["genre"] == g) for g in GENRES} == {"soft-rock": 6, "soul": 2, "pop": 3, "prog-rock": 0}
    assert sum(1 for s in SONGS if s["weeks"] == 1) == 4
    assert dict(MOODS) == {"melancholy": 21, "romantic": 5, "nostalgic": 4}, MOODS
    assert [sum(s["n1"] for s in SONGS if a <= s["year"] <= b) for _, a, b in ERAS] == [5, 3, 2, 1]
    page = (ROOT / "scripts/slow_songs_template.tpl").read_text(encoding="utf-8")
    top_g = GENRE_ORDER[0]
    top_m = MOOD_ORDER[0]
    mel_n1 = sum(s["n1"] for s in SONGS if s["mood"] == "melancholy")
    rep = {
        "{{ROWS}}": table_rows(), "{{LONG_ROWS}}": long_rows(), "{{MOOD_ROWS}}": mood_rows(),
        "{{GENRE_ROWS}}": genre_rows(), "{{ERA_ROWS}}": era_rows(), "{{NOT_N1_LIST}}": not_n1_list(),
        "{{FAQ_SCHEMA}}": faq_schema(), "{{FAQ_HTML}}": faq_html(),
        "{{POOL}}": str(POOL), "{{N}}": str(N), "{{N1}}": str(N1), "{{NOT_N1}}": str(N - N1),
        "{{DATE_LONG}}": DATE_LONG, "{{DATE_ISO}}": DATE_ISO,
        "{{TOP_GENRE}}": GENRE_LABEL[top_g].lower(), "{{TOP_GENRE_N}}": str(GENRES[top_g]),
        "{{TOP_MOOD_N}}": str(MOODS[top_m]), "{{MEL_N1}}": str(mel_n1),
        "{{OVERLAP}}": str(sum(1 for s in RADIO if s.get("youtube_id") and set(s.get("vibe", [])) & set(SLOW_VIBES)
                               and s["radio_id"] in used_ids())),
    }
    for k, v in rep.items():
        page = page.replace(k, v)
    assert "{{" not in page, "unfilled placeholder"
    PAGE.parent.mkdir(parents=True, exist_ok=True)
    PAGE.write_text(page, encoding="utf-8")
    print(f"{N} songs, {N1} number ones, pool {POOL}, top genre {top_g} {GENRES[top_g]}, moods {dict(MOODS)}, melancholy #1s {mel_n1}")


if __name__ == "__main__":
    main()
