# MusicOfThe70s.net — Master Site Brain
# Read this file at the start of EVERY session. This is universal, always-needed
# content only. Task-specific reference material (SEO rules, post template, prose
# rules, design system, linking rules, publishing workflow, data sources, session
# history) lives in .claude/skills/ and loads automatically when a task matches.
# Last Updated: 2026-09-20

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

## YouTube Compliance — ABSOLUTE (full detail: youtube-compliance skill)
- Every YouTube embed is visible, unobscured, at least 200x200 (aim 480x270), never a
  hidden or background audio player. Nothing may overlay it.
- Playback starts only from a user action. Auto-advance only while the player is on screen.
- Every YouTube ID has embeddable + madeForKids status on record no more than 30 days old:
  `python3 scripts/youtube_status.py --report` must pass before any push.
- Before AdSense is applied for: every player page has substantial non-YouTube content, no ad
  sits on or overlaps a player (check anchor/vignette auto-ad formats), and the Privacy Policy
  is first updated to disclose third-party ads and cookies.
- API key: env var only, from the site's own Google Cloud project. Never print, write or commit it.

## Site Type
Static site, Cloudflare Pages, deployed via GitHub push. NOT WordPress — no REST
API, no database, no SEO plugin. All SEO is hand-built into the HTML.

## Repo & Deploy
- Local repo: ~/musicofthe70s.net | GA tag `G-ZY77Y8DHV1` in every `<head>`
- Deploy: git push → GitHub (charlierockautomation) → Cloudflare Pages auto-deploys (~60s)
- Preview before every push: `cd ~/musicofthe70s.net && python3 -m http.server 8000 &`
- Full credentials, GitHub/Cloudflare detail: repo-deploy skill

## File Size Rule — keeps session token burn down
Every file a session loads at start (this file, content-build.md, CONTENT-INDEX.md,
keyword-research-log.md) stays at or under 195 lines. Never let one cross 195. At
session start run `wc -l CLAUDE.md content-build.md CONTENT-INDEX.md keyword-research-log.md`
and prune anything over. When one nears it, prune the oldest completed entries out to
that file's archive (SESSION-LOG-ARCHIVE.md, CONTENT-INDEX-ARCHIVE.md,
keyword-research-archive.md) so the living file stays lean. Archives are grep-only,
never read whole, and are exempt from the line cap.
Full mechanic: file-rotation skill. Tracker ownership, session handoff, and the
resume-prompt template: session-protocol skill.

## Auto-Go Rule
Defined in content-build.md: if a focus keyword has never been used as another live
post's focus keyword on this site, AND the angle is confirmed structurally distinct
from every existing post touching the same subject, that post is a go, no separate
approval checkpoint needed before building. This does not remove the content-gap
check or the PUBLISH GATE above, it only removes the extra "confirm before starting"
step once both conditions are independently verified true.

## Session Discipline

1. ONE TASK PER SESSION. Build or edit one piece of content per session.
   When done, report what was built and STOP — do not propose, queue, or
   hold open "what's next" as an ongoing thread. Charlie starts a new
   session (or runs /clear) himself when ready for the next task.

2. DO NOT ask Charlie to pick the next item when content-build.md or
   CONTENT-INDEX.md already states a clear next-in-line item or rotation
   order. Follow it automatically. Only ask when there's a genuine
   ambiguity requiring Charlie's judgment (conflicting keyword data, a
   content-gap question the Auto-Go Rule doesn't resolve, a real tradeoff)
   — not a routine "which post next."

3. NO NARRATION FLOURISHES. Skip session-timer callouts, restated recap
   paragraphs, or personality flourishes in the final report unless Charlie
   explicitly asks for a summary. End with a plain, closed statement of
   what was done.

4. END STATE = DONE, NOT PENDING. The last message of a session should read
   as a completed status report, not an open question or a menu of options.

This does not change the PUBLISH GATE rule — a completed build session
still stops and waits for Charlie's explicit go-ahead before anything goes
live. "One task per session" and "don't hold open a queue" are about not
padding the conversation with extra rounds, not about skipping the
required human review checkpoint.
