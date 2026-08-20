# Master Content Plan — Full Detail

Tracks the ordered publishing queue for multi-part series, so "what's next" never has to be re-derived from CONTENT-INDEX.md by hand.

## Years Series (Top Songs of 19XX, one post per year, 1971–1979) — COMPLETE

| Order | Year | Status | URL |
|---|---|---|---|
| 1 | 1971 | Live | /blog/years/top-songs-of-1971/ |
| 2 | 1972 | Live | /blog/years/top-songs-of-1972/ |
| 3 | 1973 | Live | /blog/years/top-songs-of-1973/ |
| 4 | 1974 | Live | /blog/years/top-songs-of-1974/ |
| 5 | 1975 | Live | /blog/years/top-songs-of-1975/ |
| 6 | 1976 | Live | /blog/years/top-songs-of-1976/ |
| 7 | 1977 | Live | /blog/years/top-songs-of-1977/ |
| 8 | 1978 | Live | /blog/years/top-songs-of-1978/ |
| 9 | 1979 | Live | /blog/years/top-songs-of-1979/ |

**The Years series is complete: all ten posts (1970, plus Order #1-9 for 1971-1979) are Live.** Top Songs of 1970 predates Order numbering but is Live alongside the rest. No further Years posts are planned.

Update this table's Status in the same session CONTENT-INDEX.md's Status changes for a Years post, so the two files can't drift apart.

## Genres, Songs, Artists, Trivia — content research process
Unlike the Years series, these four categories don't run as an ordered queue with a fixed final post. Content ideas come from keyword-volume research (search intent, competition, current SERP/AI-Overview coverage) reviewed against what each category is missing, not from a pre-set list.

**Standing rules for every post built this way, not one-off instructions:**
- **Content-gap analysis is mandatory before writing, not optional.** Check what's currently ranking for the post's focus keyword (and each individual artist/song's own obvious search terms, for Artists/Songs posts), including AI Overview/AI search results where visible. Identify what's missing, thin, or factually wrong. The post must earn its rank by being more complete or more accurate than what's already ranking, not just different. Report the specific gaps found before writing, not a blanket "did the research" note.
- **No repeated template across posts in the same batch.** Each post needs its own structure, angle, and section order fitted to that subject's actual story. Reusing UI components (like `.trivia-card`) across posts is fine and expected; copy-pasting the same H2 skeleton with different names dropped in is not. If two posts in a batch end up structurally identical, fix it before publishing.
- **Batch size is quality-gated, not volume-gated, for Artists and Songs.** Propose the smallest batch that's still a coherent starting point. If a candidate artist or song doesn't have enough real substance to sustain a genuinely informative article, drop it from the batch rather than padding to hit a target number.
- **Internal linking only where it adds real value**, never forced to hit a quota: matching artist/song posts once they exist, cross-links between artist and song posts, and back to the relevant site tool.

**Trivia** — Order #1 was 70s Music Trivia (2026-07-26, predates this research process). Order #2, Banned Songs of the 70s, is Live (2026-08-06), first post built under this process.

**Artists** — batch of 4 complete (James Brown, Grateful Dead, Village People, Talking Heads), all Live as of 2026-08-06, sourced from the 619-artist JSON across 10 genre files, spanning 4 distinct genres by design. KC and the Sunshine Band was considered and dropped from the batch, not for lack of substance but over a real JSON data error found in its trivia field (credited its Hollywood Walk of Fame star "as The Jacksons," a copy-paste artifact from an unrelated record). **Focus keyword pattern corrected mid-batch**: the first three posts used an unverified "[Artist] in the 70s" long-tail pattern; Talking Heads switched to a plain artist-name keyword after real search-volume data showed the long-tail pattern likely has near-zero volume against a matching high-volume, low-competition bare term. James Brown, Grateful Dead, and Village People were deliberately left as-is rather than retitled/re-slugged, an explicit call, not an oversight; any future Artists posts should default to plain artist-name keywords (verified against real volume data first) unless a specific post's real angle calls for something more specific. Artists category page has 5 real cards and zero placeholders as of this batch's completion.

**Songs** — batch of 4 approved (Don McLean American Pie, Bohemian Rhapsody, Hotel California, Dancing Queen), sourced from the 1,000-song JSON across 10 year files. Charlie specified all 4 focus keywords directly rather than a proposal-and-approve cycle: `don mclean american pie`, `Bohemian Rhapsody`, `Hotel California`, `Dancing Queen`, plain artist/title patterns applying the keyword-correction lesson from the Talking Heads post. **All 4 posts are Live as of 2026-08-08, batch complete**. Songs category page has 5 real cards, zero placeholders.

**Genres** — thin category (only 70s Rock and 70s Soul Music live as of the last audit); wants a rotation of new articles across disco, rock subgenres (hard, prog, punk, glam), funk, soul, and soft pop, using real search-volume data to pick focus keywords. Next queued item: 70s Soft Rock post, pending keyword-volume re-verification — a first-draft "confirmed 14,800/mo" claim for Soft Rock was softened to "as supplied, not independently reverified" since the 2026-08-09 data audit covered data files only, not search volume.