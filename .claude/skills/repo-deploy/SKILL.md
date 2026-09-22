---
name: repo-deploy
description: Repo location, GitHub/Cloudflare Pages deploy mechanics, GA tag requirement, and the local preview workflow. Use when pushing changes, setting up a local preview server, checking deploy status, or verifying the GA tag on a page.
---

# Repo & Deploy — Full Detail

- Local repo: ~/musicofthe70s.net (Crostini Linux)
- Deploy: git push → GitHub (charlierockautomation) → Cloudflare Pages auto-deploys (~60s)
- Credential helper already configured (`credential.helper store`) — no auth prompts expected
- GA tag: `G-ZY77Y8DHV1` — must be present in `<head>` on every page, no duplicates, no exceptions
- Google Search Console: verified and linked to GA4

## Preview Workflow (every time, before pushing)
```
cd ~/musicofthe70s.net && python3 -m http.server 8000 &
```
Run in background so it survives other terminal commands.
Preview at http://localhost:8000/[path]
Kill with the process ID or a fresh terminal tab once approved — never leave it running unnecessarily.
Never push anything that hasn't been previewed and approved first.
