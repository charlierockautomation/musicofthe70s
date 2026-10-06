---
name: data-sources
description: Where the site's validated Billboard JSON and NotebookLM research briefs live, and the audited real facts about each dataset (record counts, genre buckets, known gaps). Use when researching a post, pulling chart facts, picking a research prompt for NotebookLM, or checking whether a data claim about the site's own JSON files is accurate.
---

# Data Sources — Full Detail

- Billboard databases: `~/musicofthe70s.net/data/billboard/`
  - `year_end_hot100.json` (1000 records, 1970–1979)
  - `hot100_weekly.json` (522 records)
  - `country.json` (523 records)
  - `rnb.json` (515 weekly rows; weekly #1 ALBUMS on Billboard's R&B/Soul albums chart, never singles)
  - year_end_hot100.json, hot100_weekly.json and country.json validated; treat as ground truth, never contradict this data in post content.
  - `rnb.json` was rebuilt 2026-10-06 against Wikipedia's 'List of Billboard number-one R&B albums of <year>' pages (the old file had a scrambled 1972 and 7 filler rows). Its `_verification` key records this. Not independently verified beyond that: say 'album' not 'song', and re-check against Wikipedia before citing a week count.
- Research briefs: NotebookLM notebooks (20+ artist/genre notebooks, Billboard year-end notebooks per year, "Music of the 70s — Overview" notebook with genre Wikipedia sources)
- Research brief pull prompt (use in any NotebookLM notebook when gathering material for a new post):
  > "Extract everything you can find in these sources that would help write a blog post. Give me: 5–8 genuinely interesting facts (specific dates, numbers, firsts, surprises), key names/songs/albums with context, any direct quotes worth referencing with source noted, and a rough narrative arc if there is one. Plain list, no fluff."
- Never invent a fact, date, chart position, or quote that isn't in the source material or validated database. When in doubt, mark it as needing verification rather than guessing.

## Additional data audit findings (2026-08-09, read-only)
Corrected earlier assumptions: 619 artists (not 605) across 10 real genre buckets — country 100, soft-rock 69, hard-rock 68, classic-rock 66, soul 66, disco 65, funk 50, pop-crossover 50, prog-rock 50, punk 35. Country is the largest bucket and wasn't in the original plan. Glam has no dedicated bucket, only scattered subgenre text. Only 243 of 570 song-to-artist ID links resolve — known, non-blocking data-quality gap. Mood Song Matcher matches artists by mood/vibe/era tags (not genre) and shares its data file with Random Artist Picker. Birthday #1 Finder and Decade Wheel both reuse files already documented above. Random Song Generator's real live pool is 400 songs (billboard_peak <= 40 filter on the 1,000-record file), separate from the artist-level data. Trivia's real untapped material is the 50-question `js/quiz-questions.js` pool, unused by either live Trivia post.

## Peak-position limit (added 2026-10-06)
`billboard_peak` in `data/radio/radio-songs.json` and `data/songs/hot_100_songs_*.json` is a copy of the Year-End Hot 100 `rank`, not a weekly chart peak (1,000 of 1,000 rows identical). The only verifiable peak data is number-one status and weeks at #1 from `data/billboard/hot100_weekly.json`. Never label year-end rank as "peak". A real weekly peak for non-#1 songs needs a per-song outside lookup (Billboard or Wikipedia), checked individually and never guessed.

## Sourcing rule: ranks vs peaks vs weeks at #1 (added 2026-10-06, Charlie)
- `year_end_hot100.json` (and `rank` / `billboard_peak` everywhere) = year-end RANK only. Write it as "ranked #N on the YYYY year-end Hot 100" or "year-end rank". Never "peak", "peaked", "reached", "hit" or a bare "No. N".
- A weekly peak or weeks at #1 may come only from `hot100_weekly.json` (number ones only) or an outside source (Wikipedia/Billboard), and the page must say which: "this site's own weekly chart data" or a linked Wikipedia source. Never credit the year-end file for a peak or a run at the top.
- R&B/Soul chart facts: `rnb.json` is albums only (rebuilt vs Wikipedia 2026-10-06). Say "album", cite Wikipedia's list for the year, never present an album run as the song's.
- Gate: `python3 scripts/check_chart_claims.py` must print PASS before any push (it fails on a year-end rank written as a chart number, or year-end data credited for a peak/run). Table rows are not scanned, so label table columns "Year-End Rank" or "Weekly Peak", never plain "Peak".
