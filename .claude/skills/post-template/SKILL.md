---
name: post-template
description: The fixed 15-step blog post structure (H1 → intro → featured image → rest), the internal tool linking map by post type, and the internal-link anchor text/position rotation rule. Use when writing a new blog post, restructuring an existing one, or deciding which tool/anchor text/position to link internally.
---

# Blog Post Template — Full Structure

Every post, no exceptions.

**Content order is fixed and non-negotiable: H1 → intro paragraph → featured image → remaining sections.**
Never place an image (including the featured image) between the H1 and the intro paragraph. Search engines and AI crawlers weight the first ~100 words of body text heavily for topical relevance and featured snippets — an image sitting before that text pushes the keyword-bearing content down the DOM and weakens that signal. It also delays reader orientation, especially on slow connections.

1. SEO metadata block: title, slug, focus keyword, secondary keywords, meta description
2. Schema markup in `<head>` (Article + FAQPage + BreadcrumbList)
3. H1
4. Intro paragraph — hook + focus keyword in the first sentence, within the first 100 words
5. Featured image + descriptive alt text (goes here, AFTER the intro — never before it)
6. Table of Contents block
6a. Playable song list rule (added 2026-10-06, Charlie): any post with a sortable table of Play buttons (`data-inline-player`, or the `#numberOnesTable` / `#oneHitWondersTable` generators) puts that list FIRST after the Table of Contents, ahead of the Short Answer, and lists it first in the TOC. Shared CSS scrolls it in its own ~520px box with a sticky header (`.data-table-wrap:has(> table.sortable-table[data-inline-player])`, or add class `scroll-list`), so no page change is needed beyond the order. Every row needs a Play button: if a song has no `youtube_id`, add a verified one (radio-songs.json, or data/radio/number-one-videos.json for #1 hits never on a Year-End list) and run `python3 scripts/youtube_status.py`. `python3 scripts/audit_song_lists.py` reports list position and rows without Play.
6b. List-page layout rule (added 2026-10-06, Charlie): every page with a playable list (Best Songs, Number One Hits, One-Hit Wonders, Bands, Singers, Female Singers, Disco, the ten Top Songs year pages) also gets: (1) a "Jump to the playable list" button (`<p class="jump-to-list"><a class="btn-primary jump-btn" href="#<list h2 id>">`) right under the byline; (2) the table of contents as `<details class="toc-details" open>` plus the inline script that closes it under 700px (open on desktop, links stay in the HTML); (3) a two-line lead-in between the list H2 and the table, with any method or column notes moved below the table; (4) the Year-End Rank column named "Year-End Rank" (never "Peak": `billboard_peak` in the data mirrors the year-end rank) and a "#1 Hit" column flagged only from `data/billboard/hot100_weekly.json`. Generators: scripts/generate_*_table.py (Disco, Best Songs, year pages). Run `python3 scripts/check_placeholders.py` with the other pre-push checks.
7. 3+ H2 sections, ~200–300 words each, focus keyword appears naturally in at least one heading
8. FAQ section (H3 questions, `.faq-block` styling, 4–5 Q&As, AI-answer-ready per seo-rules skill)
9. Real YouTube video embed (never a placeholder note at publish time)
10. At least one internal link to a site tool — see mapping below
11. Related Posts block — 3 real cards once posts exist in those categories; never link to a post that doesn't exist yet
12. Breadcrumbs: Home › Blog › [Category] › [Post]
13. Word count: 1,200+ minimum
14. Full SEO checklist above, verified before submission (seo-rules skill)
15. Full Prose & Readability Protocol below, verified before submission (prose-image-rules skill)

## Internal Tool Linking Map
Match the post's topic to the most relevant tool and link it naturally in-context, not just tacked on at the end:

Year posts → Birthday #1 Song Finder, 70s Decade Wheel
Song/ranking posts → Random 70s Song Generator, Mood Song Matcher
Genre posts → Random Artist Picker, Random 70s Song Generator
Artist posts → Random Artist Picker, 70s Music Trivia Quiz
Trivia posts → 70s Music Trivia Quiz, Birthday #1 Song Finder

**Songs posts, standing requirement (added 2026-08-31, Charlie-confirmed)**: every Songs post whose track has a `radio_id` in `data/radio/radio-songs.json` gets a text link, anchor text the song title, to `/radio/index.html?play=<radio_id>` (Listen Now, deep-links straight to that song's jukebox tile — see js/radio.js `applyDeepLink()`). Place it naturally in-context, not tacked on; the Waterloo post (2026-08-31) put it right before the embedded video as the precedent. This is in addition to, not instead of, the two Tool links above.

**All Songs posts, standing requirement (added 2026-08-31, Charlie-confirmed)**: every Songs post also gets one text link, anchor text "Music of the 70s", to `/index.html`. Natural in-context placement, not a fixed slot; position should still vary post to post per the Anchor Text & Position Rule below.

## Internal Link Anchor Text & Position Rule (added 2026-08-28)
Applies to every internal link: tool links, same-category related posts, cross-category links.

- Anchor text = brand phrase "Music of the 70s" OR the target's own focus keyword. Never generic ("click here," "this post," "read more").
- Anchor text choice AND its position in the post (intro / which H2 / FAQ / related-posts block) must differ from the last 3–5 posts in the same category. Check the Anchor Text & Position Log in the linking-and-tools skill before placing links; log new entries there after.
- Place links where the reference occurs naturally in a sentence. Never a fixed template slot (e.g. always end of intro).
- Not a ranking guarantee. This follows Google's real internal-linking guidance (descriptive anchor text, natural placement, no manipulative patterns) — it supports discoverability/E-E-A-T, it does not promise top-of-SERP or AI-search placement, no linking system can.
- Log starts 2026-08-28 going forward; pre-existing posts not retroactively audited (token cost).
