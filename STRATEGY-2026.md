# STRATEGY-2026.md — musicofthe70s.net Content Strategy & Growth Plan
# Source of truth for the 2026 rebuild. Written 2026-09-25 (Claude chat, approved by Charlie).
# Live doc (editable): https://claude.ai/code/artifact/8501cde2-3b11-4a7f-8081-dae4f1eb9478
# CLAUDE CODE: this is a REFERENCE file, not a session-start file. It is exempt from the 195-line
# cap (like the archives). Do not read it whole every session: content-build.md's "Strategy Queue"
# says what's next; open only the section of this file that task needs (grep the "## " headings).
# Every existing rule still applies: PUBLISH GATE, No Hallucination, Keyword Rule, Auto-Go Rule,
# YouTube compliance, one link per target, no templated/scaled batches, one task per session.

---

## 1. Bottom line

Stop running the site as a queue of posts and turn it into **the chart-data authority on 1970s music**: the one place that can answer any "who, what, when, how big" question about the decade from verified Billboard data, and then let you listen to it. Nobody in the current top 10 for "music of the 70s" does both. Spotify, YouTube and Apple own the *listen* intent; Paste and Top40weekly own the *opinion list* intent. The site's 1,000 year-end songs, 253 weekly #1s and 561 charting artists are an asset none of them publish in a usable form.

The five moves, in order:

1. **Fix the plumbing first (weeks 1–2).** Visible byline and dates on every post, cited sources, category hubs that list every post (not 6 + a noindexed archive), confirm the clean-URL fix is live. Google ranks the site at positions 44–96 with zero clicks; some ranking URLs still end in `index.html`.
2. **Rebuild the homepage around the head term's real intent.** The "music of the 70s" SERP is playlists, radio and video. Put Listen Now and a genre/year jump grid above the fold, then the answer-first explainer.
3. **Publish 6 flagship data pages** only this site can make (section 6A). These are the pages AI engines and other writers cite.
4. **Re-aim the Artists rotation at the site's own data.** Elton John (12 year-end hits), The Carpenters (11), Barry Manilow, Chicago, Olivia Newton-John and ELO have zero coverage while the Bee Gees already have 8 song posts.
5. **Earn links.** 7 referring domains cap everything else. Flagship data pages are the link bait; one outreach push per page.

---

## 2. Where the site stands (audit 2026-09-25)

141 URLs in the sitemap. The problem is concentration and trust signals, not volume.

| Area | Live | Read |
| --- | --- | --- |
| Songs | 55 | Bee Gees 8, ABBA 7, Eagles 6, Stevie Wonder 4, Donna Summer 4. Heavy on a few acts. |
| Artists | 24 | 5 are ABBA (band + 4 members). No Elton John, Carpenters, Fleetwood Mac, Led Zeppelin, Chicago. |
| Genres | 12 | Good data-angle titles, but the hub shows only 6. |
| Years | 10 | Complete 1970–1979. Best-ranking pages already ("hits of 1970", pos. 46–59). |
| Trivia | 4 | Static trivia and scored quiz overlap. |
| Tools | 6 + radio | Radio has 1,000 songs. Rock Trivia Game built, unshipped by decision. |

- **Search position:** 24 ranking keywords (DataForSEO), all positions 44–96. GSC 2026-09-24: 0 clicks, 99 not indexed vs 90 indexed, 57 "Page with redirect", 7 "Redirect error" (unidentified).
- **Authority:** 7 referring domains (4 image links), backlink spam score 51.
- **Trust signals (checked on the Tragedy post):** ~2,200 words, TOC, FAQ, attributed photos, a real production detail. But **no visible byline, no published/updated date, zero external source links**. About page names Charlie; no editorial/fact-checking policy.
- **Architecture leak:** category hubs show only the 6 newest posts; the rest sit on `/archive/` pages that are `noindex`, so older posts lose their main internal path.
- **Assets:** `llms.txt` exists. `data/billboard/` holds 1,000 year-end entries, 253 unique weekly #1s, R&B and country charts; 619 artists in 10 genre files.

---

## 3. Competitive landscape

Google US page one for "music of the 70s" (2026-09-25): YouTube video pack, Spotify "70s Hits Top 100", YouTube UMG playlist, AI Overview (cites Reddit, Wikipedia "1970s in music", Spotify, Apple, YouTube), Apple Music 70s Hits Essentials, RadioTunes 70s Hits, Gold Standard Song List (raw table), Paste "100 greatest songs of the 1970s" (critic ranking), Ohio State Fashion2Fiber top-ten list.

- **No independent site owns the head term.** A site that plays the music and explains it with real chart data fits the intent better than a critic list or a raw table.
- **People Also Ask is all chart questions** ("What was the biggest hit in the 70s?", "What were the top 100 songs in 1970?"). The Billboard data answers these better than a playlist.
- **Mid-tail list terms** ("70s bands", "70s one hit wonders") go to Ultimate Classic Rock, Ranker, Forbes, Top40weekly and streaming playlists. None define their lists from chart data — that's the opening.

### Search demand (Google Ads, US, monthly, pulled 2026-09-25)

| Keyword | Vol. | Lands on |
| --- | --- | --- |
| music of the 70s | 27,100 | Homepage |
| 70s music | 27,100 | Homepage |
| songs from the 70s / 70s songs | 18,100 | Best Songs of the 70s (upgrade) |
| 70s disco music | 12,100 | Disco pillar |
| 70s bands | 12,100 | Flagship |
| best 70s songs | 8,100 | Best Songs of the 70s |
| top songs of the 70s | 6,600 | Best Songs of the 70s / #1 timeline |
| 70s love songs | 6,600 | Listening page |
| 70s one hit wonders | 5,400 | Flagship |
| 70s rock songs | 5,400 | 70s Rock pillar |
| 70s hits | 4,400 | Radio / Jukebox |
| 70s country songs | 4,400 | New country pillar |
| 70s female singers | 4,400 | Flagship |
| 70s soul music | 3,600 | Soul pillar |
| 70s dance songs | 2,400 | Disco pillar cluster |
| 70s singers | 1,900 | Biggest Artists flagship |
| 70s music trivia | 590 | Trivia (merge) |
| 70s playlist | 590 | Radio / Jukebox |

Not yet verified (DataForSEO credits ran out): "70s rock bands", "yacht rock", "70s TV theme songs", "70s party songs", "70s road trip songs", "every number one song of the 70s". Keyword Rule applies — verify in WordStream before building.

---

## 4. Positioning

**Line:** *Music of the 70s: every hit, every chart, every story, and you can play it all.*

Every page delivers at least two of these three promises:

| Promise | On the page |
| --- | --- |
| The chart record | Real Billboard numbers: peak, weeks at #1, year-end rank, R&B/country crossovers |
| The story behind it | One verified detail most sites miss (like the Tragedy explosion sound) |
| Press play | Every list deep-links into Listen Now at that song (`/radio/?play=<radio_id>`) |

Two audiences: nostalgia (45+, searches by song/year/"who sang") served by song and year pages; discovery (under 35, arrives from TikTok/soundtracks, wants to hear it first) served by homepage and radio.

Not: a generic opinion top-100, a lyrics site, or a mass-produced page per song.

---

## 5. Site architecture and internal linking

Homepage on top ("Music of the 70s": play button, jump grid, answer-first explainer), five pillars under it, stories underneath:

- **Listen Now** — genre stations, Jukebox Grid, song deep links
- **The Charts (NEW)** — Every #1 hit, one-hit wonders, biggest artists, etc.
- **Genres** — genre pillars, subgenre posts, best-of lists
- **Years** — 1970 to 1979, #1s by year, Birthday #1 tool
- **Artists** — artist pages, member pages, Random Artist Picker
- **Foundation: song stories and trivia** — each links up to its artist, genre pillar, year page and radio slot

### Structural changes

1. **Hubs list everything.** Each category hub shows every post, grouped (songs by artist or year, artists by genre). "Latest" cards on top are fine, but the full list sits on the indexable hub. `/archive/` is no longer the only path to older posts.
2. **Genre pages become real pillars.** Each of the 10 data genres gets one pillar (1,500–2,500 words) linking every artist, song and subgenre post in it, plus "Play this genre" into its radio station. `/blog/genres/70s-rock/` becomes the rock pillar linking its 6 subgenre posts (resolves the flagged overlap).
3. **Year pages become year hubs.** Add "Every #1 of <year>" and links to every song/artist post from that year. Birthday #1 tool links in here.
4. **Artist pages get a Songs block** listing live song posts and chart hits from the data, each with a play link.
5. **Trivia merge.** Scored quiz = primary page for "70s music trivia"; static 64-question post = its "answers and explanations" companion, cross-linked. No 301 unless truly redundant.
6. **Breadcrumbs everywhere** (Home › Genres › Disco › Bee Gees › Night Fever) with BreadcrumbList schema.

### Linking rules

- Keep: one link per target per post, no quotas, one primary destination + up to two secondary.
- Add: every song post links to its **year page** and its **genre pillar**.
- Add: data-generated "Related from the charts" block at the end of every post (same year / artist / genre).
- Anchors: target's focus keyword or song/artist name; homepage anchor stays "Music of the 70s".

---

## 6. Content pillars and priority queue

Next ~40 pieces: ~30% upgrades, ~20% flagship data pages, ~50% new stories.

### 6A. Flagship data pages ("The Charts" pillar)

One deep, sourced page each, built from `data/billboard/`: sortable table, answer-first summary, methodology note, play links into the radio. **One per session, never a templated batch.**

| # | Page | Focus keyword | Vol. | Built from |
| --- | --- | --- | --- | --- |
| 1 | Every #1 Hit of the 1970s | verify | verify | 253 unique weekly #1s, `hot100_weekly.json` |
| 2 | 70s One-Hit Wonders, by the charts | 70s one hit wonders | 5,400 | Year-end + weekly data; each act verified as its only US Top 40 hit |
| 3 | The Biggest Artists of the 1970s | 70s singers | 1,900 | Year-end counts (Bee Gees, Elton John 12 each; Carpenters 11) |
| 4 | The Biggest 70s Bands | 70s bands | 12,100 | Same data, groups only, genre + radio links |
| 5 | 70s Female Singers | 70s female singers | 4,400 | Women in the data (Karen Carpenter, Helen Reddy, ONJ, Donna Summer, Carole King…) |
| 6 | 70s #1 Hits Timeline | top songs of the 70s (check vs Best Songs) | 6,600 | Week-by-week #1 run, interactive |

One-hit wonder definition: 368 acts appear on the year-end lists only once — far too broad. Define as "one Top 40 hit in their whole US career", verify each act, state the definition on the page.

### 6B. Upgrades to existing pages

| Page | Target | Vol. | Change |
| --- | --- | --- | --- |
| Homepage | music of the 70s / 70s music | 27,100 each | Play-first layout, jump grid, ~150-word answer block, FAQ from PAA |
| Best Songs of the 70s | songs from the 70s, best 70s songs | 18,100 + 8,100 | Expand to 100 songs with year, peak, play link; explain selection method |
| Disco Music of the 70s | 70s disco music | 12,100 | Disco pillar; add 70s dance songs section |
| 70s Rock | 70s rock songs | 5,400 | Rock pillar linking the 6 subgenre posts |
| 70s Soul Music | 70s soul music | 3,600 | Link every soul/R&B post; add R&B chart #1s |
| Top Songs of 1970–1979 | hits of 1970, etc. | 590–720 each | "#1s this year" block, play links, link every song post of that year |
| Trivia pair | 70s music trivia | 590 | Scored quiz primary, static post = answers companion |

### 6C. New genre pillar

- **70s Country Music** (`70s country songs`, 4,400). Country is the biggest artist bucket (100 artists); Dolly Parton, Willie Nelson, Jolene etc. already live, but only a country-rock page exists.

### 6D. Artists rotation (re-aimed)

Alternate a **chart giant** (big in the data, zero coverage) with a **search giant**. No ABBA or Bee Gees posts before 2026-11-25.

| Order | Artist | Why | Bucket |
| --- | --- | --- | --- |
| 1 | Elton John | 12 year-end hits | pop-crossover |
| 2 | Led Zeppelin | Search giant; albums-over-singles angle | hard rock |
| 3 | The Carpenters | 11 year-end hits | soft rock |
| 4 | Fleetwood Mac | Search giant; "Dreams" in the AI Overview | soft rock |
| 5 | Chicago | 8 year-end hits | classic rock |
| 6 | Pink Floyd | Search giant; prog pillar anchor | prog rock |
| 7 | Olivia Newton-John | 8 year-end hits; country/pop crossover | country / pop |
| 8 | Electric Light Orchestra | 8 year-end hits | prog / pop |
| 9 | The Jackson 5 | 7 year-end hits, 4 #1s | soul |
| 10 | Earth, Wind & Fire | Named in the AI Overview for disco/funk | funk |

Then: Barry Manilow, Three Dog Night, Helen Reddy, Gladys Knight & the Pips, KC and the Sunshine Band, John Denver, Diana Ross. Yes and Genesis: sections of the prog pillar, not standalone pages (few US singles).

### 6E. Songs rotation (re-aimed)

- New ~30-song round-robin batch drawn only from 6D artists once their pages are live; same quality gate.
- Favor songs with their own search demand (e.g. "Your Song", "Dreams", "Stairway to Heaven", "September", "We've Only Just Begun"); verify each first.

### 6F. Listening pages tied to the radio (cap: 4)

- 70s Love Songs (6,600), 70s Party Songs (verify), 70s Road Trip Songs (verify), 70s Slow Songs (390 — fold into Love Songs if thin).
- Real editorial lists: 25–40 songs, one verified line of story each, year and peak, "Play the whole list" into Listen Now.

### 6G. Freshness track

- **This Week in 1970s Music**: one weekly post from `hot100_weekly.json` (what was #1 this week in each year of the decade), with real commentary, not a data dump. Max 52/year.

---

## 7. AI search playbook (AI Overviews, ChatGPT, Perplexity, Gemini)

### Every page

1. **Answer block first:** 40–60 words under the H1 answering the main question with the key number.
2. **Self-contained H2s:** name the song/artist again rather than "it"/"the band".
3. **Fact table per post:** released, peak, weeks at #1, year-end rank, writers, producer, label.
4. **Cite sources inline:** Billboard chart pages, RIAA database, official artist sites, interviews. **3+ external citations per post.** Biggest single gap today.
5. **Visible byline + dates:** "By Charlie · Published … · Updated …" linking to the author page; match in Article schema (`author`, `datePublished`, `dateModified`).
6. **FAQ from real questions** (People Also Ask, Reddit), not invented ones. Keep FAQPage schema.
7. **Entity schema:** MusicRecording for songs (`byArtist`, `datePublished`, `recordingOf`); MusicGroup/Person for artists with `sameAs` → Wikipedia, Wikidata, MusicBrainz, AllMusic.

### Site-level

- **llms.txt:** update each time a flagship ships; list the Charts pillar first.
- **robots.txt:** allow GPTBot, OAI-SearchBot, PerplexityBot, ClaudeBot, Google-Extended (unless Charlie decides otherwise).
- **Bing Webmaster Tools + IndexNow** (Cloudflare toggle) — Charlie does this; feeds ChatGPT search and Copilot.
- **Methodology page:** data sources, song verification, YouTube checks, corrections. Linked from every data page.
- **Reddit/forums:** genuine answers on r/70smusic, r/ClassicRock, r/OldSchoolCool, link only when it's the best answer. Never spam.

### Monthly test

Ask ChatGPT, Perplexity and Google AI Mode the same 10 questions ("What was the biggest hit of 1976?", "Who had the most #1s in the 70s?", "What were the 70s one-hit wonders?" …) and log whether the site is cited. Lost questions go into the queue.

---

## 8. Technical and trust fixes (Phase 0 — do first)

| # | Fix | Why | Effort |
| --- | --- | --- | --- |
| 1 | Confirm the 2026-09-24 clean-URL fix is pushed and live; resubmit sitemap; request indexing on the 10 Years pages | `/index.html` URLs still ranking | 1 session |
| 2 | Identify and fix the 7 GSC "Redirect error" URLs | Blocks those pages | part of #1 (Charlie exports the list from GSC) |
| 3 | Visible byline + published/updated dates on every post, matched in schema | E-E-A-T, AI citation | 1 session |
| 4 | Author page for Charlie (why he writes about the decade, 80s concerts, process, links to his other music sites) | Real-person signal | 1 session |
| 5 | Methodology / editorial policy page | Trust + citable | 1 session |
| 6 | Category hubs list every post | Fixes orphaned older posts | 1 session |
| 7 | 3+ external source links on existing posts, starting with Years pages and Best Songs of the 70s | Largest content-quality gap | rolling, 5 posts/session |
| 8 | Bing Webmaster Tools + IndexNow | ChatGPT/Copilot index | Charlie, 30 min |
| 9 | robots.txt AI-crawler review; llms.txt refresh | AI discovery | 15 min |
| 10 | Schema audit: MusicRecording, MusicGroup/Person with `sameAs`, BreadcrumbList | Entity linking | 1 session |
| 11 | Core Web Vitals on /radio/ and tools: click-to-load facade that still shows the visible player (YouTube compliance) | Mobile ranking | 1 session |
| 12 | AdSense readiness pass after 1–6 (Privacy Policy ad disclosure, no ads near players) | Per CLAUDE.md | checklist |

---

## 9. 90-day rollout (one Claude Code session/day, 5 days/week)

| Weeks | Dates | Focus |
| --- | --- | --- |
| 1–2 | Sep 28 – Oct 9 | Phase 0 fixes 1–11; Bing + IndexNow; author + methodology pages |
| 3 | Oct 12–16 | Homepage rebuild; hubs list every post; Flagship #1 Every #1 Hit |
| 4 | Oct 19–23 | Best Songs of the 70s upgrade; Artist: Elton John; first Elton John song |
| 5 | Oct 26–30 | Flagship #2 One-Hit Wonders; Artist: Led Zeppelin; start This Week in 1970s Music |
| 6 | Nov 2–6 | Disco pillar; Artist: The Carpenters; source pass on Years pages |
| 7 | Nov 9–13 | 70s Country Music pillar; Artist: Fleetwood Mac; songs for Elton, Zeppelin |
| 8 | Nov 16–20 | Flagship #3 Biggest Artists; Rock pillar consolidation; Artist: Chicago |
| 9 | Nov 23–27 | 70s Love Songs page; Artist: Pink Floyd; trivia merge |
| 10 | Nov 30 – Dec 4 | Flagship #4 70s Bands; Soul pillar; Artist: Olivia Newton-John |
| 11 | Dec 7–11 | Flagship #5 Female Singers; Artist: ELO; outreach for flagships 1–4 |
| 12 | Dec 14–18 | 70s Party Songs; Artist: Jackson 5; songs round-robin |
| 13 | Dec 21 – Jan 1 | Flagship #6 #1 Hits Timeline; 90-day KPI review |

**Weekly rhythm after Phase 0:** Mon flagship/upgrade · Tue artist · Wed song · Thu This Week in 1970s Music · Fri song or source-citation pass.

**Outreach (from week 5, Charlie):** per flagship, 10–15 genuine contacts — oldies stations/DJs, 70s tribute bands, music-history newsletters/podcasts, newspaper nostalgia columns, Wikipedia list-page editors (as a cited source, never spam).

**Seasonal hooks:** Halloween, Thanksgiving road trips, December parties, January 2027 "50 years ago" (1977's #1s turning 50).

---

## 10. Measurement (check at 30 / 60 / 90 days)

| KPI | 2026-09-25 | Day 30 | Day 90 |
| --- | --- | --- | --- |
| Indexed pages (GSC) | 90 of 189 | 85%+ of sitemap | 95%+ |
| Page with redirect / Redirect error | 57 / 7 | 0 new | 0 |
| Keywords in top 20 | 0 | 5+ | 30+ |
| Monthly search clicks | 0 | first clicks | 500+ |
| Referring domains | 7 | 9+ | 15+ |
| AI citations (10-question test) | not measured | baseline | 2+ of 10 |
| Posts with byline, dates, 3+ sources | ~0 | 100% of new | 100% site-wide |

Early signals: Years pages moving from the 40s–50s into the top 20; impressions on flagship keywords within 3 weeks of launch. To-do for Charlie: add musicofthe70s.net to the GSC MCP connector on the Chromebook (currently only classicrockartists.com).

---

## 11. Sources

- Live site, sitemap, About page, Tragedy post, Genres hub — fetched 2026-09-25
- Repo: content-build.md, CLAUDE.md, keyword-research-log.md, data/billboard/year_end_hot100.json, data/billboard/hot100_weekly.json
- DataForSEO (2026-09-25): Google US SERP "music of the 70s", Google Ads volumes, ranked keywords + backlink summary for musicofthe70s.net
- Competitors: pastemagazine.com, goldstandardsonglist.com, top40weekly.com, ultimateclassicrock.com, ranker.com, forbes.com, en.wikipedia.org/wiki/1970s_in_music
