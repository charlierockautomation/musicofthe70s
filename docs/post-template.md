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
7. 3+ H2 sections, ~200–300 words each, focus keyword appears naturally in at least one heading
8. FAQ section (H3 questions, `.faq-block` styling, 4–5 Q&As, AI-answer-ready per seo-rules.md)
9. Real YouTube video embed (never a placeholder note at publish time)
10. At least one internal link to a site tool — see mapping below
11. Related Posts block — 3 real cards once posts exist in those categories; never link to a post that doesn't exist yet
12. Breadcrumbs: Home › Blog › [Category] › [Post]
13. Word count: 1,200+ minimum
14. Full SEO checklist above, verified before submission (seo-rules.md)
15. Full Prose & Readability Protocol below, verified before submission (prose-image-rules.md)

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
- Anchor text choice AND its position in the post (intro / which H2 / FAQ / related-posts block) must differ from the last 3–5 posts in the same category. Check the Anchor Text & Position Log in content-build.md before placing links; log new entries there after.
- Place links where the reference occurs naturally in a sentence. Never a fixed template slot (e.g. always end of intro).
- Not a ranking guarantee. This follows Google's real internal-linking guidance (descriptive anchor text, natural placement, no manipulative patterns) — it supports discoverability/E-E-A-T, it does not promise top-of-SERP or AI-search placement, no linking system can.
- Log starts 2026-08-28 going forward; pre-existing posts not retroactively audited (token cost).