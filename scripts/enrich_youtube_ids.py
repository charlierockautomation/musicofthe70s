#!/usr/bin/env python3
"""Fill in real, verified-embeddable YouTube video IDs for data/radio/radio-songs.json.

Resumable: writes the file after every lookup, so a quota cutoff mid-run
loses no progress. Safe to re-run as many times as needed (skips records
that already have a youtube_id or are already on the excluded list).

Never invents an ID. A song with no embeddable match found is written to
data/radio/radio-songs-excluded.md with title/artist/reason and skipped on
future runs (tracked in radio-songs-excluded.json so it isn't retried
forever, but re-checked if that file is deleted).

Usage:
    YOUTUBE_API_KEY=... python3 scripts/enrich_youtube_ids.py [--limit N]

Reads scripts/.env for YOUTUBE_API_KEY if not already in the environment.
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(ROOT, "data", "radio", "radio-songs.json")
EXCLUDED_JSON_PATH = os.path.join(ROOT, "data", "radio", "radio-songs-excluded.json")
EXCLUDED_MD_PATH = os.path.join(ROOT, "data", "radio", "radio-songs-excluded.md")
ENV_PATH = os.path.join(ROOT, "scripts", ".env")

SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"


def load_env_file(path):
    if not os.path.exists(path):
        return
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())


class QuotaExceeded(Exception):
    pass


def api_get(url, params, max_retries=8):
    query = urllib.parse.urlencode(params)
    req = urllib.request.Request(f"{url}?{query}")
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")
            # Daily quota exhaustion (this project's real cap has been observed at
            # 100 search.list calls/day) comes back as 429 RESOURCE_EXHAUSTED with
            # "per day" in the message, not the more commonly-documented 403
            # quotaExceeded. Treat both as the same permanent-for-today condition
            # and stop immediately rather than burning retries against a limit
            # that won't clear until the daily reset.
            if ("quotaExceeded" in body
                    or ("RESOURCE_EXHAUSTED" in body and "per day" in body)):
                raise QuotaExceeded from e
            if e.code in (429, 500, 502, 503, 504) and attempt < max_retries - 1:
                wait = min(60, 2 ** attempt)
                print(f"  transient HTTP {e.code}, retrying in {wait}s "
                      f"(attempt {attempt + 1}/{max_retries})")
                time.sleep(wait)
                continue
            raise


def find_embeddable_video(api_key, query):
    """Search for `query`, return the first embeddable video ID, or None."""
    search_res = api_get(SEARCH_URL, {
        "part": "id",
        "q": query,
        "type": "video",
        "maxResults": 5,
        "key": api_key,
    })

    video_ids = [item["id"]["videoId"] for item in search_res.get("items", [])]
    if not video_ids:
        return None, "no search results"

    videos_res = api_get(VIDEOS_URL, {
        "part": "status",
        "id": ",".join(video_ids),
        "key": api_key,
    })

    for item in videos_res.get("items", []):
        status = item.get("status", {})
        if status.get("embeddable") and status.get("privacyStatus") == "public":
            return item["id"], None

    return None, "no embeddable/public candidate among search results"


def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path) as f:
        return json.load(f)


def atomic_write_json(path, data):
    """Write via a temp file + os.replace so a concurrent reader (e.g. the site
    fetching this file while it's being rewritten) never sees a truncated file."""
    tmp_path = f"{path}.tmp"
    with open(tmp_path, "w") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp_path, path)


def save_catalog(catalog):
    atomic_write_json(CATALOG_PATH, catalog)


def save_excluded(excluded):
    atomic_write_json(EXCLUDED_JSON_PATH, excluded)
    with open(EXCLUDED_MD_PATH, "w") as f:
        f.write("# Radio songs excluded (no embeddable YouTube video found)\n\n")
        f.write("Reviewed by scripts/enrich_youtube_ids.py. Never a fabricated ID, ")
        f.write("just an honest report of what search did not find.\n\n")
        f.write("| Year | Title | Artist | Reason |\n|---|---|---|---|\n")
        for rec in sorted(excluded, key=lambda r: (r["year"], r["title"])):
            f.write(f"| {rec['year']} | {rec['title']} | {rec['artist']} | {rec['reason']} |\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None,
                         help="max number of lookups to attempt this run")
    parser.add_argument("--sleep", type=float, default=2.0,
                         help="seconds to sleep between API calls")
    args = parser.parse_args()

    load_env_file(ENV_PATH)
    api_key = os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        sys.exit("ERROR: YOUTUBE_API_KEY not set (env var or scripts/.env)")

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
    for rec in pending:
        if args.limit is not None and attempted >= args.limit:
            break
        attempted += 1
        query = rec["youtube_search"]
        try:
            video_id, reason = find_embeddable_video(api_key, query)
        except QuotaExceeded:
            print(f"Quota exceeded after {attempted - 1} lookups this run "
                  f"({enriched_this_run} enriched). Stopping cleanly, resume later.")
            save_catalog(catalog)
            save_excluded(excluded)
            return
        except Exception as e:
            print(f"Unexpected error after {attempted - 1} lookups this run "
                  f"({enriched_this_run} enriched): {e!r}. Stopping cleanly, resume later.")
            save_catalog(catalog)
            save_excluded(excluded)
            return

        if video_id:
            rec["youtube_id"] = video_id
            enriched_this_run += 1
            print(f"OK  {rec['year']} {rec['title']!r} -> {video_id}")
        else:
            excluded.append({
                "radio_id": rec["radio_id"],
                "year": rec["year"],
                "title": rec["title"],
                "artist": rec["artist"],
                "reason": reason,
            })
            excluded_ids.add(rec["radio_id"])
            print(f"MISS {rec['year']} {rec['title']!r}: {reason}")

        save_catalog(catalog)
        save_excluded(excluded)
        time.sleep(args.sleep)

    total_enriched = sum(1 for r in catalog if r.get("youtube_id"))
    print(f"\nRun complete. {enriched_this_run} enriched this run.")
    print(f"Totals: {total_enriched}/{len(catalog)} enriched, {len(excluded)} excluded.")


if __name__ == "__main__":
    main()
