# Design System & URL Structure — Full Detail

## Design System (do not deviate without explicit approval)
- Fonts: Playfair Display (headings, 700/900) + Inter (body, 400–700), Google Fonts CDN
- Colors:
  - `--bg-primary: #1a1a2e`
  - `--bg-card: #16213e`
  - `--bg-elevated: #0f3460`
  - `--accent-gold: #f5a623`
  - `--accent-warm: #e8956d`
  - `--text-primary: #f0e6d3`
  - `--text-muted: #9ca3af`
  - `--border-subtle: #2d3561`
- Reusable classes already in css/style.css: `.container`, `.section`, `.breadcrumb`, `.page-intro`, `.card`, `.tool-grid`/`.tool-card`, `.badge`/`.badge-gold`, `.seo-content`, `.section-divider`, `.btn-primary`/`.btn-secondary`
- Blog-specific classes: `.category-grid`/`.category-card`, `.post-grid`/`.post-card`, `.toc-block`, `.video-embed`, `.faq-block`/`.faq-item` (gold left-border, visually distinct from body text), `.related-posts`, `.placeholder-tag`
- Never add new fonts or colors outside this token set without explicit approval.
- Blog post spacing: H1 to intro ~24-32px, list to following content ~24-32px, H2 section spacing ~40-48px — consistent across all posts, defined in css/style.css, never inline styles.

## URL Structure
/blog/index.html (hub)
/blog/genres/ (rock-music-of-the-70s, disco-and-dance, rb-and-soul, etc.)
/blog/songs/ (top-songs-of-1970, best-70s-one-hit-wonders, etc.)
/blog/artists/
/blog/years/ (top-songs-of-1970 through top-songs-of-1979)
/blog/trivia/

Category folders are singular content types, not keyword-stuffed subfolders. Do not nest keywords redundantly (e.g. avoid `/blog/songs/70s-songs-top-songs/`). The domain already carries "70s" — do not repeat it unnecessarily in every slug.