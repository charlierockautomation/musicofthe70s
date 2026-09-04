# CONTENT-BUILD.md — musicofthe70s.net Master Content & Linking Tracker
# CLAUDE / CLAUDE CODE: Read this alongside CLAUDE.md and CONTENT-INDEX.md before planning any session.
# Full build write-ups + completed queue history: SESSION-LOG-ARCHIVE.md (grep it, don't open whole).
# Internal-linking strategy, the Tools-as-Pillars table, and the Anchor Text & Position Log moved to
#   docs/linking-and-tools.md 2026-09-02 — open that during the linking step of a build, not at session start.
# Keep this file under 195 lines: prune shipped rows to SESSION-LOG-ARCHIVE.md (see docs/file-rotation.md).
# Last Updated: 2026-09-04 (Georgia on My Mind, slot #13, Built-Local, awaiting review)

---

## Current State (as of 2026-09-04)

- Song YMCA (Songs, slot #12) went LIVE 2026-09-04 (pushed, confirmed HEAD matches
  origin/main at start of this session).
- Last built: Georgia on My Mind (Songs, artist-linked rotation queue slot #13), built and
  verified locally 2026-09-04, NOT yet pushed, awaiting Charlie's review per Publish Gate.
  Focus keyword `Georgia on My Mind` (literal song title, no logged WordStream pull; verified
  as real search phrasing per seo-rules.md's autocomplete/PAA path instead, same as the
  song-title precedent already used across this rotation queue). Forward backlink added to
  the Willie Nelson artist page same session (list-item anchor in the "Every Number One"
  section, same pattern as the Stevie Wonder/Superstition precedent). Angle: the Stardust
  album story, not the Ray Charles standard, distinct from the artist page's one-line mention
  of the song. Real sourced detail: Columbia execs' recorded pushback quote, the Enactron
  mobile truck parked at Emmylou Harris and Brian Ahern's house (Mickey Raphael's harmonica
  recorded from their tiled shower), the country #1 week (1978-06-10, this site's own
  data/billboard/country.json), the 1979 Grammy, and the Ray Charles/Georgia-state-song
  coincidence (both landmarks in 1979). No radio_id for this song in
  data/radio/radio-songs.json, so no Listen Now deep link this post (only post in the queue
  so far without one). `verify_post.py` needed two iterations (sentence-length %, title length,
  one subheading-rule fix); clean after fixes (1,266 words, 1.027% density, 97.3% sentences
  under 20 words). Category/hub/archive cards and sitemap/llms.txt regenerated locally
  (Songs 26, total 76 pending push).
- Songs artist-linked rotation queue: slots 1-12 LIVE, slot #13 (Georgia on My Mind)
  Built-Local. Next up after approval: slot #14, Get on the Good Foot (James Brown).
- Note: local main had an unpushed CI-workflow commit (709eda5, `.github/workflows/
  update-generated-files.yml`) sitting ahead of remote. Rebased this session's push around
  it (Charlie-approved); the workflow commit is preserved on local branch
  `ci-workflow-pending`, not lost, still not on remote per the standing PAT-scope call.
- Genres Rotation Queue is fully clear. Years series complete (10/10). Trivia has no cap.
- Standing flags for Charlie (not blocking any build):
  - Rock Trivia Game (7th tool) is built but NOT shipped — decided against 2026-08-27. Stays built and
    unpublished, not part of the active rotation. Permanent: not going to be done.

## How This File Works

1. Before writing anything new, check CONTENT-INDEX.md for what's already live — never duplicate.
2. Pick the next item from the Rotation Queue below. If a category has no ready item, skip to the next rather than forcing it.
3. Every new post links to at least one Tool (Tools-as-Pillars table: docs/linking-and-tools.md).
4. Every new post checks the "link owed" table (docs/linking-and-tools.md) for a cross-category opportunity, and logs its internal links in the Anchor Text & Position Log there.
5. Update this file's Current State block and prune shipped rows to SESSION-LOG-ARCHIVE.md every session, per the Content Tracker Ownership rule in CLAUDE.md.

---

## Path Forward — Pillars, Rotation, and Linking (added 2026-08-22)

**Pillars.** The site's two permanent pillar types are the homepage and the six interactive tools (Tools-as-Pillars table: docs/linking-and-tools.md). Every new post links to whichever pillar its content actually supports — not the homepage by default, and not a mismatched tool for the sake of having a tool link.

**Active rotation set.** Genres, Songs, Artists, Trivia. Years is a closed, complete 1970-1979 series (no cap, no further posts planned) and sits outside active rotation unless a genuinely new Years angle comes up. Rotate across the four active categories rather than clearing one before starting the next; if a category has no keyword-checked, non-overlapping angle ready, skip it for that turn instead of forcing a thin post (already the rule in item 2 above — restated here as it applies specifically to rotation planning).

**Before starting any new post:**
1. Check CONTENT-INDEX.md — never duplicate a live or planned post.
2. Cross-check the live sitemap, https://musicofthe70s.net/sitemap.xml, as the source of truth for what's actually published. CONTENT-INDEX.md can drift from the live site (the 2026-08-14 Funk entry is a real example — see Session Log).
3. Check the category's live post count against its cap (Genres 6, Artists 6, Songs 6). Trivia has no cap (Charlie-confirmed 2026-08-24).

**Every post's linking checklist:**
1. Link up to its own category hub page.
2. Link to at least one relevant Tool (a pillar).
3. Check the "link owed" table (docs/linking-and-tools.md) for a cross-category link to close, and close it in both directions the same session.
4. Never repeat the same internal link target twice within one post (standing rule).

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

## Category Rotation Queue (current / open items only)

Completed and decided-against slots live in SESSION-LOG-ARCHIVE.md ("Completed & Decided-Against
Rotation Queue History" plus the 2026-09-02 prune section). Only what is still open is below.

| Category | Content | Status |
|---|---|---|
| Songs (rotation, artist-linked) | 42-song artist round-robin queue | Slots 1-12 LIVE, slot 13 (Georgia on My Mind) Built-Local awaiting review. Slot 14, Get on the Good Foot (James Brown), up next after approval. Full ordered list in the next section. |
| Rock genre-page overlap | /blog/genres/70s-rock/ vs its 6 subgenre pages | Flagged, not queued: a structural edit to a live post (NotebookLM idea: make it a nav hub). Charlie's call. |
| Trivia UX overlap | static 64-question post vs scored 50-question quiz | Flagged, not queued: an edit to live content. Charlie's call. |
| Artists genre-rotation | Led Zeppelin, Pink Floyd, Yes, Genesis (rock buckets) | Zero-coverage gaps still needing sorting into the genre-rotation order below. |

Artists rotation rule (2026-08-24): rotate future Artists posts by genre bucket, working through the 10
real data/artists/ files, not names off a flat list. Buckets done so far: country (Dolly Parton, Willie
Nelson), soft-rock/folk (Carole King, Jim Croce), funk (George Clinton, Rick James), soul (Marvin Gaye,
Al Green), disco (Village People, Donna Summer). Duplicate-ID artists placed by Charlie's direct call
each time. Full per-post build write-ups: grep CONTENT-INDEX-ARCHIVE.md / SESSION-LOG-ARCHIVE.md.

---

## Songs Rotation Queue — artist-linked batch (added 2026-08-31)

42 songs, chart-verified against `data/billboard/` (Hot100 year-end/weekly + country #1, real singles only, no album-chart entries) for artists with a Live Artists page, minus songs already Live in Songs. Order is round-robin across artists, not grouped, so consecutive posts don't repeat an artist. Each post links back to its artist page; each artist page gets a body-text link forward to the song page once it's Live (add on the same session the song publishes, not as a follow-up).

**Standard form, every post in this queue from Waterloo on (Charlie-confirmed 2026-08-31)**: in addition to the artist backlink and the two Tool links, every post also gets (1) a text link, anchor the song title, to `/radio/index.html?play=<radio_id>` where that song has a `radio_id` in `data/radio/radio-songs.json` (see post-template.md's Internal Tool Linking Map and js/radio.js `applyDeepLink()`), and (2) a text link, anchor "Music of the 70s", to `/index.html`. Both natural in-context, not fixed slots.

**Before writing each one**: real focus-keyword volume check (Keyword Rule, non-negotiable) and content-gap analysis (content-plan.md standing rules) still apply, same as every other post. Batch is quality-gated: if a candidate doesn't have enough real story substance for 1,200+ words, drop it rather than pad it, same call as KC and the Sunshine Band getting dropped from the Artists batch. Build one at a time; report before moving to the next.

**George Clinton mapping flagged, not auto-confirmed**: "Give Up the Funk" and "Flash Light" are chart-credited to Parliament, not George Clinton by name. Included here on the assumption his artist page covers Parliament-Funkadelic and can take the backlink; confirm before building #16/#29 or drop them.

1. Waterloo — ABBA — **LIVE 2026-08-31**
2. How Can You Mend a Broken Heart — Bee Gees — **LIVE 2026-08-31**
3. Killer Queen — Queen / Brian May and Queen — **LIVE 2026-09-01**
4. One of These Nights — Eagles the Band — **LIVE 2026-09-01**
5. Let's Stay Together — Al Green — **LIVE 2026-09-01**
6. What's Going On — Marvin Gaye — **LIVE 2026-09-02**
7. Hot Stuff — Donna Summer — **LIVE 2026-09-02**
8. Superstition — Stevie Wonder — **LIVE 2026-09-03**
9. Jolene — Dolly Parton — **LIVE 2026-09-03**
10. Bad, Bad Leroy Brown — Jim Croce — **LIVE 2026-09-03**
11. It's Too Late / I Feel the Earth Move — Carole King — **LIVE 2026-09-03**
12. Y.M.C.A. — Village People — **LIVE 2026-09-04**
13. Georgia on My Mind — Willie Nelson — **Built-Local 2026-09-04, awaiting review**
14. Get on the Good Foot — James Brown
15. You and I — Rick James
16. Give Up the Funk (Tear the Roof off the Sucker) — George Clinton (Parliament, flagged above)
17. Knowing Me, Knowing You — ABBA
18. Jive Talkin' — Bee Gees
19. Somebody to Love — Queen / Brian May and Queen
20. Best of My Love — Eagles the Band
21. Tired of Being Alone — Al Green
22. Let's Get It On — Marvin Gaye
23. Bad Girls — Donna Summer
24. You Are the Sunshine of My Life — Stevie Wonder
25. I Will Always Love You — Dolly Parton
26. Time in a Bottle — Jim Croce
27. In the Navy — Village People
28. Blue Eyes Crying in the Rain — Willie Nelson
29. Flash Light — George Clinton (Parliament, flagged above)
30. Take a Chance on Me — ABBA
31. You Should Be Dancing — Bee Gees
32. New Kid in Town — Eagles the Band
33. Last Dance — Donna Summer
34. Sir Duke — Stevie Wonder
35. The Name of the Game — ABBA
36. Night Fever — Bee Gees
37. Heartache Tonight — Eagles the Band
38. MacArthur Park — Donna Summer
39. Living for the City — Stevie Wonder
40. How Deep Is Your Love — Bee Gees
41. Too Much Heaven — Bee Gees
42. Tragedy — Bee Gees

**Zero-candidate artists, no song slot possible from current data**: Grateful Dead, Iggy Pop, Talking Heads, Agnetha Faltskog, Anni-Frid Lyngstad, Benny Andersson, Bjorn Ulvaeus — no confirmed Hot100/country single in the JSON, matches the "zero chart entries" angle already used in their Live posts.

**#13, Georgia on My Mind (Willie Nelson): Built-Local 2026-09-04, awaiting Charlie's review. Next after approval: #14, Get on the Good Foot (James Brown).**

---

## Category Status Summary (current, corrected against the 2026-08-22 sitemap audit)

| Category | Live Posts | State |
|---|---|---|
| Years | 10 | Series complete, no further posts planned |
| Songs | 25 | Slots 1-12 of the artist-linked rotation queue LIVE (Waterloo, How Can You Mend a Broken Heart, Killer Queen, One of These Nights, Let's Stay Together, What's Going On, Hot Stuff, Superstition, Jolene, Bad Bad Leroy Brown, Carole King It's Too Late, Song YMCA). Slot 13 (Georgia on My Mind) Built-Local. Four-post batch (Bridge Over Troubled Water, Stayin Alive, I Will Survive, Seasons in the Sun) published 2026-08-28. Over its 6-post cap since 2026-08-16 by design; still thin relative to the 1,000-record song database |
| Artists | 24 | George Clinton (funk bucket) published 2026-08-27, first Artists post in the funk bucket. Jim Croce published the same day, first post under the folk-rock/singer-songwriter camp. Rick James (funk bucket, second post) published 2026-08-29. Marvin Gaye (soul bucket, first post) published 2026-08-29. Al Green (soul bucket, second post) published 2026-08-30. Donna Summer (disco bucket, second post) published 2026-08-31. Thin relative to the 601-artist JSON pool — real tool dead-end risk (grep "Sitemap-Verified Findings" SESSION-LOG-ARCHIVE.md) |
| Trivia | 4 | No cap (Charlie-confirmed 2026-08-24): 70s Music Trivia, 70s Music Quiz, ABBA vs Queen, Banned Songs of the 70s |
| Genres | 12 | Rotation Queue fully clear; every real, coherent Genres angle surfaced so far has shipped |

Full detail on how each of these numbers was reached, and the 2026-08-22 Sitemap-Verified Findings, is in SESSION-LOG-ARCHIVE.md.
