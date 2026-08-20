# Data Sources — Full Detail

- Billboard databases: `~/musicofthe70s.net/data/billboard/`
  - `year_end_hot100.json` (1000 records, 1970–1979)
  - `hot100_weekly.json` (522 records)
  - `country.json` (523 records)
  - `rnb.json` (522 records)
  - All validated — treat as ground truth, never contradict this data in post content.
- Research briefs: NotebookLM notebooks (20+ artist/genre notebooks, Billboard year-end notebooks per year, "Music of the 70s — Overview" notebook with genre Wikipedia sources)
- Research brief pull prompt (use in any NotebookLM notebook when gathering material for a new post):
  > "Extract everything you can find in these sources that would help write a blog post. Give me: 5–8 genuinely interesting facts (specific dates, numbers, firsts, surprises), key names/songs/albums with context, any direct quotes worth referencing with source noted, and a rough narrative arc if there is one. Plain list, no fluff."
- Never invent a fact, date, chart position, or quote that isn't in the source material or validated database. When in doubt, mark it as needing verification rather than guessing.

## Additional data audit findings (2026-08-09, read-only)
Corrected earlier assumptions: 619 artists (not 605) across 10 real genre buckets — country 100, soft-rock 69, hard-rock 68, classic-rock 66, soul 66, disco 65, funk 50, pop-crossover 50, prog-rock 50, punk 35. Country is the largest bucket and wasn't in the original plan. Glam has no dedicated bucket, only scattered subgenre text. Only 243 of 570 song-to-artist ID links resolve — known, non-blocking data-quality gap. Mood Song Matcher matches artists by mood/vibe/era tags (not genre) and shares its data file with Random Artist Picker. Birthday #1 Finder and Decade Wheel both reuse files already documented above. Random Song Generator's real live pool is 400 songs (billboard_peak <= 40 filter on the 1,000-record file), separate from the artist-level data. Trivia's real untapped material is the 50-question `js/quiz-questions.js` pool, unused by either live Trivia post.