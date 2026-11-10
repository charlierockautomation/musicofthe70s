---
type: plan
status: active
tags: [upgrades-queue, retarget, retitle, master-plan-2026-11]
relatedTo: [master-plan-2026-11, content-build, article-standard]
---

# Upgrades Queue (live pages, URL never changes)

Source: MASTER-PLAN-2026-11.md "Live pages to retarget or upgrade" and the band retitle list (Nov 8, 2026).
No URL changes, no new redirects. Every upgrade registers the page in scripts/article_standard_pages.json and passes scripts/check_standard.py, then waits for Charlie's review.
Re-run the keyword rule (article-standard skill) before each row; log pulls in keyword-research-log.md.
Status values: `queued` · `in progress` · `built, awaiting review` · `LIVE` · `SKIPPED (reason)`.

## A. Retargets that run in build-queue step 4 (pillars first)

| # | Page | URL | New focus keyword | Google/mo | AI/mo | Change | Runs at | Status |
|---|---|---|---|---|---|---|---|---|
| A1 | Best Songs of the 70s | /blog/songs/best-songs-of-the-70s/ | 70s songs (+ best 70s songs) | 18,100 / 8,100 | 14,243 / 1,531 | Retitle, expand into the 70s Songs pillar (type pillar) | 4.1 | queued |
| A2 | 70s Bands | /blog/artists/70s-bands/ | 70s bands (+ 70s artists) | 12,100 / 2,400 | 2,441 / 1,004 | Hub over every band and artist page, genre sections (punk 1,000, funk 590, southern rock 590, disco groups 480, R&B groups 480, soul groups 260) | 4.2 | LIVE 2026-11-09 |
| A3 | Birthday #1 Song Finder | /pages/birthday-number-one | number one song on my birthday | 1,300 | 19 | Real content section, FAQ, linked from every date page (rework with the #1 Hits hub) | 4.4 | LIVE 2026-11-09 |
| A4 | 70s Number One Hits | /blog/songs/70s-number-one-hits/ | 70s number one hits (+ top songs of 19XX) | 480 + 2,400 to 2,900 per year | 2 + 197 to 362 per year | Hub: links to Years, the Birthday #1 Song Finder and the date pages | 4.4 | LIVE 2026-11-09 |
| A5 | Listen Now radio | /radio/ | 70s hits (+ 70s radio) | 4,400 / 880 | 4,238 / 1,376 | Answer-first article section under the player (type tool) | 4.5 | LIVE 2026-11-10 |
| A6 | Disco Music of the 70s | /blog/genres/disco-music-of-the-70s/ | 70s disco songs (+ disco songs) | 12,100 / 14,800 | 574 / 6,418 | Full playable list, hub links | 4.6 | LIVE 2026-11-10 |
| A7 | 70s Soul Music | /blog/genres/70s-soul-music/ | 70s soul songs (+ 70s soul music) | 3,600 / 3,600 | 253 / 7 | Playable list, hub links | 4.6 | queued |
| A8 | Pop Songs of the 70s | /blog/genres/pop-songs-of-70s/ | 70s pop songs | 3,600 | 17 | Retitle to the exact phrase | 4.6 | queued |
| A9 | 70s Soft Rock | /blog/genres/70s-soft-rock/ | 70s soft rock (+ songs) | 2,900 / 880 | 309 / 205 | Link to the yacht rock page once it exists | 4.6 | queued |
| A10 | 70s Funk | /blog/genres/70s-funk/ | 70s funk songs (+ 70s funk) | 720 / 1,300 | 175 / 269 | Playable list | 4.6 | queued |

Step 4.6 is five pages: one per session, in the order A6, A7, A8, A9, A10.

## B. Rotation slot 5.6 (upgrade an existing page to the standard), in this order

| # | Page | URL | Current title / H1 | Change | Status |
|---|---|---|---|---|---|
| B1 | YMCA (Google ranks it first) | /blog/songs/song-ymca/ | Song YMCA: The Studio Question That Built a Disco Anthem | Full upgrade. Re-pick the keyword (the plan's "Song YMCA" example to avoid; check "ymca song" / "ymca" / "y.m.c.a." in DataForSEO). Gate dry run 2026-11-08 failed 15 checks: K1, K2 cluster, A1, A2, S1, S2, T1, T3, T4, L1, L3, N1, N5, X1 (see content-build.md) | queued |
| B2 | How Can You Mend a Broken Heart (Google ranks it first) | /blog/songs/how-can-you-mend-a-broken-heart/ | (check at build) | Full upgrade | queued |
| B3 | Somebody to Love (Google ranks it first) | /blog/songs/somebody-to-love/ | Somebody to Love: The Song Freddie Mercury Wrote Alone | Full upgrade | queued |
| B4 | ABBA | /blog/artists/abba/ | ABBA: The Band That Needed Permission for Its Own Name | Retitle to "ABBA songs" (60,500), title and H1 only. Not a new ABBA post, so the ABBA/Bee Gees new-post block does not apply | queued |
| B5 | Queen | /blog/artists/queen-freddie-mercury/ | Queen Freddie Mercury: Two Nights That Defined Their 70s | Retitle to "Queen songs" (49,500), title and H1 only | queued |
| B6 | Bee Gees | /blog/artists/bee-gees/ | Bee Gees: The Story of Pop's Most Successful Sibling Act | Retitle to "Bee Gees songs" (40,500), title and H1 only | queued |
| B7 | Eagles | /blog/artists/eagles-the-band/ | Eagles the Band: The Lineup Swap That Changed Everything | Retitle to "Eagles songs" (40,500), title and H1 only | queued |
| B8 | Grateful Dead | /blog/artists/grateful-dead/ | Grateful Dead in the 70s: The Band the Charts Missed | Retitle to "Grateful Dead songs" (27,100), title and H1 only | queued |
| B9 | Talking Heads | /blog/artists/talking-heads/ | Talking Heads: Built From Found Objects, Not a Plan | Retitle to "Talking Heads songs" (18,100), title and H1 only | queued |
| B10 | Village People | /blog/artists/village-people/ | Village People in the 70s: The Disco Act Everyone Missed | Retitle to "Village People songs" (5,400), title and H1 only | queued |
| B11 | Chicago | /blog/artists/chicago-band-songs/ | Chicago Songs: The Band's 12 Hits Played, 1 at Number One | DataForSEO Nov 9 (US): "chicago songs" ~2,840 clickstream vs "chicago band songs" ~260 (40,500 combined, KD 13, mixed intent city/musical). Title + H1 lead with "Chicago Songs", "the band" early; focus keyword chicago songs; URL unchanged | LIVE 2026-11-09 (retitle) |
| B12 | ELO | /blog/artists/electric-light-orchestra-songs/ | ELO Songs: Electric Light Orchestra's 11 Hits, 5 Top Tens | DataForSEO Nov 9 (US): "elo songs" ~1,290 clickstream vs "electric light orchestra songs" ~310 (22,200 combined, KD 19). Title + H1 lead with "ELO Songs", then "Electric Light Orchestra"; focus keyword elo songs; URL unchanged | LIVE 2026-11-09 (retitle) |
| B13 | Chicago + ELO | (both pages above) | (unchanged) | Full Article Standard upgrade still owed: check_standard.py 2026-11-09 fails ELO 12 checks, Chicago 11 (facts box, answer-first, Sources, Updated date, FAQ repeats body, You Might Also Like, Listen button, official-videos records, schema BlogPosting/MusicGroup/ItemList, N2/N3/N5 links). Keyword checks K1/K2 pass. Register in article_standard_pages.json when upgraded | queued |

Title check 2026-11-08, no change needed (title and H1 already carry "[band] songs"): Fleetwood Mac, Led Zeppelin, Earth Wind & Fire, Pink Floyd, Three Dog Night, Carpenters, Jackson 5, KC and the Sunshine Band.
After B13, slot 5.6 takes the next existing page by Google rank or volume (pull ranked keywords for the domain in DataForSEO and add rows here).
