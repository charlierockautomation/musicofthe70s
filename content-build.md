# CONTENT-BUILD.md — musicofthe70s.net Master Content & Linking Tracker
# CLAUDE / CLAUDE CODE: Read this alongside CLAUDE.md and CONTENT-INDEX.md before planning any session.
# Full history (every completed/decided-against slot, every past session's full build write-up) lives in SESSION-LOG-ARCHIVE.md. Don't open it in full — grep it for a specific term when you need one (e.g. `grep -i "iggy pop" SESSION-LOG-ARCHIVE.md`). Append new entries there directly at session end; don't grow this file with them.
# Current status: We Will Rock You (Songs) is LIVE (2026-08-23, pushed and confirmed on the real site). Rock Trivia Game (new 7th Tool, not a Trivia-category post) is BUILT and locally previewed 2026-08-23, awaiting Charlie's go-ahead per the Publish Gate before commit/push. Everything else completed to date is in the archive.

## How This File Works

1. Before writing anything new, check CONTENT-INDEX.md for what's already live — never duplicate.
2. Pick the next item from the Rotation Queue below. If a category has no ready item, skip to the next rather than forcing it.
3. Every new post links to at least one Tool (see Tools as Pillars).
4. Every new post checks the Internal Linking Strategy's "link owed" table for a cross-category opportunity.
5. Update this file's Session Log every session, per the Content Tracker Ownership rule in CLAUDE.md.

---

## Path Forward — Pillars, Rotation, and Linking (added 2026-08-22)

**Pillars.** The site's two permanent pillar types are the homepage and the six interactive tools (see Tools as Pillars below). Every new post links to whichever pillar its content actually supports — not the homepage by default, and not a mismatched tool for the sake of having a tool link.

**Active rotation set.** Genres, Songs, Artists, Trivia. Years is a closed, complete 1970-1979 series (no cap, no further posts planned) and sits outside active rotation unless a genuinely new Years angle comes up. Rotate across the four active categories rather than clearing one before starting the next; if a category has no keyword-checked, non-overlapping angle ready, skip it for that turn instead of forcing a thin post (already the rule in item 2 above — restated here as it applies specifically to rotation planning).

**Before starting any new post:**
1. Check CONTENT-INDEX.md — never duplicate a live or planned post.
2. Cross-check the live sitemap, https://musicofthe70s.net/sitemap.xml, as the source of truth for what's actually published. CONTENT-INDEX.md can drift from the live site (the 2026-08-14 Funk entry is a real example — see Session Log).
3. Check the category's live post count against its cap (Genres 6, Artists 6, Songs 6, Trivia 4) so the new post's place in that category's rotation is clear before writing.

**Every post's linking checklist:**
1. Link up to its own category hub page.
2. Link to at least one relevant Tool (a pillar).
3. Check the Internal Linking Strategy's "link owed" table for a cross-category link to close, and close it in both directions the same session.
4. Never repeat the same internal link target twice within one post (standing rule).

**Database growth.** Every new post's angle comes from a real, verified content-gap check — live SERP plus this site's own JSON data — not a generic keyword-driven post. This is the actual mechanism that has kept every post on the site distinct (30+ distinct structures logged in the Session Log below) while still growing the database on a steady rotation, and it's what keeps the site clear of Google's scaled-content-abuse risk (see the standing guardrail in profile/topic notes). Don't relax this check for the sake of rotation speed.

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

## Sitemap-Verified Findings (NotebookLM audit, sitemap.xml added 2026-08-22)

**Source of this section:** a full crawl of the real sitemap.xml against content-build.md and the artist/song JSON, done in NotebookLM. Treat everything below as verified unless marked otherwise — this replaces the earlier "UNKNOWN" placeholders for tool URLs and a couple of assumed slugs.

**Confirmed inventory:** 67 live URLs total. Slugs for two posts match what this file already had on file, now confirmed against the live site rather than assumed: Queen is at `/blog/artists/queen-freddie-mercury/`, Eagles at `/blog/artists/eagles-the-band/`. Bee Gees (`/blog/artists/bee-gees/`) and Banned Songs of the 70s (`/blog/trivia/banned-songs-of-the-70s/`) are confirmed live — both had already rotated off their category's front-grid card but are not missing content, just archived, consistent with the rotation-cap design.

**Real structural skew, worth a decision before the next batch:**
- **ABBA density**: 9 of 67 URLs (13.4% of the entire site) are ABBA-related (5 Artists, 3 Songs, 1 Trivia). Not a defect — it followed a real, explicitly-approved batch assignment — but worth knowing before adding a 10th.
- **Songs is thin**: only 8 posts total, 3 of them ABBA and 2 Eagles. No dedicated Songs post exists yet for most major non-ABBA/Eagles/Queen acts.
- **Artists is thin relative to the database**: 13 live Artists posts against 601 unique artists in the JSON data. Combined with the point below, this is a real (not cosmetic) UX gap.
- **Tool dead-end risk, newly identified, not previously tracked in this file**: Random Artist Picker and Mood Song Matcher both draw from the full 601-artist pool, but only 13 of those artists have a live profile to land on — most tool interactions currently have no matching post to route to. Same shape of problem, smaller scale, for Birthday #1 Song Finder against only 8 live Songs posts. This is a real internal-linking gap, not just a content-count one, and is now the strongest concrete argument for the next several Artists/Songs picks: closing it directly improves what the tools (the pillars) actually do.
- **Rock genre-page overlap flagged, not yet acted on**: `/blog/genres/70s-rock/` (the general overview) sits alongside 6 already-live subgenre pages (hard rock, soft rock, prog rock, punk rock, folk rock, country rock) that cover much of the same ground in more depth. NotebookLM's recommendation — turn the general 70s Rock page into a navigational hub linking out to the subgenre pages rather than trying to compete with them on the same keywords — is a real, reasonable fix, but is a structural edit to an existing live post, not a new-post decision; flagging here for Charlie's call rather than queuing it as a Rotation Queue item.
- **Trivia UX overlap flagged, not yet acted on**: the static 64-question `70s-music-trivia` post and the scored 50-question `70s-music-quiz` post cover close to the same ground. NotebookLM's suggestion (reposition the static post as a scannable "study guide" with a CTA into the scored quiz) is reasonable but, again, an edit to existing live content — Charlie's call, not an automatic action item.

**Real, verified content gaps** (major 1970s figures with zero Artist or Song page on the site): Stevie Wonder, Marvin Gaye, Al Green, Donna Summer, Led Zeppelin, Pink Floyd, Yes, Genesis, Dolly Parton, Willie Nelson, Carole King, Jim Croce. These are genuine gaps confirmed against the live sitemap, not assumptions — good candidates for the next few Rotation Queue slots, each still needing its own real keyword check and content-gap pass before writing (same standing process as every prior post).

**Five article opportunities recommended off this audit** (ranked, full detail in session notes): (1) Brian May and Queen — a craft/technique post (Red Special origin, multi-tracked "orchestral" guitar work, `110,000/mo` on `brian may and queen`) — LIVE; (2) We Will Rock You (Songs, `201,000/mo` cluster, also closes some of the thin-Songs gap) — LIVE; (3) George Clinton (Artists, Funk); (4) Rick James in the 70s (Artists, Funk); (5) an all-rock Trivia post built from the existing quiz-question pool — **built 2026-08-23 as a new interactive Tool instead of a Trivia-category blog post** (Trivia was at its 4-post cap; see Rock Trivia Game entry below), using the classic-rock/hard-rock/prog-rock/punk-new-wave artist JSON rather than the smaller 50-question quiz pool.

**Rotation Queue slot 1 (Artists) — GREENLIT 2026-08-22 under the Auto-Go Rule above**: Brian May and Queen. Focus keyword `brian may and queen` (110,000/mo) — confirmed never used as a focus keyword on this site before. Angle (Red Special origin story, sixpence-coin pick technique, multi-tracked "orchestral" guitar arrangements, the "No Synthesizers!" liner-note era) confirmed structurally distinct from the live Queen post's own material (which covers the Dec 1976 Grundy/Sex Pistols incident and the Bohemian Rhapsody video shoot, not guitar craft or recording technique). Both Auto-Go conditions independently met — Charlie confirmed proceeding no-questions-asked; Claude Code owns the build end to end per the 2026-08-19 workflow update. Task brief handed off same session — see the prompt below.

---

## Tools as Pillars (real data, confirmed via repo audit 2026-08-09)

| Tool | Real Data Source | Confirmed Facts |
|---|---|---|
| Random 70s Song Generator | data/songs/hot_100_songs_1970-1979.json | 1,000 records but filtered to billboard_peak <= 40 for display, real live pool is 400 songs. Own genre/mood/vibe schema per song, separate from the artist-level genre field. |
| Birthday #1 Song Finder | data/billboard/hot100_weekly.json | 522 weekly #1 records, full 1970-1979 coverage. Same file already used for Years-post research. |
| Mood Song Matcher | data/artists/*.json (same as Artist Picker) | Matches ARTISTS by mood/vibe/era tags, not genre. Tags: mood (happy 331, nostalgic 296, pumped-up 233, romantic 231, rebellious 207, melancholy 202), vibe (reflect 298, chill 272, party 250, drive 234, dance 221, rock-out 188), era (late-70s 541, mid-70s 517, early-70s 415). Does NOT map to Genres content — use the genre field instead. |
| Random Artist Picker | data/artists/*.json (10 files) | 619 total records, but 601 unique artists — 18 artist IDs appear in two genre files each (e.g. Elton John in both pop-crossover and soft-rock, Mott the Hoople in both classic-rock and hard-rock; full list in Session Log). Real genre buckets: country 100, soft-rock 69, hard-rock 68, classic-rock 66, soul 66, disco 65, funk 50, pop-crossover 50, prog-rock 50, punk 35 (contaminated with 12 new-wave-subgenre artists). No dedicated Glam bucket — glam artists exist only as subgenre text inside hard-rock (10: Angel, Dokken, Gary Glitter, Ian Hunter, Mott the Hoople, New York Dolls, Slade, Suzi Quatro, T. Rex, The Sweet) and pop-crossover (7: Bowie, Elton John, David Essex, Mud, Pilot, The Rubettes, Wizzard) — 17 unique glam-tagged artists total. **Correction, 2026-08-09**: the "country 100" bucket is the whole `genre: "country"` field, not the same thing as "country rock" — only 8 of those 100 are actually subgenre-tagged `country-rock`; the real country-rock roster is 14 unique artists spread across three files (8 country, 6 classic-rock, 2 soft-rock, minus 1 cross-file duplicate). Same class of gap as Glam and Punk: don't trust a genre-bucket count for a subgenre-specific post without checking the actual `subgenre` field first. |
| 70s Music Trivia Quiz | js/quiz-questions.js | 50 questions. Unused by either of the first two live Trivia posts; now the full data source for the built-but-not-yet-live "70s Music Quiz" post (all 50, scored), and also powers this tool page's own quick 10-question random rounds. |
| 70s Decade Wheel | data/billboard/year_end_hot100.json | Same file as the Years blog posts. No distinct dataset. |
| Rock Trivia Game (new, built 2026-08-23) | data/artists/artists_classic_rock.json, _hard_rock, _prog_rock, _punk_new_wave.json (219 artists) | Real 7th tool, at `/pages/rock-trivia-game.html`, keyword `rock trivia game` (given directly by Charlie). `scripts/generate_rock_trivia_data.py` generates `js/rock-trivia-data.js` (1,384 questions: classic-rock 424, hard-rock 426, prog-rock 322, punk-new-wave 212) entirely from structured fields (album title/year, song title, formed year, origin) — no free-text parsing, no invented facts. Category select (4 genres + All Rock) plus a date-seeded Daily Challenge (same 10 questions site-wide per calendar day, blocks replay same day, drives the return-visit hook) with a localStorage streak counter and personal-best score. Built as a Tool rather than a Trivia post because Trivia was at its 4-post cap; content-gap check (WebSearch) found existing "rock trivia game" results are generic decade-spanning quiz sites/apps (Sporcle, FunTrivia, mobile apps), none built on this site's own verified 70s-specific data or offering a daily-streak mechanic. Rerun the generator script after any edit to the four source JSON files. Full build/test detail in the Session Log., not urgent but worth knowing:** only 243 of 570 distinct artistIds referenced in the song data actually resolve to a real artist record — most song-to-artist links are currently broken. Not blocking content work, but would block any future feature that tries to join songs and artists programmatically.

---

## Internal Linking Strategy

Every post links up to its category page and to at least one relevant Tool. Cross-category links matter as much as same-category "Related Posts" — right now every Related Posts block on the site only links within its own category, which pools link equity instead of letting it flow site-wide.

**Link owed** (cross-category links that should exist once their target is built):

| Existing Post | Owes a link to | Category |
|---|---|---|
*(Table empty as of 2026-08-16 — the last open row, Bohemian Rhapsody -> Glam or Prog Rock, was closed by the new 70s Progressive Rock post; link added and confirmed both directions.)*

---

## Category Rotation Queue (current/open items only)

Full history of everything already built or decided against lives in SESSION-LOG-ARCHIVE.md's "Completed & Decided-Against Rotation Queue History" section — this table only tracks what's actually open right now.

| Category | Content | Status |
|---|---|---|
| Songs | We Will Rock You | **LIVE 2026-08-23** — https://musicofthe70s.net/blog/songs/we-will-rock-you/. Focus keyword `We Will Rock You`, given directly by Charlie ("the best post for this keyword on the internet"); confirmed never used as a focus keyword on this site before. Angle: the song's stomp-clap origin, not guitar or incident history, so it stays distinct from the live Freddie Mercury post (Grundy incident, Bohemian Rhapsody video shoot) and the live Brian May and Queen post (Red Special, sixpence pick, multi-tracked guitar). Structure: the real Bingley Hall crowd moment that inspired Brian May (Wikipedia-verified, A Day at the Races Tour, early 1977) leads into the actual Wessex Sound Studios recording session (real personnel: Mercury/May/Deacon stomping and clapping, Taylor on backing vocals and percussion, session musicians Elizabeth Edwards and Andrew Turner), then the prime-number-delay physics trick May used to fake a stadium crowd, then why the track deliberately has almost no guitar or drum kit, closing on the double A-side's real chart run (Hot 100 debut #87, peak #4, Billboard year-end #25 pulled directly from `data/billboard/year_end_hot100.json`, Grammy Hall of Fame 2009, Rolling Stone #330). Caught and corrected a real JSON self-contradiction before writing: the song JSON's `billboard_peak: 25` field is actually the year-end chart rank, not the true weekly Hot 100 peak; the real #4 peak came from independent verification (Billboard.com retrospective), matching the JSON's own `fun_fact` text, so both numbers were used correctly rather than trusting the mislabeled field. `verify_post.py` needed two iterations: a keyword-in-consecutive-sentences fail at two separate `<p>`-tag-adjacency boundaries (an FAQ answer's own two sentences, and a body H2-to-H2 section boundary), fixed by rewording one sentence at each spot. Passed clean after that (1,477 words, density 1.490%). **Real process gap found and fixed mid-session**: the post shipped its first review with all four H2 sections as long unbroken runs of one-sentence `<p>` tags and zero H3 subheads, a direct repeat of the exact defect the Subheading Rule was created to prevent (see 2026-08-16 in session-log.md) despite the rule already being written down. Charlie caught it, not the process. Fixed by adding real H3 subheads (2 per H2, each naming its actual content) to this post, and, more importantly, added a mechanical check to `scripts/verify_post.py` itself: flags any H2 body section with more than 10 consecutive one-sentence `<p>` tags before a subhead, threshold calibrated against three already-compliant live posts (70s Funk, Folk Rock, Progressive Rock all cap at exactly 10). This is now a standing, automated part of every future `verify_post.py` run, not a rule that depends on being remembered. Mobile check (375px/390px) passed via real Playwright rendering both before and after the H3 fix, no horizontal overflow, TOC/FAQ/related-posts all stack correctly, nav collapses to hamburger. Video: official Queen channel "We Will Rock You (Official Video)", oEmbed-verified. Image: Freddie Mercury performing live in New Haven, CT, November 1977 (Carl Lender, CC BY-SA 3.0, via Wikimedia Commons), cropped to site's 43:24 ratio, 156KB jpg / 109KB webp. Category/hub cards and sitemap regenerated; Bohemian Rhapsody rotated off the Songs front grid into archive as a result (still Live at its own URL, cap is 6, this is expected rotation behavior, not a removal). **9th Songs post**, over the 6-post cap by design per Charlie's direct go-ahead. |
| Artists (candidate, not yet slotted) | Marvin Gaye, Al Green, Donna Summer, Led Zeppelin, Pink Floyd, Yes, Genesis, Dolly Parton, Willie Nelson, Carole King, Jim Croce | Confirmed zero-coverage gaps via the 2026-08-22 sitemap audit (see below) — real candidates, each still needs its own keyword check + content-gap pass before queuing, same as every prior post. |
| Artists (candidate, not yet slotted) | George Clinton, Rick James in the 70s | Funk-category candidates from the 2026-08-22 audit; each needs its own keyword check + overlap check before queuing. |
| Rock genre-page overlap | `/blog/genres/70s-rock/` vs. its 6 subgenre pages | Flagged, not queued — a structural edit to an existing live post (NotebookLM's suggestion: turn it into a nav hub), Charlie's call, not an automatic action item. |
| Trivia UX overlap | Static 64-question post vs. scored 50-question quiz | Flagged, not queued — same as above, an edit to existing live content, Charlie's call. |

Years series is complete (10/10, 1970-1979, all Live) — no Years slots, none planned.

---

## Category Status Summary (current, corrected against the 2026-08-22 sitemap audit)

| Category | Live Posts | State |
|---|---|---|
| Years | 10 | Series complete, no further posts planned |
| Songs | 9 | We Will Rock You published 2026-08-23. Over its 6-post cap since 2026-08-16; thin relative to the artist database — see candidates above |
| Artists | 15 | Stevie Wonder published 2026-08-23. Thin relative to the 601-artist JSON pool — real tool dead-end risk, see Sitemap-Verified Findings above |
| Trivia | 4 | At cap (70s Music Trivia, 70s Music Quiz, ABBA vs Queen, Banned Songs of the 70s) |
| Genres | 12 | Rotation Queue fully clear; every real, coherent Genres angle surfaced so far has shipped |

Full detail on how each of these numbers was reached is in SESSION-LOG-ARCHIVE.md.
