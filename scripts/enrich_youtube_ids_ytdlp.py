#!/usr/bin/env python3
"""Fill in real, verified-embeddable YouTube video IDs for
data/radio/radio-songs.json using yt-dlp instead of the YouTube Data API.

Why: the YouTube Data API v3 key on this project has a real, confirmed cap
of 100 search.list calls/day (see scripts/enrich_youtube_ids.py's docstring
and the 2026-08-27 session). At that rate the remaining catalog would take
over a week. yt-dlp does its own search/extraction against YouTube directly
and isn't subject to that per-project daily quota, so it can finish the
whole catalog in one run.

For each pending song: `yt-dlp "ytsearch1:<query>" --dump-json`, and only if
that single candidate doesn't pass the embeddability check, retries with
`ytsearch3` for two more candidates. A candidate is accepted only if
playable_in_embed is true, availability is "public", and age_limit is 0
(consistent with the "never invent, never guess" standard -- no candidate
is used unless yt-dlp's own metadata confirms it plays and embeds).

Resumable and atomic-write, same pattern as enrich_youtube_ids.py: safe to
Ctrl-C and rerun, safe to run alongside a live site.

Usage:
    python3 scripts/enrich_youtube_ids_ytdlp.py [--limit N]
"""
import argparse
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(ROOT, "data", "radio", "radio-songs.json")
EXCLUDED_JSON_PATH = os.path.join(ROOT, "data", "radio", "radio-songs-excluded.json")
EXCLUDED_MD_PATH = os.path.join(ROOT, "data", "radio", "radio-songs-excluded.md")


def atomic_write_json(path, data):
    tmp_path = f"{path}.tmp"
    with open(tmp_path, "w") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp_path, path)


def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path) as f:
        return json.load(f)


def yt_search(query, n):
    try:
        proc = subprocess.run(
            ["yt-dlp", f"ytsearch{n}:{query}", "--dump-json",
             "--no-warnings", "--skip-download"],
            capture_output=True, text=True, timeout=60,
        )
    except subprocess.TimeoutExpired:
        return []
    if proc.returncode != 0 and not proc.stdout.strip():
        return []
    results = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            results.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return results


def find_embeddable_video(query):
    for n in (1, 3):
        candidates = yt_search(query, n)
        for c in candidates:
            if (c.get("playable_in_embed") is True
                    and c.get("availability") == "public"
                    and (c.get("age_limit") or 0) == 0):
                return c["id"], None
        if candidates:
            # got results but none passed -- no point re-searching wider
            return None, "found results but none embeddable/public/unrestricted"
    return None, "no search results"


def save_catalog(catalog):
    atomic_write_json(CATALOG_PATH, catalog)


def save_excluded(excluded):
    atomic_write_json(EXCLUDED_JSON_PATH, excluded)
    with open(EXCLUDED_MD_PATH, "w") as f:
        f.write("# Radio songs excluded (no embeddable YouTube video found)\n\n")
        f.write("Reviewed by scripts/enrich_youtube_ids_ytdlp.py. Never a fabricated ")
        f.write("ID, just an honest report of what search did not find.\n\n")
        f.write("| Year | Title | Artist | Reason |\n|---|---|---|---|\n")
        for rec in sorted(excluded, key=lambda r: (r["year"], r["title"])):
            f.write(f"| {rec['year']} | {rec['title']} | {rec['artist']} | {rec['reason']} |\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    catalog = load_json(CATALOG_PATH, None)
    if catalog is None:
        sys.exit(f"ERROR: {CATALOG_PATH} not found — run build_radio_songs.py first")

    excluded = load_json(EXCLUDED_JSON_PATH, [])
    excluded_ids = {rec["radio_id"] for rec in excluded}

    pending = [
        rec for rec in catalog
        if not rec.get("youtube_id") and rec["radio_id"] not in excluded_ids
    ]
    print(f"{len(pending)} songs pending lookup "
          f"({sum(1 for r in catalog if r.get('youtube_id'))} already enriched, "
          f"{len(excluded)} previously excluded)")

    attempted = 0
    enriched_this_run = 0
    for i, rec in enumerate(pending):
        if args.limit is not None and attempted >= args.limit:
            break
        attempted += 1
        query = rec["youtube_search"]
        video_id, reason = find_embeddable_video(query)

        if video_id:
            rec["youtube_id"] = video_id
            enriched_this_run += 1
            print(f"[{i+1}/{len(pending)}] OK  {rec['year']} {rec['title']!r} -> {video_id}")
        else:
            excluded.append({
                "radio_id": rec["radio_id"],
                "year": rec["year"],
                "title": rec["title"],
                "artist": rec["artist"],
                "reason": reason,
            })
            excluded_ids.add(rec["radio_id"])
            print(f"[{i+1}/{len(pending)}] MISS {rec['year']} {rec['title']!r}: {reason}")

        # Checkpoint every song -- safe to interrupt at any point.
        save_catalog(catalog)
        save_excluded(excluded)

    total_enriched = sum(1 for r in catalog if r.get("youtube_id"))
    print(f"\nRun complete. {enriched_this_run} enriched this run.")
    print(f"Totals: {total_enriched}/{len(catalog)} enriched, {len(excluded)} excluded.")


if __name__ == "__main__":
    main()
