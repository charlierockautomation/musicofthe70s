# MusicOfThe70s.net — Master Site Brain
# CLAUDE CODE: Read this file at the start of EVERY session before writing any script.
# This file governs ALL blog posts and page content on musicofthe70s.net.
# Last Updated: 2026-08-09 (content-build.md created; Content Tracker Ownership and Session Handoff rules added)

---

## Site Type
Static site. Cloudflare Pages. Deployed via GitHub push.
NOT WordPress. No REST API. No database. No Rank Math or any SEO plugin.
All SEO is hand-built directly into the HTML — meta tags, schema, headings, internal links.

---

## Repo & Deploy

- Local repo: ~/musicofthe70s.net (Crostini Linux)
- Deploy: git push → GitHub (charlierockautomation) → Cloudflare Pages auto-deploys (~60s)
- Credential helper already configured (`credential.helper store`) — no auth prompts expected
- GA tag: G-ZY77Y8DHV1 — must be present in `<head>` on every page, no duplicates, no exceptions
- Google Search Console: verified and linked to GA4

### Preview Workflow (every time, before pushing)

cd ~/musicofthe70s.net && python3 -m http.server 8000 &

Run in background so it survives other terminal commands.
Preview at http://localhost:8000/[path]
Kill with the process ID or a fresh terminal tab once approved — never leave it running unnecessarily.
Never push anything that hasn't been previewed and approved first.

---

## Design System (do not deviate without explicit approval)

- Fonts: Playfair Display (headings, 700/900) + Inter (body, 400–700), Google Fonts CDN
- Colors:
  - `--bg-primary: #1a1a2e`
  - `--bg-card: #16213e`
  - `--bg-elevated: #0f3460`
  - `--accent-gold: #f5a623`
  - `--accent-warm: #e8956d`
  - `--text-primary: #f0e6d3`
  - `--text-muted: #9ca3af`
  - `--border-subtle: #2d3561`
- Reusable classes already in css/style.css: `.container`, `.section`, `.breadcrumb`, `.page-intro`, `.card`, `.tool-grid`/`.tool-card`, `.badge`/`.badge-gold`, `.seo-content`, `.section-divider`, `.btn-primary`/`.btn-secondary`
- Blog-specific classes: `.category-grid`/`.category-card`, `.post-grid`/`.post-card`, `.toc-block`, `.video-embed`, `.faq-block`/`.faq-item` (gold left-border, visually distinct from body text), `.related-posts`, `.placeholder-tag`
- Never add new fonts or colors outside this token set without explicit approval.
- Blog post spacing: H1 to intro ~24-32px, list to following content ~24-32px, H2 section spacing ~40-48px — consistent across all posts, defined in css/style.css, never inline styles.

---

## URL Structure

/blog/index.html (hub)
/blog/genres/ (rock-music-of-the-70s, disco-and-dance, rb-and-soul, etc.)
/blog/songs/ (top-songs-of-1970, best-70s-one-hit-wonders, etc.)
/blog/artists/
/blog/years/ (top-songs-of-1970 through top-songs-of-1979)
/blog/trivia/


Category folders are singular content types, not keyword-stuffed subfolders. Do not nest keywords redundantly (e.g. avoid `/blog/songs/70s-songs-top-songs/`). The domain already carries "70s" — do not repeat it unnecessarily in every slug.

---

## THE KEYWORD RULE — NON-NEGOTIABLE

This is the most important section in this file. Every post starts here, before a single word of content is written.

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

---

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
- [ ] At least one internal link to a site tool (see Internal Linking below)
- [ ] At least one internal link to a related blog post (once one exists in that category)
- [ ] Featured image has descriptive alt text containing the keyword or a close variant
- [ ] All images have alt text — none blank, none generic ("image1.jpg")
- [ ] H1 used exactly once per page, matches or closely echoes the title
- [ ] Heading hierarchy is clean — no skipped levels (H2 before H3, never H3 before H2)
- [ ] Schema markup present: Article + FAQPage + BreadcrumbList (see below)
- [ ] Word count 1,200+ for blog posts
- [ ] FAQ section present, written for direct AI/answer-engine extraction (see below)
- [ ] Mobile check passed at 375px and 390px (see Mobile below)
- [ ] No broken links, no placeholder text of any kind remaining
- [ ] Page loads with no console errors
- [ ] Content order correct: H1 → intro paragraph → featured image → rest (image never sits before the intro)
- [ ] Prose & Readability Protocol followed: one sentence per `<p>`, 75%+ sentences under 20 words, no em-dashes in prose, no AI-cliché words, all 3+ item lists formatted as real bulleted/numbered lists
- [ ] All images optimized: under 200KB, WebP with fallback, responsive srcset, explicit width/height, mobile legibility checked for text-dense images

A post is not "done" until every box above is checked. Report the checklist status when a post is submitted for review.

---

## AI Answer Engine / FAQ Optimization

FAQ answers are written to be lifted whole by AI search (ChatGPT, Perplexity, Google AI Overviews, voice assistants) as a standalone correct answer with no other context.

Rules for every FAQ entry:
- Question phrased exactly as a person would type or speak it
- Answer is 40–70 words, one self-contained paragraph
- Answer restates the key fact in its own first sentence — never opens with "Yes" or "No" alone
- No reference to "as mentioned above" or anything requiring the rest of the page for context
- Every fact must be traceable to the research brief/source material — no invented specifics
- 4–5 FAQ entries minimum per post

---

## Schema Markup (required on every blog post)

Every blog post needs JSON-LD schema in the `<head>` covering:
- `Article` (headline, datePublished, author, image)
- `FAQPage` (mainEntity array matching the visible FAQ block exactly — questions and answers must be word-for-word identical to what's rendered on the page)
- `BreadcrumbList` (matching the visible breadcrumb trail)

Do not let schema content drift from visible page content — they must match exactly or it's a liability, not a benefit.

---

## Blog Post Template — Full Structure (every post, no exceptions)

**Content order is fixed and non-negotiable: H1 → intro paragraph → featured image → remaining sections.**
Never place an image (including the featured image) between the H1 and the intro paragraph. Search engines and AI crawlers weight the first ~100 words of body text heavily for topical relevance and featured snippets — an image sitting before that text pushes the keyword-bearing content down the DOM and weakens that signal. It also delays reader orientation, especially on slow connections.

1. SEO metadata block: title, slug, focus keyword, secondary keywords, meta description
2. Schema markup in `<head>` (Article + FAQPage + BreadcrumbList)
3. H1
4. Intro paragraph — hook + focus keyword in the first sentence, within the first 100 words
5. Featured image + descriptive alt text (goes here, AFTER the intro — never before it)
6. Table of Contents block
7. 3+ H2 sections, ~200–300 words each, focus keyword appears naturally in at least one heading
8. FAQ section (H3 questions, `.faq-block` styling, 4–5 Q&As, AI-answer-ready per rules above)
9. Real YouTube video embed (never a placeholder note at publish time)
10. At least one internal link to a site tool — see mapping below
11. Related Posts block — 3 real cards once posts exist in those categories; never link to a post that doesn't exist yet
12. Breadcrumbs: Home › Blog › [Category] › [Post]
13. Word count: 1,200+ minimum
14. Full SEO checklist above, verified before submission
15. Full Prose & Readability Protocol below, verified before submission

### Internal Tool Linking Map
Match the post's topic to the most relevant tool and link it naturally in-context, not just tacked on at the end:

Year posts → Birthday #1 Song Finder, 70s Decade Wheel
Song/ranking posts → Random 70s Song Generator, Mood Song Matcher
Genre posts → Random Artist Picker, Random 70s Song Generator
Artist posts → Random Artist Picker, 70s Music Trivia Quiz
Trivia posts → 70s Music Trivia Quiz, Birthday #1 Song Finder


---

## Blog Hub "Latest Posts" Rotation

The Blog Hub's "Latest Posts" row is capped at 9 cards, newest first by
`datePublished`. Once a 10th post exists, the oldest drops off
automatically to make room, so the row never grows past 9 and never
needs manual pruning.

This is generated, not hand-edited. `scripts/generate_blog_hub_cards.py`
scans every `blog/<category>/<slug>/index.html` on disk, reads each
post's Article schema headline/datePublished, meta description, and
featured image, and rewrites the block between the
`<!-- LATEST-POSTS-START -->` / `<!-- LATEST-POSTS-END -->` markers in
`blog/index.html`. Never hand-edit cards inside those markers, the next
run will overwrite them.

The card excerpt is the post's own meta description, reused as-is, not
a separately hand-written blurb. Keep that in mind when writing a
post's meta description: it now doubles as visible hub-page prose, so
it must follow the same prose rules as body content (no em-dashes, no
banned words) even though it's typed into a `<meta>` tag.

Wired into `.github/workflows/update-generated-files.yml` alongside the
sitemap generator, same automatic-on-push mechanism, same standing
blocker: NOT YET PUSHED as of 2026-07-30, the deploy PAT lacks
`workflow` scope. Until that's resolved, run
`python3 scripts/generate_blog_hub_cards.py` manually and commit
`blog/index.html` after publishing or removing a post.

Category pages (`/blog/years/index.html` etc.) are NOT covered by this
rotation, they still get cards added by hand per the Publishing
Workflow below. Only the Blog Hub's "Latest Posts" row rotates.

---

## Prose & Readability Protocol (STRICT ADHERENCE)

### The "Human" Rule
Write as if you've heard this song 100 times — on vinyl, in a car, at 2am. Use sensory and emotional language. Reference specific sonic textures, production choices, and the feeling of listening live. This must read as written by a human who loves music, not a generic AI rewrite of Wikipedia.

### Readability Architecture
- One sentence per line. Each sentence wrapped in its own `<p>` tag — never bundle multiple sentences into one dense paragraph block.
- Keep 75%+ of sentences under 20 words.
- No em-dashes anywhere, ever, in prose — including in list item lead-ins, bold lead-ins, or FAQ answers. Use commas, colons, or periods instead.
  - **Exception:** a single em-dash-style character used strictly as a numeric separator (e.g. a chart position marker like `"Song Title" — #36`) is acceptable ONLY inside a bulleted list item, never in flowing prose sentences. When in doubt, use a colon instead even there.
- Avoid AI-cliché words entirely: "delve," "tapestry," "testament," "haunting," "sonic landscape," "stands the test of time." If one of these is genuinely the only correct word for a specific context, it may appear once in the entire post, never twice.

### List Formatting Rule — MANDATORY
Any list of 3+ items, names, artists, songs, or examples must be a real bulleted or numbered HTML list (`<ul>`/`<ol>`), never crammed into one paragraph with parenthetical asides.
- If a sentence needs more than one parenthetical aside to convey a list of examples, it must be converted to a list instead.
- **Bad (never do this):** "Several acts placed two songs apiece, including Simon & Garfunkel ("Song A" and "Song B"), The Beatles ("Song C" and "Song D"), and The Carpenters ("Song E" and "Song F")."
- **Good:** A one-sentence lead-in, followed by a proper bulleted list with one artist/entry per line.
- This applies to every section of every post — body content, FAQ answers, image captions, and list items alike. It overrides default prose habits; check against it explicitly before submitting a post for review.

---

## Image Optimization (mandatory before any image is used, not just sourcing)

Beyond sourcing/licensing (see Image Sourcing below), every image used on the site must be performance-optimized before it ships:

- **File size target: under 200KB** for the primary display size. An unoptimized image (e.g. a raw multi-MB PNG straight from an image generator) must be compressed before use — never publish a multi-megabyte image file.
- **Format: WebP preferred**, with a PNG or JPG fallback for compatibility.
- **Responsive `srcset` required**: generate at least 3 sizes (e.g. 400w, 800w, 1200w) so mobile devices load an appropriately small file rather than downscaling a full-size desktop image in the browser.
- **Explicit `width`/`height` attributes** on every `<img>` tag to prevent layout shift (Core Web Vitals).
- **Always pair HTML `width`/`height` attributes with `height: auto;` in CSS** on the same selector. Without it, the attribute-derived height wins as a fixed pixel value and `aspect-ratio` in CSS will not override it, the image will not scale proportionally at other viewport widths. Also always set `display: block;` explicitly on any image class, never reuse a class originally written for a placeholder `<div>` (e.g. one using `display: flex` to center placeholder text) on a real `<img>` without checking for this. Verify with real rendering (browser or headless), not just static CSS reading, since this specific bug is invisible from the CSS alone.
- **Match `aspect-ratio` to the actual source image ratio where practical**, not a fixed generic ratio like 16:9. If the source and box ratios differ, `object-fit: cover` crops the difference. Small mismatches crop only a sliver and are usually fine, but matching exactly costs nothing and removes the crop entirely.
- **`loading="lazy"`** for any image below the fold; the featured image (likely the LCP element) should remain eager-loading.
- **Mobile legibility check for dense/infographic-style images**: if an image contains embedded text (charts, infographics, data visuals), explicitly verify that text remains readable when the image is rendered at mobile width (~375px), not just that the image scales without breaking layout. If embedded text becomes illegible at mobile width, do not use that image as a full-width featured image on small screens — use a simplified crop, a mobile-specific alternate version, or reconsider the image choice entirely. Report this check explicitly, don't assume responsive scaling alone solves it.

This check is part of the SEO Scoring Target checklist and the Mobile Check below — an image that fails file-size or legibility standards blocks a post from being marked ready to push.

---

## Data Sources

- Billboard databases: `~/musicofthe70s.net/data/billboard/`
  - `year_end_hot100.json` (1000 records, 1970–1979)
  - `hot100_weekly.json` (522 records)
  - `country.json` (523 records)
  - `rnb.json` (522 records)
  - All validated — treat as ground truth, never contradict this data in post content.
- Research briefs: NotebookLM notebooks (20+ artist/genre notebooks, Billboard year-end notebooks per year, "Music of the 70s — Overview" notebook with genre Wikipedia sources)
- Research brief pull prompt (use in any NotebookLM notebook when gathering material for a new post):
  > "Extract everything you can find in these sources that would help write a blog post. Give me: 5–8 genuinely interesting facts (specific dates, numbers, firsts, surprises), key names/songs/albums with context, any direct quotes worth referencing with source noted, and a rough narrative arc if there is one. Plain list, no fluff."
- Never invent a fact, date, chart position, or quote that isn't in the source material or validated database. When in doubt, mark it as needing verification rather than guessing.

---

## Image Sourcing

- Wikimedia Commons preferred (free, properly licensed)
- Every Commons image gets a visible credit line: `Image Credit: Photo by [Author], [License], via Wikimedia Commons`
- Only use images with free licenses (CC BY, CC BY-SA, public domain) — skip anything non-free
- NotebookLM-generated infographics are usable as featured images where genuinely relevant and well-designed
- Every image needs real, descriptive alt text — never blank, never a filename, never generic

---

## Mobile Check (required before any post ships)

Verify in Chrome DevTools responsive mode at 375px (iPhone SE) and 390px (iPhone 14) width:
- No horizontal scroll
- TOC block stacks correctly
- FAQ block stacks correctly
- Related-posts cards stack to single column
- Images scale correctly, no overflow
- Nav collapses to hamburger correctly
Report pass/fail explicitly before a post is considered ready to push.

---

## Publishing Workflow

1. Write/generate post content following the full template above
2. Run `python3 scripts/verify_post.py <path/to/post/index.html> "<focus keyword>"` — checks word count, keyword density, sentence-length distribution, em-dash count (correctly distinguishing the list-item numeric-separator exception from prose), banned words, FAQ schema/visible match, heading hierarchy, and keyword placement in one pass. Built 2026-07-31 after the same checks were re-derived by hand on four straight posts; use it instead of re-deriving them manually.
3. Preview locally (see Preview Workflow)
4. Run through the full SEO checklist — every box checked
5. Run the mobile check
6. Report checklist + mobile results before asking for approval to commit
7. Once approved: `git add -A && git commit -m "[description]" && git push`
8. Verify live site post-deploy (~60s wait, then hard refresh and check)

---

## Master Content Plan

Tracks the ordered publishing queue for multi-part series, so "what's next" never has to be re-derived from CONTENT-INDEX.md by hand. This section didn't exist before 2026-07-30; created when Top Songs of 1972 was flagged as "Order #2" in a task brief that assumed it already existed. Top Songs of 1970 predates this tracking (built before the Years series was formalized as an ordered sequence) and isn't given an Order number here; the explicit order starts at 1971.

### Years Series (Top Songs of 19XX, one post per year, 1971–1979) — COMPLETE

| Order | Year | Status | URL |
|---|---|---|---|
| 1 | 1971 | Live | /blog/years/top-songs-of-1971/ |
| 2 | 1972 | Live | /blog/years/top-songs-of-1972/ |
| 3 | 1973 | Live | /blog/years/top-songs-of-1973/ |
| 4 | 1974 | Live | /blog/years/top-songs-of-1974/ |
| 5 | 1975 | Live | /blog/years/top-songs-of-1975/ |
| 6 | 1976 | Live | /blog/years/top-songs-of-1976/ |
| 7 | 1977 | Live | /blog/years/top-songs-of-1977/ |
| 8 | 1978 | Live | /blog/years/top-songs-of-1978/ |
| 9 | 1979 | Live | /blog/years/top-songs-of-1979/ |

**The Years series is complete: all ten posts (1970, plus Order #1-9 for 1971-1979) are Live.** Top Songs of 1970 predates Order numbering (see note above) but is Live alongside the rest. No further Years posts are planned.

Update this table's Status column in the same session a post's CONTENT-INDEX.md Status changes, so the two files never disagree about what's live.

### Genres, Songs, Artists, Trivia — content research process

Unlike the Years series, these four categories don't run as an ordered queue with a fixed final post. Content ideas come from keyword-volume research (search intent, competition, current SERP/AI-Overview coverage) reviewed against what each category is missing, not from a pre-set list. First used 2026-08-06 when Charlie supplied real keyword-volume data (WordStream-style export) for review against these four categories.

**Standing rules for every post built this way, not one-off instructions:**
- **Content-gap analysis is mandatory before writing, not optional.** Check what's currently ranking for the post's focus keyword (and each individual artist/song's own obvious search terms, for Artists/Songs posts), including AI Overview/AI search results where visible. Identify what's missing, thin, or factually wrong. The post must earn its rank by being more complete or more accurate than what's already ranking, not just different. Report the specific gaps found before writing, not a blanket "did the research" note.
- **No repeated template across posts in the same batch.** Each post needs its own structure, angle, and section order fitted to that subject's actual story. Reusing UI components (like `.trivia-card`) across posts is fine and expected; copy-pasting the same H2 skeleton with different names dropped in is not. If two posts in a batch end up structurally identical, fix it before publishing.
- **Batch size is quality-gated, not volume-gated, for Artists and Songs.** Propose the smallest batch that's still a coherent starting point. If a candidate artist or song doesn't have enough real substance to sustain a genuinely informative article, drop it from the batch rather than padding to hit a target number.
- **Internal linking only where it adds real value**, never forced to hit a quota: matching artist/song posts once they exist, cross-links between artist and song posts, and back to the relevant site tool.

**Trivia** — Order #1 was 70s Music Trivia (2026-07-26, predates this research process). Order #2, Banned Songs of the 70s, is Live (2026-08-06), first post built under this process; see the Session Log entry below for the gap analysis it ran.

**Artists** — batch of 4 complete (James Brown, Grateful Dead, Village People, Talking Heads), all Live as of 2026-08-06, sourced from the 619-artist JSON across 10 genre files, spanning 4 distinct genres by design. KC and the Sunshine Band was considered and dropped from the batch, not for lack of substance but over a real JSON data error found in its trivia field (see Session Log below). **Focus keyword pattern corrected mid-batch**: the first three posts used an unverified "[Artist] in the 70s" long-tail pattern; Talking Heads switched to a plain artist-name keyword after real search-volume data showed the long-tail pattern likely has near-zero volume against a matching high-volume, low-competition bare term. James Brown, Grateful Dead, and Village People were deliberately left as-is rather than retitled/re-slugged, an explicit call, not an oversight; any future Artists posts should default to plain artist-name keywords (verified against real volume data first) unless a specific post's real angle calls for something more specific. Artists category page has 5 real cards and zero placeholders as of this batch's completion.

**Songs** — batch of 4 approved (Don McLean American Pie, Bohemian Rhapsody, Hotel California, Dancing Queen), sourced from the 1,000-song JSON across 10 year files. Charlie specified all 4 focus keywords directly rather than a proposal-and-approve cycle: `don mclean american pie`, `Bohemian Rhapsody`, `Hotel California`, `Dancing Queen`, plain artist/title patterns applying the keyword-correction lesson from the Talking Heads post. **All 4 posts are Live as of 2026-08-08, batch complete**: American Pie and Bohemian Rhapsody (2026-08-07), Hotel California and Dancing Queen (2026-08-08). Bohemian Rhapsody, Hotel California, and Dancing Queen all applied the literal-keyword-phrase lesson cleanly from their first drafts, no possessive-mismatch repeat after American Pie's first-draft catch, confirming the reminder works when actually followed from the start rather than caught after the fact. Songs category page has 5 real cards, zero placeholders.

---

## Tool-to-Blog Linking (Tier 1/2/3) — Tier 1 parked

Charlie proposed linking the site's interactive tools (Random 70s Song Generator, Random Artist Picker, Trivia Quiz, Decade Wheel) directly to on-site content instead of sending users to YouTube search results, to keep visitors on-domain. Scoped into three tiers 2026-08-06:
- **Tier 1**: swap each tool's "Search on YouTube" link for a real inline video embed. Blocked on a real data gap: none of the tools' JSON records store an actual video ID, only a `youtube_search` query string. A real embed needs either a live YouTube Data API lookup (new infrastructure, API key/quota/cost, this site is static with no backend) or a one-time verified-video-ID enrichment pass across up to 1,619 records. **Parked, not proceeding**, per explicit instruction.
- **Tier 2**: link tool results to matching blog posts about that specific song/artist, when one exists.
- **Tier 3**: lightweight auto-generated song/artist profile pages built from existing JSON data, for everything that doesn't get full blog-post treatment.

Tier 2 and Tier 3 are correctly gated on Artists/Songs posts actually existing first. Neither is scoped or started; there's no backlog of individual posts to link to yet.

---

## Content Tracker Ownership

Claude Code owns writing to content-build.md and CONTENT-INDEX.md. At the end of every session that builds, edits, or audits any content on this site, update both files directly to reflect what happened. Save in place before ending the session. Never wait for Charlie to paste in an externally-edited version of either file.

---

## Session Handoff

At the end of every session, after finishing the work and updating the tracker files, tell Charlie what the next item in content-build.md's Rotation Queue is. Wait for his confirmation before starting it in a new session.

---

## How to Resume Any Session

Paste this at the start of a new Claude Code session:

Read CLAUDE.md in ~/musicofthe70s.net.
Current task: [describe]
Post/page: [name]
Focus keyword: [keyword — verified against real search phrasing]


---

## Session Log

| Date | Task | Notes |
|---|---|---|
| 2026-07-24 | Blog scaffold built | Hub + 5 category pages + 1970-in-music post template built with placeholders. Blog nav link added site-wide. Design system confirmed and documented. |
| 2026-07-24 | Footer year fix | © 2025 → © 2026 site-wide, bundled into same commit as blog scaffold (17 files, commit 75dd3dd). |
| 2026-07-24 | CLAUDE.md created | Master brain file established. Keyword rule (slug word-order matching, density 2-4 uses, no plugin so manual SEO checklist) formalized after catching a mismatch between a drafted focus keyword and slug on the first real post draft. |
| 2026-07-24 | Prose, content-order, and image rules added | Formalized after reviewing the first real post draft (top-songs-of-1970): (1) image was placed between H1 and intro paragraph, weakening keyword-in-first-100-words signal — content order now fixed in the template; (2) "Artists With Multiple Hits" section was one dense paragraph with 9 parenthetical asides — List Formatting Rule now mandates real bulleted lists for any 3+ item list; (3) featured infographic was 6.3MB unoptimized PNG at 2752x1536, illegible at mobile width — Image Optimization section added requiring compression, WebP, responsive srcset, and explicit mobile-legibility checks for text-dense images. All three added as permanent checklist items, not one-time fixes.
| 2026-07-25 | Keyword density rule corrected: flat count → percentage formula | The original "2-4 uses across a 1,200+ word post" rule was a flat count that didn't scale across posts of different lengths (a 4,000-word post could still show only 2 uses and read under-optimized, while a 1,200-word post at 4 uses sits near stuffing territory). Replaced with density = (uses ÷ total words) × 100, target range 0.5%-2%, spam threshold above 3%. Framed explicitly as a sanity check against stuffing, not a quota to hit exactly. Matching line in the SEO Scoring Target checklist updated to match.
| 2026-07-25 | Featured-image/thumb aspect-ratio bug found and fixed | Both blog posts' featured images and all card thumbnails were rendering at a fixed pixel height regardless of viewport width (cropped/zoomed look on mobile, wrong proportions on desktop). Root cause: `.post-featured-img`/`.post-card .post-thumb` were originally written for a placeholder `<div>` (display:flex to center placeholder text); reusing those classes on real `<img>` tags broke sizing two ways: (1) missing `height: auto` meant the HTML height attribute won over CSS `aspect-ratio`, (2) an earlier attempted fix (`img.post-thumb { display:block }`) had lower CSS specificity than the flex-declaring rule and silently never took effect. Static CSS reading did not surface this, only real rendering did (installed headless Chromium via Playwright to verify). Fixed by adding `height:auto` and raising selector specificity. Also matched `aspect-ratio` to the actual source image ratio (43:24) instead of a generic 16:9, eliminating a small (0.78%) object-fit:cover crop entirely, a zero-cost improvement once the ratio mismatch was noticed. New Image Optimization rules added above to prevent recurrence and require real-render verification for this class of bug going forward.
| 2026-07-30 | Master Content Plan section added | A task brief for Top Songs of 1972 referred to it as "Order #2" in "CLAUDE.md's Master Content Plan," assuming a section that didn't exist yet. Added it (see above) to track the Years series (1971-1979) as an explicit ordered queue with a Status column per year, separate from CONTENT-INDEX.md's flat Blog Posts table. Top Songs of 1970 predates the series being treated as an ordered sequence and isn't numbered; order starts at 1971. Going forward, update this table's Status in the same session CONTENT-INDEX.md's Status changes for a Years post, so the two files can't drift apart.
| 2026-07-30 | Blog Hub "Latest Posts" capped at 9 with auto-rotation | Requested explicitly: cap the hub's Latest Posts row at 9 cards, oldest drops off automatically as new posts publish, wired in rather than manual. Built `scripts/generate_blog_hub_cards.py` (same disk-scanning philosophy as the sitemap generator) and added `<!-- LATEST-POSTS-START/END -->` markers in `blog/index.html` so it can safely regenerate just that block. Tested the actual rotation behavior with temporary fake posts before shipping, confirmed the oldest genuinely drops once a 10th post exists, not just reasoned about in the abstract. Found and fixed a real side effect while building this: card excerpts now reuse each post's meta description verbatim (previously invisible metadata), which surfaced a pre-existing em-dash in the 1970 post's meta description as visible prose for the first time, violating the no-em-dash rule; fixed that post's meta description (em-dash to colon) as an in-scope consequence of this change. Documented above that meta descriptions now double as visible hub prose and must follow prose rules. Wired into `.github/workflows/update-generated-files.yml` (renamed from `update-sitemap.yml` to reflect broader scope) alongside the sitemap generator, same standing blocker: not yet pushed, PAT lacks `workflow` scope.
| 2026-07-31 | verify_post.py built for the checklist audit | The same manual density/sentence-length/em-dash checks had been re-derived by hand on four straight posts (1971, Soul, 1972, 1973), each time flagged in the task brief as worth automating. Built `scripts/verify_post.py`: one script, checks word count, keyword density (0.5-2% range), sentence-length distribution (75%+ under 20 words), em-dash count (correctly distinguishing the documented list-item numeric-separator exception from flowing prose, not a blanket zero-tolerance check), banned words, FAQ schema-vs-visible match (word-for-word, 40-70 word range, no bare "Yes"/"No" openers), heading hierarchy, and keyword placement (title/meta/first-100-words/H2). Added as step 2 of the Publishing Workflow above. First real use on Top Songs of 1973 caught the em-dash exception needed refining (initial version flat-failed any em-dash before the script correctly special-cased `<li>` numeric separators).
| 2026-08-05 | Top Songs of 1978 published, ninth Years post, Order #8 | Cleanest chart-position verification pass in the series: all 13 named positions cross-checked against `year_end_hot100.json`, zero mismatches. Largest multi-hit-artist gap caught so far: task brief confirmed only 3 multi-hit artists (Andy Gibb, Bee Gees, Steely Dan) plus one flagged-unconfirmed (Player, later confirmed at #7 and used); full 100-record audit found 12 confirmed multi-hit artists by exact-string grouping, a 9-artist gap. Split-credit ambiguity found (same class as 1976's Elton John/Kiki Dee case): Olivia Newton-John's solo entry ("Hopelessly Devoted to You," #35) kept separate from her duet credit "John Travolta & Olivia Newton-John" (#13, #69), explicit call stated in the post body itself. **Resolved the "You Light Up My Life" year conflict flagged as an open item on the Best Songs of the 70s post**: `year_end_hot100.json` buckets it under 1978 at #3, but that record's own fun_fact text says "in 1977," and `hot100_weekly.json` corroborates only 1977 (ten weeks at #1 starting October 1977, zero 1978 weekly entries); same JSON self-contradiction class as the 1974 Olivia Newton-John and 1976 Elton John cases; post states no calendar year for the song, resolving the conflict by omission rather than picking a side. Featured image's source ratio (2752x1536) is exactly 43:24, matching the site's existing `.post-featured-img` CSS aspect-ratio exactly for the first time in the series; sized output to 1200x670 instead of the usual 1200x675 for a true zero-crop fit. Video embed (Bee Gees "Night Fever") confirmed via oEmbed as the official `@beegees` channel; the real embedded-iframe Playwright playback stress test was inconclusive in this session's sandbox (player stuck in `unstarted-mode`), but the identical null result reproduced on the already-live, working 1977 video under the same test, confirming a sandbox/environment limitation (no CDN egress or codec support for actual YouTube streams in headless Chromium here) rather than a bad video choice; flagged honestly, oEmbed channel verification used as the substitute check going forward whenever this environment limitation recurs. `verify_post.py` passed clean on the first run, no iteration needed. Category/hub cards: Years category page now has all 9 years (1970-1978) with real cards for the first time, a complete run; Blog Hub rotation newly dropped **Bee Gees: The Story of Pop's Most Successful Sibling Act** (fifth post to roll off the 9-card cap). sitemap.xml regenerated (29 URLs). Reviewer (Charlie) caught category/hub cards missing from the initial draft before push, same class of omission as the 1972 post; both were added and verified in the same session before commit this time, not as a follow-up. **For Top Songs of 1979 (final Years post)**: budget time for the same multi-hit-artist full-audit gap (has occurred on every post from 1974 onward) and check whether this sandbox's YouTube-playback-test limitation is still present or was environment-specific to this session.
| 2026-08-06 | Top Songs of 1979 published, tenth Years post, Order #9, final entry | Confirmed the sandbox video-playback-test limitation flagged on 1978 is still present, not session-specific: same `unstarted-mode` non-result on a fresh video (The Knack "My Sharona") under identical test conditions; oEmbed channel verification (`TheKnackVEVO`) used as the substitute check again. Chart-position cross-check found one real mismatch: "Heaven Knows" (#39) is credited "Donna Summer and Brooklyn Dreams," not solo Donna Summer as the brief's "four songs" framing implied. Multi-hit-artist audit continued the established pattern: brief only got the Bee Gees right (3), undercounted Chic at 2 (actually 3, "I Want Your Love" #62 unmentioned), missed 9 of the 12 confirmed multi-hit artists entirely. Two split-credit calls made and stated explicitly in the post body itself (not just internal notes), per the task's specific instruction: Donna Summer (3 solo + 1 duet, kept separate for the systematic count, still credited with "four entries" narratively since that's true and traceable) and Barbra Streisand (duet vs. solo, neither reaches 2+ alone, given its own dedicated FAQ). **Caught two invented, unsourced details in my own first draft before they shipped**: a claim that "MacArthur Park" hit #1 "earlier that year" (1979) when the JSON's own fun_fact places that #1 run in November 1978; and a self-contradictory, unsourced Michael Jackson age ("21-year-old" in one section, "thirteen-year-old" in another), neither number ever verified, both removed and replaced with the JSON-verified fact (his first solo single, one week at #1). Donna Summer panel, flagged pre-build as the densest text block in the series (four song titles plus four chart numbers), explicitly checked at 3x mobile scale per the task's request rather than assumed from desktop, fully legible. `verify_post.py` passed clean on the first run. Category/hub cards added before push this session, not as a follow-up: Years category page now lists all 10 posts, 1970 through 1979, the full series in one place for the first time. Blog Hub rotation newly dropped **Top Songs of 1971** (sixth post to roll off the 9-card cap). sitemap.xml regenerated (30 URLs). No "Operations Hub" section was found anywhere in CLAUDE.md or CONTENT-INDEX.md despite the task brief referencing one; flagging that the reference doesn't match anything on disk rather than inventing a section to match it, same as prior sessions' handling of brief assumptions that outran the actual file state. |
| 2026-08-06 | **Years series wrap-up: 10 posts, 1970-1979, complete** | The Years series ran 2026-07-24 (1970 scaffold) through 2026-08-06 (1979), ten posts total, no Planned rows left in that category. Recurring issues worth carrying forward as standing checklist items for whatever content type comes next, not one-time fixes specific to Years: **(1) Multi-hit-artist undercounts.** Every task brief from 1974 onward under-listed multi-hit artists when checked against the full validated dataset directly, gaps ranging from 1 artist (1974) to 11 artists (1976). A full grouped-by-exact-string audit against the source data, not the brief's shorthand list, is required any time a post claims a "these are the artists with N+ entries" list. **(2) Split-credit artists.** Real people charting under two different credited strings (solo vs. duet, or two different duet partners) showed up repeatedly: Elton John & Kiki Dee (1976), John Travolta & Olivia Newton-John (1978), Donna Summer & Brooklyn Dreams and Neil Diamond & Barbra Streisand (1979). The rule that held up across all of them: never silently merge or silently split, state the counting call explicitly in the post body itself, not just an internal note, and let exact-string grouping govern any systematic "tied artists" list even when a narrative sentence elsewhere describes the same person's total output more loosely. **(3) NotebookLM watermark removal.** Every generated infographic from 1976 onward has needed the same bottom-right "NotebookLM" watermark painted over before use, often invisible in a chat-reviewed crop but present at full resolution; check every image at full resolution before publishing, don't trust a cropped preview. **(4) JSON self-contradictions.** The validated Billboard JSON has, on at least three occasions (Olivia Newton-John 1974, "You Light Up My Life" 1977/1978, and this session's near-miss on "MacArthur Park"'s year), disagreed with its own embedded `fun_fact` text or been ambiguous about which calendar year a chart entry belongs to; when this happens, prefer omitting the disputed specific over guessing, and cross-check against `hot100_weekly.json` when available since it corroborated the correct year both prior times. **(5) Sandbox video-playback-test limitation.** Confirmed present across two separate sessions (1978 and 1979) with different videos, not a one-off: the real embedded-iframe Playwright stress test cannot reach a playable state in this environment regardless of video validity. oEmbed channel-identity verification is the reliable substitute check going forward; don't keep re-diagnosing this as if it might be video-specific. **Deferred, not decided in this session**: what content type comes next. No "Operations Hub" or equivalent planning section exists in CLAUDE.md or CONTENT-INDEX.md to defer to, despite a task brief referencing one; this is a plain flag for the next planning session to pick up, not a broken reference to fix now. |
| 2026-08-06 | Content research process defined for Genres/Songs/Artists/Trivia; Banned Songs of the 70s published as first post under it | Charlie supplied real keyword-volume data for review against these four categories, the "what's next" decision flagged as deferred at the end of the Years series wrap-up above. Recommended and got approval for one keyword despite modest volume (`banned songs of the 70s`, 390/mo) over several higher-volume broad terms, on intent-match and low-competition grounds; separately flagged and resolved a real cannibalization risk (`70's music greatest hits`, 90.5K/mo) against the already-Live "Best Songs of the 70s" post: confirmed that post is a chronological Billboard chart countdown, a genuine "greatest hits" post would need deep-cut/album framing to not be the same post twice, so it was correctly shelved rather than built. **Video swapped mid-build after a real problem, not a sandbox artifact**: the planned Sex Pistols embed (official SexPistolsVEVO channel) failed live playback with an explicit geo-restriction error, different in kind from the recurring `unstarted-mode` sandbox stall seen on every prior post's video test; caught via the actual page, not assumed, swapped to The Kinks' official "Lola" video, verified via both a direct-origin test and the live post. Full details (content-gap analysis findings, sourcing standard, myths-debunked structure) are in this post's own CONTENT-INDEX.md row. **Tool-to-blog linking scoped into three tiers, Tier 1 (inline YouTube embeds on tool result cards) parked**: none of the four tools' JSON records store a real video ID, only a `youtube_search` query string, so a real embed needs either new API infrastructure or a large one-time data-enrichment pass; this is a genuine scope gap, not something "same data already on hand" could fix, flagged rather than silently built around. Tier 2 (tool results linking to matching blog posts) and Tier 3 (auto-generated profile pages) are correctly gated on Artists/Songs posts existing first, neither started. **Next up**: Artists and Songs batch proposals (bare-minimum size, quality-gated per CLAUDE.md's new standing rules above) are pending Charlie's explicit approval before any writing starts on either. |
| 2026-08-06 | Artists batch proposed and approved (4 artists); James Brown in the 70s published, first of the four | Proposed batch: James Brown (Soul/Funk), Grateful Dead (Classic/Jam Rock), Village People (Disco), Talking Heads (Punk/New Wave), one per genre by design, sourced from the 619-artist JSON. **KC and the Sunshine Band considered and dropped**: strong substance otherwise (verified name-origin story, real George McCrae songwriting connection), but its JSON trivia field contains a real data error, crediting its Hollywood Walk of Fame star "as The Jacksons," a copy-paste artifact from an unrelated record; dropped to keep the batch at a clean 4-genre spread rather than silently using or silently fixing a flawed source record. Charlie approved the batch in full. Built James Brown in the 70s first: full content-gap analysis found every currently-ranking result is whole-career biography, none decade-scoped; built the post around 4 independently verified 70s-specific stories instead (1970 band walkout and J.B.'s formation, "Get on the Good Foot" cross-checked against the site's own `year_end_hot100.json`, "The Payback" soundtrack rejection, "the One" rhythm concept). **Disputed-claim handling carried over from the Banned Songs post**: a widely repeated "not funky enough" quote in the Payback story is denied by the director who's supposed to have said it; left out, only the independently corroborated dismissal used. **Real decade-scope finding, same class as the "Je t'aime" and "Another Brick in the Wall" boundary calls in prior posts**: 2 of the source JSON's 3 trivia bullets for James Brown (a 1968 MLK riot-prevention concert, a 1986 Rock Hall induction) fall outside the 1970-1979 window a "James Brown in the 70s" post covers; neither used. Structure deliberately runs 4 incident-vignettes instead of the Bee Gees post's 6 career-phase arc, satisfying the batch's no-repeated-template rule from the first post onward. Video required a real channel-identity check same as every post since Banned Songs' geo-block scare: `JamesBrownVevo` confirmed official, playback confirmed via real Playwright test. `verify_post.py` needed one iteration (word count and keyword density both started under floor, fixed with real content not padding, including a keyword-bearing H2 since none of the original headings carried the exact focus phrase). Category/hub cards added same session: Artists category page down to 1 remaining placeholder slot. Blog Hub rotation dropped **Top Songs of 1972** for the first time. sitemap.xml regenerated (32 URLs). Live-verification needed an unusually long edge-cache settle, roughly 40 seconds and multiple races between nodes before both the Artists category page and Blog Hub stabilized; confirmed stable across 5 consecutive fetches before reporting done. **Remaining in this batch**: Grateful Dead, Village People, Talking Heads, each needing its own full content-gap analysis and its own distinct structure before writing. |
| 2026-08-06 | Grateful Dead in the 70s published, second of the four-artist batch | Content-gap analysis started with a direct query against the site's own validated data, not a web search: the Grateful Dead have zero entries in `year_end_hot100.json` or `hot100_weekly.json`, confirmed before writing anything. Independently verified why: "Truckin'" peaked at just #64 on the Hot 100 (Dec 25, 1971), their career-best on that chart until "Touch of Grey" broke the Top 10 in 1987. Turned that absence into the post's actual thesis (live legend outweighing chart history) rather than treating it as a data gap to route around; no currently-ranking bio explains that specific mismatch. **Third distinct structure in the batch, no-repeated-template rule holding for a second post running**: not Bee Gees' 6-phase chronology, not James Brown's 4 incident-vignettes; this one runs a single throughline across all 4 sections instead. Added real depth over two vague source-JSON trivia bullets: Wall of Sound got real specs (70 tons, 3 stories, 100 ft wide, Cow Palace debut March 23 1974) in place of "one of the largest ever built"; the Truckin' drug-bust bullet got the real date, location, and arrest count in place of "a real-life drug raid." **Video swapped for a genuine blocker, not a sandbox artifact**: the first candidate (1974 Winterland live footage, official channel) is age-restricted and cannot be embedded anywhere, confirmed via YouTube's own age-restriction error rather than the usual environment stall; swapped to the same channel's audio upload, confirmed real playback. Image needed a second export pass: first crop landed at 198.9KB, right at the 200KB ceiling, re-exported at lower JPEG quality for real margin (172KB), a reminder to check exact byte counts near the limit rather than trusting a rounded `du -h` reading. `verify_post.py` needed one iteration (word count, density, missing keyword-bearing H2, same pattern as James Brown). Category/hub cards added same session: **Artists category page now has zero remaining placeholder cards** (Bee Gees, James Brown, Grateful Dead, all real, all Live). Blog Hub rotation dropped Top Songs of 1973. sitemap.xml regenerated (33 URLs). Live-verification settle took roughly 60 seconds across 6 fetch attempts this time, longer than James Brown's ~40s; confirmed stable across 3 consecutive fetches before reporting done, same discipline as every post since the edge-cache race was first noticed. **Remaining in this batch**: Village People, Talking Heads. |
| 2026-08-06 | Village People in the 70s published, third of the four-artist batch | Content-gap analysis started the same way as Grateful Dead's: checked the site's own `year_end_hot100.json` first, found and confirmed both chart facts directly ("Y.M.C.A." #8 year-end 1979, 3 weeks at #2 weekly; "In the Navy" #48 year-end, #3 weekly), richer than the source artist JSON's trivia field. Real find independently verified beyond the JSON: Felipe Rose, the group's actual first recruit, was discovered dancing at NYC's The Anvil in Native American dress before Village People existed as a group, not a costume choice but a reflection of his real Lakota Sioux heritage; seeing Rose is what gave producer Jacques Morali the idea to build a full archetypal lineup. **Fourth distinct structure in the batch, no-repeated-template rule holding across all 4 Artists posts built so far**: a surface-story-versus-hidden-story reveal, distinct from Bee Gees' chronology, James Brown's incident-vignettes, and Grateful Dead's single-thesis-throughline. Image needed no distortion for the first time in this batch, the source photo's ratio already matched the site's 43:24 target almost exactly. Video confirmed via oEmbed (`@villagepeople` official channel) and real playback test on the first candidate tried, no swap needed this time (unlike James Brown's density fixes or Grateful Dead's age-restriction swap). `verify_post.py` needed the same one-iteration pattern as the last two posts: word count, density, and a missing keyword-bearing H2 all fixed with real content. **Charlie asked directly which keyword variant appears where** (title/meta/alt-text/etc.); answered precisely rather than assuming: exact phrase everywhere except image alt text, which uses a close variant (artist name plus year, not "in the 70s"), consistent with CLAUDE.md's stated rule and the same pattern already used on James Brown and Grateful Dead, not a new decision. **Artists category page had zero placeholder slots left**, so this card was appended as a straight 4th card, the first append rather than placeholder-swap in this batch. Blog Hub rotation dropped Top Songs of 1974. sitemap.xml regenerated (34 URLs), one transient single-fetch cache blip during live verification (33 vs. 34 on one of seven checks), resolved on the next fetch, not treated as a real problem. **Batch nearly done**: Talking Heads is the last of the 4, still needing its own full content-gap analysis and its own distinct structure (something other than chronology, incident-vignettes, single-thesis, or surface/hidden-reveal) before writing. |
| 2026-08-06 | **Focus keyword pattern corrected mid-batch, real volume data caught what phrase-existence checks missed** | Charlie supplied real WordStream keyword-volume data for "Talking Heads" and pointed out the last 3 posts' `[Artist] in the 70s` keyword pattern had never been checked against actual search volume, only against "does this phrase appear somewhere," which is a weaker test than it looks like. Data showed plain `talking heads` at 110K/mo and `byrne talking heads` at 135K/mo, both almost certainly dwarfing the long-tail decade-qualified pattern. Corrected going forward: switched to plain `Talking Heads`, matching the site's own original Artists-post precedent (Bee Gees already used a bare artist name before the long-tail pattern started). **Explicit decision, not silently applied**: James Brown, Grateful Dead, and Village People stay as published, no retitle or re-slug of already-indexed live posts; the fix applies going forward only. Also flagged honestly rather than oversold: the volume tool's "Low" competition rating is paid-ad competition, not organic ranking difficulty, a bare band-name query still faces Wikipedia/AllMusic/the band's own site regardless of that rating. Attempted to pull the rest of Charlie's 285-row keyword export via the WordStream tool directly (both plain fetch and headless browser automation); the tool's own results step errored consistently, likely bot-blocking automated traffic; abandoned per explicit instruction rather than continuing to fight it. **Standing rule added for future Artists posts**: default to plain artist-name focus keywords, verified against real volume data before committing, not phrase-existence checks alone. |
| 2026-08-06 | Talking Heads published, fourth and final entry in the Artists batch, **batch complete** | Content-gap analysis found the site's own `year_end_hot100.json` has zero Talking Heads entries anywhere in the 1970s, same finding shape as Grateful Dead's zero-chart-entries case; since Grateful Dead already used a chart-absence thesis, this post needed a genuinely different angle rather than repeating it. **Fifth and final distinct structure in the batch, no-repeated-template rule held for all 5 Artists posts now Live**: "identity assembled from found objects", three unplanned accidents (a friend's TV Guide term became the name, a coincidental Son of Sam timing gave "Psycho Killer" its edge, Eno's arrival reshaped the sound) closing on the zero-chart irony, distinct from Bee Gees' chronology, James Brown's incident-vignettes, Grateful Dead's single-thesis-throughline, and Village People's surface/hidden-reveal. Real depth added over a vague source-JSON name-origin bullet: verified the real story via Chris Frantz's memoir *Remain in Love* (friend Michael "Wayne" Zieve's TV Guide, rejected earlier names, Tina Weymouth's shirts, a stranger calling it "terrible" in Washington Square Park). **Caught an unverified claim before it shipped**: a first-draft sentence about the song's French bridge being a deliberate narrative "distance" device wasn't supported by real sources; checked and corrected to the real detail (Tina Weymouth wrote the French bridge herself). `verify_post.py` needed a genuine consecutive-keyword fix traced to the script's actual `<p>`-tag-based sentence list this time (an image caption immediately followed by the first body paragraph), not the heading-adjacency pattern assumed from prior posts, worth remembering the script's real logic rather than pattern-matching from memory next time this check fails. Category/hub cards added same session: Artists category page appended as a straight 5th card, zero placeholders remaining. sitemap.xml regenerated (35 URLs). **Batch wrap-up**: 5 Artists posts now Live (Bee Gees, James Brown, Grateful Dead, Village People, Talking Heads), 5 genuinely distinct structures proven out as a real, repeatable practice, not a one-time discipline. Songs batch (bare-minimum, quality-gated, sourced from the 1,000-song JSON across 10 year files) is the next piece of unfinished work from the original 3-part task brief (Banned Songs, Artists, Songs), still pending its own batch proposal and Charlie's approval before any writing starts. |
| 2026-08-07 | Songs batch approved (4 songs, keywords specified directly); Don McLean American Pie published, first of the four | Charlie approved the proposed batch (American Pie, Bohemian Rhapsody, Hotel California, Dancing Queen) and specified all 4 focus keywords directly rather than requiring a separate approval cycle: `don mclean american pie`, `Bohemian Rhapsody`, `Hotel California`, `Dancing Queen`, all plain artist/title patterns, applying the correction already learned from the Talking Heads post. **The same mistake nearly repeated itself immediately**: first draft of the American Pie post consistently used the natural possessive "Don McLean's American Pie" throughout title, meta, H1, and intro, which does not match the literal specified phrase "don mclean american pie" (no possessive). `verify_post.py` caught it immediately as a hard zero-uses failure, not a density-adjustment case; fixed by switching to the exact unpossessive phrase in every keyword-scored location while keeping the more natural possessive in body prose and the breadcrumb where it doesn't affect scoring. **Standing lesson for the remaining 3 songs in this batch**: when Charlie specifies an exact keyword phrase, use that literal phrase (including punctuation/possessive choices) in every scored location, don't paraphrase into more natural-sounding text even when the paraphrase captures the same concept. Content-gap analysis found the site's own JSON confirmed the chart facts but only in thin, generic trivia language ("cryptic lyrics have fueled decades of interpretation"); real differentiated depth came from independent research: the actual Feb 3, 1959 crash details, McLean's specific 40-year deflection quote, and the April 2015 manuscript auction ($1.2M, 16 pages, 237 lines) where he finally explained the song, none of which the source JSON's trivia field mentioned at all. Image needed two crop attempts, the only public-domain 70s-era photo found was an unusually narrow portrait (0.77 ratio vs. the site's 1.79 target), first crop badly cut the face, second attempt got it right; worth remembering that portrait-orientation sources need real crop-position testing, not just a single first attempt, when the ratio mismatch is this extreme. Category/hub cards added same session: Songs category page down to 1 remaining placeholder. Blog Hub rotation dropped Top Songs of 1977. sitemap.xml regenerated (36 URLs). **Remaining in this batch**: Bohemian Rhapsody, Hotel California, Dancing Queen, each still needing its own full content-gap analysis, its own distinct structure, and strict literal-keyword-phrase discipline in every scored location from the first draft onward, not caught after the fact. |
| 2026-08-07 | Bohemian Rhapsody published, second of the four-song batch | Applied the literal-keyword-phrase lesson from American Pie cleanly this time: used the exact specified phrase "Bohemian Rhapsody" consistently from the first draft, `verify_post.py`'s keyword checks passed immediately instead of the zero-uses failure American Pie hit. Content-gap analysis found the source JSON's trivia field already had the Kenny Everett story, unusually rich for a song-level record, but still generic ("cryptic lyrics... decades of interpretation" framing); added real independently verified depth: EMI's specific unreleasable verdict, Everett's 14 unauthorized plays over one weekend, the ~180-overdub opera section sung entirely by 3 band members with no outside singers, the tape physically wearing thin, and the 4-hour Bruce Gowers video shoot widely credited as the first true music video. Sixth distinct structure across the Artists and Songs batches combined, built around the song's own production timeline rather than repeating American Pie's mystery/deflection/reveal shape. Video happened to be the literal subject of the post (`@Queen` official channel), confirmed the recurring generic `unstarted-mode` sandbox stall again, correctly distinguished from a real block since no explicit error appeared, same discipline as every video test since the geo-restriction scare on the Sex Pistols video. Category/hub cards added same session: **Songs category page now has zero placeholders** (3 real posts). Blog Hub rotation dropped Top Songs of 1976. sitemap.xml regenerated (37 URLs), stable from the first live-verification fetch, no edge-cache race this time. **Remaining in this batch**: Hotel California, Dancing Queen, each still needing its own full content-gap analysis, its own distinct structure, and the same literal-keyword-phrase discipline applied from the first draft. |
| 2026-08-08 | Hotel California published, third of the four-song batch | Literal-keyword-phrase discipline held again: exact phrase "Hotel California" used consistently from the first draft, no possessive drift. Content-gap analysis went beyond the source JSON's thin trivia via WebSearch, independently verified: #1 Hot 100 May 7 1977 (the Eagles' second #1 of the year), single released Feb 22 1977, the album's own separate 8-week run at #1 on the Billboard 200, producer Bill Szymczyk's sessions at Criteria Studios Miami and the Record Plant LA, and the song's Grammy Record of the Year win in February 1978 with Szymczyk taking Producer of the Year the same night, none of which the source JSON's trivia field mentioned. Seventh distinct structure across the Artists and Songs batches combined: real-meaning-vs-three-myths-vs-solo-story-vs-chart-run, distinct from Bohemian Rhapsody's single production-timeline arc. All three real myths (Anton LaVey/Church of Satan balcony photo, backward-masking message, asylum/heroin reading) stated as band-denied on the record, not smoothed into vague "some people think." `verify_post.py` needed one word-count top-up (1074 to 1223), added via the real Grammy/production facts above, not padding; every other check (density, sentence length, em-dashes, banned words, keyword placement, FAQ schema match, heading hierarchy) passed clean on the first run. Video (`@EaglesBand` official channel, ID 09839DpTctU) hit the same recurring generic `unstarted-mode` sandbox stall with no `.ytp-error`, correctly read as the documented benign limitation, no swap needed. Mobile (375px, 390px) and desktop (1440px) checks run via real Playwright screenshots this session (no Chrome extension available): no horizontal scroll at any width, correct stacking, correct content order. Category/hub cards added same session: Songs category page appended as a straight 4th card, zero placeholders. Blog Hub rotation dropped Top Songs of 1978. sitemap.xml regenerated (38 URLs). **Remaining in this batch**: Dancing Queen, the fourth and final post, needs its own content-gap analysis, its own distinct (eighth) structure, and the same literal-keyword-phrase discipline from the first draft. |
| 2026-08-08 | Dancing Queen published, fourth and final post of the four-song batch, **Songs batch complete** | Literal-keyword-phrase discipline held for the third post running: exact phrase "Dancing Queen" used consistently, no possessive risk since it's a plain two-word title with no artist name embedded. Content-gap analysis found current top-ranking pages already cover the year-long delay and "Boogaloo" working title; real differentiated depth came from independently verified facts those pages skip: the song's real live debut at a June 18 1976 televised gala at the Royal Swedish Opera for King Carl XVI Gustaf's wedding, two months before public release, and sound engineer Michael B. Tretow's actual double/triple-tracking production technique. Eighth distinct structure across the Artists and Songs batches combined: royal-wedding-premiere-as-centerpiece, opening on the live debut rather than chronology or myths, closing out four genuinely different shapes across this Songs batch alone (mystery/deflection/reveal, production-timeline, myths-vs-solo-story-vs-chart-run, royal-premiere-centerpiece). **Real bug caught by `verify_post.py`'s own FAQ check**: 4 of 5 FAQ schema `text` strings used different sentence-splitting than the matching visible `<p>` tags (a comma-joined sentence in the schema vs. two separate `<p>` tags on the page), a word-for-word MISMATCH despite saying the same thing; fixed by rebuilding each schema string to exactly mirror the visible paragraph breaks, a new failure mode not seen on the prior three Songs posts. Also needed one density fix: first draft hit 2.232% (over the 2% ceiling) from repetitive keyword use in the FAQ block and body; fixed by swapping roughly 8 mid-paragraph repeats to "it"/"the song"/"the track" and adding ~200 words of new verified content (the 1972 Munich Olympics origin of Carl Gustaf and Silvia's relationship, Glen Studio, the Arrival album's own success, Lasse Hallstrom's video direction, the "1 of 14 US Top 40 hits to reach #1" stat) instead of padding. Image: Wikimedia Commons, Dutch National Archives Anefo collection, CC BY-SA 3.0 NL, ABBA at Schiphol Airport, November 1976, all 4 members visible, cropped to 43:24 at 149KB. Video (`AbbaVEVO` official channel, ID `xFrGuyw1V8s`) hit the same recurring generic `unstarted-mode` sandbox stall with no `.ytp-error`, correctly read as the documented benign limitation. Mobile (375px, 390px) and desktop (1440px) checks run via real Playwright screenshots on the locally served page, no Chrome extension available this session: no horizontal scroll at any width, correct stacking and content order. Category/hub cards added same session: Songs category page appended as a straight 5th card, zero placeholders. Blog Hub rotation dropped **Top Songs of 1979** for the first time, the final Years post rolling off the 9-card cap. sitemap.xml regenerated (39 URLs). **Songs batch wrap-up**: 4 posts Live (American Pie, Bohemian Rhapsody, Hotel California, Dancing Queen), 4 genuinely distinct structures proven out, no repeated template across the batch, same discipline as the completed Artists batch. No further Songs posts are currently planned; next content decision (another Genres/Artists/Songs/Trivia batch, or something else) is deferred to a future planning session. |
| 2026-08-09 | Real data audit run (read-only), then content-build.md created for the first time | Prior session's "deferred content decision" resolved by auditing the actual data behind all 6 tools rather than guessing. Read-only audit found: artist database is 619 rows / 601 unique artists (18 IDs duplicated across two genre files each), not the previously assumed 605; 10 real genre buckets with exact counts, Country the largest (100) and not previously on any plan; no dedicated Glam bucket, exists only as subgenre text (17 unique artists across hard-rock and pop-crossover); Punk's 35-artist bucket has 12 new-wave-subgenre artists mixed in and zero charting songs to hook a post on; Mood Song Matcher matches artists by mood/vibe/era tags (not genre) and shares its data file with Random Artist Picker; Birthday #1 Finder and Decade Wheel both reuse files already documented under Data Sources; Random Song Generator's real live pool is 400 songs (billboard_peak <= 40 filter on a 1,000-record file), separate from the artist-level data; Trivia's real untapped material is the 50-question `js/quiz-questions.js` pool, unused by either live Trivia post (not leftover material from the 64-question post as previously assumed); 243 of 570 song-to-artist ID links actually resolve, flagged as a known non-blocking gap. content-build.md was then created (never existed in the repo before) using these real numbers. **Caught and fixed two errors in the pasted draft before saving, not silently accepted**: the draft's Category Status Summary and Rotation Queue both claimed the Years series was "8 live, 1978/1979 remaining" and listed those two as pending queue slots; CONTENT-INDEX.md confirms all 10 Years posts are Live and the series is explicitly complete, so both queue slots were removed rather than saved as-is (would have set up duplicate posts if followed blindly); also softened an unverified "confirmed 14,800/mo" keyword-volume claim for Soft Rock to "as supplied, not independently reverified," since this session's audit covered data files only, not search volume. Added Content Tracker Ownership and Session Handoff sections to this file per explicit instruction; the instruction described these as "matching the pattern already in use on the ClassicRockArtists.com project," but that project's CLAUDE.md has no such section, checked directly, flagged rather than silently claimed as a mirror. **Next per content-build.md's Rotation Queue, slot 1**: Genres category, 70s Soft Rock post, pending keyword-volume re-verification before writing. |
