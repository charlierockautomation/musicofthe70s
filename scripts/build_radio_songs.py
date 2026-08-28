#!/usr/bin/env python3
"""Merge data/songs/hot_100_songs_19XX.json (1970-1979) into one radio catalog.

Adds a youtube_id placeholder (null) to every record for later enrichment.
Idempotent: re-running preserves any youtube_id already filled in by
enrich_youtube_ids.py, keyed on radio_id (see below).

Source `id` (a title slug) collides across years/artists for real distinct
chart entries (e.g. "Superstar" by Murray Head and The Carpenters both
charted in 1971; "I Love the Nightlife" by Alicia Bridges charted in both
1978 and 1979; two different "Superstar" cover versions both charted in
1971 itself). radio_id = f"{year}-{rank}-{id}" is added as the unique key
for this catalog (rank is unique within a single year's chart); the
original `id` is kept as-is for provenance.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SONGS_DIR = os.path.join(ROOT, "data", "songs")
OUT_DIR = os.path.join(ROOT, "data", "radio")
OUT_PATH = os.path.join(OUT_DIR, "radio-songs.json")

YEARS = range(1970, 1980)


def load_existing_ids():
    if not os.path.exists(OUT_PATH):
        return {}
    with open(OUT_PATH) as f:
        existing = json.load(f)
    return {rec["radio_id"]: rec.get("youtube_id") for rec in existing}


def main():
    existing_ids = load_existing_ids()
    merged = []
    for year in YEARS:
        path = os.path.join(SONGS_DIR, f"hot_100_songs_{year}.json")
        with open(path) as f:
            songs = json.load(f)
        for song in songs:
            record = dict(song)
            radio_id = f"{year}-{song['rank']}-{song['id']}"
            record["radio_id"] = radio_id
            record["youtube_id"] = existing_ids.get(radio_id)
            merged.append(record)

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(merged, f, indent=2)

    total = len(merged)
    enriched = sum(1 for r in merged if r["youtube_id"])
    years_present = sorted({r["year"] for r in merged})
    print(f"Wrote {OUT_PATH}")
    print(f"Total songs: {total} (expected 1000)")
    print(f"Years present: {years_present}")
    print(f"Already enriched with youtube_id: {enriched}/{total}")

    ids = [r["radio_id"] for r in merged]
    if len(ids) != len(set(ids)):
        raise SystemExit("ERROR: duplicate radio_id found in merged catalog")

    assert total == 1000, f"expected 1000 songs, got {total}"


if __name__ == "__main__":
    main()
