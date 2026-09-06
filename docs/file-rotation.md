# File Rotation & Size Discipline — Full Detail

Why this exists: every file a session loads at start burns input tokens on every
turn for the whole session. Left unmanaged, the trackers grow without limit and
each session gets slower and more expensive for the same work. This is the rule
that keeps that from happening.

## Two tiers of file

### Tier 1 — loaded every session (HARD CAP 195 lines)
- `CLAUDE.md`
- `content-build.md`
- `CONTENT-INDEX.md`
- `keyword-research-log.md`
- any `docs/*.md` spoke a task actually opens

Rule: never let one cross 195 lines (safety line; the real ceiling is 199, 195
gives margin). Check at session start:
```
wc -l CLAUDE.md content-build.md CONTENT-INDEX.md keyword-research-log.md
```
Anything at or over 195 gets pruned before any other work, and the prune is
reported in the session handoff.

How to prune (do NOT rotate Tier 1 into numbered files — keep one living file):
- Move the OLDEST completed / historical entries out to the matching archive.
- "Completed" = a post that is Live, a rotation-queue slot that shipped, a keyword
  pull whose post is Live, a point-in-time audit whose numbers are now stale.
- Keep only current state, open items, and standing rules in the living file.

### Tier 2 — archives (grep-only, NOT loaded whole, exempt from the line cap)
- `SESSION-LOG-ARCHIVE.md`   <- prune target for content-build.md
- `CONTENT-INDEX-ARCHIVE.md` <- prune target for CONTENT-INDEX.md
- `keyword-research-archive.md` <- prune target for keyword-research-log.md

Rules for archives:
- Never open one in full. Grep for the term you need:
  `grep -i "iggy pop" SESSION-LOG-ARCHIVE.md`
- Append new entries directly to the bottom with a heredoc — don't read the file
  first.
- Line count does not matter here (grep returns only matching lines). Size is
  capped instead: when an archive passes ~300KB, start a numbered continuation
  (`SESSION-LOG-ARCHIVE-2.md`, etc.), add a one-line pointer to it at the top of
  the part-1 file, and append to the highest-numbered part from then on. Grep all
  parts at once with a glob: `grep -i "term" SESSION-LOG-ARCHIVE*.md`.

## Living-file → archive map

| Living file (Tier 1)   | Prune to (Tier 2)          | What moves |
|---|---|---|
| content-build.md       | SESSION-LOG-ARCHIVE.md     | shipped rotation-queue rows, full build write-ups, stale audits |
| CONTENT-INDEX.md       | CONTENT-INDEX-ARCHIVE.md   | full per-post research/build notes (the lean lookup row stays) |
| keyword-research-log.md| keyword-research-archive.md| pulls whose focus keyword is now on a Live post |

`docs/linking-and-tools.md` holds the Tools-as-Pillars table, the Internal Linking
Strategy, and the Anchor Text & Position Log — pulled out of content-build.md
because they are only needed during the internal-linking step of a build, not
every session. Load it then, not at session start. The Anchor Text & Position Log
grows one row per internal link; when that file nears 195 lines, prune its oldest
rows to CONTENT-INDEX-ARCHIVE.md the same way.

## Current line counts (update when you prune)

Last checked 2026-09-02, right after the big prune:
- CLAUDE.md: 100
- content-build.md: (target < 180)
- CONTENT-INDEX.md: (target < 160)
- keyword-research-log.md: (target < 150)
- docs/linking-and-tools.md: (target < 180)
- every other docs/*.md: under 80, no action

## History

2026-09-02: this rule and doc created. Found that CLAUDE.md's `@docs/*.md`
references were auto-importing all 10 spokes (~14k tokens) into every session
despite the file claiming "none of /docs/ auto-loads" — the `@` prefix was the
import trigger. Stripped every `@` to a plain path. Slimmed content-build.md
(250 lines), keyword-research-log.md (372), and CONTENT-INDEX.md (181, with a
duplicated Blog Posts block) back under cap; moved the shipped write-ups and
completed queue rows to the archives; split the linking/tools material into
docs/linking-and-tools.md. Session-start load dropped from roughly 52k tokens to
roughly 9k.
