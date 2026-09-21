#!/usr/bin/env python3
"""Regenerate the Listen Now station guide in radio/index.html.

The guide is independent, non-YouTube content: station descriptions, era
context and Billboard chart facts computed from data/radio/radio-songs.json.
Every number comes from the catalog (nothing is invented). Chart position
facts use the Year-End Hot 100 `rank` field only (billboard_peak in this
catalog just mirrors that rank, so it is NOT used).

Writes between the STATION-GUIDE:START / STATION-GUIDE:END markers.
Idempotent: safe to re-run after the catalog changes.

Usage: python3 scripts/build_radio_content.py
"""
import collections
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(ROOT, "data", "radio", "radio-songs.json")
PAGE = os.path.join(ROOT, "radio", "index.html")

# Station labels and one-line descriptions. Descriptions say what the label
# means on this site; they make no chart-history claims (those come from data).
STATIONS = {
    "pop": ("Pop", "The widest net on the dial: melodic, polished singles from the decade's chart-topping vocalists and groups."),
    "soul": ("Soul", "Vocal-driven soul and Motown-style records, from smooth ballads to uptempo cuts."),
    "soft-rock": ("Soft Rock", "Mellow, melodic rock and singer-songwriter hits that lean on harmony and warmth."),
    "classic-rock": ("Classic Rock", "Guitar-led rock and pop-rock staples from the decade's biggest rock acts."),
    "disco": ("Disco", "Dance-floor records built on a steady beat, from early disco to the late-decade peak."),
    "country": ("Country", "Country and country-pop singles that also made the Billboard Hot 100."),
    "funk": ("Funk", "Groove-first records built around bass lines, horns and rhythm."),
    "hard-rock": ("Hard Rock", "Heavier, louder guitar rock from the rock side of the chart."),
    "rnb": ("R&amp;B", "Rhythm and blues records from across the decade, a small station with plenty of variety."),
    "prog-rock": ("Prog Rock", "Progressive and art-rock acts whose singles made the Hot 100, the smallest station."),
}
ORDER = ["pop", "soul", "soft-rock", "classic-rock", "disco", "country", "funk", "hard-rock", "rnb", "prog-rock"]
ERA_NAMES = {"early-70s": "early 70s", "mid-70s": "mid 70s", "late-70s": "late 70s"}


def e(text):
    return html.escape(str(text), quote=False)


def join_names(items):
    items = list(items)
    if len(items) <= 2:
        return " and ".join(items)
    return ", ".join(items[:-1]) + ", and " + items[-1]


def top_artists(rows, n=3):
    counts = collections.Counter(r["artist"] for r in rows)
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:n]
    return [f"{e(a)} ({c})" for a, c in ranked]


def station_card(genre, rows):
    label, blurb = STATIONS[genre]
    years = collections.Counter(r["year"] for r in rows)
    busiest_year, busiest_n = sorted(years.items(), key=lambda kv: (-kv[1], kv[0]))[0]
    eras = collections.Counter(r["era"] for r in rows)
    era_text = ", ".join(f"{n} {ERA_NAMES.get(k, k)}" for k, n in sorted(eras.items(), key=lambda kv: -kv[1]))
    best = sorted(rows, key=lambda r: (r["rank"], r["year"]))[:3]
    best_text = "; ".join(f"{e(r['title'])} by {e(r['artist'])} ({r['year']}, #{r['rank']})" for r in best)
    return f'''      <div class="station-card">
        <h3>{label} Station</h3>
        <p>{blurb}</p>
        <p class="sc-meta">{len(rows)} songs, {min(years)} to {max(years)}. Busiest year: {busiest_year} ({busiest_n} songs). By era: {era_text}.</p>
        <p class="sc-meta">Highest on the Year-End Hot 100: {best_text}.</p>
        <p class="sc-meta">Most charted artists here: {join_names(top_artists(rows))}.</p>
      </div>'''


def build(rows):
    by_genre = collections.defaultdict(list)
    for r in rows:
        by_genre[r["genre"]].append(r)
    per_year = collections.Counter(r["year"] for r in rows)
    even = len(set(per_year.values())) == 1
    per_year_txt = f"{next(iter(per_year.values()))} songs from each year" if even else "songs from every year"
    top_all = sorted(collections.Counter(r["artist"] for r in rows).items(), key=lambda kv: (-kv[1], kv[0]))
    cutoff = top_all[min(3, len(top_all) - 1)][1]
    leaders = [f"{e(a)} ({c})" for a, c in top_all if c >= cutoff][:6]
    no1 = sorted((r for r in rows if r["rank"] == 1), key=lambda r: r["year"])
    trs = "\n".join(
        f'          <tr><td>{r["year"]}</td><td>{e(r["title"])}</td><td>{e(r["artist"])}</td></tr>' for r in no1)
    cards = "\n".join(station_card(g, by_genre[g]) for g in ORDER if g in by_genre)
    return f'''
    <section class="container section" id="station-guide">
      <div class="station-guide-intro">
        <h2>The Stations at a Glance</h2>
        <p>Listen Now draws on {len(rows):,} songs from Billboard's Year-End Hot 100 lists for {min(per_year)} to {max(per_year)}, {per_year_txt}. Each song is filed under one station, using this site's own genre labels. All counts and chart positions below come straight from that list.</p>
      </div>
      <div class="station-guide-grid">
{cards}
      </div>
    </section>

    <section class="container section seo-content" id="chart-facts">
      <h2>Chart Facts From the Catalog</h2>
      <p>The artists with the most songs on these ten Year-End lists are {join_names(leaders)}.</p>
      <h3>The Year-End #1 for Every Year</h3>
      <div class="chart-table-wrap">
        <table class="chart-table">
          <thead><tr><th>Year</th><th>Song</th><th>Artist</th></tr></thead>
          <tbody>
{trs}
          </tbody>
        </table>
      </div>
      <p>Want the stories behind the songs? Browse the <a href="/blog/years/index.html">year-by-year charts</a>, the <a href="/blog/genres/index.html">genre guides</a>, the <a href="/blog/artists/index.html">artist profiles</a> and the <a href="/blog/songs/index.html">song deep dives</a>.</p>
    </section>
'''


def main():
    with open(CATALOG, encoding="utf-8") as f:
        rows = json.load(f)
    with open(PAGE, encoding="utf-8") as f:
        page = f.read()
    pat = re.compile(r"(<!-- STATION-GUIDE:START[^>]*-->)(.*?)(<!-- STATION-GUIDE:END -->)", re.S)
    if not pat.search(page):
        raise SystemExit("ERROR: STATION-GUIDE markers not found in radio/index.html")
    page = pat.sub(lambda m: m.group(1) + build(rows) + "    " + m.group(3), page)
    with open(PAGE, "w", encoding="utf-8") as f:
        f.write(page)
    words = len(re.sub(r"<[^>]+>", " ", build(rows)).split())
    print(f"Station guide written: {len(rows)} songs, about {words} words of generated copy.")


if __name__ == "__main__":
    main()
