# Prose, Readability & Image Rules — Full Detail

## Prose & Readability Protocol (STRICT ADHERENCE)

### The "Human" Rule
Write as if you've heard this song 100 times — on vinyl, in a car, at 2am. Use sensory and emotional language. Reference specific sonic textures, production choices, and the feeling of listening live. This must read as written by a human who loves music, not a generic AI rewrite of Wikipedia.

### Readability Architecture
- One sentence per line. Each sentence wrapped in its own `<p>` tag — never bundle multiple sentences into one dense paragraph block.
- Keep 75%+ of sentences under 20 words.
- No em-dashes anywhere, ever, in prose — including in list item lead-ins, bold lead-ins, or FAQ answers. Use commas, colons, or periods instead.
  - **Exception:** a single em-dash-style character used strictly as a numeric separator (e.g. a chart position marker like `"Song Title" — #36`) is acceptable ONLY inside a bulleted list item, never in flowing prose sentences. When in doubt, use a colon instead even there.
- Avoid AI-cliché words entirely: "delve," "tapestry," "testament," "haunting," "sonic landscape," "stands the test of time." If one of these is genuinely the only correct word for a specific context, it may appear once in the entire post, never twice.

### Subheading Rule — MANDATORY
Any H2 section with a long, unbroken run of body paragraphs (a real "wall of text" when scanned, not a hard sentence-count trigger) must be broken up with real H3 subheadings. Each subheading names what that specific chunk is actually about, not a generic label like "More Info" or "Details." One subheading per distinct idea or story beat within the section, not one per paragraph. This is a standard build-checklist item for every post on every site, not something that needs to be re-specified per task; check for it the same way word count and sentence length get checked, before calling a post ready to review.

### List Formatting Rule — MANDATORY
Any list of 3+ items, names, artists, songs, or examples must be a real bulleted or numbered HTML list (`<ul>`/`<ol>`), never crammed into one paragraph with parenthetical asides.
- If a sentence needs more than one parenthetical aside to convey a list of examples, it must be converted to a list instead.
- **Bad (never do this):** "Several acts placed two songs apiece, including Simon & Garfunkel ("Song A" and "Song B"), The Beatles ("Song C" and "Song D"), and The Carpenters ("Song E" and "Song F")."
- **Good:** A one-sentence lead-in, followed by a proper bulleted list with one artist/entry per line.
- This applies to every section of every post — body content, FAQ answers, image captions, and list items alike. It overrides default prose habits; check against it explicitly before submitting a post for review.

## Image Optimization (mandatory before any image is used, not just sourcing)
Beyond sourcing/licensing (see below), every image used on the site must be performance-optimized before it ships:

- **File size target: under 200KB** for the primary display size. An unoptimized image (e.g. a raw multi-MB PNG straight from an image generator) must be compressed before use — never publish a multi-megabyte image file. Check exact byte counts when near the limit — a rounded `du -h` reading can hide going over.
- **Format: WebP preferred**, with a PNG or JPG fallback for compatibility.
- **Responsive `srcset` required**: generate at least 3 sizes (e.g. 400w, 800w, 1200w) so mobile devices load an appropriately small file rather than downscaling a full-size desktop image in the browser.
- **Explicit `width`/`height` attributes** on every `<img>` tag to prevent layout shift (Core Web Vitals).
- **Always pair HTML `width`/`height` attributes with `height: auto;` in CSS** on the same selector. Without it, the attribute-derived height wins as a fixed pixel value and `aspect-ratio` in CSS will not override it, the image will not scale proportionally at other viewport widths. Also always set `display: block;` explicitly on any image class, never reuse a class originally written for a placeholder `<div>` (e.g. one using `display: flex` to center placeholder text) on a real `<img>` without checking for this. Verify with real rendering (browser or headless), not just static CSS reading, since this specific bug is invisible from the CSS alone.
- **Match `aspect-ratio` to the actual source image ratio where practical**, not a fixed generic ratio like 16:9. If the source and box ratios differ, `object-fit: cover` crops the difference. Small mismatches crop only a sliver and are usually fine, but matching exactly costs nothing and removes the crop entirely.
- **`loading="lazy"`** for any image below the fold; the featured image (likely the LCP element) should remain eager-loading.
- **Mobile legibility check for dense/infographic-style images**: if an image contains embedded text (charts, infographics, data visuals), explicitly verify that text remains readable when the image is rendered at mobile width (~375px), not just that the image scales without breaking layout. If embedded text becomes illegible at mobile width, do not use that image as a full-width featured image on small screens — use a simplified crop, a mobile-specific alternate version, or reconsider the image choice entirely. Report this check explicitly, don't assume responsive scaling alone solves it.

This check is part of the SEO Scoring Target checklist and the Mobile Check — an image that fails file-size or legibility standards blocks a post from being marked ready to push.

## Image Sourcing
- Wikimedia Commons preferred (free, properly licensed)
- Every Commons image gets a visible credit line: `Image Credit: Photo by [Author], [License], via Wikimedia Commons`
- Only use images with free licenses (CC BY, CC BY-SA, public domain) — skip anything non-free
- NotebookLM-generated infographics are usable as featured images where genuinely relevant and well-designed
- Every image needs real, descriptive alt text — never blank, never a filename, never generic