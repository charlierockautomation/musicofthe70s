---
name: linking-and-tools
description: The Tools-as-Pillars table (real data behind each interactive tool), the internal linking strategy (primary/secondary destinations), and where the Anchor Text & Position Log lives. Use during the internal-linking step of building or editing a post, when picking which tool to link to, or when checking the last 3-5 same-category anchor text/position entries before placing a new internal link (see references/anchor-text-position-log.md).
---

# Internal Linking & Tools-as-Pillars — Full Detail

Only needed during the internal-linking step of a build. Open this then, not at
session start.

Related: the post-template skill holds the Internal Tool Linking Map (which tool
matches which post type) and the Anchor Text & Position Rule itself. This skill
holds the strategy context and the running log.

---

## Tools as Pillars (real data, confirmed via repo audit 2026-08-09)

The site's two permanent pillar types are the homepage and the interactive tools.
Every new post links to whichever pillar its content actually supports, not the
homepage by default, and not a mismatched tool for the sake of a tool link.

| Tool | Real Data Source | Confirmed Facts |
|---|---|---|
| Random 70s Song Generator | data/songs/hot_100_songs_1970-1979.json | 1,000 records but filtered to billboard_peak <= 40 for display, real live pool is 400 songs. Own genre/mood/vibe schema per song, separate from the artist-level genre field. |
| Birthday #1 Song Finder | data/billboard/hot100_weekly.json | 522 weekly #1 records, full 1970-1979 coverage. Same file already used for Years-post research. |
| Mood Song Matcher | data/artists/*.json (same as Artist Picker) | Matches ARTISTS by mood/vibe/era tags, not genre. Tags: mood (happy 331, nostalgic 296, pumped-up 233, romantic 231, rebellious 207, melancholy 202), vibe (reflect 298, chill 272, party 250, drive 234, dance 221, rock-out 188), era (late-70s 541, mid-70s 517, early-70s 415). Does NOT map to Genres content, use the genre field instead. |
| Random Artist Picker | data/artists/*.json (10 files) | 619 total records, 601 unique artists (18 IDs appear in two genre files). Buckets: country 100, soft-rock 69, hard-rock 68, classic-rock 66, soul 66, disco 65, funk 50, pop-crossover 50, prog-rock 50, punk 35 (contaminated with 12 new-wave artists). No dedicated Glam bucket (17 glam artists scattered in hard-rock and pop-crossover). "country 100" is the whole genre:"country" field, not country-rock (real country-rock roster is 14 artists across 3 files). Don't trust a bucket count for a subgenre post without checking the subgenre field. |
| 70s Music Trivia Quiz | js/quiz-questions.js | 50 questions. Powers the built-but-not-live "70s Music Quiz" post (all 50, scored) and this tool page's own 10-question random rounds. |
| 70s Decade Wheel | data/billboard/year_end_hot100.json | Same file as the Years blog posts. No distinct dataset. |
| Rock Trivia Game (built 2026-08-23, NOT pushed) | data/artists/ classic_rock, hard_rock, prog_rock, punk_new_wave (219 artists) | 7th tool, at /pages/rock-trivia-game.html, keyword `rock trivia game`. `scripts/generate_rock_trivia_data.py` builds `js/rock-trivia-data.js` (1,384 questions) from structured fields only, no free-text parsing. Category select + date-seeded Daily Challenge with localStorage streak. Rerun the generator after editing any of the 4 source JSON files. Awaiting Charlie's go-ahead per the Publish Gate. |

Known data-quality gap (non-blocking): only 243 of 570 distinct artistIds in the
song data resolve to a real artist record. Would block any future feature that
joins songs and artists programmatically.

---

## Internal Linking Strategy

Every post links up to its category page and to at least one relevant Tool.
Cross-category links matter as much as same-category "Related Posts" links.

Each post gets one **primary destination** (the single most topically relevant
pillar, hub, or tool, not the homepage by default) and up to two **secondary
destinations**, only where genuinely useful. Never link to hit a quota.

**Link owed** (cross-category links that should exist once their target is built):

*(Table empty as of 2026-08-16 — the last open row, Bohemian Rhapsody -> Glam or
Prog Rock, was closed by the 70s Progressive Rock post; link added both
directions.)*

---

## Anchor Text & Position Log

Rule (also in post-template skill): before placing any internal link, check the
last 3-5 rows for the same category in references/anchor-text-position-log.md.
Anchor text AND position must not repeat within that window. Anchor text = brand
phrase "Music of the 70s" OR the target's own focus keyword, never generic. Log
new entries there after placing links. Log starts 2026-08-28; prior posts not
backfilled.

When references/anchor-text-position-log.md nears 195 lines, prune its oldest
rows to CONTENT-INDEX-ARCHIVE.md.
