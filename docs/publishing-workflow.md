# Publishing Workflow — Full Detail

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

## Mobile Check (required before any post ships)
Verify in Chrome DevTools responsive mode at 375px (iPhone SE) and 390px (iPhone 14) width:
- No horizontal scroll
- TOC block stacks correctly
- FAQ block stacks correctly
- Related-posts cards stack to single column
- Images scale correctly, no overflow
- Nav collapses to hamburger correctly
Report pass/fail explicitly before a post is considered ready to push.

## Publishing Workflow
1. Write/generate post content following the full template (post-template.md)
2. Run `python3 scripts/verify_post.py <path/to/post/index.html> "<focus keyword>"` — checks word count, keyword density, sentence-length distribution, em-dash count (correctly distinguishing the list-item numeric-separator exception from prose), banned words, FAQ schema/visible match, heading hierarchy, and keyword placement in one pass. Built 2026-07-31 after the same checks were re-derived by hand on four straight posts; use it instead of re-deriving them manually.
3. Preview locally (see repo-deploy.md)
4. Run through the full SEO checklist — every box checked (seo-rules.md)
5. Run the mobile check
6. Report checklist + mobile results before asking for approval to commit
7. Once approved: `git add -A && git commit -m "[description]" && git push`
8. Verify live site post-deploy (~60s wait, then hard refresh and check)

## Tool-to-Blog Linking (Tier 1/2/3) — Tier 1 parked
Charlie proposed linking the site's interactive tools (Random 70s Song Generator, Random Artist Picker, Trivia Quiz, Decade Wheel) directly to on-site content instead of sending users to YouTube search results, to keep visitors on-domain. Scoped into three tiers 2026-08-06:
- **Tier 1**: swap each tool's "Search on YouTube" link for a real inline video embed. Blocked on a real data gap: none of the tools' JSON records store an actual video ID, only a `youtube_search` query string. A real embed needs either a live YouTube Data API lookup (new infrastructure, API key/quota/cost, this site is static with no backend) or a one-time verified-video-ID enrichment pass across up to 1,619 records. **Parked, not proceeding**, per explicit instruction.
- **Tier 2**: link tool results to matching blog posts about that specific song/artist, when one exists.
- **Tier 3**: lightweight auto-generated song/artist profile pages built from existing JSON data, for everything that doesn't get full blog-post treatment.

Tier 2 and Tier 3 are correctly gated on Artists/Songs posts actually existing first. Neither is scoped or started; there's no backlog of individual posts to link to yet.