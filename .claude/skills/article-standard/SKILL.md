---
name: article-standard
description: The Article Standard every new article and every upgraded page must meet (ClassicRockArtists.com standard fitted to this site), the page-type schema table, the keyword rule run before writing, and the save-time gate scripts/check_standard.py that refuses a failing page. Use before writing, upgrading, or committing any article, playlist, band/artist page, pillar, chart page, quiz, or tool page.
type: skill
status: active
tags: [article-standard, seo, schema, gates, publishing]
relatedTo: [seo-rules, post-template, prose-image-rules, publishing-workflow, linking-and-tools, youtube-compliance]
---

# Article Standard (from MASTER-PLAN-2026-11.md, set up 2026-11-08)

Site intent: people who want to **hear and remember** 70s music.
Every page answers one of: a list to play, an act's biggest songs, what was #1, who sang or wrote a song.
This standard overrides older rules in seo-rules, post-template and prose-image-rules wherever they conflict.
Legacy pages keep their old shape until their upgrade slot comes up in the queue.

## The gate (save-time, a failing page is not saved)

1. Register the page in `scripts/article_standard_pages.json` before the first commit:
   `"blog/artists/journey-songs/index.html": {"type": "band", "keyword": "journey songs", "subject": "Journey", "secondary": [], "related_songs": null, "pillar": null}`
   (`related_songs` null = auto-detect song stories whose H1 names the act; `pillar` null = path rule.)
2. Run `python3 scripts/check_standard.py <page>` until it prints `RESULT: PASS`.
3. `scripts/verify_post.py` runs the same gate on registered pages and FAILS any page new to git that is not registered.
4. `.git/hooks/pre-commit` (copy of `scripts/hooks/pre-commit`) refuses a commit when a staged registered page fails, a new page is unregistered, or staged HTML names classicrockartists.com. Never use `--no-verify`.
5. `python3 scripts/check_standard.py --registered` and `--site` belong in the PUBLISH GATE list (CLAUDE.md).

A WARN line never fails but must be eyeballed (Title-Case keyword, long quoted passages).

## Rules (gate code in brackets)

| Element | Rule |
| --- | --- |
| Focus keyword [K1] | Highest-volume real phrasing across Google and AI search (keyword rule below). Used naturally. Never leads with a generic word: "Song YMCA" is the example to avoid. Never a lyrics or meaning keyword. |
| Anti-stuffing [K2] | Same limits as ClassicRockArtists: density max 1.0% for a phrase keyword, 2.0% when the keyword is just the subject's name; keyword in max 2 H2s and max 1/3 of H2s; max 2 uses per 300 words (name: 3); never in two consecutive sentences; each secondary keyword max 3 uses; no "Search Intent / Fans Also Search / Best For / Similar To" labels. |
| Keyword placement [P1-P8] | Exact-match focus keyword in every one of these places (set 2026-11-15; this skill is the single authority, seo-rules points here): P1 the `<title>`, at or near the front (max 3 words before it). P2 the URL slug in keyword word order: new pages FAIL, a live URL only WARNs and is never changed. P3 the meta description. P4 the first body sentence. P5 at least one H2 or H3 (the K2 ceiling of max 2 H2s and max 1/3 of H2s still applies). P6 the featured image alt text (the first image above the first H2). P7 the final content section, once (pages of 400+ words). P8 density floor 0.5%, measured on the words outside `<table>` song lists and `ul.post-full-list` link directories. Otherwise a list page's table words would need more uses than the 2-per-300-words ceiling allows in the prose. The K2 ceilings stay as they are. Natural variants carry every other mention. If a sentence only exists to hold the keyword, delete it. |
| Self-contained facts [C1] | Any sentence stating a fact (chart peak, date, writer, lineup, certification) names its subject. No pronoun-led fact sentence ("It reached...", "The band...", "They...", "She...") in the first five intro sentences or as the first sentence under an H2. |
| Question H2s [C4] | Use question-style H2s where they read naturally ("Who Wrote Hotel California?"), with the direct answer as the first sentence under each. Not gated. |
| Information gain [C5] | At least 3 sourced facts or angles that are not on the topic's Wikipedia page, each logged in `sources/log/<slug>.json`. Research from sources, never memory. Checked at review, not gated. |
| On-page basics [O1-O5] | From the seo-rules checklist, gated 2026-11-15: O1 exactly one H1, O2 no skipped heading levels, O3 alt text on every image (FAIL). O4 title 60 chars where possible and O5 meta description max 155 (WARN; O5 becomes FAIL once Journey's 158-char meta is fixed in the quick-fix pass). C4 question H2s is a WARN. |
| Answer first [A1] | The first two sentences answer the search: who sang it, who wrote it, the year, the peak, or the act's biggest hits. The gate needs 2+ facts-box facts in those two sentences. No teaser openers. |
| Listen button on a playlist page | Add `data-playlist="#tableId"` (keep `data-yt` as fallback) and label it "Listen to <page name>": the click starts the list's continuous player from the first song (js/listen-button.js). |
| Facts box [A2] | `<aside class="facts-box"><dl><div><dt>..</dt><dd>..</dd></div>..</dl></aside>` (one `<div>` per fact so the shared `.facts-box` card grid in css/style.css lays it out 3/2/1 columns) right under the intro, before the TOC and the first H2. Song rows: Writer, Artist, Released, Hot 100 peak, Weeks at No. 1. Band or artist rows: Active, Genre, Biggest 70s hits, No. 1 hits. Playlist, album, TV and chart pages also carry one. |
| Writing [W1-W4] | One sentence per paragraph. No em dashes anywhere (body, title, meta). H3s break long sections. No lyrics (no lyrics section; quote speech, never song words). No first-person concert claims ("I saw them live", "my first concert"). |
| Sources [S1-S2] | Sources section with 3+ named outlets, opened this session, Wikipedia never the only source. Log every source in `sources/log/<slug>.json` as `[{"url": "...", "claim": "...", "opened": "YYYY-MM-DD"}]`. Chart data from data/billboard is credited and links `/about/methodology/`. |
| Trust [T1] | Byline `By <a href="https://musicofthe70s.net/about/author/">Charlie</a> &middot; Published Month D, YYYY &middot; Updated Month D, YYYY`. The visible Updated date must equal the schema `dateModified` (gated). No fake freshness (Charlie, 2026-11-15): the Updated date and `dateModified` move to today ONLY when the session makes a real content change (wording, facts, sections, headings, keyword placement). Byline, markup, schema or date-format fixes alone are not content changes. A page that only fails T1 gets both dates set to its real last content-change date from git history (`git log -p -- <page>`), never today. T5 WARNs when `dateModified` is today but the text, headings, title, meta and alts match the last commit before today. Sources linked (S1). |
| Structure [T2-T4] | Collapsible TOC: `<nav class="toc-block"><details class="toc-details" open><summary>Table of Contents</summary><ol>..</ol></details></nav>`, entries match the H2s in order. FAQ (`<section class="faq-block" id="faq">`), 3+ H3 questions, answers 1 to 3 sentences, every answer adds a fact not in the body. "You Might Also Like" section last, 3+ real cards. |
| Listen [L1-L3] | Listen button at the top that plays in place: `<p class="listen-row"><button type="button" class="btn-primary listen-btn" data-yt="ID" data-title="Song - Artist">&#9654; Listen to Song</button></p>` before the first H2 plus `<script src="/js/listen-button.js" defer></script>`. Every list plays through the shared continuous player (`table[data-inline-player]` + `/js/table-player.js`). Official or label uploads only: record each ID in `data/official-videos.json` (`{"official": true, "channel": "...", "verified": "YYYY-MM-DD"}`); fan uploads never qualify. Topic exception (Charlie, 2026-11-09): when no artist, label or VEVO channel has the original recording, a label-delivered "<Artist> - Topic" upload of the original recording qualifies (record `"source": "topic"` and the label); search 4+ ways first. YouTube status must also pass (youtube-compliance skill). |
| Links [N1-N6] | Up to the pillar. Down to every related song story already on the site (and those song pages get a link back up in the same session). 2 to 4 sideways links to pages under the same pillar. At least one link to /radio/ or a tool. Each internal target once across body and cards. Never link to classicrockartists.com. |
| Schema [X1] | Per page type, table below. |
| Verify | Live check on desktop and at 390px (Playwright Chromium). Nothing goes live without Charlie's review (PUBLISH GATE). |

## Schema by page type (the `type` in the registry)

All pages also carry BreadcrumbList and the site's Person author (Charlie, `@id` https://musicofthe70s.net/about/author/). Use `BlogPosting`, not `Article`.

| type | Schema the gate requires |
| --- | --- |
| song | BlogPosting + MusicRecording (name, byArtist, inAlbum, datePublished, recordingOf MusicComposition with composer) + VideoObject for the embed (name, description, thumbnailUrl, uploadDate, embedUrl) + FAQPage |
| band / artist | BlogPosting with about: MusicGroup (band) or Person (artist) with name, genre, sameAs Wikipedia and MusicBrainz, foundingDate for bands + ItemList of MusicRecording + FAQPage |
| playlist | BlogPosting + MusicPlaylist (numTracks = track count, track list of MusicRecording) + FAQPage |
| album | BlogPosting + MusicAlbum (albumProductionType, byArtist, datePublished, track list) + FAQPage |
| tv | BlogPosting with about: TVSeries + VideoObject for clips + FAQPage |
| pillar | CollectionPage + ItemList of the pages it links to |
| chart | BlogPosting + ItemList of MusicRecording + Dataset (Billboard data, links /about/methodology/) |
| quiz | Quiz (scored quiz) |
| trivia | BlogPosting + FAQPage (trivia lists) |
| tool | WebApplication (tools and radio) |

The 2026-09-17 "MusicRecording rejected" decision in seo-rules is superseded by this table.
`scripts/check_schema.py` still runs site-wide on top of this.

## Pillars

| Pillar | URL |
| --- | --- |
| Home | / |
| 70s Songs | /blog/songs/best-songs-of-the-70s/ |
| 70s Number One Hits | /blog/songs/70s-number-one-hits/ (also Years, date pages, Birthday #1 Song Finder, Decade Wheel) |
| 70s Bands & Singers | /blog/artists/70s-bands/ (plus the 70s Rock Bands pillar once built) |
| 70s Genres | /blog/genres/ |
| Listen to 70s Music | /radio/ (also Random 70s Song, Mood Song Matcher) |
| 70s Music Trivia | /blog/trivia/ |

Path rules live in `pillar_for()` in scripts/check_standard.py and in the Pillar column of CONTENT-INDEX.md.
Every song list links to /radio/; every date page links to the Birthday #1 Song Finder.

## Keyword rule (every page, before writing)

1. Pull Google volume for US, Canada and UK (`kw_data_google_ads_search_volume`, location codes 2840, 2124, 2826) and AI volume (`ai_optimization_keyword_data_search_volume`) in DataForSEO for the focus keyword and its variants.
2. Artists and bands: pick "[act] songs" or the bare name, whichever is the bigger songs-intent search.
3. Rows marked "Check name" (Boston, Heart, Bread, Kiss, Rush, America, The Who, Toto, Genesis, Kansas, Yes, Heatwave, The Band, Wings, Chic, War): run `serp_organic_live_advanced` first and skip the act if the results are not about it. Record the skip in the queue file.
4. Floor: under 300 Google and under 50 AI = not built. Mark the row SKIPPED with the numbers.
5. Word-order variants with the same volume: pick the one that reads verbatim in a natural English sentence ("journey songs" over "songs journey"). Never set a keyword the page can't use verbatim, because P1-P8 need the exact phrase.
6. Log every pull in keyword-research-log.md (date, keyword, US/CA/UK, AI, decision).
7. When bands-queue.md or artists-queue.md runs out, research the next rows in DataForSEO and add them.

## Upgrades

An upgrade keeps the URL (no URL changes on live pages, no new redirects).
Register the page in the registry, rebuild it to the standard, and pass the gate before asking Charlie for review.
A title-only retitle (band "[band] songs" rows) changes `<title>`, H1, og/twitter titles and the schema headline only.

## Quick-fix pass on live pages (2026-11-15)

`python3 scripts/check_standard.py --placement` is a read-only audit of every live blog page against P1-P8, C1 and T1.
It takes the keyword from the registry, then the tracker tables, then the slug (only when the slug words appear verbatim in the title and H1).
QUICK = title, meta, opening sentence, one heading's wording, alt text, pronoun-led fact sentences, Updated date, a sentence in the final section, a density gap of 10 uses or fewer (rewording existing variant mentions).
NOT QUICK = no recorded keyword, no featured image, a bigger density gap, anything needing research or new sections. Those pages wait for their upgrades-queue slot.
Never change a live slug in this pass, no redirects. The PUBLISH GATE still applies to every batch.
