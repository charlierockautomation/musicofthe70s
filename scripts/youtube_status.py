#!/usr/bin/env python3
"""Record embeddable / madeForKids status for every YouTube ID the site uses.

Calls videos.list (part=status) in batches of 50 and writes
data/youtube-status.json: per ID, embeddable, madeForKids, privacyStatus and
checked_at (UTC). YouTube allows storing this API data for at most 30 calendar
days, so refresh (or delete) it before then:
  default    re-check IDs that are missing or 25+ days old
  --refresh  re-check every ID
  --report   NO API call; exit 1 if any ID is missing, older than 30 days, or
             blocked (not embeddable / made for kids / not public) on a page
verify_post.py calls status_problems() for the same rule.

IDs come from data/radio/radio-songs.json and every youtube.com/embed/<id> in
the site's HTML; IDs no longer used are dropped.

Quota: videos.list = 1 unit per request (50 IDs), so a full refresh of N IDs
costs ceil(N/50) of the 10,000 units/day default.

API key: ONLY from the YOUTUBE_API_KEY environment variable, from a Google
Cloud project dedicated to this site. Never written to a file or printed.

Usage: YOUTUBE_API_KEY=... python3 scripts/youtube_status.py [--refresh]
       python3 scripts/youtube_status.py --report
"""
import argparse
import datetime
import glob
import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(ROOT, "data", "radio", "radio-songs.json")
STATUS_PATH = os.path.join(ROOT, "data", "youtube-status.json")
API_URL = "https://www.googleapis.com/youtube/v3/videos"
MAX_AGE_DAYS = 30        # YouTube's storage limit for API data
REFRESH_AFTER_DAYS = 25  # default run re-checks before the limit is reached
BATCH = 50
EMBED_RE = re.compile(r"youtube(?:-nocookie)?\.com/embed/([A-Za-z0-9_-]{11})")

def now():
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)

def age_days(rec):
    try:
        return (now() - datetime.datetime.fromisoformat(rec["checked_at"])).total_seconds() / 86400
    except (KeyError, ValueError, TypeError):
        return None

def site_ids():
    """{video_id: {'radio'|'page'}} for every ID the site uses."""
    ids = {}
    with open(CATALOG, encoding="utf-8") as f:
        for song in json.load(f):
            if song.get("youtube_id"):
                ids.setdefault(song["youtube_id"], set()).add("radio")
    pages = glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)
    for path in pages:
        if os.sep + ".git" + os.sep in path:
            continue
        with open(path, encoding="utf-8") as f:
            for vid in EMBED_RE.findall(f.read()):
                ids.setdefault(vid, set()).add("page")
    return ids

def load_videos():
    if not os.path.exists(STATUS_PATH):
        return {}
    with open(STATUS_PATH, encoding="utf-8") as f:
        return json.load(f).get("videos", {})

def save_videos(videos):
    lines = ",\n".join(
        f"  {json.dumps(k)}: {json.dumps(v, sort_keys=True, separators=(',', ':'))}"
        for k, v in sorted(videos.items()))
    text = f'{{\n "max_age_days": {MAX_AGE_DAYS},\n "videos": {{\n{lines}\n }}\n}}\n'
    tmp = STATUS_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, STATUS_PATH)

def blocked_reason(rec):
    if rec.get("missing"):
        return "not returned by the API (deleted or private)"
    if rec.get("embeddable") is not True:
        return "not embeddable"
    if rec.get("madeForKids") is not False:
        return "made for kids" if rec.get("madeForKids") is True else "no madeForKids value"
    if rec.get("privacyStatus") != "public":
        return f"privacyStatus={rec.get('privacyStatus')}"
    return None

def problems(ids_with_sources, videos):
    """Return (hard, soft). hard = must fix before publishing."""
    hard, soft = [], []
    for vid, sources in sorted(ids_with_sources.items()):
        rec = videos.get(vid)
        if rec is None:
            hard.append(f"{vid}: no status on record")
            continue
        age = age_days(rec)
        if age is None or age > MAX_AGE_DAYS:
            hard.append(f"{vid}: status missing checked_at or older than {MAX_AGE_DAYS} days")
            continue
        why = blocked_reason(rec)
        if why:
            on_page = "page" in sources
            (hard if on_page else soft).append(f"{vid}: {why}" + (" (embedded on a page)" if on_page else " (radio drops it)"))
    return hard, soft

def status_problems(ids):
    """For verify_post.py: hard problems for these IDs (page embeds)."""
    hard, soft = problems({i: {"page"} for i in ids}, load_videos())
    return hard + soft

def fetch(key, ids):
    query = urllib.parse.urlencode({"part": "status", "id": ",".join(ids), "key": key, "maxResults": BATCH})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(f"{API_URL}?{query}", timeout=30) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as err:
            reason = "unknown"
            try:
                reason = json.load(err)["error"]["errors"][0]["reason"]
            except Exception:
                pass
            if err.code in (429, 500, 502, 503, 504) and attempt < 4 and reason != "quotaExceeded":
                time.sleep(min(60, 2 ** attempt))
                continue
            sys.exit(f"YouTube API error: HTTP {err.code} ({reason}). Progress so far is saved; re-run to continue.")
        except urllib.error.URLError as err:
            sys.exit(f"Network error: {err.reason}. Progress so far is saved; re-run to continue.")

def run_check(refresh):
    key = os.environ.get("YOUTUBE_API_KEY")
    if not key:
        sys.exit("ERROR: set YOUTUBE_API_KEY in the environment (key from the site's own Google Cloud "
                 "project; never put it in a file).")
    ids = site_ids()
    videos = {k: v for k, v in load_videos().items() if k in ids}  # drop IDs no longer used
    todo = [v for v in sorted(ids)
            if refresh or v not in videos or (age_days(videos[v]) is None) or age_days(videos[v]) >= REFRESH_AFTER_DAYS]
    print(f"{len(ids)} IDs in use; checking {len(todo)} ({'full refresh' if refresh else 'missing or 25+ days old'}).")
    requests = 0
    for i in range(0, len(todo), BATCH):
        batch = todo[i:i + BATCH]
        data = fetch(key, batch)
        requests += 1
        stamp = now().isoformat()
        found = {item["id"]: item.get("status", {}) for item in data.get("items", [])}
        for vid in batch:
            st = found.get(vid)
            if st is None:
                videos[vid] = {"missing": True, "embeddable": False, "checked_at": stamp}
            else:
                videos[vid] = {"embeddable": st.get("embeddable"), "madeForKids": st.get("madeForKids"),
                               "privacyStatus": st.get("privacyStatus"), "checked_at": stamp}
        save_videos(videos)  # checkpoint after every batch
        print(f"  batch {requests}/{math.ceil(len(todo) / BATCH)} done")
    print(f"Done: {requests} API requests = {requests} quota units (videos.list is 1 unit per request).")
    report()

def report():
    ids, videos = site_ids(), load_videos()
    hard, soft = problems(ids, videos)
    ages = [a for a in (age_days(videos[v]) for v in ids if v in videos) if a is not None]
    print(f"IDs in use: {len(ids)} | with status: {sum(1 for v in ids if v in videos)} | "
          f"oldest check: {max(ages):.1f} days" if ages else f"IDs in use: {len(ids)} | with status: 0")
    print(f"Full refresh would cost {math.ceil(len(ids) / BATCH)} quota units.")
    for line in soft:
        print("  note:", line)
    for line in hard:
        print("  FAIL:", line)
    print("STATUS CHECK:", "FAIL" if hard else "PASS")
    return 1 if hard else 0

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--refresh", action="store_true", help="re-check every ID, not just missing/stale ones")
    ap.add_argument("--report", action="store_true", help="no API call; exit 1 if any ID is missing/stale/blocked")
    args = ap.parse_args()
    if args.report:
        sys.exit(report())
    run_check(args.refresh)

if __name__ == "__main__":
    main()
