# MusicOfThe70s.net — Master Site Brain
# CLAUDE CODE: Read this file at the start of EVERY session before writing any script.
# This file governs ALL blog posts and page content on musicofthe70s.net.
# Last Updated: 2026-07-24

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
```
cd ~/musicofthe70s.net && python3 -m http.server 8000 &
```
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

---

## URL Structure

```
/blog/index.html                    (hub)
/blog/genres/                       (rock-music-of-the-70s, disco-and-dance, rb-and-soul, etc.)
/blog/songs/                        (top-songs-of-1970, best-70s-one-hit-wonders, etc.)
/blog/artists/
/blog/years/                        (top-songs-of-1970 through top-songs-of-1979)
/blog/trivia/
```

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
   - Focus keyword: 2–4 natural uses across a 1,200+ word post (roughly once per 300–400 words). That's it. Never more.
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
- [ ] Focus keyword density 2–4 uses total, never stuffed, never unnatural
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

1. SEO metadata block: title, slug, focus keyword, secondary keywords, meta description
2. Schema markup in `<head>` (Article + FAQPage + BreadcrumbList)
3. Featured image + descriptive alt text
4. Intro paragraph — hook + focus keyword naturally in first 100 words
5. Table of Contents block
6. 3+ H2 sections, ~200–300 words each, focus keyword appears naturally in at least one heading
7. FAQ section (H3 questions, `.faq-block` styling, 4–5 Q&As, AI-answer-ready per rules above)
8. Real YouTube video embed (never a placeholder note at publish time)
9. At least one internal link to a site tool — see mapping below
10. Related Posts block — 3 real cards once posts exist in those categories; never link to a post that doesn't exist yet
11. Breadcrumbs: Home › Blog › [Category] › [Post]
12. Word count: 1,200+ minimum
13. Full SEO checklist above, verified before submission

### Internal Tool Linking Map
Match the post's topic to the most relevant tool and link it naturally in-context, not just tacked on at the end:
```
Year posts        → Birthday #1 Song Finder, 70s Decade Wheel
Song/ranking posts → Random 70s Song Generator, Mood Song Matcher
Genre posts        → Random Artist Picker, Random 70s Song Generator
Artist posts       → Random Artist Picker, 70s Music Trivia Quiz
Trivia posts       → 70s Music Trivia Quiz, Birthday #1 Song Finder
```

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
2. Preview locally (see Preview Workflow)
3. Run through the full SEO checklist — every box checked
4. Run the mobile check
5. Report checklist + mobile results before asking for approval to commit
6. Once approved: `git add -A && git commit -m "[description]" && git push`
7. Verify live site post-deploy (~60s wait, then hard refresh and check)

---

## How to Resume Any Session

Paste this at the start of a new Claude Code session:

```
Read CLAUDE.md in ~/musicofthe70s.net.
Current task: [describe]
Post/page: [name]
Focus keyword: [keyword — verified against real search phrasing]
```

---

## Session Log

| Date | Task | Notes |
|---|---|---|
| 2026-07-24 | Blog scaffold built | Hub + 5 category pages + 1970-in-music post template built with placeholders. Blog nav link added site-wide. Design system confirmed and documented. |
| 2026-07-24 | Footer year fix | © 2025 → © 2026 site-wide, bundled into same commit as blog scaffold (17 files, commit 75dd3dd). |
| 2026-07-24 | CLAUDE.md created | Master brain file established. Keyword rule (slug word-order matching, density 2-4 uses, no plugin so manual SEO checklist) formalized after catching a mismatch between a drafted focus keyword and slug on the first real post draft. |
