---
name: session-log
description: Standing lessons learned across past sessions (multi-hit-artist undercounts, split-credit artists, JSON self-contradictions, sandbox video-test limitation, edge-cache settle time, near-limit file sizes). Use before starting a Years/Artists/Songs build to avoid re-making a mistake already caught once, or when something feels like it might have been solved before. Full chronological session history is in references/full-chronological-log.md — open it only when you need to check whether a specific past fix was already made or trace a specific date/topic.
---

# Session Log — Standing Lessons

Check this before assuming a past fix wasn't already made, or before re-deriving a lesson
that's already been learned once. For anything not covered by the standing lessons below,
grep references/full-chronological-log.md for the relevant date or topic rather than
reading it top to bottom.

## Standing Lessons (extracted, quick-reference)
- **Multi-hit-artist undercounts**: task briefs have under-listed multi-hit artists on every
  Years post from 1974 on (gaps of 1–11 artists). Always full-audit the source data directly
  by exact-string grouping, never trust the brief's shorthand list.
- **Split-credit artists** (solo vs. duet credit strings): never silently merge or split —
  state the counting call explicitly in the post body itself, and let exact-string grouping
  govern any "tied artists" list even when a narrative sentence describes the same person's
  output more loosely elsewhere.
- **JSON self-contradictions**: the validated Billboard JSON has, on at least three
  occasions, disagreed with its own embedded `fun_fact` text or been ambiguous about which
  calendar year a chart entry belongs to. When this happens, prefer omitting the disputed
  specific over guessing, and cross-check against `hot100_weekly.json` when available.
- **Sandbox video-playback-test limitation**: confirmed across many sessions with different
  videos — the real embedded-iframe Playwright stress test cannot reach a playable state in
  this environment regardless of video validity. oEmbed channel-identity verification is the
  reliable substitute check. A genuine, explicit geo-restriction or age-restriction error is
  a real blocker, distinct from the sandbox stall, and does require a video swap.
- **Disputed/unverified claims**: check widely repeated quotes/claims against real sources
  before shipping; drop anything denied by the actual source or unverifiable, use only
  independently corroborated facts.
- **Literal keyword phrasing**: when Charlie specifies an exact keyword phrase, use that
  literal phrase (including punctuation/possessive choices) in every scored location, don't
  paraphrase into more natural-sounding text even when the paraphrase captures the same idea.
- **Edge-cache settle**: live-verification after deploy can take 40–60+ seconds across
  multiple fetch attempts before stabilizing; confirm stable across several consecutive
  fetches before reporting done, don't trust the first check.
- **Near-limit file sizes**: check exact byte counts when an image lands near the 200KB
  ceiling — a rounded `du -h` reading can hide going over.
- **Aspect-ratio/sizing bugs are invisible from static CSS** — verify image scaling with
  real rendering (headless Chromium/Playwright), not just reasoning about the stylesheet.
