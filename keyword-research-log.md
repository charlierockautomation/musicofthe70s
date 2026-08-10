# KEYWORD-RESEARCH-LOG.md — musicofthe70s.net Raw Keyword Data
# Site-wide raw keyword-volume pulls (WordStream or equivalent), reusable across future posts.
# Separate from content-build.md: that file tracks planning/rotation decisions, this file is
# the raw data those decisions get made from. A term can sit here unused for a long time before
# it becomes a Rotation Queue slot — that's expected, not stale.
# Last Updated: 2026-08-09

---

## How This File Works

1. When Charlie supplies a real keyword-volume pull (WordStream or similar), log it here in full before it's used for any single post — don't let a pull exist only in chat history.
2. Split every pull into **Real** (genuinely about the site's subject matter) vs **Noise** (same term, different subject, contaminating the data) before drawing any conclusion from it.
3. Mark a term's status once a decision is made: `confirmed focus keyword` (in use on a specific Live or in-progress post), `future post candidate` (real volume, no post built yet), or `excluded — contamination` (real volume, but for an unrelated subject, not usable for this site).
4. content-build.md's Rotation Queue should link back here when a slot's keyword was pulled from a logged entry, instead of re-describing the number inline.

---

## Queen (band) — pull for Rotation Queue slot 2, 2026-08-09

Source: WordStream, supplied by Charlie, 2026-08-09. Pulled against the search term "Queen band" to get past the bare "Queen" monarchy-collision problem flagged during this session's keyword check (Wikipedia/SERP results for bare "queen" skew toward Queen Victoria/Elizabeth before the band appears).

### Real (genuinely about the band)

| Term | Volume/mo | Status |
|---|---|---|
| queen freddie mercury | 673,000 | **Confirmed focus keyword** — used on the Queen Artists post, 2026-08-09 |
| we will rock you | 201,000 (cluster) | Future post candidate — likely its own Songs post given the volume, not yet scoped |
| brian may and queen | 110,000 | Future post candidate — possible angle for a future Queen-adjacent post (guitar/gear angle, or a Brian May-focused piece) |

### Noise (real volume, wrong subject — excluded)

| Term | Note |
|---|---|
| queen of the stone age | Queens of the Stone Age, a different band entirely. Excluded, not a Queen (1970s) target. |
| mississippi queen | Mountain's 1970 song "Mississippi Queen," unrelated to the band Queen. Excluded. |

---

## 70s Country Rock — pull for Rotation Queue slot, 2026-08-09

Source: supplied by Charlie, 2026-08-09.

### Real (genuinely about the genre)

| Term | Volume/mo | Status |
|---|---|---|
| 70's country rock | 210 | Tied with the row below, low competition |
| country rock 70s | 210 | Tied with the row above, low competition |
| 70s country rock | — | **Confirmed focus keyword** — clean word order and no apostrophe, matches the site's URL-slug convention exactly; used on the Country Rock Genres post, 2026-08-09 |

No noise/contamination terms supplied in this pull.

---

## Disco Music of the 70s — pull for Rotation Queue slot, 2026-08-10

Source: WordStream, supplied by Charlie, 2026-08-10.

### Real (genuinely about the genre)

| Term | Volume/mo | Status |
|---|---|---|
| Disco Music of the 70s | 12,100 | **Confirmed focus keyword** — used on the Disco Genres post, 2026-08-10 |
| 70s disco | 9,900 | Secondary/alternate keyword for the same article, not the primary target |
| funk 70's | 6,600 | Flagged as likely confirmation for the already-planned Funk Genres slot; check against that slot's actual keyword assumption before the post gets built, since no keyword was confirmed for it yet as of this pull |
| disco mix 70's & 80's | 5,400 (Unspecified competition) | Distinct future content type, a mix/playlist framing rather than a genre article; not used on this post |
| dance music (cluster) | 4,400 (several tied variants) | Possible future post or secondary angle; too broad and undifferentiated to commit to a single post yet |

No contamination terms supplied in this pull.

---

## Session Log

| Date | Task | Notes |
|---|---|---|
| 2026-08-09 | File created, first entry logged | Built to hold the "Queen band" WordStream pull ahead of writing Rotation Queue slot 2. Confirmed `queen freddie mercury` (673,000/mo) as the real focus keyword over bare "Queen," which this session's own SERP check found is heavily monarchy-dominated (Queen Victoria, Queen Elizabeth, "The Queen" all outrank the band in a plain search). "We will rock you" and "brian may and queen" logged as real future candidates rather than used immediately, so they aren't re-derived from scratch later. Two contamination terms (Queens of the Stone Age, Mountain's "Mississippi Queen") logged explicitly as excluded so they don't get mistaken for real Queen-band volume in a future pull. |
| 2026-08-09 | 70s Country Rock pull logged | Two tied, low-competition terms supplied ("70's country rock" and "country rock 70s," both 210/mo). Neither matches the site's exact slug-word-order convention as written; `70s country rock` logged and confirmed as the actual focus keyword, a clean normalization of the two tied variants rather than a third independent pull. No contamination terms in this pull, low volume overall is a real tradeoff of a genuinely niche fusion subgenre, not a data problem. |
| 2026-08-10 | Disco Music of the 70s pull logged | Five real terms supplied, no noise. `Disco Music of the 70s` (12,100/mo) confirmed as the focus keyword; `70s disco` (9,900/mo) logged as a secondary/alternate for the same post rather than a separate target. `funk 70's` (6,600/mo) flagged for the already-queued but not-yet-keyword-checked 70s Funk slot; checked content-build.md directly and confirmed no keyword was assumed there yet, so this is a real head start rather than a contradiction to resolve. `disco mix 70's & 80's` (5,400/mo, Unspecified competition) and the `dance music` cluster (4,400/mo, several tied variants) logged as real future candidates, deliberately not folded into this post since neither matches a genre-article framing. |
