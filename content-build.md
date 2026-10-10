# CONTENT-BUILD.md — musicofthe70s.net Master Content & Linking Tracker
# CLAUDE / CLAUDE CODE: Read this alongside CLAUDE.md and CONTENT-INDEX.md before planning any session.
# Full build write-ups + completed queue history: SESSION-LOG-ARCHIVE.md (grep it, don't open whole).
# Internal-linking strategy, the Tools-as-Pillars table, and the Anchor Text & Position Log moved to
#   .claude/skills/linking-and-tools/SKILL.md 2026-09-02 — open that during the linking step of a build, not at session start.
# Keep this file under 195 lines: prune shipped rows to SESSION-LOG-ARCHIVE.md (see .claude/skills/file-rotation/SKILL.md).
# Last Updated: 2026-10-09 (Rock hub / trivia / genre-list decisions recorded; S1-S6 queued)

---

## Current State (as of 2026-09-25)

- Songs artist-linked rotation queue (42 slots): complete, all LIVE. Closing post was Tragedy
  (Bee Gees, slot #42, `tragedy bee gees`, 2026-09-25, commit 61c51d7). Full per-slot detail
  (MacArthur Park, Heartache Tonight, Night Fever, New Kid in Town, Last Dance, Sir Duke, The
  Name of the Game, Blue Eyes Crying in the Rain, Marvin Gaye Let's Get It On, Al Green Tired
  of Being Alone, etc.) pruned to SESSION-LOG-ARCHIVE.md 2026-09-25. New Songs picks now come
  from the Strategy Queue below (STRATEGY-2026.md section 6E).
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

## Strategy Queue (audited 2026-10-09 against live repo + site)

Source: STRATEGY-2026.md (reference, exempt from cap; open only the named section). Only NOT STARTED / PARTIAL
items listed. DONE items (Phase 0 items 1-6, 9-11 + 12 core pages, flagships 6A 1-6, homepage, Best Songs, Disco,
Soul, chart-archive gap fix) are in SESSION-LOG-ARCHIVE.md "Strategy Queue as of 2026-10-09".

**GUARDRAIL: no ABBA or Bee Gees posts before 2026-11-25** (section 6D). Newest live: Tragedy 2026-09-25.

1. **Phase 0 trust fixes left** (section 8)
   - Item 7 PARTIAL: 94 of 110 posts have <3 external links (songs 56, artists 24, genres 5, Years 1975-79, trivia 4). 5/session, start Years 1975-79
   - Item 8 NOT STARTED, Charlie's action: Bing Webmaster + IndexNow (no msvalidate tag or key file in repo)
2. **AdSense readiness (item 12) PARTIAL** (section 8; CLAUDE.md YouTube rule)
   - Contact page, About publisher identity, Privacy Policy ad text, sitemap (131 URLs, no gaps) are in place
   - Left: Charlie confirms hello@musicofthe70s.net receives mail (unverifiable from here); run `youtube_status.py --report`; audit player pages for non-YouTube content and anchor/vignette overlap
3. **Homepage rebuild**: DONE, nothing queued
4. **Flagship/upgrade pages left** (section 6A/6B): all 6 flagships resolved
   - 70s Rock hub + 4 genre lists (pop, funk, hard rock, country rock): DECIDED 2026-10-09, see Genre Lists and Hub Rollout below
   - Trivia pair: DECIDED 2026-10-09, cross-link only (no merge), see S6 below
5. **Genre pillars** (section 6C): 70s Country Music NOT STARTED (`70s country songs`, 4,400; only 70s-country-rock exists). Start after the Genre Lists and Hub Rollout group (S1-S6) or when Charlie picks it
6. **Artists rotation NOT STARTED** (section 6D, in order; 0 of 10 live): Elton John, Led Zeppelin, The Carpenters, Fleetwood Mac, Chicago, Pink Floyd, Olivia Newton-John, ELO, Jackson 5, Earth Wind & Fire. Then 6D "then" list
7. After the above: Songs from live 6D artists (6E), listening pages cap 4 (6F), This Week in 1970s Music (6G): all NOT STARTED

Known prose misses (low priority): Number One Hits density 0.195%; 1970 year page density + sentence length;
subheading rule FAIL on 10 year pages, soft-rock, punk, Talking Heads (pre-existing).
Rhythm: Mon flagship/upgrade, Tue Artist, Wed Song, Thu 6G, Fri Song or source pass. Charlie builds when he has time.

### Decided 2026-10-09 (Charlie; Search Console last 3 mo, whole site: 0 clicks, 276 impressions, avg pos ~52; Rock hub <12 impressions, no ranking to protect)
1. **Rock hub** (/blog/genres/70s-rock/): hub + short playable teaser, NOT a full playable list. Keep ALL existing content, changes additive. Link all 6 subgenre pages (hard rock, soft rock, prog, punk, folk rock, country rock). Teaser = 15-20 top rock songs from data/billboard. Subgenre pages keep their own full lists. Needs hard rock + country rock list pages built first.
2. **Trivia pair** (70s-music-trivia static 64 Qs, 70s-music-quiz scored 50 Qs): NO merge, NO redirects, NO URL changes. Cross-link only: CTA on static post to the quiz; link from quiz back to static post (answers/study guide). Compare question sets; if many duplicates, REPORT count and propose rewrites. No rewrites without Charlie's approval (scaled/duplicate-content guardrail).
3. **Full playable lists** for pop (230 songs), funk (58), hard rock (28), country rock (22), same pattern as soft rock, folk rock, glam, prog (2026-10-06 chart-archive fix). Pop needs a performance check first (page weight, mobile load with 230 players; consider lazy loading, pagination or year filters). Player stays visible and unobscured (YouTube Required Minimum Functionality, fixed on radio page).

### Genre Lists and Hub Rollout (one task per session, in order)
Standing checklist for EVERY session S1-S6: content-gap check; PUBLISH GATE (local-server review, never commit or push live content without Charlie's explicit go-ahead); 3+ external source links on any page touched; internal link rule (same target once per article); clean URLs only; run check_clean_urls.py and check_schema.py; mobile check; update content-build.md and CONTENT-INDEX.md; end with the closed status report.
ABBA / Bee Gees: no new posts or pages about them before 2026-11-25 (their songs may appear inside list pages).
Tools: generate_genre_lists.py PAGES + generate_beyond_year_end.py.
- S1. Pop list page (230 songs), including the performance check first: DONE 2026-10-09 (live, f2aa129; 230 rows, no videos load until Play, no pagination needed)
- S2. Funk list page (58): DONE 2026-10-09 (live, b5b46e9; 58 rows, 11 #1 hits, Sources section added with 4 Wikipedia links)
- S3. Hard rock list page (28): DONE 2026-10-09 (live, a86a521; 28 rows, 1 #1 hit, Sources section added with 4 Wikipedia links)
- S4. Country rock list page (22): OPEN
- S5. Rock hub rework (needs S3 and S4 done): OPEN
- S6. Trivia/quiz cross-linking + duplicate-question report: OPEN


**Flagged, not in rotation (Charlie's call, unaffected by the strategy queue):**
| Item | Detail | Status |
|---|---|---|
| Rock genre-page overlap | /blog/genres/70s-rock/ vs its 6 subgenre pages | RESOLVED 2026-10-09: hub + teaser (S5) |
| Trivia UX overlap | static 64-question post vs scored 50-question quiz | RESOLVED 2026-10-09: cross-link only (S6) |

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
