# MusicOfThe70s.net — Content & URL Index
# CLAUDE CODE: Read this file at the start of EVERY session, before CLAUDE.md rules are applied.
# This file is the single source of truth for what exists on the site.
# UPDATE THIS FILE every time a page or post is created, edited, or published.
# Never claim a page exists, never link to a page, and never generate a "Related Posts"
# card for a page that isn't listed below with status "Live."
# Last Updated: 2026-07-25 (corrected stale status flag on Top Songs of 1970)

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
| Top Songs of 1970 | https://musicofthe70s.net/blog/years/top-songs-of-1970/index.html | Years | top songs of 1970 | Live | ~1,683 | 2026-07-24 | 2026-07-25 | Birthday #1 Song Finder, 70s Decade Wheel | Verified live via direct fetch 2026-07-25 (HTTP 200, content renders correctly). Related Posts block omitted (no other Live posts to link). NOTE: a local, uncommitted retrofit (content-order fix, list-rebuild for "Artists With Multiple Hits," image optimization/srcset) exists in the working tree but has NOT been pushed — the live version does not yet comply with the content-order, list-formatting, or image-optimization rules added to CLAUDE.md after this post's last push. Flagging as a known gap, not re-marking Built-Local, since the page itself is genuinely live per this file's own Status definition. |

**Planned posts (not yet started — listed so slugs are reserved and duplicates are avoided):**

| Title (working) | Planned URL | Category | Focus Keyword (verify before writing) |
|---|---|---|---|
| Top Songs of the 70s (all-decade ranked list) | /blog/songs/top-songs-of-the-70s/ | Songs | top songs of the 70s |
| Rock Music of the 70s | /blog/genres/rock-music-of-the-70s/ | Genres | rock music of the 70s |
| Disco Music of the 70s | /blog/genres/disco-music-of-the-70s/ | Genres | disco music of the 70s |
| 70s Music Trivia Questions | /blog/trivia/70s-music-trivia-questions/ | Trivia | 70s music trivia questions |
| [Artist spotlight — TBD which artist] | /blog/artists/[slug]/ | Artists | TBD |
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
- Total published blog posts: 1 (confirmed Live)
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
