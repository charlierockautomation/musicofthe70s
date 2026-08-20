# SEO Rules — Full Detail

## THE KEYWORD RULE — NON-NEGOTIABLE
This is the most important section in this doc. Every post starts here, before a single word of content is written.

1. **The focus keyword must be how real people actually search** — never invented, never chosen because it "sounds natural." Verify against:
   - Google's People Also Ask box for the topic
   - Google autocomplete/related searches
   - Any keyword volume data already gathered for the site (WordStream, Ahrefs, KeywordKeg exports)
   - NotebookLM research briefs sometimes surface real phrasing too — check them

2. **Slug must contain the focus keyword in the exact same word order as the keyword itself.**
   - Keyword: `top songs of 1970` → Slug: `top-songs-of-1970`
   - Never: keyword `top songs of 1970` with slug `1970-in-music` — word order must match.

3. **Title should lead with the focus keyword** where it reads naturally. Don't force it into an awkward first three words if it breaks readability — but it should appear at or near the front of the title, not buried at the end.

4. **Density — use it correctly, never stuff it:**
   - Keyword density is calculated as: (number of times the exact focus keyword phrase appears ÷ total word count) × 100.
   - Example: 10 uses in a 1,000-word post = 1% density.
   - Target range: 0.5%–2% density is normal and natural. Going over 3% starts to read as spam to readers and should be avoided.
   - Don't aim for a strict percentage as a hard target. Modern search engines and human readers both prefer natural language over forced placement. Use the 0.5%–2% range as a sanity check against stuffing, not a quota to hit exactly.
   - It MUST appear in: the title, the meta description, the first 100 words of the intro, at least one H2 or H3 heading, and the URL slug.
   - It should NEVER appear in two consecutive sentences, never appear unnaturally (e.g. tacked onto the end of a sentence that doesn't need it), and never appear in a way a human reader would notice as repetitive.
   - Secondary/related keywords (2–3 per post) carry the rest of the semantic weight naturally through the body. This is what actually pushes topical relevance now — not keyword repetition.

5. If a post's real search-intent keyword doesn't fit the URL structure cleanly, flag it and ask before proceeding rather than guessing.

## SEO Scoring Target (no plugin — this is manual, but the target is real)
Because this is a static site with no Rank Math or Yoast, "the high 90s" means hitting every item below, not a plugin score. Treat this as the actual checklist:

- [ ] Focus keyword in title (near the front)
- [ ] Focus keyword in slug (exact word order match)
- [ ] Focus keyword in meta description
- [ ] Focus keyword in first 100 words
- [ ] Focus keyword in at least one H2/H3
- [ ] Focus keyword density 0.5%–2% (uses ÷ total words × 100), never stuffed, never over 3%
- [ ] 2–3 secondary keywords woven naturally throughout
- [ ] Meta description ≤155 characters, includes keyword, written to earn the click (not just descriptive)
- [ ] Title tag ≤60 characters where possible
- [ ] At least one internal link to a site tool (see post-template.md)
- [ ] At least one internal link to a related blog post (once one exists in that category)
- [ ] Featured image has descriptive alt text containing the keyword or a close variant
- [ ] All images have alt text — none blank, none generic ("image1.jpg")
- [ ] H1 used exactly once per page, matches or closely echoes the title
- [ ] Heading hierarchy is clean — no skipped levels (H2 before H3, never H3 before H2)
- [ ] No wall-of-text H2 sections — long unbroken paragraph runs get real, specific H3 subheadings (see Subheading Rule in prose-image-rules.md)
- [ ] Schema markup present: Article + FAQPage + BreadcrumbList (see below)
- [ ] Word count 1,200+ for blog posts
- [ ] FAQ section present, written for direct AI/answer-engine extraction (see below)
- [ ] Mobile check passed at 375px and 390px (see publishing-workflow.md)
- [ ] No broken links, no placeholder text of any kind remaining
- [ ] Page loads with no console errors
- [ ] Content order correct: H1 → intro paragraph → featured image → rest (image never sits before the intro)
- [ ] Prose & Readability Protocol followed (see prose-image-rules.md)
- [ ] All images optimized per prose-image-rules.md

A post is not "done" until every box above is checked. Report the checklist status when a post is submitted for review.

## AI Answer Engine / FAQ Optimization
FAQ answers are written to be lifted whole by AI search (ChatGPT, Perplexity, Google AI Overviews, voice assistants) as a standalone correct answer with no other context.

Rules for every FAQ entry:
- Question phrased exactly as a person would type or speak it
- Answer is 40–70 words, one self-contained paragraph
- Answer restates the key fact in its own first sentence — never opens with "Yes" or "No" alone
- No reference to "as mentioned above" or anything requiring the rest of the page for context
- Every fact must be traceable to the research brief/source material — no invented specifics
- 4–5 FAQ entries minimum per post

## Schema Markup (required on every blog post)
Every blog post needs JSON-LD schema in the `<head>` covering:
- `Article` (headline, datePublished, author, image)
- `FAQPage` (mainEntity array matching the visible FAQ block exactly — questions and answers must be word-for-word identical to what's rendered on the page)
- `BreadcrumbList` (matching the visible breadcrumb trail)

Do not let schema content drift from visible page content — they must match exactly or it's a liability, not a benefit.