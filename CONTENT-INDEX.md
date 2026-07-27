# MusicOfThe70s.net — Content & URL Index
# CLAUDE CODE: Read this file at the start of EVERY session, before CLAUDE.md rules are applied.
# This file is the single source of truth for what exists on the site.
# UPDATE THIS FILE every time a page or post is created, edited, or published.
# Never claim a page exists, never link to a page, and never generate a "Related Posts"
# card for a page that isn't listed below with status "Live."
# Last Updated: 2026-07-26 (70s Music Trivia post live, first Trivia post; site-wide back-to-top button added)

---

## How To Use This File

- Before writing any new content: check this file first for existing posts to link to internally.
- Before creating a "Related Posts" card: the target post MUST be listed below with Status = Live. If it isn't listed, don't link it — leave the card out or point to a tool instead.
- After creating, editing, or publishing anything: add/update its row in the correct table below in the SAME session, before ending the session.
- Never duplicate a URL or slug. Check this file before assigning a new slug to avoid collisions.
- Status values: `Live` (pushed and confirmed on the real site) · `Built-Local` (exists in repo, not yet pushed) · `Placeholder` (template exists, content not written) · `Planned` (not started)

---

## Core Site Pages (Tools)

| Page | URL | Status | Notes |
|---|---|---|---|
| Home | https://musicofthe70s.net/ | Live | Hero, featured tool, all-tools grid, SEO intro paragraph |
| Tools anchor | https://musicofthe70s.net/#tools | Live | In-page anchor on homepage |
| Random 70s Song Generator | https://musicofthe70s.net/pages/random-70s-song.html | Live | Featured tool. Has full SEO section "One Decade, Every Sound You Can Imagine." Focus keyword: 70s songs |
| Birthday #1 Song Finder | https://musicofthe70s.net/pages/birthday-number-one.html | Live | Focus keyword: number one songs 70s |
| Mood Song Matcher | https://musicofthe70s.net/pages/mood-song-matcher.html | Live | Focus keyword: best 70s songs |
| Random Artist Picker | https://musicofthe70s.net/pages/random-artist-picker.html | Live | Focus keyword: 70s artists |
| 70s Music Trivia Quiz | https://musicofthe70s.net/pages/70s-trivia-quiz.html | Live | Focus keyword: 70s music trivia |
| 70s Decade Wheel | https://musicofthe70s.net/pages/70s-decade-wheel.html | Live | Focus keyword: music of the 70s by year |
| About | https://musicofthe70s.net/pages/about.html | Live | |
| Privacy Policy | https://musicofthe70s.net/pages/privacy-policy.html | Live | |

---

## Blog Hub & Category Pages

| Page | URL | Status | Notes |
|---|---|---|---|
| Blog Hub | https://musicofthe70s.net/blog/index.html | Live | Placeholder post cards — needs real post cards as posts publish |
| Genres category | https://musicofthe70s.net/blog/genres/index.html | Live | Placeholder cards |
| Songs category | https://musicofthe70s.net/blog/songs/index.html | Live | Placeholder cards |
| Artists category | https://musicofthe70s.net/blog/artists/index.html | Live | Placeholder cards |
| Years category | https://musicofthe70s.net/blog/years/index.html | Live | Placeholder cards |
| Trivia category | https://musicofthe70s.net/blog/trivia/index.html | Live | Placeholder cards |

**Action needed:** update each category index page with real post cards as posts are published in that category. Remove placeholder cards once real ones exist.

---

## Blog Posts

One row per post. Add a new row the moment a post file is created — even before content is written — so slugs never collide.

| Title | URL | Category | Focus Keyword | Status | Word Count | Published | Last Updated | Internal Tool Link Used | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 70s Music Trivia: 64 Questions to Test Yourself | https://musicofthe70s.net/blog/trivia/70s-music-trivia/index.html | Trivia | 70s music trivia | Live | ~5,951 | 2026-07-26 | 2026-07-26 | 70s Music Trivia Quiz, Birthday #1 Song Finder | Verified live: 64 cards, 64 TOC links, reveal/explain interaction, and site-wide back-to-top button (added post-approval, no footer overlap) all confirmed via real Chromium rendering. First Trivia post. New reusable `.trivia-card` component (see css/style.css + js/trivia-card.js), 64 self-contained Q&A cards with See Answer/Explain reveal interaction, real Chromium-tested (Playwright). Keyword density intentionally very low (0.067%, 4 uses / 5,951 words) per explicit approval to prioritize natural placement over hitting 0.5%-2% at this page length. FAQPage schema covers all 64 cards (~4,300 words) in place of a standard small `.faq-block` — the cards themselves are this post's FAQ section, a deliberate format substitution for this post type. Schema text for the 7 list-containing cards is a natural-language flattening of the visible `<ul>` items (JSON can't contain HTML lists), not byte-identical to the rendered list — flagging as a structural constraint, not a drift bug. One internal blog-post link (Bee Gees, card #8, bolded). Source-verified: confirmed the flagged duplicate (Bee Gees/Saturday Night Fever) and spot-checked 5 of the 10 reconstructed questions against the raw 70s_Trivia.txt export, all faithful. Related Posts block omitted (no other Live post in Trivia category). No video embed per this post type (task-approved). Added 5th card to Blog Hub's "Latest Posts" row (no Trivia placeholder slot existed there). Resolved from Planned-table row ("70s Music Trivia Questions" / wrong slug+keyword) which has been removed. |
| Bee Gees: The Story of Pop's Most Successful Sibling Act | https://musicofthe70s.net/blog/artists/bee-gees/index.html | Artists | Bee Gees | Live | ~1,479 | 2026-07-26 | 2026-07-26 | Random Artist Picker | First Artists post. Title trimmed from the drafted "The Complete Story..." (65 chars) to fit the 60-char soft target; card labels still use the fuller "Complete Story" title since that's not capped. Featured image (NCRV photo, Wikimedia Commons) is CC BY-SA 3.0 Netherlands; credit line explicitly carries ShareAlike terms. Added a 4th card to the Blog Hub's "Latest Posts" row since no Artists placeholder slot existed there to replace (hub only ever had 3: Years/Genres/Songs). Related Posts block omitted (no other Live post in Artists category). Resolved from Planned-table placeholder ("[Artist spotlight — TBD which artist]") which has been removed. |
| Best Songs of the 70s: The Ultimate Decade Ranking | https://musicofthe70s.net/blog/songs/best-songs-of-the-70s/index.html | Songs | best songs of the 70s | Live | ~1,415 | 2026-07-26 | 2026-07-26 | Random 70s Song Generator, Mood Song Matcher | First Songs post. Featured image is a 5-photo Wikimedia Commons collage (not AI-generated); one source photo (Debby Boone, by John Mathew Smith & www.celebrity-photos.com) is CC BY-SA 2.0, so the composite is credited and released under CC BY-SA 2.0 terms per ShareAlike. Data conflict found and flagged (not fixed): year_end_hot100.json misfiles "You Light Up My Life" under 1978, contradicting its own embedded fun_fact text and the weekly file, both of which confirm 1977; post does not state a year for this song, so no content impact. Related Posts block omitted (no other Live post in Songs category). Corrected from stale Planned-table row ("Top Songs of the 70s" / top-songs-of-the-70s, wrong keyword) which has been removed. |
| 70s Rock: The Sound That Defined a Decade | https://musicofthe70s.net/blog/genres/70s-rock/index.html | Genres | 70s rock | Live | ~1,628 | 2026-07-25 | 2026-07-25 | Random Artist Picker, Random 70s Song Generator | First Genres post. Verified live via direct fetch 2026-07-25 (HTTP 200, content order H1→intro→image confirmed, optimized image serving). Related Posts block omitted (no other Live post in another category to link, per this file's own rule). Removed from Planned table (superseded the old "rock-music-of-the-70s" placeholder row with corrected, volume-verified keyword). Keyword density 7 uses / 1,628 words = 0.43%, inside the new 0.5%-2% range (see CLAUDE.md Keyword Rule update). |
| Top Songs of 1970 | https://musicofthe70s.net/blog/years/top-songs-of-1970/index.html | Years | top songs of 1970 | Live | ~1,683 | 2026-07-24 | 2026-07-25 | Birthday #1 Song Finder, 70s Decade Wheel | Retrofit pushed and verified live 2026-07-25: content order fixed (image now after intro), "Artists With Multiple Hits" rebuilt as real lists, image optimized (raw 6.3MB PNG replaced with compressed JPG/WebP + srcset, all under 200KB). Previously-flagged compliance gap is now closed. Related Posts block omitted (no other Live posts to link). |

**Planned posts (not yet started — listed so slugs are reserved and duplicates are avoided):**

| Title (working) | Planned URL | Category | Focus Keyword (verify before writing) |
|---|---|---|---|
| Disco Music of the 70s | /blog/genres/disco-music-of-the-70s/ | Genres | disco music of the 70s |
| Top Songs of 1971 through 1979 (9 more) | /blog/years/top-songs-of-19[71-79]/ | Years | top songs of 19[XX] |

---

## Redirect / Legacy URLs (do not reuse these paths)

| Old Path | Renamed To | Date | Notes |
|---|---|---|---|
| /blog/years/1970-in-music/ | /blog/years/top-songs-of-1970/ | 2026-07-24 | Slug renamed to match corrected focus keyword "top songs of 1970" per Keyword Rule. Never reassign this old path. |

---

## Quick Stats (update at a glance)

- Total live tool pages: 9
- Total live blog hub/category pages: 6
- Total published blog posts: 5 (all confirmed Live)
- Total placeholder/in-progress posts: 0
- Last full site audit: 2026-07-25

---

## End-of-Session Checklist for Claude Code

Before ending any session that touched content:
- [ ] New/edited page added or updated in the correct table above
- [ ] Slug checked against this file for duplicates before assigning
- [ ] Status field accurate (Live only if actually pushed and verified)
- [ ] Quick Stats counts updated
- [ ] "Last Updated" date at the top of this file updated
