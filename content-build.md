# CONTENT-BUILD.md — musicofthe70s.net Master Content & Linking Tracker
# CLAUDE / CLAUDE CODE: Read this alongside CLAUDE.md and CONTENT-INDEX.md before planning any session.
# Full build write-ups + completed queue history: SESSION-LOG-ARCHIVE.md (grep it, don't open whole).
# Internal-linking strategy, the Tools-as-Pillars table, and the Anchor Text & Position Log moved to
#   .claude/skills/linking-and-tools/SKILL.md 2026-09-02 — open that during the linking step of a build, not at session start.
# Keep this file under 195 lines: prune shipped rows to SESSION-LOG-ARCHIVE.md (see .claude/skills/file-rotation/SKILL.md).
# Last Updated: 2026-09-25 (Tragedy, Bee Gees, slot #42, LIVE, queue complete)

---

## Current State (as of 2026-09-25)

- Tragedy (Songs, slot #42, final slot in the 42-song queue): focus keyword `tragedy bee gees`
  (6,600/mo, informational, vs. 60,500/mo bare `tragedy` rejected as generic-word/Steps-cover
  wrong-intent, same call as MacArthur Park). **LIVE 2026-09-25 (commit 61c51d7, pushed to
  origin/main, live-verified; regen commit 0a31f17).** Full build write-up: SESSION-LOG-ARCHIVE.md.
  This was the last open slot in the 42-song artist-linked rotation queue; queue is now
  complete, all 42 slots LIVE.

- MacArthur Park (Songs, slot #38): focus keyword `macarthur park donna summer`. **LIVE 2026-09-22
  (commit 081a94d, pushed to origin/main, live-verified).** Full build write-up pruned to
  SESSION-LOG-ARCHIVE.md 2026-09-25.

- Heartache Tonight (slot #37, `heartache tonight`), Night Fever (slot #36), New Kid in Town (slot
  #32), Last Dance (slot #33), Sir Duke (slot #34), The Name of the Game (slot #35), Blue Eyes Crying
  in the Rain (slot #28), Marvin Gaye Let's Get It On (slot #22), and Al Green Tired of Being Alone
  (slot #21): all confirmed LIVE, Charlie-approved. Full write-ups pruned to SESSION-LOG-ARCHIVE.md.
- Songs artist-linked rotation queue: all 42 slots LIVE, queue complete. Most recent LIVE post:
  Tragedy (Bee Gees, 2026-09-25).
- Note: local main preserves an unpushed CI-workflow commit (709eda5) on local branch
  `ci-workflow-pending`, not on remote per the standing PAT-scope call (Charlie-approved).
- Genres Rotation Queue is fully clear. Years series complete (10/10). Trivia has no cap.
- Standing flags for Charlie (not blocking any build):
  - Rock Trivia Game (7th tool) is built but NOT shipped — decided against 2026-08-27. Stays built and
    unpublished, not part of the active rotation. Permanent: not going to be done.

## How This File Works

1. Before writing anything new, check CONTENT-INDEX.md for what's already live — never duplicate.
2. Pick the next item from the Rotation Queue below. If a category has no ready item, skip to the next rather than forcing it.
3. Every new post links to at least one Tool (Tools-as-Pillars table: .claude/skills/linking-and-tools/SKILL.md).
4. Every new post checks the "link owed" table (.claude/skills/linking-and-tools/SKILL.md) for a cross-category opportunity, and logs its internal links in the Anchor Text & Position Log there.
5. Update this file's Current State block and prune shipped rows to SESSION-LOG-ARCHIVE.md every session, per the Content Tracker Ownership rule in CLAUDE.md.

---

## Path Forward — Pillars, Rotation, and Linking (added 2026-08-22)

**Pillars.** The site's two permanent pillar types are the homepage and the six interactive tools (Tools-as-Pillars table: .claude/skills/linking-and-tools/SKILL.md). Every new post links to whichever pillar its content actually supports — not the homepage by default, and not a mismatched tool for the sake of having a tool link.

**Active rotation set.** Genres, Songs, Artists, Trivia. Years is a closed, complete 1970-1979 series (no cap, no further posts planned) and sits outside active rotation unless a genuinely new Years angle comes up. Rotate across the four active categories rather than clearing one before starting the next; if a category has no keyword-checked, non-overlapping angle ready, skip it for that turn instead of forcing a thin post (already the rule in item 2 above — restated here as it applies specifically to rotation planning).

**Before starting any new post:**
1. Check CONTENT-INDEX.md — never duplicate a live or planned post.
2. Cross-check the live sitemap, https://musicofthe70s.net/sitemap.xml, as the source of truth for what's actually published. CONTENT-INDEX.md can drift from the live site (the 2026-08-14 Funk entry is a real example — see Session Log).
3. Check the category's live post count against its cap (Genres 6, Artists 6, Songs 6). Trivia has no cap (Charlie-confirmed 2026-08-24).

**Every post's linking checklist:**
1. Link up to its own category hub page.
2. Link to at least one relevant Tool (a pillar).
3. Check the "link owed" table (.claude/skills/linking-and-tools/SKILL.md) for a cross-category link to close, and close it in both directions the same session.
4. Never repeat the same internal link target twice within one post (standing rule).
5. Link to the song's year page and its genre pillar (STRATEGY-2026.md section 5).
6. Every new post gets a visible byline, published/updated dates, and 3+ external source links (STRATEGY-2026.md section 8, items 3 and 7).

**Database growth.** Every new post's angle comes from a real, verified content-gap check — live SERP plus this site's own JSON data — not a generic keyword-driven post. This is the actual mechanism that has kept every post on the site distinct (30+ distinct structures logged across the archives) while still growing the database on a steady rotation, and it's what keeps the site clear of Google's scaled-content-abuse risk (see the standing guardrail in profile/topic notes). Don't relax this check for the sake of rotation speed.

**Auto-Go Rule (added 2026-08-22, Charlie-confirmed):** If a focus keyword has never been used as another live post's focus keyword on this site, AND the angle is confirmed structurally distinct from every existing post that touches the same subject (the standard acknowledge-and-distinguish check every post already runs), that post is a go — no separate approval checkpoint needed before Claude Code starts building. This does not remove the content-gap/overlap check itself, or the standing PUBLISH GATE (still no commit/push without Charlie's local-review go-ahead) — it only removes the extra "confirm before starting" step once both conditions are independently verified true.

---

## Content Selection & Quality Gate (added 2026-08-22)

**Article Selection Gate — answer all 8 before queuing anything:** Why should this exist? What reader need does it satisfy? What content gap does it fill? Does the site already cover this (check live sitemap + CONTENT-INDEX.md)? Would updating an existing post serve better than a new one? What makes it different from what's already rankable elsewhere? Which pillar/hub/tool does it strengthen? What can this site specifically provide that a generic page can't? If these can't be answered clearly, don't queue it — this formalizes what every Session Log entry below has already been doing case-by-case.

**Internal linking, reframed:** each post gets one **primary destination** (the single most topically relevant pillar, hub, or tool — not the homepage by default) and up to two **secondary destinations**, only where genuinely useful to the reader. Never link to hit a quota. This sits on top of, not instead of, the existing linking checklist above (category hub + Tool + link-owed table).

**Quality bar before calling anything done:** would a serious 70s-music fan find this genuinely useful and worth returning to — and could it be found elsewhere in essentially the same form? If the honest answer to the second question is yes, the angle needs more depth or a sharper unique angle before it ships, not more words. (No conflict with `verify_post.py`'s word-count floor — every past case of hitting that floor was filled with real, verified facts, never padding; keep doing that.)

**The standing loop, stated plainly:** existing content -> identify gaps -> pick the best-justified opportunity -> verify facts -> build -> that work surfaces new gaps -> repeat. This is already how the site has grown; nothing new to build, just naming it so it's explicit.

**Division of labor — NotebookLM is NOT part of the regular pipeline.** Normal opportunity selection runs entirely inside this file and the live repo: Rotation Queue + Article Selection Gate + Auto-Go Rule, using Claude Code's own real data access (JSON files, live sitemap, WebSearch, `verify_post.py`). NotebookLM only has content-build.md, the homepage PDF, and whatever's manually added — no live repo access, no WebSearch, no verification tools — so it has no role in picking or building individual posts.

**NotebookLM's one job: Claude Code flags when a fresh baseline audit is needed** — e.g. CONTENT-INDEX.md has visibly drifted from the live site, the Rotation Queue backlog is empty and needs a new inventory pass, or a significant stretch of posts has shipped since the last audit. When Claude Code raises that flag, Charlie brings it to chat, and chat supplies the NotebookLM prompt to refresh the inventory/rotation baseline (same shape as the 2026-08-22 sitemap audit above). Outside of that trigger, NotebookLM isn't touched.

**On CLAUDE.md specifically:** none of the above needs to go there. CLAUDE.md governs Claude Code's tactical build conventions (PUBLISH GATE, Prose Protocol, verify_post.py checklist, etc.) and stays under 200 lines by standing rule — that ceiling doesn't change. Everything in this section is strategic/selection-level, which is what content-build.md is for; Claude Code already reads this file alongside CLAUDE.md before planning any session, so nothing is lost by keeping it here instead.

---

## Strategy Queue (2026-09-25)

Source of truth: STRATEGY-2026.md (approved 2026-09-25 rebuild plan). Reference file, exempt from
the 195-line cap — open only the section named below, never the whole file. This section replaces
the old Category Rotation Queue table and the Artists genre-rotation rule; completed/decided-against
history for both stays in SESSION-LOG-ARCHIVE.md.

**Phase 0 — technical/trust fixes (STRATEGY-2026.md section 8), one per session, in order:**
1. Confirm clean-URL fix is live, resubmit sitemap, request indexing (item 1)
2. Fix the GSC "Redirect error" URLs (item 2)
3. Visible byline + published/updated dates on every post, matched in schema (item 3)
4. Author page for Charlie (item 4)
5. Methodology / editorial policy page (item 5)
6. Category hubs list every post (item 6)
7. 3+ external source links on existing posts, rolling 5/session (item 7)
8. robots.txt AI-crawler review; llms.txt refresh (item 9)
9. Schema audit: MusicRecording, MusicGroup/Person `sameAs`, BreadcrumbList (item 10)
10. Core Web Vitals on /radio/ and tools, click-to-load facade (item 11)

(Item 8 in STRATEGY-2026.md, Bing Webmaster Tools/IndexNow, is Charlie's own action, not a session
build. Item 12, AdSense readiness, follows per CLAUDE.md's YouTube Compliance rule once 1-6 land.)

**Weekly rhythm, once Phase 0 clears (repeats):**
- Mon — flagship data page or upgrade page
- Tue — Artist
- Wed — Song
- Thu — "This Week in 1970s Music" (STRATEGY-2026.md section 6G)
- Fri — Song, or a source-citation pass (Phase 0 item 7 continuation)

**Ordering within each slot:**
- Flagships (Mon): STRATEGY-2026.md section 6A, table order 1-6
- Upgrades (Mon, alternating with flagships): STRATEGY-2026.md section 6B, table order
- 70s Country pillar: STRATEGY-2026.md section 6C
- Artists (Tue): STRATEGY-2026.md section 6D, table order, then the "then:" list after it
- Songs (Wed/Fri): STRATEGY-2026.md section 6E, drawn only from live 6D artists
- Listening pages (fold into Mon or Fri as needed): STRATEGY-2026.md section 6F, cap 4

**Pause:** no ABBA or Bee Gees posts before 2026-11-25 (STRATEGY-2026.md section 6D).

**Flagged, not in rotation (Charlie's call, unaffected by the strategy queue):**
| Item | Detail | Status |
|---|---|---|
| Rock genre-page overlap | /blog/genres/70s-rock/ vs its 6 subgenre pages | Structural edit to a live post (NotebookLM idea: make it a nav hub). |
| Trivia UX overlap | static 64-question post vs scored 50-question quiz | Edit to live content. |

---

## Songs Rotation Queue — artist-linked batch (added 2026-08-31, complete)

42-song artist round-robin queue, chart-verified against `data/billboard/`. All 42 slots LIVE as
of Tragedy (Bee Gees, 2026-09-25); queue complete. Full ordered list, standard-form linking rule,
and zero-candidate artist notes pruned to SESSION-LOG-ARCHIVE.md 2026-09-25 (grep "Songs Rotation
Queue — artist-linked batch, full ordered list"). New Songs picks now come from the Strategy Queue
above (STRATEGY-2026.md section 6E, drawn from live 6D artists).

---

## Category Status Summary (current, corrected against the 2026-08-22 sitemap audit)

| Category | Live Posts | State |
|---|---|---|
| Years | 10 | Series complete, no further posts planned |
| Songs | 55 | All 42 slots of the artist-linked rotation queue LIVE, queue complete, most recently Tragedy (Bee Gees, 2026-09-25). Over its 6-post cap since 2026-08-16 by design; still thin relative to the 1,000-record song database |
| Artists | 24 | George Clinton (funk bucket) published 2026-08-27, first Artists post in the funk bucket. Jim Croce published the same day, first post under the folk-rock/singer-songwriter camp. Rick James (funk bucket, second post) published 2026-08-29. Marvin Gaye (soul bucket, first post) published 2026-08-29. Al Green (soul bucket, second post) published 2026-08-30. Donna Summer (disco bucket, second post) published 2026-08-31. Thin relative to the 601-artist JSON pool — real tool dead-end risk (grep "Sitemap-Verified Findings" SESSION-LOG-ARCHIVE.md) |
| Trivia | 4 | No cap (Charlie-confirmed 2026-08-24): 70s Music Trivia, 70s Music Quiz, ABBA vs Queen, Banned Songs of the 70s |
| Genres | 12 | Rotation Queue fully clear; every real, coherent Genres angle surfaced so far has shipped |

Full detail on how each of these numbers was reached, and the 2026-08-22 Sitemap-Verified Findings, is in SESSION-LOG-ARCHIVE.md.
