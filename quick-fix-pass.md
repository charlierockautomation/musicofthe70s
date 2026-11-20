---
type: plan
status: active
tags: [quick-fix-pass, article-standard, keyword-placement, ai-citation]
relatedTo: [article-standard, content-build, upgrades-queue]
---

# Quick-Fix Pass (live pages, started 2026-11-15)

Live blog pages that fail only the quick-fix checks of `scripts/check_standard.py` (P1-P8 keyword placement, C1 pronoun-led fact sentences, T1 Updated date = schema dateModified).
Regenerate this list any time with `python3 scripts/check_standard.py --placement` (read-only).
Rules: never change a live slug, no redirects, no new research or sections (those pages wait for upgrades-queue.md).
Batches of 10 to 15 pages per session in the order below (highest search volume first: Years, Genres, Artists, Songs, Trivia).
Every fixed page must pass `--placement`. PUBLISH GATE applies to every batch: build, preview, Charlie's go-ahead, then commit and push.
Delete a row once its batch is LIVE. When the table is empty, remove the Quick-fix pass item from content-build.md and delete this file.
Most pages need T1 only: add `&middot; Updated Month D, YYYY` to the byline and set the schema dateModified to the same date.

Batch 1 (the 13 registered pages): LIVE 2026-11-15 (5c44ebd, regen e383552), 13/13 live URLs verified.
Batch 2 (12 Years + Genres pages): LIVE 2026-11-15 (24a168e, regen 49cdfcb), 12/12 live URLs verified.
Batch 3 (15 artist pages A to E, plus Journey meta and C5): LIVE 2026-11-15 (9bf912c, regen 98f59dc), 16/16 live URLs verified.
Batch 11 (rows 132-151, Quiz, Banned Songs and 18 date pages): LIVE 2026-11-19 (6efd722), 20/20 live URLs 200 with real dates, hub has Journey and Rock Bands. Date pages: datePublished = real git first-commit date (was 2027 calendar date), byline "Published X, Updated Nov 19, 2026", dateModified 2026-11-19, keyword in featured image alt; the 18 .tpl templates and generator DATE constants updated to match (jul_15 regen diff = only these edits). Quiz (Oct 9) and Banned (Oct 23) T1-only from git. Blog hub and homepage Latest rows now sort by real dates: Journey and 70s Rock Bands are back in. Dolly Parton O2 (h1>h3) is the only QUICK page left (row 152).
Batch 10 (rows 118-131, 14 song pages Take It Easy to You Should Be Dancing): LIVE 2026-11-19 (dee7c51, sitemap in tracker commit). Content edits = Nov 19 (11 pages); T1-only from git (Take It Easy, We Will Rock You = Oct 23; You Should Be Dancing Nov 10). Country Roads: P7 keyword in closing line raised the K2 window 9 to 10 and density to 1.04%; fixed by "wrote the song" in the FAQ answer and its schema text (2 places). Next = row 132 (trivia date pages, P6 = keyword in featured image alt).
Batch 9 (rows 103-117, 15 song pages Mr. Blue Sky to Take a Chance on Me): LIVE 2026-11-19 (965188f, sitemap in tracker commit). Content edits = Nov 19 (11 pages); T1-only from git (New Kid in Town, Seasons in the Sun = Nov 11; Somebody to Love, Song YMCA = Oct 23). Rhiannon: P4 keyword in first sentence raised the K2 window 3 to 4, fixed by moving the keyword from the origin H2/TOC to the charts H2/TOC and adding two FAQ H3 uses (P8 0.52%).
Batch 8 (rows 88-102, 15 song pages I'll Be There to Midnight Train to Georgia): LIVE 2026-11-19 (3302ed2, regen unchanged, sitemap in tracker commit). Content edits = Nov 19 (13 pages); T1-only from git (Killer Queen Oct 23, Midnight Train Nov 10). Let's Get It On P7 met by a closing line after the Mood Song Matcher line; Kashmir P4 keyword moved from the next intro line (K2 window kept at 4).
Batch 7 (rows 73-87, 15 song pages Dreams to If You Leave Me Now): LIVE 2026-11-19 (b5b8fc5, sitemap in tracker commit). Content edits = Nov 19 (11 pages); T1-only from git (Heartache Tonight, Hotel California = Oct 23; How Deep Is Your Love Nov 11; I Am Woman Oct 18). C1 detector flags generic "The song/single/band" openers too; name the act ("Parliament's single"). I Will Always Love You: P4 keyword moved out of the closing intro line so the K2 window did not rise.
Batch 6 (rows 58-72, 15 song pages Al Green to Hot Stuff): LIVE 2026-11-19 (2dce712, sitemap regen in the tracker commit). Content edits = Nov 19 (10 pages); T1-only from git (Bohemian Rhapsody, Dancing Queen = Oct 23; Comfortably Numb Oct 25; Close to You Nov 10; Bridge Over Troubled Water Nov 11). Carole King P7 met by keyword in the closing line, not the H2 (an H2 edit raised K2 window 5 to 6). Tired of Being Alone keyword now in 2 of 6 H2s (limit 2).
Batch 5 (rows 43-57, artists R-W + songs to ABBA Waterloo): LIVE 2026-11-16 (d3a0619, sitemap 72893e5), 15/15 live dates verified. Content edits = Nov 16; T1-only from git (Rick James, Talking Heads = Oct 23; Three Dog Night Oct 14; Love Songs, Party Songs Oct 24). List templates (dance, road trip, slow, party) carry the edits; slow-songs generator drifts (pool 536 vs 535), do not rerun it in a quick-fix.
Batch 4 (15 artist pages F to Q): LIVE 2026-11-16 (8bd38f0, sitemap e646b09), 15/15 live URLs verified. Content edits = Nov 16; T1-only from git (George Clinton, Iggy Pop, Queen = Oct 23; Jackson 5 Oct 13; John Denver Oct 15; Pink Floyd Oct 12).
Batch 3 dates: content edits = Nov 15; T1-only from git (Bee Gees, Bjorn Ulvaeus, Carole King, Eagles = Oct 23 Sources section; Diana Ross Oct 16; EWF Oct 14).
Dates (Charlie, 2026-11-15): today only on a real content change; a T1-only page gets its real last content-change date from git history (Hard Rock 2026-10-09, Punk Rock 2026-10-06, 70s Rock 2026-10-09).
Found in batch 2: all 12 legacy pages already fail the K2 stuffing ceilings (worst 300-word window 5 to 8, several with the keyword in 3+ H2s). Edits in this pass never raise K2; de-stuffing is not in the quick-fix scope yet (open question for Charlie).

Batch 3 also: Journey meta trimmed to 152 chars, O5 switched to FAIL (upgrades-queue C5 done).

| # | Page | Keyword | Fails |
|---|---|---|---|
| 152 | blog/artists/dolly-parton/ | dolly parton | O2 heading order (h1>h3) |

## NOT QUICK (queued in upgrades-queue.md, not dropped)

B14: the 10 pages with no recorded focus keyword (keyword rule first, full standard, floor decision recorded). Chicago and ELO run as B13.
B15: 70s Music Trivia full rewrite.

## FAQ-format lines from verify_post (5 batch-1 pages)

MISMATCH and "missing visible question" were a verify_post bug (it compared &#x27; with '), fixed 2026-11-15: schema and visible FAQ text match on all 5.
The remaining "len FAIL" lines are the legacy 40-70-word rule. Article Standard T3 (answers 1 to 3 sentences, each adding a fact) overrides it and all 5 pages pass T3, so no page edit is queued. Open question for Charlie: should verify_post judge registered pages by T3 instead (as it already does for K2)?
