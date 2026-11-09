---
type: plan
status: active
tags: [spokes-queue, new-spokes, master-plan-2026-11]
relatedTo: [master-plan-2026-11, content-build, article-standard]
---

# New Spokes Queue

Source: MASTER-PLAN-2026-11.md "New spokes (keyword table)" (Nov 8, 2026). Rotation slot 5.3 takes the first `queued` row.
70s Christmas Songs runs earlier as build-queue step 3 (time-sensitive, live before December). 70s Rock Bands runs as step 4.3 (pillar).
Re-run the keyword rule (article-standard skill) first; "check" AI volume = pull it at build time. Log pulls in keyword-research-log.md.
Status values: `queued` · `in progress` · `built, awaiting review` · `LIVE` · `SKIPPED (reason)`.

| # | Page | Focus keyword | Google/mo | AI/mo | Pillar | Page type (schema) | Runs at | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | 70s Christmas Songs | 70s christmas songs | 590 | 73 (1970s christmas songs 103) | Listen (time-sensitive: live before December); built under 70s Songs path pillar (/blog/songs/) | playlist | Step 3 | built, awaiting review (2026-11-09) |
| 2 | 70s Rock Bands | 70s rock bands | 14,800 | 1,062 | Bands & Singers (pillar page) | pillar | Step 4.3 | queued |
| 3 | Yacht Rock Songs | yacht rock songs | 9,900 | 851 | Soft Rock (genre) | playlist | 5.3 | queued |
| 4 | Saturday Night Fever Soundtrack | saturday night fever soundtrack | 8,100 | 44 | Disco (genre) | album | 5.3 | queued |
| 5 | Grease Soundtrack | grease soundtrack | 6,600 | 182 | 70s Songs | album | 5.3 | queued |
| 6 | Soul Train | soul train | 33,100 | check | Listen / Soul | tv | 5.3 | queued |
| 7 | American Bandstand | american bandstand | 9,900 | check | Listen | tv | 5.3 | queued |
| 8 | 70s R&B Songs | 70s r&b / 70s r&b songs | 1,600 / 1,000 | 696 / 363 | Soul (genre) | playlist | 5.3 | queued |
| 9 | 70s Country Singers | 70s country singers | 1,900 | 196 | Country (genre) | pillar-style list (choose band/artist list or playlist at build) | 5.3 | queued |
| 10 | Best Albums of the 70s | best albums of the 70s / 70s albums | 1,300 / 720 | 209 / 503 | 70s Songs | playlist or ItemList of MusicAlbum (decide at build) | 5.3 | queued |
| 11 | 70s TV Theme Songs | 70s tv theme songs | 320 | 87 | 70s Songs | playlist | 5.3 | queued |
| 12 | 70s Motown Songs | 70s motown songs | 320 | 76 | Soul (genre) | playlist | 5.3 | queued |
| 13 | 70s Wedding Songs | 70s wedding songs | 320 | 67 | Listen | playlist | 5.3 | queued |
| 14 | 70s trivia posts, engagement content tied to Rock Trivia Game; angle and keywords to be picked with DataForSEO when the row comes up | (pick at build) | (pull) | (pull) | Trivia | trivia | 5.3 | queued |

Order rule: never two pages in the same genre back to back across the whole rotation (Yacht Rock is soft rock, SNF is disco, Soul Train and R&B and Motown are soul). When this queue runs out, research new spokes in DataForSEO and add them.
Genre band sections (70s punk, funk, southern rock bands, disco groups, R&B groups, soul groups) live inside the 70s Bands pillar (upgrades-queue.md A2), not as pages.
