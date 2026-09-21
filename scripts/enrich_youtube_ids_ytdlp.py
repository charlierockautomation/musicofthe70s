#!/usr/bin/env python3
"""RETIRED. Do not use.

This script used yt-dlp, which scrapes YouTube instead of using the YouTube
Data API. YouTube's Developer Policies prohibit scraping YouTube and obtaining
scraped YouTube data (III.E.6) and using anything other than YouTube API
Services to access API data (III.I.14). Retired 2026-09-20 in the YouTube
compliance audit (see .claude/skills/youtube-compliance/SKILL.md).

Use scripts/enrich_youtube_ids.py (Data API) to find IDs, then
scripts/youtube_status.py to record embeddable / madeForKids status.
"""
import sys

sys.exit("enrich_youtube_ids_ytdlp.py is retired: it scrapes YouTube, which the "
         "YouTube Developer Policies prohibit. Use scripts/enrich_youtube_ids.py "
         "and scripts/youtube_status.py instead.")
