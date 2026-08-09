# CONTENT-BUILD.md — musicofthe70s.net Master Content & Linking Tracker
# CLAUDE / CLAUDE CODE: Read this alongside CLAUDE.md and CONTENT-INDEX.md before planning any session.
# Data verified via a real repo audit, 2026-08-09 — see Session Log for what changed from the first draft.
# Rotation Queue slots 1-2 (70s Soft Rock, Queen) shipped 2026-08-09 — next up is slot 1, Country Rock of the 70s (Genres).

---

## How This File Works

1. Before writing anything new, check CONTENT-INDEX.md for what's already live — never duplicate.
2. Pick the next item from the Rotation Queue below. If a category has no ready item, skip to the next rather than forcing it.
3. Every new post links to at least one Tool (see Tools as Pillars).
4. Every new post checks the Internal Linking Strategy's "link owed" table for a cross-category opportunity.
5. Update this file's Session Log every session, per the Content Tracker Ownership rule in CLAUDE.md.

---

## Tools as Pillars (real data, confirmed via repo audit 2026-08-09)

| Tool | Real Data Source | Confirmed Facts |
|---|---|---|
| Random 70s Song Generator | data/songs/hot_100_songs_1970-1979.json | 1,000 records but filtered to billboard_peak <= 40 for display, real live pool is 400 songs. Own genre/mood/vibe schema per song, separate from the artist-level genre field. |
| Birthday #1 Song Finder | data/billboard/hot100_weekly.json | 522 weekly #1 records, full 1970-1979 coverage. Same file already used for Years-post research. |
| Mood Song Matcher | data/artists/*.json (same as Artist Picker) | Matches ARTISTS by mood/vibe/era tags, not genre. Tags: mood (happy 331, nostalgic 296, pumped-up 233, romantic 231, rebellious 207, melancholy 202), vibe (reflect 298, chill 272, party 250, drive 234, dance 221, rock-out 188), era (late-70s 541, mid-70s 517, early-70s 415). Does NOT map to Genres content — use the genre field instead. |
| Random Artist Picker | data/artists/*.json (10 files) | 619 total records, but 601 unique artists — 18 artist IDs appear in two genre files each (e.g. Elton John in both pop-crossover and soft-rock, Mott the Hoople in both classic-rock and hard-rock; full list in Session Log). Real genre buckets: country 100, soft-rock 69, hard-rock 68, classic-rock 66, soul 66, disco 65, funk 50, pop-crossover 50, prog-rock 50, punk 35 (contaminated with 12 new-wave-subgenre artists). No dedicated Glam bucket — glam artists exist only as subgenre text inside hard-rock (10: Angel, Dokken, Gary Glitter, Ian Hunter, Mott the Hoople, New York Dolls, Slade, Suzi Quatro, T. Rex, The Sweet) and pop-crossover (7: Bowie, Elton John, David Essex, Mud, Pilot, The Rubettes, Wizzard) — 17 unique glam-tagged artists total. |
| 70s Music Trivia Quiz | js/quiz-questions.js | 50 questions, completely unused by either live Trivia post — real untapped reservoir for the next Trivia post. |
| 70s Decade Wheel | data/billboard/year_end_hot100.json | Same file as the Years blog posts. No distinct dataset. |

**Known data-quality issue, not urgent but worth knowing:** only 243 of 570 distinct artistIds referenced in the song data actually resolve to a real artist record — most song-to-artist links are currently broken. Not blocking content work, but would block any future feature that tries to join songs and artists programmatically.

---

## Internal Linking Strategy

Every post links up to its category page and to at least one relevant Tool. Cross-category links matter as much as same-category "Related Posts" — right now every Related Posts block on the site only links within its own category, which pools link equity instead of letting it flow site-wide.

**Link owed** (cross-category links that should exist once their target is built):

| Existing Post | Owes a link to | Category |
|---|---|---|
| Bohemian Rhapsody | A Glam or Prog Rock genre post | Genres |
| Hotel California | Eagles bio | Artists |
| Dancing Queen | ABBA bio | Artists |
| Dancing Queen | Disco Music of the 70s (already Planned) | Genres |
| Village People | Disco Music of the 70s (already Planned) | Genres |

---

## Category Rotation Queue

Genre priority reordered against real artist-bucket sizes (bigger bucket = more source material to draw from, not necessarily higher search volume — still verify keywords before writing).

Years series is complete (10/10, 1970-1979, all Live, confirmed against CONTENT-INDEX.md) — no Years slots in this queue, none planned.

| Slot | Category | Content | Status |
|---|---|---|---|
| ~~1~~ | ~~Genres~~ | ~~70s Soft Rock~~ | **Done, Live 2026-08-09** — see CONTENT-INDEX.md and Session Log below |
| ~~2~~ | ~~Artists~~ | ~~Queen~~ | **Done, Live 2026-08-09** — closed the Bohemian Rhapsody link-owed gap; see keyword-research-log.md and Session Log below |
| 1 | Genres | Country Rock of the 70s (100 artists, the single largest genre bucket in the real data — not on the original plan, surfaced by the audit) | pending keyword check |
| 2 | Genres | Disco Music of the 70s (already Planned, keyword already set, 65 real artists, Dancing Queen and Village People both waiting to link to it) | pending |
| 3 | Artists | Eagles (closes Hotel California link-owed gap; verify NFL-team search ambiguity first — the Queen keyword check found the site's own risk assumptions aren't always right, confirm with a real SERP/volume check, don't assume Eagles is safer just because it was flagged as such) | pending keyword check |
| 4 | Genres | 70s Hard Rock (68 artists) | pending keyword check |
| 5 | Artists | ABBA (closes Dancing Queen link-owed gap) | pending keyword check |
| 6 | Genres | Classic Rock of the 70s (66 artists — CHECK FIRST whether this genuinely differs from the already-live "70s Rock" post or is a data-labeling overlap before building; don't duplicate) | needs a content decision, not just a keyword check |
| 7 | Trivia | Next Trivia post drawing from the untapped 50-question QUIZ_POOL in js/quiz-questions.js | needs a content decision on format |
| 8 | Genres | 70s Funk (50 artists; check against the live Soul post for overlap first) | pending keyword check |
| 9 | Genres | Progressive Rock in the 70s (50 artists; fold in "concept albums" as a section) | pending keyword check |
| 10 | Genres | Pop Crossover of the 70s (50 artists — decide if this is distinct from Soft Rock/Yacht Rock or overlapping before building) | needs a content decision |
| 11 | Genres | 70s Punk Rock (real count closer to 23 once new-wave contamination is filtered out; can't lean on chart-hit hooks, zero punk songs in the chart data) | pending keyword check |
| 12 | Genres | Glam Rock in the 70s (no dedicated bucket — must be manually curated from hard-rock's 10 and pop-crossover's 7 subgenre-tagged artists) | needs manual curation before writing, not a simple pull |

---

## Category Status Summary

| Category | Live Posts | State |
|---|---|---|
| Years | 10 (1970-1979) | Series complete, no further posts planned |
| Songs | 5 | Batch complete, no further batch approved yet |
| Artists | 6 | Queen shipped 2026-08-09; Eagles and ABBA remain for the outstanding link-owed gaps |
| Trivia | 2 | Real untapped data exists (50-question pool), needs a format decision |
| Genres | 3 live (zero placeholders) + 1 Planned | First Rotation Queue item (70s Soft Rock) shipped 2026-08-09; still the category with the most real material left to draw from |

---

## Session Log

| Date | Task | Notes |
|---|---|---|
| 2026-08-09 | File created directly by Claude Code, first real save to the repo | Prior draft only ever existed in chat, never actually saved here — this is the first real version. Corrected against a full data audit: 619 rows across 10 artist files but only 601 unique artists (18 IDs duplicated across two files each: april-wine, dan-fogelberg, dr-hook, firefall, gordon-lightfoot, harry-chapin, jackson-browne, jim-croce, john-prine, loggins-and-messina, mott-the-hoople, orleans, poco, pure-prairie-league, the-j-geils-band, van-morrison, warren-zevon, elton-john). Confirmed 10 real genre buckets with exact counts; found Country is the largest bucket (100 artists) and wasn't in the original plan at all; found Glam has no dedicated bucket and needs manual curation (10 hard-rock + 7 pop-crossover = 17 unique, corrected up from an initial verbal count of 9 for hard-rock that missed Dokken/"glam metal"); found Punk's bucket is contaminated with 12 new-wave-subgenre artists and has zero charting songs to draw hooks from; corrected Mood Song Matcher's tags as emotional/activity-based rather than genre-based; confirmed Trivia's real untapped material is the 50-question quiz pool rather than 64-post leftovers; flagged the broken song-to-artist ID join (243/570 resolve) as a known but non-blocking issue. **Also corrected two factual errors in the pasted draft before saving**: the draft claimed Years was "8 live, 1978/1979 remaining" and listed both as queue slots 12/14 — false, CONTENT-INDEX.md confirms all 10 Years posts (1970-1979) are Live and the series is explicitly marked complete with no further posts planned; both queue slots removed rather than saved as-is, which would have set up duplicate posts. The "confirmed 14,800/mo" keyword-volume claim for Soft Rock was softened to "as supplied, not independently reverified" since this session's audit covered data files only, not keyword volume. |
| 2026-08-09 | Rotation Queue slot 1 built: 70s Soft Rock published, Live | Keyword volume (14,800/mo, `70s soft rock`) confirmed by Charlie as re-verified via WordStream, taken as given, not re-checked this session. Artist roster pulled directly from `data/artists/artists_soft_rock.json` (69 real artists), no invented names, per explicit instruction. Real data hook: this site's own `data/songs/*.json` genre field shows 1979 (25 hits) and 1976 (23) as the genre's two biggest years, ahead of the commonly assumed mid-70s peak, a specific correction not found on any currently-ranking page. Tenth distinct structure across all Artists/Songs/Genres posts to date: data-correction-driven rather than named-era chronology (both prior Genres posts used chronology). **Link-owed gap closed both directions**: this post cites the Eagles' "One of These Nights" (soft-rock-tagged at song level) with a forward link to Hotel California; Hotel California's chart-run section was edited in the same session to add a link back, re-verified clean afterward (1,259 words, still passes). Removed from the Link Owed table above accordingly. `verify_post.py` flagged a false-positive banned-word hit on "tapestry" (the literal album title *Tapestry*, not the cliché usage) — confirmed the identical false positive already exists unflagged on the live "70s Rock" post, predates the script, not treated as a real failure. No image-gen tool was available this session; sourced a real Wikimedia Commons photo (Carole King, Cash Box 1971, public domain) instead of a NotebookLM infographic, consistent with how Songs/Artists posts source images. Genres category page's last placeholder card replaced — zero placeholders left in that category. Rotation Queue renumbered, slot 1 (Soft Rock) marked done and struck through rather than deleted, so the queue's history stays visible. **Next up**: Queen (Artists), closes the Bohemian Rhapsody link-owed gap. |
| 2026-08-09 | Rotation Queue slot 2 built: Queen published, Live | **Keyword check reversed the task brief's own assumption**: the brief called bare "Queen" more distinctive than "Eagles," but a real SERP check found bare "queen" is dominated by monarchy results (Queen Victoria, Queen Elizabeth, "The Queen" disambiguation) before the band appears; flagged to Charlie instead of guessed. Charlie supplied a real WordStream pull for "Queen band," confirming `queen freddie mercury` (673,000/mo) as the real focus keyword. **New file created**: `keyword-research-log.md`, a site-wide raw keyword-data log separate from this file's planning/rotation role — logs the full Queen pull (real terms vs. contamination), the confirmed keyword, and two future post candidates (`we will rock you` 201K/mo cluster, `brian may and queen` 110K/mo) so they aren't re-derived later. Artist data pulled directly from `data/artists/artists_hard_rock.json` (Queen's real bucket), not general knowledge. Content-gap analysis found currently-ranking pages are whole-career biographies (same pattern as James Brown); built around two specific 1970s nights instead: the Dec 1, 1976 dental-emergency cancellation that put the Sex Pistols on the Bill Grundy show, and the Nov 1975 Bohemian Rhapsody video shoot (kept brief, linked to the site's own full post rather than duplicated). Eleventh distinct structure across Artists/Songs/Genres combined: dual-anchor-contrast, opening on two deliberately paired opposite nights. **Link-owed gap closed both directions**: Queen post links to Bohemian Rhapsody; Bohemian Rhapsody's "Four Hours That Invented the Music Video" section edited to link back, re-verified clean (1,232 words). Removed from the Link Owed table above accordingly. Bonus real link added to Banned Songs of the 70s (Sex Pistols' "God Save the Queen" tie-in), not required but found naturally while writing. `verify_post.py` caught a real false positive: the Yes/No-opener check flagged an answer starting "No rock act had built..." even though the question wasn't yes/no-phrased; reworded rather than debated. Image (1977 News of the World press kit, public domain) deliberately different from the photo already used on the Bohemian Rhapsody post, to avoid reusing the same image across two posts about the same band. Artists category page appended as a straight 6th card. Blog Hub rotation dropped Village People in the 70s. sitemap.xml regenerated (41 URLs). **Next up**: Country Rock of the 70s (Genres, slot 1), the single largest real artist bucket (100) and not on the original content plan at all, surfaced only by the 2026-08-09 data audit. |
