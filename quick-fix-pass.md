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
| 103 | blog/songs/mr-blue-sky/ | mr. blue sky | T1 C1 |
| 104 | blog/songs/new-kid-in-town/ | new kid in town | T1 |
| 105 | blog/songs/night-fever/ | night fever | T1 C1 |
| 106 | blog/songs/one-of-these-nights/ | one of these nights | T1 P7 C1 |
| 107 | blog/songs/rhiannon-fleetwood-mac/ | rhiannon fleetwood mac | T1 P4 P6 P7 P8 C1 |
| 108 | blog/songs/rocket-man-elton-john/ | rocket man elton john | T1 P6 P7 C1 |
| 109 | blog/songs/seasons-in-the-sun/ | seasons in the sun | T1 |
| 110 | blog/songs/september-earth-wind-and-fire/ | september earth wind and fire | T1 P6 |
| 111 | blog/songs/sir-duke-stevie-wonder/ | sir duke stevie wonder | T1 P6 P7 |
| 112 | blog/songs/somebody-to-love/ | somebody to love | T1 |
| 113 | blog/songs/song-ymca/ | song ymca | T1 |
| 114 | blog/songs/stairway-to-heaven/ | stairway to heaven | T1 P6 C1 |
| 115 | blog/songs/stayin-alive/ | stayin alive | T1 C1 |
| 116 | blog/songs/superstition-stevie-wonder/ | superstition stevie wonder | T1 P6 |
| 117 | blog/songs/take-a-chance-on-me/ | take a chance on me | T1 P7 C1 |
| 118 | blog/songs/take-it-easy/ | take it easy | T1 |
| 119 | blog/songs/take-me-home-country-roads/ | take me home country roads | T1 P6 P7 |
| 120 | blog/songs/telephone-line-elo/ | telephone line elo | T1 P6 C1 |
| 121 | blog/songs/the-name-of-the-game-abba/ | the name of the game abba | T1 P6 P7 P8 C1 |
| 122 | blog/songs/time-in-a-bottle-jim-croce/ | time in a bottle jim croce | T1 P6 C1 |
| 123 | blog/songs/tiny-dancer/ | tiny dancer | T1 C1 |
| 124 | blog/songs/too-much-heaven/ | too much heaven | T1 C1 |
| 125 | blog/songs/tragedy-bee-gees/ | tragedy bee gees | T1 P6 P7 |
| 126 | blog/songs/we-will-rock-you/ | we will rock you | T1 |
| 127 | blog/songs/whats-going-on-marvin-gaye/ | what's going on marvin gaye | T1 P6 C1 |
| 128 | blog/songs/wish-you-were-here-pink-floyd/ | wish you were here pink floyd | T1 P6 C1 |
| 129 | blog/songs/you-and-i-rick-james/ | you and i rick james | T1 C1 |
| 130 | blog/songs/you-are-the-sunshine-of-my-life/ | you are the sunshine of my life | T1 P7 C1 |
| 131 | blog/songs/you-should-be-dancing/ | you should be dancing | T1 |
| 132 | blog/trivia/70s-music-quiz/ | 70s music quiz | T1 P7 |
| 133 | blog/trivia/april-17-in-music-history/ | april 17 in music history | T1 P6 |
| 134 | blog/trivia/august-19-in-music-history/ | august 19 in music history | T1 P6 |
| 135 | blog/trivia/banned-songs-of-the-70s/ | banned songs of the 70s | T1 |
| 136 | blog/trivia/december-12-in-music-history/ | december 12 in music history | T1 P6 |
| 137 | blog/trivia/december-3-in-music-history/ | december 3 in music history | T1 P6 |
| 138 | blog/trivia/february-1-in-music-history/ | february 1 in music history | T1 P6 |
| 139 | blog/trivia/february-13-in-music-history/ | february 13 in music history | T1 P6 |
| 140 | blog/trivia/january-9-in-music-history/ | january 9 in music history | T1 P6 |
| 141 | blog/trivia/july-15-in-music-history/ | july 15 in music history | T1 P6 |
| 142 | blog/trivia/june-12-in-music-history/ | june 12 in music history | T1 P6 |
| 143 | blog/trivia/march-20-in-music-history/ | march 20 in music history | T1 P6 |
| 144 | blog/trivia/may-1-in-music-history/ | may 1 in music history | T1 P6 |
| 145 | blog/trivia/may-29-in-music-history/ | may 29 in music history | T1 P6 |
| 146 | blog/trivia/november-12-in-music-history/ | november 12 in music history | T1 P6 |
| 147 | blog/trivia/november-19-in-music-history/ | november 19 in music history | T1 P6 |
| 148 | blog/trivia/november-28-in-music-history/ | november 28 in music history | T1 P6 |
| 149 | blog/trivia/november-7-in-music-history/ | november 7 in music history | T1 P6 |
| 150 | blog/trivia/october-8-in-music-history/ | october 8 in music history | T1 P6 |
| 151 | blog/trivia/september-16-in-music-history/ | september 16 in music history | T1 P6 |

## NOT QUICK (queued in upgrades-queue.md, not dropped)

B14: the 10 pages with no recorded focus keyword (keyword rule first, full standard, floor decision recorded). Chicago and ELO run as B13.
B15: 70s Music Trivia full rewrite.

## FAQ-format lines from verify_post (5 batch-1 pages)

MISMATCH and "missing visible question" were a verify_post bug (it compared &#x27; with '), fixed 2026-11-15: schema and visible FAQ text match on all 5.
The remaining "len FAIL" lines are the legacy 40-70-word rule. Article Standard T3 (answers 1 to 3 sentences, each adding a fact) overrides it and all 5 pages pass T3, so no page edit is queued. Open question for Charlie: should verify_post judge registered pages by T3 instead (as it already does for K2)?
