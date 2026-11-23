---
type: handoff
status: open
tags: [bands-queue, rotation-slot-5-4, music-of-the-70s, ac-dc]
relatedTo: [content-build, bands-queue, spokes-queue]
---

# Handoff: slot 5.3 Yacht Rock LIVE, next = slot 5.4 Band AC/DC

## State (2026-11-21)
- /blog/genres/yacht-rock-songs/ LIVE (200). Page commit a62dc1a, regen + tracker commit c21c5a3, pushed to main. youtube_status PASS (16 of 16 IDs). Handoff slot-5-3 archived.
- Build files: .base/step-5.3/build.py, scripts/generate_yacht_rock_chart.py, video-decisions.md, sources/log/yacht-rock-songs.json. 16 of 16 play (3 Topic uploads: Pablo Cruise, Bobby Caldwell, Sanford & Townsend).
- spokes-queue.md row 3 LIVE, keyword-research-log.md and content-build.md updated.
- Uncommitted, untouched: .claude/hooks/cap-bash-output.py, run-capped.sh, .base/ working files, reports/.
- Preview server on port 8070 may still be running (kill if not needed).

## Next
1. Slot 5.4 Band: AC/DC (bands-queue.md row 2, hard rock, 60,500 US, AI 5,077). Keyword rule first (journey songs pattern: pick "ac/dc songs" or the bare name, whichever is the bigger songs-intent search; slug in keyword word order), log pull in keyword-research-log.md, register in scripts/article_standard_pages.json, official video IDs only, all gates, local preview, STOP for Charlie's go-ahead (PUBLISH GATE).
2. Genre rotation: last pages were Michael Jackson (pop), Yacht Rock (soft rock); hard rock is fine. 70s-only page (1975-1979 for AC/DC internationally; check what the US Hot 100 carries).

## Lessons from 5.3 (use in 5.4)
- K2 window: H1 counts toward the 300-word window. Keep H1 and TOC/H2 free of the exact keyword when P8 needs 9+ uses; put P5 on an H3 and spread uses 150+ words apart.
- Do not run downloaded JS (data.js) with node require; parse as JSON text. Auto mode denies it.
- Wikipedia extracts strip tables; use action=parse wikitext for peaks (add 3s delay between calls or it rate-limits).
- Subagent WebFetch gives extractions, not raw HTML: flag quoted lines for Charlie's spot-check.
- Steps: YOUTUBE status run is Charlie's (L3 fails until then); regen scripts run one per Bash call (batched calls get no classifier verdict).

## Open items for Charlie
- 5.7 linking pass: add back-links to yacht-rock-songs from 70s-soft-rock, earth-wind-and-fire-songs, genres hub; also MJ page back-links (jackson-5-songs, diana-ross-songs, 70s-singers) still owed.
- Rotate the YOUTUBE_API_KEY embedded in the settings.local.json allow rule and delete that line.
- Dolly Parton page claim "died August 25, 2026" not verifiable by Claude.
- Rock with You "No. 1 January 19, 1980" rests on Stereogum only.
- Chrome not installed in sandbox; Playwright Chromium works for desktop + 390px checks. Live-page 390px check of the yacht page not done (only local preview).
