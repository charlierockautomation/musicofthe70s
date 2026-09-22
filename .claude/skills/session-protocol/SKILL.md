---
name: session-protocol
description: Content tracker ownership rules, the file-size check to run at session start, the session handoff/resume-prompt template, and the new-content-batch checklist. Use at the start of a session, at the end of a session when updating trackers, or when starting a new Artists/Songs/Genres/Trivia batch.
---

# Session Protocol — Full Detail

## Content Tracker Ownership
Claude Code owns writing to content-build.md and CONTENT-INDEX.md. At the end of every session that builds, edits, or audits any content on this site, update both files directly to reflect what happened. Save in place before ending the session. Never wait for Charlie to paste in an externally-edited version of either file.

## File Size Discipline
At session start, run `wc -l CLAUDE.md content-build.md CONTENT-INDEX.md keyword-research-log.md`. Any file at or over 195 lines gets pruned before other work: move its oldest completed entries to the matching archive (SESSION-LOG-ARCHIVE.md / CONTENT-INDEX-ARCHIVE.md / keyword-research-archive.md). Archives are grep-only and never read whole. Full mechanic: file-rotation skill. Also update the linking-and-tools skill's Anchor Text & Position Log (not content-build.md) after placing internal links.

## Session Handoff
At the end of every session, after finishing the work and updating the tracker files, tell Charlie what the next item in content-build.md's Rotation Queue is. Wait for his confirmation before starting it in a new session.

## How to Resume Any Session
Paste this at the start of a new Claude Code session:

```
Read CLAUDE.md, content-build.md, CONTENT-INDEX.md, and keyword-research-log.md in ~/musicofthe70s.net.
Then run: wc -l CLAUDE.md content-build.md CONTENT-INDEX.md keyword-research-log.md  (prune anything >=195 per the file-rotation skill)
Current task: [describe]
Post/page: [name]
Focus keyword: [keyword — verified against real search phrasing]
```

## Read Efficiency on Tracker/Reference Files (multi-slot sessions)
Applies to content-build.md, CONTENT-INDEX.md, anchor-text-position-log.md, and any
other file re-checked once per rotation slot in a multi-item session (Years series
batches, Genre rotation slots, etc.):
1. Use Read's offset/limit for just the section needed for current slot (rotation
   entry, row around a grep hit) — not whole file.
2. Tracker already read once this session, unedited since — don't re-read whole to
   re-check status. Use what's known. Re-read only lines changed after an edit.
3. Grep-friendly lookups (slug, entry, append-after line): grep -n for line number
   first, then Read offset/limit around it. Never read-whole-file-to-find-a-line.
4. Updating: targeted Edit (old_string/new_string), not whole-file rewrite — untouched
   sections never pass through context.
Doesn't change rotation order, tracking logic, or Auto-Go Rule — only read volume per file.

## New Content Batch Checklist
When Charlie greenlights a new batch (Artists, Songs, Genres, or Trivia):
1. Run content-gap analysis per the content-plan skill's standing rules before proposing anything
2. Propose the smallest coherent batch — quality-gated, not volume-gated
3. Get explicit approval before writing (unless Charlie has already specified exact keywords)
4. Build one post at a time, each with its own structure (no-repeated-template rule)
5. Add category/hub cards the same session a post goes Live, not as a follow-up
6. Update content-build.md and CONTENT-INDEX.md the same session
7. Regenerate sitemap.xml
8. Check line counts; prune to archives if any tracker hit 195 (file-rotation skill)
