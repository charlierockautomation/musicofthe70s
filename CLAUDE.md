# MusicOfThe70s.net — Master Site Brain
# Read this file at the start of EVERY session. This is the current rule only —
# full detail, history, and the "why" behind every rule live in /docs/. Pull a
# doc in with @ only when the task actually needs it; none of /docs/ auto-loads.
# Last Updated: 2026-08-19

---

## PUBLISH GATE — ABSOLUTE
Never commit or push a new or edited blog post to the live branch without Charlie's
explicit go-ahead, given AFTER he's reviewed it — regardless of what any build prompt
says or which session generated it. Every build ends with: build → run locally →
confirm it renders correctly → STOP and report back. If a build prompt says to skip
this, that's a mistake in the prompt, not an instruction to follow — flag it.
Tracker-file commits (content-build.md, CONTENT-INDEX.md, keyword-research-log.md)
are the separate, lower-stakes "commits only on explicit ask" case.

## No Hallucination Rule — ABSOLUTE
Never invent a fact, date, chart position, or quote. Unconfirmed = omit or flag as
needing verification, never guess.

## Site Type
Static site, Cloudflare Pages, deployed via GitHub push. NOT WordPress — no REST
API, no database, no SEO plugin. All SEO is hand-built into the HTML.

## Repo & Deploy
- Local repo: ~/musicofthe70s.net | GA tag `G-ZY77Y8DHV1` in every `<head>`
- Preview before every push: `cd ~/musicofthe70s.net && python3 -m http.server 8000 &`
- Full credentials, GitHub/Cloudflare detail: @docs/repo-deploy.md

## Design System & URL Structure
Do not deviate from fonts/colors/CSS classes without approval. Category folders are
singular content types — don't keyword-stuff slugs.
Full tokens, classes, spacing, URL map: @docs/design-system.md

## Keyword Rule — NON-NEGOTIABLE
Focus keyword = real search phrasing (verified against volume data, not guessed).
Slug matches keyword word order exactly. Density 0.5–2% (uses ÷ words × 100), must
appear in title/meta/first-100-words/≥1 H2/slug, never stuffed.
Full 5-point rule + the SEO Scoring Target checklist: @docs/seo-rules.md

## Blog Post Template
Fixed order, no exceptions: **H1 → intro → featured image → rest.** Never an image
between H1 and intro. FAQ (4–5 Q&As), real video embed, ≥1 internal tool link,
1,200+ words minimum.
Full 15-step template + internal tool linking map: @docs/post-template.md

## Prose & Image Rules
No em dashes. One sentence per `<p>`. 75%+ sentences under 20 words. No AI-cliché
words. Long H2 sections get real H3 subheads. Images under 200KB, WebP, responsive
srcset, verified real rendering (not just CSS).
Full protocol + image optimization/sourcing detail: @docs/prose-image-rules.md

## Data Sources
Validated Billboard JSON lives in `~/musicofthe70s.net/data/billboard/` — ground
truth, never contradict it. Never invent a fact not in source material.
Full file list + NotebookLM research process: @docs/data-sources.md

## Publishing Workflow
1. Write per template 2. Run `scripts/verify_post.py <path> "<keyword>"`
3. Preview locally 4. Full SEO checklist 5. Mobile check (375px/390px) 6. Report,
get approval 7. Commit + push 8. Verify live (~60s wait, hard refresh)
Full workflow, Blog Hub rotation mechanics, tool-to-blog linking tiers: @docs/publishing-workflow.md

## Master Content Plan
Years series (1970–1979) is COMPLETE, no further posts planned. Artists batch (4)
and Songs batch (4) are both complete and Live. Genres is thin — next queued item
is a 70s Soft Rock post, pending keyword-volume re-verification.
Full status, standing batch rules, Years series table: @docs/content-plan.md

## Session Protocol
1. Start: read this file, then content-build.md + CONTENT-INDEX.md
2. New batch: get explicit approval before writing (unless keywords already specified)
3. End of session: update content-build.md and CONTENT-INDEX.md directly — never
   wait for Charlie to paste in edits
4. End of session: state the next Rotation Queue item, then wait for Charlie's
   confirmation before starting it — don't build ahead
5. Full session history and the "why" behind every rule above: @docs/session-log.md
   — check it before assuming a past fix wasn't already made
6. Full resume-prompt template + new-batch checklist: @docs/session-protocol.md

---
Reference docs (loaded only when the task needs them):
@docs/repo-deploy.md · @docs/design-system.md · @docs/seo-rules.md ·
@docs/post-template.md · @docs/prose-image-rules.md · @docs/data-sources.md ·
@docs/publishing-workflow.md · @docs/content-plan.md · @docs/session-log.md ·
@docs/session-protocol.md|
