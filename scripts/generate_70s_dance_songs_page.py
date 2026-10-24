#!/usr/bin/env python3
"""Build /blog/songs/70s-dance-songs/ (6F Listening page, Dance Songs).

The 30 songs come from data/radio/radio-songs.json (vibe tag "dance", embeddable YouTube ID),
and none repeats on /blog/songs/70s-party-songs/ (asserted below). Year, year-end rank, genre,
YouTube ID and radio_id are read from that file, never typed here. Every weeks-at-#1 figure,
chart date and neighbouring number one is computed from data/billboard/hot100_weekly.json,
so no story line is hand-typed. Songs that never reached #1 get only their year-end rank
(a rank, never called a peak) and their genre tag.

Run: python3 scripts/generate_70s_dance_songs_page.py
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
PAGE = ROOT / "blog/songs/70s-dance-songs/index.html"
DATE_LONG = "October 24, 2026"
DATE_ISO = "2026-10-24"

# (radio_id, Songs post slug or None); #1 status and story are computed from the weekly file
PICKS = [
    ("1970-28-i-want-you-back", "i-want-you-back"),
    ("1972-99-get-on-the-good-foot", "james-brown-get-on-the-good-foot"),
    ("1973-8-will-it-go-round-in-circles", None),
    ("1974-3-loves-theme", None),
    ("1974-5-dancing-machine", None),
    ("1974-12-jungle-boogie", None),
    ("1975-7-shining-star", None),
    ("1975-21-pick-up-the-pieces", None),
    ("1975-12-jive-talkin", "jive-talkin"),
    ("1976-15-love-hangover", None),
    ("1976-20-boogie-fever", None),
    ("1976-31-you-should-be-dancing", "you-should-be-dancing"),
    ("1976-26-shake-shake-shake-shake-your-booty", None),
    ("1976-97-disco-duck", None),
    ("1977-12-dancing-queen", "dancing-queen"),
    ("1977-7-dont-leave-me-this-way", None),
    ("1977-93-boogie-nights", None),
    ("1978-2-night-fever", "night-fever"),
    ("1978-1-shadow-dancing", None),
    ("1978-20-dance-dance-dance-yowsah-yowsah-yowsah", None),
    ("1978-54-disco-inferno", None),
    ("1979-4-da-ya-think-im-sexy", None),
    ("1979-9-ring-my-bell", None),
    ("1979-7-hot-stuff", "donna-summer-hot-stuff"),
    ("1979-2-bad-girls", "bad-girls"),
    ("1979-20-good-times", None),
    ("1979-45-hes-the-greatest-dancer", None),
    ("1979-37-i-was-made-for-dancin", None),
    ("1979-25-shake-your-body-down-to-the-ground", None),
    ("1979-91-dont-stop-til-you-get-enough", None),
]

RADIO = json.loads((ROOT / "data/radio/radio-songs.json").read_text())
RADIO_BY_ID = {s["radio_id"]: s for s in RADIO}
WEEKLY = json.loads((ROOT / "data/billboard/hot100_weekly.json").read_text())
SEQ = sorted((r for y in WEEKLY.values() for r in y), key=lambda r: r["week_start"])
GENRE_LABEL = {"disco": "Disco", "funk": "Funk", "soul": "Soul", "pop": "Pop"}
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


def story(s):
    run = s["run"]
    if not run:
        return (f"Number {s['rank']} on the {s['year']} year-end Hot 100, tagged "
                f"{GENRE_LABEL.get(s['genre'], s['genre']).lower()} in this site's song data.")
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
LONG_RUNS = sorted(((s["title"], s["weeks"]) for s in SONGS if s["weeks"] >= 2),
                   key=lambda r: (-r[1], r[0]))
POOL = sum(1 for s in RADIO if s.get("youtube_id") and "dance" in s.get("vibe", []))
ERAS = [("1970 to 1973", 1970, 1973), ("1974 to 1976", 1974, 1976),
        ("1977 and 1978", 1977, 1978), ("1979", 1979, 1979)]
WORDS = [("Dance, Dancing, Dancer, Dancin'", r"danc"), ("Boogie", r"boogie"),
         ("Shake", r"shake"), ("Disco", r"disco")]
GENRES = Counter(s["genre"] for s in SONGS)


def esc(s):
    return html.escape(s, quote=True)


def party_ids():
    src = (ROOT / "scripts/generate_70s_party_songs_page.py").read_text()
    return set(re.findall(r'^\s+\("(\d{4}-[^"]+)"', src, re.M))


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
    for i, (t, w) in enumerate(LONG_RUNS):
        s = next(x for x in SONGS if x["title"] == t)
        cls = ' class="row-highlight"' if i < 2 else ""
        rows.append(f'              <tr{cls}><td>{esc(t)}</td><td>{esc(s["artist"])}</td><td>{w}</td><td>{s["year"]}</td></tr>')
    return "\n".join(rows)


def word_rows():
    rows = []
    for label, pat in WORDS:
        hit = [s for s in SONGS if re.search(pat, s["title"], re.I)]
        names = ", ".join(f'"{esc(s["title"])}"' for s in hit)
        rows.append(f'              <tr><td>{label}</td><td>{len(hit)}</td><td>{names}</td></tr>')
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
    ("What are the best 70s dance songs?",
     "The best 70s dance songs on this list include the Bee Gees' \"Night Fever,\" Andy Gibb's \"Shadow Dancing,\" "
     "ABBA's \"Dancing Queen\" and Donna Summer's \"Bad Girls.\" All {N} are checked against Billboard chart data, "
     "and every one can be played from the table at the top of the page, one after another."),
    ("What is the number one dance song of the 70s?",
     "The longest run at number one on this list belongs to the Bee Gees' \"Night Fever,\" with eight weeks from "
     "March 18, 1978. Andy Gibb's \"Shadow Dancing\" followed with seven weeks from June 17, 1978. Both come from the "
     "weekly Billboard Hot 100 file on this site."),
    ("What is the difference between 70s dance songs and 70s party songs?",
     "A 70s dance song here is picked for the floor itself, often with dancing named in the title, while the "
     "companion party songs list leans on singalong hits. The two lists share no songs. Each has its own {N} tracks "
     "and its own player."),
    ("Did every 70s dance song on this list reach number one?",
     "No, {N1} of the {N} dance songs on this list reached number one on the Billboard Hot 100. The other "
     "{NOT_N1} are year-end Hot 100 entries, including \"Dancing Machine\" at number 5 for 1974 and \"Dance, Dance, "
     "Dance (Yowsah, Yowsah, Yowsah)\" at number 20 for 1978."),
    ("Where can I listen to 70s dance songs?",
     "You can play all {N} 70s dance songs from the table at the top of this page, with no sign-in. Press Play on "
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
    assert not (party_ids() & {s["radio_id"] for s in SONGS}), "overlaps 70s Party Songs"
    assert BY["1978-2-night-fever"]["weeks"] == 8 and BY["1978-1-shadow-dancing"]["weeks"] == 7
    assert BY["1979-2-bad-girls"]["weeks"] == 5 and BY["1979-4-da-ya-think-im-sexy"]["weeks"] == 4
    assert N1 == 21, N1
    page = (ROOT / "scripts/dance_songs_template.tpl").read_text(encoding="utf-8")
    top_era = max(ERAS, key=lambda e: sum(1 for s in SONGS if e[1] <= s["year"] <= e[2]))
    rep = {
        "{{ROWS}}": table_rows(), "{{LONG_ROWS}}": long_rows(), "{{WORD_ROWS}}": word_rows(),
        "{{ERA_ROWS}}": era_rows(), "{{NOT_N1_LIST}}": not_n1_list(),
        "{{FAQ_SCHEMA}}": faq_schema(), "{{FAQ_HTML}}": faq_html(),
        "{{POOL}}": str(POOL), "{{N}}": str(N), "{{N1}}": str(N1), "{{NOT_N1}}": str(N - N1),
        "{{DATE_LONG}}": DATE_LONG, "{{DATE_ISO}}": DATE_ISO, "{{N_LONG}}": str(len(LONG_RUNS)),
        "{{DISCO_N}}": str(GENRES["disco"]), "{{TOP_ERA}}": top_era[0],
        "{{TOP_ERA_N}}": str(sum(1 for s in SONGS if top_era[1] <= s["year"] <= top_era[2])),
        "{{DANCE_TITLES}}": str(sum(1 for s in SONGS if re.search("danc", s["title"], re.I))),
    }
    for k, v in rep.items():
        page = page.replace(k, v)
    assert "{{" not in page, "unfilled placeholder"
    PAGE.parent.mkdir(parents=True, exist_ok=True)
    PAGE.write_text(page, encoding="utf-8")
    print(f"{N} songs, {N1} number ones, pool {POOL}, top era {top_era[0]}, long runs {len(LONG_RUNS)}")


if __name__ == "__main__":
    main()
