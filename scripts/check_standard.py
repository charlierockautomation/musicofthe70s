#!/usr/bin/env python3
"""check_standard.py: the Article Standard save-time gate (MASTER-PLAN-2026-11.md, "Article standard").

Every NEW article, and every existing page when it is upgraded, must pass this before it is committed.
Modeled on the ClassicRockArtists.com gates (check-stuffing.py, check-writing.py, check-template.py,
check-schema.py), fitted to this site: people who want to hear and remember 70s music.
Rules in prose: .claude/skills/article-standard/SKILL.md.

USAGE
  check_standard.py <page/index.html> --keyword "eagles songs" --type band [--subject "Eagles"]
                    [--secondary "a,b"] [--related-songs "/blog/songs/x/,/blog/songs/y/"]
  check_standard.py <page/index.html>          # page registered in scripts/article_standard_pages.json
  check_standard.py --registered               # every registered page
  check_standard.py --site                     # site-wide: no link to classicrockartists.com
  check_standard.py --staged                   # git pre-commit mode (scripts/hooks/pre-commit)

Page types (schema table in the plan): song, band, artist, playlist, album, tv, pillar, chart, quiz, trivia, tool.

Exit 0 = PASS, 1 = at least one FAIL, 2 = bad usage. WARN lines never fail.

Checks
  K1 keyword natural: focus keyword never leads with a generic word ("song ymca" is the example to avoid),
     never a lyrics/meaning keyword; Title-Case keyword mid-sentence = WARN
  K2 anti-stuffing, same limits as ClassicRockArtists: density phrase <= 1.0% / name <= 2.0%; keyword in <= 2 H2s
     and <= 1/3 of H2s; per 300 words phrase <= 2 / name <= 3; never in two consecutive sentences; each
     secondary <= 3 uses; no reader-facing SEO filler
  A1 answer first: the first two sentences carry at least 2 of the facts-box facts
  A2 facts box: <aside class="facts-box"> under the intro, before the TOC and first H2, with the required rows
  W1 one sentence per paragraph   W2 no em dash (body, title, meta)   W3 no lyrics heading, long quotes WARN
  W4 no first-person concert claims
  S1 Sources section: 3+ external links, never Wikipedia only, every link logged as opened in
     sources/log/<slug>.json   S2 Billboard/Hot 100 data credited to /about/methodology/
  T1 byline "By Charlie" linked to /about/author/, Published and Updated dates
  T2 collapsible TOC (nav.toc-block > details.toc-details > summary, the site's list-page pattern) matching the H2s in order
  T3 FAQ (#faq): 3+ H3 questions, answers 1-3 sentences, no answer repeating body text
  T4 You Might Also Like: last section, 3+ cards, every card target exists
  L1 Listen button (button.listen-btn[data-yt]) before the first H2 + /js/listen-button.js
  L2 every list plays through the shared player (/js/table-player.js, table[data-inline-player]);
     list page types must have one   L3 every YouTube ID recorded as official/label in data/official-videos.json
     and passing data/youtube-status.json
  N1 link up to the pillar   N2 down to every related song story   N3 2 to 4 sideways (same pillar)
  N4 one link to /radio/ or a tool   N5 each target once   N6 never classicrockartists.com
  X1 schema by page type, plus BreadcrumbList and the Person author (Charlie)
"""
import argparse
import html as htmllib
import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "scripts" / "article_standard_pages.json"
OFFICIAL = ROOT / "data" / "official-videos.json"
SOURCE_LOG_DIR = ROOT / "sources" / "log"
SITE = "https://musicofthe70s.net"
AUTHOR_PATH = "/about/author/"
METHODOLOGY_PATH = "/about/methodology/"

TYPES = ["song", "band", "artist", "playlist", "album", "tv", "pillar", "chart", "quiz", "trivia", "tool"]
LISTEN_TYPES = {"song", "band", "artist", "playlist", "album", "tv", "chart"}
LIST_TYPES = {"band", "artist", "playlist", "album", "chart"}
FACTS_REQUIRED = {
    "song": {"writer": ["writer", "writers", "written by", "songwriter", "songwriters"],
             "artist": ["artist", "recorded by"],
             "released": ["released", "release date"],
             "peak": ["hot 100 peak", "billboard hot 100 peak", "peak"],
             "weeks at #1": ["weeks at no. 1", "weeks at #1", "weeks at number one", "weeks at no 1"]},
    "band": {"active": ["active", "active years", "years active"], "genre": ["genre", "genres"],
             "biggest hits": ["biggest 70s hits", "biggest hits", "biggest 1970s hits"],
             "#1 count": ["no. 1 hits", "#1 hits", "number one hits", "no 1 hits", "hot 100 no. 1s", "no. 1s"]},
}
FACTS_REQUIRED["artist"] = FACTS_REQUIRED["band"]

# The plan's 7 pillars. Pillar column in CONTENT-INDEX.md uses these names.
PILLARS = {
    "Home": "/",
    "70s Songs": "/blog/songs/best-songs-of-the-70s/",
    "70s Number One Hits": "/blog/songs/70s-number-one-hits/",
    "70s Bands & Singers": "/blog/artists/70s-bands/",
    "70s Genres": "/blog/genres/",
    "Listen to 70s Music": "/radio/",
    "70s Music Trivia": "/blog/trivia/",
}
TOOLS = ["/pages/random-70s-song", "/pages/birthday-number-one", "/pages/mood-song-matcher",
         "/pages/random-artist-picker", "/pages/70s-trivia-quiz", "/pages/70s-decade-wheel"]


def pillar_for(path):
    """Pillar name for a site path (clean URL). Same rules as the Pillar column in CONTENT-INDEX.md."""
    p = path if path.endswith("/") or "." in path.rsplit("/", 1)[-1] or path.startswith("/pages/") else path + "/"
    p = re.sub(r"index\.html$", "", p)
    if p in ("/", "/blog/", "/pages/about", "/pages/contact", "/pages/privacy-policy", "/pages/terms-of-use") \
            or p.startswith("/about/"):
        return "Home"
    for name, url in PILLARS.items():
        if p == url and name != "Home":
            return "Home"  # a pillar page sits under the homepage
    if p.startswith("/blog/years/") or re.match(r"^/blog/trivia/[a-z]+-\d+-in-music-history/$", p) \
            or p.startswith("/blog/trivia/this-week-in-music-history") \
            or p in ("/pages/birthday-number-one", "/pages/70s-decade-wheel"):
        return "70s Number One Hits"
    if p.startswith("/blog/songs/"):
        return "70s Songs"
    if p.startswith("/blog/artists/") or p == "/pages/random-artist-picker":
        return "70s Bands & Singers"
    if p.startswith("/blog/genres/"):
        return "70s Genres"
    if p.startswith("/radio/") or p in ("/pages/random-70s-song", "/pages/mood-song-matcher"):
        return "Listen to 70s Music"
    if p.startswith("/blog/trivia/") or p in ("/pages/70s-trivia-quiz", "/pages/rock-trivia-game"):
        return "70s Music Trivia"
    return "Home"


# ---------------------------------------------------------------- text helpers
def norm(s):
    s = htmllib.unescape(s).replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    return re.sub(r"\s+", " ", s).strip()


def strip_tags(s):
    return norm(re.sub(r"<[^>]+>", " ", s)).replace(" ,", ",").replace(" .", ".")


ABBREV_RE = re.compile(r"\b(No|Nos|Mr|Mrs|Ms|Dr|St|Jr|Sr|vs|Vol|Inc|Co|Ltd|Mt|Ft)\.(?=\s)")
INITIALS_RE = re.compile(r"\b([A-Z])\.(?=\s?[A-Z]\.)")


def split_sentences(text):
    text = ABBREV_RE.sub("\\1\u0001", text)
    text = INITIALS_RE.sub("\\1\u0001", text)
    parts = re.split(r"(?<=[.!?])[\"')\]]*\s+(?=[A-Z0-9\"'(])", text)
    return [s.replace("\u0001", ".") for s in parts if s.strip()]


STOPWORDS = set("a an and are as at be but by for from had has have he her his i in is it its of on or "
                "she that the their they this to was were which who with you your".split())


def content_words(s):
    return {w for w in re.findall(r"[a-z0-9']+", s.lower()) if w not in STOPWORDS}


def kw_regex(kw):
    parts = [re.escape(w) for w in norm(kw).lower().split()]
    return re.compile(r"(?<![\w])" + r"\s+".join(parts) + r"(?![\w])", re.I)


def tok(s):
    return re.findall(r"[a-z0-9]+", norm(s).lower().replace("'", "").replace("&", "and"))


BLOCK_TAGS = {"p", "li", "h1", "h2", "h3", "h4", "h5", "h6", "td", "th", "dt", "dd", "div", "blockquote",
              "figcaption", "summary", "details", "section", "aside", "ul", "ol", "table", "tr", "br", "hr", "nav"}


class Units(HTMLParser):
    """Text units, one per block element, tagged with the innermost block tag and its class."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.units, self.buf, self.stack, self.skip = [], [], [], 0

    def cur(self):
        return self.stack[-1] if self.stack else ("body", "")

    def flush(self):
        text = norm("".join(self.buf))
        self.buf = []
        if text:
            tag, cls = self.cur()
            self.units.append((tag, text, cls, tuple(c for _, c in self.stack)))

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "iframe"):
            self.skip += 1
            return
        if tag in BLOCK_TAGS:
            self.flush()
            self.stack.append((tag, dict(attrs).get("class", "") or ""))

    def handle_endtag(self, tag):
        if tag in ("script", "style", "iframe"):
            self.skip = max(0, self.skip - 1)
            return
        if tag in BLOCK_TAGS:
            self.flush()
            if any(t == tag for t, _ in self.stack):
                while self.stack and self.stack.pop()[0] != tag:
                    pass

    def handle_data(self, data):
        if not self.skip:
            self.buf.append(data)

    def close(self):
        super().close()
        self.flush()


def units_of(fragment):
    p = Units()
    p.feed(fragment)
    p.close()
    return p.units


# ---------------------------------------------------------------- page model
def page_path(file):
    rel = Path(file).resolve().relative_to(ROOT).as_posix()
    rel = re.sub(r"index\.html$", "", rel)
    rel = re.sub(r"\.html$", "", rel)
    return "/" + rel


def internal_path(href):
    """Clean site path for an internal href, or None for external / in-page links."""
    href = htmllib.unescape(href.strip())
    if href.startswith(SITE):
        href = href[len(SITE):] or "/"
    if not href.startswith("/") or href.startswith("//"):
        return None
    path = href.split("#")[0]
    path = re.sub(r"index\.html(?=$|\?)", "", path)
    path = re.sub(r"\.html(?=$|\?)", "", path)
    return path or "/"


def path_exists(path):
    base = path.split("?")[0]
    if base == "/":
        return (ROOT / "index.html").exists()
    rel = base.strip("/")
    return (ROOT / rel / "index.html").exists() or (ROOT / (rel + ".html")).exists() or (ROOT / rel).is_file()


def load_registry():
    try:
        return json.loads(REGISTRY.read_text(encoding="utf-8")).get("pages", {})
    except (OSError, ValueError):
        return {}


def song_story_pages():
    """{path: h1 text} for every single-song story under /blog/songs/ (lists and the pillar excluded)."""
    out = {}
    for f in sorted((ROOT / "blog" / "songs").glob("*/index.html")):
        slug = f.parent.name
        if slug.startswith("70s-") or slug in ("best-songs-of-the-70s", "archive"):
            continue
        m = re.search(r"<h1[^>]*>(.*?)</h1>", f.read_text(encoding="utf-8", errors="ignore"), re.S)
        out[f"/blog/songs/{slug}/"] = strip_tags(m.group(1)) if m else slug
    return out


class Report:
    def __init__(self):
        self.rows = []

    def add(self, code, ok, msg, warn=False):
        self.rows.append((code, "WARN" if (warn and not ok) else ("PASS" if ok else "FAIL"), msg))

    @property
    def passed(self):
        return all(s != "FAIL" for _, s, _ in self.rows)

    def print(self, title):
        print(f"=== {title} ===")
        for code, status, msg in self.rows:
            print(f"{status:<5} {code:<4} {msg}")
        fails = sum(1 for _, s, _ in self.rows if s == "FAIL")
        print(f"\nRESULT: {'PASS' if self.passed else f'FAIL ({fails} check(s) failed)'}")


# ---------------------------------------------------------------- schema
def ld_nodes(html):
    nodes, errors = [], []
    for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            data = json.loads(raw)
        except ValueError as e:
            errors.append(str(e))
            continue
        stack = [data]
        while stack:
            n = stack.pop()
            if isinstance(n, list):
                stack.extend(n)
            elif isinstance(n, dict):
                nodes.append(n)
                stack.extend(v for v in n.values() if isinstance(v, (dict, list)))
    return nodes, errors


def types_of(n):
    t = n.get("@type", [])
    return set(t if isinstance(t, list) else [t])


def find(nodes, t):
    return [n for n in nodes if t in types_of(n)]


def as_list(v):
    return v if isinstance(v, list) else ([] if v is None else [v])


def check_schema(html, ptype, has_video, rep):
    nodes, errors = ld_nodes(html)
    probs = [f"invalid JSON-LD: {e}" for e in errors]

    def need(t, props=(), where=None):
        found = find(where if where is not None else nodes, t)
        if not found:
            probs.append(f"no {t}")
            return None
        n = found[0]
        miss = [p for p in props if n.get(p) in (None, "", [])]
        if miss:
            probs.append(f"{t} missing {', '.join(miss)}")
        return n

    def faq():
        need("FAQPage", ["mainEntity"])

    def video():
        if has_video:
            need("VideoObject", ["name", "description", "thumbnailUrl", "uploadDate", "embedUrl"])

    def recordings(container, label):
        recs = [r for r in as_list(container) if isinstance(r, dict)]
        items = []
        for r in recs:
            items.append(r.get("item", r) if "ListItem" in types_of(r) else r)
        if not items:
            probs.append(f"{label} has no tracks")
        elif not all("MusicRecording" in types_of(i) for i in items if isinstance(i, dict)):
            probs.append(f"{label} entries must be MusicRecording")
        return items

    if not find(nodes, "BreadcrumbList"):
        probs.append("no BreadcrumbList")
    if ptype not in ("pillar", "tool", "quiz"):
        posts = find(nodes, "BlogPosting")
        if not posts:
            probs.append("no BlogPosting" + (" (page uses Article)" if find(nodes, "Article") else ""))
    persons = [n for n in find(nodes, "Person") if n.get("name") == "Charlie"]
    if ptype not in ("tool",) and not persons:
        probs.append("no Person author named Charlie")
    for post in find(nodes, "BlogPosting") + find(nodes, "Article"):
        a = post.get("author", {})
        if isinstance(a, dict) and a.get("@id") != SITE + AUTHOR_PATH:
            probs.append("BlogPosting author is not the site's Person (@id /about/author/)")

    if ptype == "song":
        rec = need("MusicRecording", ["name", "byArtist", "inAlbum", "datePublished", "recordingOf"])
        if rec:
            comp = rec.get("recordingOf")
            if not (isinstance(comp, dict) and "MusicComposition" in types_of(comp) and comp.get("composer")):
                probs.append("MusicRecording.recordingOf must be a MusicComposition with composer")
        video()
        faq()
    elif ptype in ("band", "artist"):
        post = (find(nodes, "BlogPosting") or [{}])[0]
        about = post.get("about")
        want = "MusicGroup" if ptype == "band" else "Person"
        if not (isinstance(about, dict) and want in types_of(about)):
            probs.append(f"BlogPosting.about must be a {want}")
        else:
            props = ["name", "genre", "sameAs"] + (["foundingDate"] if ptype == "band" else [])
            miss = [p for p in props if not about.get(p)]
            if miss:
                probs.append(f"about {want} missing {', '.join(miss)}")
            same = " ".join(as_list(about.get("sameAs")))
            if "wikipedia.org" not in same or "musicbrainz.org" not in same:
                probs.append("about.sameAs needs Wikipedia and MusicBrainz")
        lst = need("ItemList", ["itemListElement"])
        if lst:
            recordings(lst.get("itemListElement"), "ItemList")
        faq()
    elif ptype == "playlist":
        pl = need("MusicPlaylist", ["name", "numTracks", "track"])
        if pl:
            tracks = recordings(pl.get("track"), "MusicPlaylist.track")
            if isinstance(pl.get("numTracks"), int) and pl["numTracks"] != len(tracks):
                probs.append(f"numTracks {pl['numTracks']} != {len(tracks)} tracks")
        faq()
    elif ptype == "album":
        al = need("MusicAlbum", ["name", "albumProductionType", "byArtist", "datePublished", "track"])
        if al:
            recordings(al.get("track"), "MusicAlbum.track")
        faq()
    elif ptype == "tv":
        post = (find(nodes, "BlogPosting") or [{}])[0]
        if not (isinstance(post.get("about"), dict) and "TVSeries" in types_of(post["about"])):
            probs.append("BlogPosting.about must be a TVSeries")
        if not find(nodes, "VideoObject"):
            probs.append("no VideoObject for the clips")
        faq()
    elif ptype == "pillar":
        cp = need("CollectionPage", ["@id", "url", "name", "mainEntity"])
        if cp is not None and not find(nodes, "ItemList"):
            probs.append("no ItemList of the linked pages")
    elif ptype == "chart":
        lst = need("ItemList", ["itemListElement"])
        if lst:
            recordings(lst.get("itemListElement"), "ItemList")
        ds = need("Dataset", ["name", "description", "creator"])
        if ds and METHODOLOGY_PATH not in json.dumps(ds):
            probs.append("Dataset must link the methodology page")
    elif ptype == "quiz":
        need("Quiz", ["name", "hasPart"])
    elif ptype == "trivia":
        faq()
    elif ptype == "tool":
        need("WebApplication", ["name", "url", "applicationCategory"])
    rep.add("X1", not probs, f"schema ({ptype}): " + ("; ".join(probs) if probs else "all required types present"))


# ---------------------------------------------------------------- main check
GENERIC_LEAD = {"song", "songs", "lyrics", "track", "tracks", "music", "single"}
FILLER_RE = re.compile(r"^\s*(search intent|fans also search|best for|similar to)\b\s*:?", re.I)
CONCERT_RE = re.compile(
    r"\b(I|we)\s+(saw|caught|watched|heard)\s+(them|him|her|the band|the group|it|[A-Z][\w']+)\s+"
    r"(live|in concert|play|perform)|\bmy first (concert|show|gig)\b|\b(I|we) (was|were) (there|in the crowd|at the show)\b"
    r"|\bI remember (seeing|being at|watching them)\b|\bwhen I saw\b|\bI (went to|attended) (the|their|his|her|a) (show|concert|gig)",
    re.I)
EXCLUDE_P_CLASSES = ("post-byline", "post-img-caption", "jump-to-list", "listen-row", "card", "post-card", "faq-src")


def check(file, keyword, ptype, subject=None, secondary=(), related_songs=None, pillar=None):
    rep = Report()
    html = Path(file).read_text(encoding="utf-8")
    path = page_path(file)
    slug = path.rstrip("/").rsplit("/", 1)[-1] or "home"
    m = re.search(r"<article\b.*?</article>", html, re.S)
    if not m:
        rep.add("--", False, "no <article> element")
        return rep
    article = m.group(0)
    ymal_i = article.find("You Might Also Like")
    rel_i = article.find('class="related-posts"')
    cut = min([i for i in (ymal_i, rel_i) if i != -1], default=-1)
    if cut != -1:
        cut = article.rfind("<section", 0, cut) if article.rfind("<section", 0, cut) != -1 else cut
    body = article if cut == -1 else article[:cut]
    title = strip_tags((re.search(r"<title>(.*?)</title>", html, re.S) or [None, ""])[1]) if "<title>" in html else ""
    desc_m = re.search(r'<meta name="description" content="(.*?)"', html, re.S)
    desc = norm(desc_m.group(1)) if desc_m else ""
    kw = norm(keyword).lower()
    kre = kw_regex(kw)
    tier = "name" if subject and tok(subject) == tok(kw) else "phrase"

    # K1 keyword natural
    kt = tok(kw)
    bad = []
    if kt and kt[0] in GENERIC_LEAD:
        bad.append(f'leads with generic word "{kt[0]}" (reads as "{keyword.title()}")')
    if kt and kt[-1] in ("lyrics", "meaning"):
        bad.append(f'"{kt[-1]}" keyword (no lyrics on this site)')
    rep.add("K1", not bad, "focus keyword natural: " + ("; ".join(bad) if bad else f'"{keyword}" ({tier} keyword)'))
    if any(w in kt for w in ("song", "songs", "music", "hits", "bands")):
        caps = [mo.group(0) for mo in kre.finditer(strip_tags(" ".join(re.findall(r"<p[^>]*>(.*?)</p>", body, re.S))))
                if mo.group(0)[0].isupper() and mo.group(0) != mo.group(0).upper()
                and all(w[:1].isupper() for w in mo.group(0).split() if w[0].isalpha())]
        if caps:
            rep.add("K1", False, f'keyword Title-Cased in prose {len(caps)}x (e.g. "{caps[0]}"): use it as a normal phrase',
                    warn=True)

    # K2 stuffing
    units = units_of(body)
    prose = [(t, x, c) for t, x, c, _ in units]
    full = " ".join(x for _, x, _ in prose)
    wc = len(full.split())
    hits = len(kre.findall(full))
    dens = hits / wc * 100 if wc else 0
    maxd = 2.0 if tier == "name" else 1.0
    rep.add("K2", dens <= maxd, f"density {dens:.2f}% ({hits} uses / {wc} words, max {maxd}% {tier})")
    h2s = [x for t, x, _ in prose if t == "h2"]
    kh2 = [h for h in h2s if kre.search(h)]
    rep.add("K2", len(kh2) <= 2 and len(kh2) <= len(h2s) / 3,
            f"keyword in {len(kh2)} of {len(h2s)} H2s (max 2 and max 1/3)")
    pos, off = [], 0
    for _, x, _ in prose:
        pos += [off + len(x[:mo.start()].split()) for mo in kre.finditer(x)]
        off += len(x.split())
    worst = max((sum(1 for q in pos[i:] if q < p + 300) for i, p in enumerate(pos)), default=0)
    maxw = 3 if tier == "name" else 2
    consec, prev = [], False
    for t, x, _ in prose:
        if re.fullmatch(r"h[1-6]", t):
            prev = False
            continue
        for s in split_sentences(x):
            hit = bool(kre.search(s))
            if hit and prev:
                consec.append(s[:70])
            prev = hit
    rep.add("K2", worst <= maxw and not consec,
            f"worst 300-word window {worst} (max {maxw}); consecutive-sentence hits {len(consec)}"
            + (f' e.g. "{consec[0]}"' if consec else ""))
    over = [f"{s} x{len(kw_regex(s).findall(full))}" for s in secondary
            if not (norm(s).lower() in kw or kw in norm(s).lower()) and len(kw_regex(s).findall(full)) > 3]
    rep.add("K2", not over, "secondary keywords " + (("over 3: " + ", ".join(over)) if over else f"OK ({len(secondary)})"))
    filler = [x[:40] for _, x, _ in prose if FILLER_RE.match(x)]
    rep.add("K2", not filler, "no SEO filler labels" + (f": {filler[0]}" if filler else ""))

    # intro paragraphs: <p> before the facts box / TOC / first H2, minus byline and listen rows
    first_h2 = body.find("<h2")
    pre = body[:first_h2 if first_h2 != -1 else len(body)]
    fb_i = pre.find('class="facts-box"')
    toc_i = pre.find('class="toc-block')
    intro_end = min([i for i in (fb_i, toc_i) if i != -1], default=len(pre))
    intro_ps = [strip_tags(p) for cls, p in re.findall(r'<p(?: class="([^"]*)")?[^>]*>(.*?)</p>', pre[:intro_end], re.S)
                if not any(c in (cls or "") for c in EXCLUDE_P_CLASSES)]
    intro_sents = [s for p in intro_ps for s in split_sentences(p)][:2]

    # A2 facts box
    fbm = re.search(r'<aside class="facts-box"[^>]*>(.*?)</aside>', body, re.S)
    facts = {}
    if fbm:
        for lab, val in re.findall(r"<(?:dt|th)[^>]*>(.*?)</(?:dt|th)>\s*<(?:dd|td)[^>]*>(.*?)</(?:dd|td)>", fbm.group(1), re.S):
            facts[strip_tags(lab).lower().rstrip(":")] = strip_tags(val)
    req = FACTS_REQUIRED.get(ptype, {})
    probs = []
    if not fbm:
        if req or ptype in ("playlist", "album", "tv", "chart"):
            probs.append('no <aside class="facts-box"> under the intro')
    else:
        if not intro_sents:
            probs.append("facts box sits above the intro")
        if toc_i != -1 and fb_i > toc_i:
            probs.append("facts box is below the TOC")
        if first_h2 != -1 and body.find('class="facts-box"') > first_h2:
            probs.append("facts box is below the first H2")
        for name, labels in req.items():
            if not any(lab in facts for lab in labels):
                probs.append(f"missing row: {name}")
    rep.add("A2", not probs, "facts box: " + ("; ".join(probs) if probs else f"{len(facts)} rows under the intro"))

    # A1 answer first
    two = " ".join(intro_sents).lower()
    matched = []
    for lab, val in facts.items():
        pieces = [v.strip() for v in re.split(r",|;| and |/|&", val) if len(v.strip()) > 2]
        years = re.findall(r"\b19[5-9]\d\b", val)
        nums = re.findall(r"\b\d{1,3}\b", val) if any(w in lab for w in ("peak", "weeks", "no. 1", "#1", "number")) else []
        if any(p.lower() in two for p in pieces) or any(y in two for y in years) \
                or any(re.search(rf"(no\.?|number|#)\s*{n}\b|\b{n} weeks?\b", two) for n in nums):
            matched.append(lab)
    need_n = 2 if facts else 0
    rep.add("A1", bool(facts) and len(matched) >= need_n,
            f"first two sentences answer the search: {len(matched)} facts-box facts matched {matched or ''}"
            + (f' | "{" ".join(intro_sents)[:140]}"' if intro_sents else " | no intro sentences found"))

    # W1 one sentence per paragraph
    multi = []
    for cls, p in re.findall(r'<p(?: class="([^"]*)")?[^>]*>(.*?)</p>', body, re.S):
        if any(c in (cls or "") for c in EXCLUDE_P_CLASSES):
            continue
        t = strip_tags(p)
        if t and len(split_sentences(t)) > 1:
            multi.append(t[:70])
    rep.add("W1", not multi, f"one sentence per paragraph: {len(multi)} multi-sentence <p>"
            + (f' e.g. "{multi[0]}"' if multi else ""))
    # W2 em dash
    em = len(re.findall(r"\u2014|&mdash;|&#8212;|&#x2014;", article)) + title.count("\u2014") + desc.count("\u2014")
    rep.add("W2", em == 0, f"em dashes in body/title/meta: {em}")
    # W3 lyrics
    lyr_heads = [x for t, x, _ in prose if re.fullmatch(r"h[1-6]", t) and re.search(r"\blyrics\b", x, re.I)]
    rep.add("W3", not lyr_heads, "no lyrics section" + (f": {lyr_heads[0]}" if lyr_heads else ""))
    quotes = [q for _, x, _ in prose for q in re.findall(r'"([^"]{40,})"', x) if len(q.split()) >= 8]
    if quotes:
        rep.add("W3", False, f"{len(quotes)} quoted passage(s) of 8+ words: confirm none is a lyric "
                f'(e.g. "{quotes[0][:60]}")', warn=True)
    # W4 first-person concert claims
    conc = [mo.group(0) for mo in CONCERT_RE.finditer(full)]
    rep.add("W4", not conc, "no first-person concert claims" + (f': "{conc[0]}"' if conc else ""))

    # S1 sources
    src = re.search(r'<section class="sources"[^>]*>(.*?)</section>', article, re.S)
    probs = []
    ext = []
    if not src:
        probs.append("no Sources section")
    else:
        ext = [h for h in re.findall(r'href="(https?://[^"]+)"', src.group(1)) if not h.startswith(SITE)]
        if len(ext) < 3:
            probs.append(f"{len(ext)} external sources (min 3)")
        if ext and all("wikipedia.org" in h for h in ext):
            probs.append("Wikipedia is the only source")
        logf = SOURCE_LOG_DIR / f"{slug}.json"
        try:
            log = {e["url"]: e for e in json.loads(logf.read_text(encoding="utf-8")) if e.get("opened")}
        except (OSError, ValueError, KeyError, TypeError):
            log = {}
            probs.append(f"no source log {logf.relative_to(ROOT)} (each source: url, claim, opened)")
        unopened = [h for h in ext if htmllib.unescape(h) not in log]
        if log and unopened:
            probs.append(f"{len(unopened)} source(s) not logged as opened, e.g. {unopened[0]}")
    rep.add("S1", not probs, "sources named and opened: " + ("; ".join(probs) if probs else f"{len(ext)} sources, all opened"))
    links = [h for h in re.findall(r'<a\b[^>]*href="([^"]+)"', article)]
    paths = [internal_path(h) for h in links]
    if re.search(r"\b(Hot 100|Billboard)\b", full):
        rep.add("S2", METHODOLOGY_PATH in paths, "chart data credited to the methodology page "
                + ("(linked)" if METHODOLOGY_PATH in paths else "(Billboard/Hot 100 named, /about/methodology/ not linked)"))

    # T1 byline
    bl = re.search(r'<p class="post-byline">(.*?)</p>', body, re.S)
    probs = []
    if not bl:
        probs.append("no byline")
    else:
        b = bl.group(1)
        if not re.search(r'By <a href="(?:https://musicofthe70s\.net)?/about/author/">Charlie</a>', b):
            probs.append('not "By Charlie" linked to /about/author/')
        if not re.search(r"Published\s+\w+ \d{1,2}, \d{4}", b):
            probs.append("no Published date")
        if not re.search(r"Updated\s+\w+ \d{1,2}, \d{4}", b):
            probs.append("no Updated date")
    rep.add("T1", not probs, "byline: " + ("; ".join(probs) if probs else "By Charlie, published and updated dates"))

    # T2 collapsible TOC
    toc = re.search(r'<nav class="toc-block[^"]*"[^>]*>\s*<details class="toc-details"[^>]*>(.*?)</details>', body, re.S)
    probs = []
    if not toc:
        probs.append("TOC is not collapsible (nav.toc-block > details.toc-details > summary)"
                     if 'class="toc-block' in body else "no TOC")
    else:
        if "<summary" not in toc.group(1):
            probs.append("TOC has no <summary>")
        toc_ids = re.findall(r'href="#([^"]+)"', toc.group(1))
        h2_ids = [i for i in re.findall(r'<h2[^>]*id="([^"]+)"', body)]
        missing = [i for i in toc_ids if f'id="{i}"' not in article]
        if missing:
            probs.append(f"TOC links to missing ids: {missing[:3]}")
        if [i for i in h2_ids if i in toc_ids] != [i for i in toc_ids if i in h2_ids] or set(h2_ids) - set(toc_ids):
            probs.append("TOC does not match the H2s one-to-one in order")
        no_id = len(re.findall(r"<h2(?![^>]*\bid=)[^>]*>", re.sub(r'<section[^>]*\bid="[^"]+"[^>]*>\s*<h2', "<section>", body)))
        if no_id:
            probs.append(f"{no_id} H2(s) without an id")
    rep.add("T2", not probs, "collapsible TOC: " + ("; ".join(probs) if probs else "OK"))

    # T3 FAQ adds facts not in the body
    fq = re.search(r'<section class="faq-block" id="faq">(.*?)</section>', body, re.S)
    probs = []
    if not fq and ptype != "tool":
        probs.append("no FAQ section (#faq)")
    elif fq:
        parts = re.split(r"(<h3[^>]*>.*?</h3>)", fq.group(1), flags=re.S)
        qs = []
        for part in parts:
            if part.startswith("<h3"):
                qs.append([strip_tags(part), []])
            elif qs:
                qs[-1][1] += [s for p in re.findall(r"<p[^>]*>(.*?)</p>", part, re.S) for s in split_sentences(strip_tags(p))]
        if len(qs) < 3:
            probs.append(f"{len(qs)} questions (min 3)")
        body_wo_faq = body.replace(fq.group(0), "")
        body_sets = [content_words(s) for t, x, _, _ in units_of(body_wo_faq) if not re.fullmatch(r"h[1-6]", t)
                     for s in split_sentences(x)]
        for q, ans in qs:
            if not q.endswith("?"):
                probs.append(f"not a question: {q[:40]}")
            if not 1 <= len(ans) <= 3:
                probs.append(f"answer has {len(ans)} sentences: {q[:40]}")
            for a in ans:
                aw = content_words(a)
                if len(aw) >= 6 and any(len(bw) >= 6 and len(aw & bw) / min(len(aw), len(bw)) >= 0.7 for bw in body_sets):
                    probs.append(f'answer repeats body text: "{a[:55]}"')
        rep.add("T3", not probs, "FAQ adds new facts: " + ("; ".join(probs[:4]) if probs else f"{len(qs)} questions OK"))
    if not fq:
        rep.add("T3", ptype == "tool", "FAQ: " + ("; ".join(probs) if probs else "not required for tools"))

    # T4 You Might Also Like
    ym = re.search(r"<section[^>]*>\s*<h2[^>]*>\s*You Might Also Like\s*</h2>(.*?)</section>", article, re.S)
    probs = []
    if not ym:
        heading = re.search(r'class="related-posts">\s*<h2>(.*?)</h2>', article)
        probs.append("no You Might Also Like section" + (f' (heading reads "{strip_tags(heading.group(1))}")' if heading else ""))
    else:
        cards = re.findall(r'class="[^"]*\bpost-card\b', ym.group(1))
        if len(cards) < 3:
            probs.append(f"{len(cards)} cards (min 3)")
        dead = [p for p in (internal_path(h) for h in re.findall(r'href="([^"]+)"', ym.group(1))) if p and not path_exists(p)]
        if dead:
            probs.append(f"card targets missing: {dead[:2]}")
        after = article[ym.end():]
        if re.search(r"<(h2|p|section)\b", after):
            probs.append("content after the You Might Also Like cards")
    rep.add("T4", not probs, "You Might Also Like: " + ("; ".join(probs) if probs else "OK"))

    # L1 Listen button
    if ptype in LISTEN_TYPES:
        lb = re.search(r'<button[^>]*class="[^"]*\blisten-btn\b[^"]*"[^>]*data-yt="([\w-]{11})"', pre) or \
             re.search(r'<button[^>]*data-yt="([\w-]{11})"[^>]*class="[^"]*\blisten-btn\b', pre)
        probs = []
        if not lb:
            jump = "jump-btn" in pre
            probs.append("no Listen button before the first H2" + (" (page has a jump link, which does not play in place)" if jump else ""))
        if "/js/listen-button.js" not in html:
            probs.append("page does not load /js/listen-button.js")
        rep.add("L1", not probs, "Listen button plays in place: " + ("; ".join(probs) if probs else "OK"))
    # L2 shared continuous player
    probs = []
    tables = re.findall(r"<table\b[^>]*>.*?</table>", html, re.S)
    play_tables = [t for t in tables if "data-yt=" in t]
    if play_tables and "/js/table-player.js" not in html:
        probs.append("lists with Play buttons but no /js/table-player.js")
    if any("data-inline-player" not in t[:t.find(">") + 1] for t in play_tables):
        probs.append("a playable table without data-inline-player")
    if ptype in LIST_TYPES and not play_tables:
        probs.append(f"{ptype} page has no playable list")
    rep.add("L2", not probs, "shared continuous player: " + ("; ".join(probs) if probs else f"{len(play_tables)} playable list(s)"))
    # L3 official uploads only
    ids = sorted(set(re.findall(r"youtube(?:-nocookie)?\.com/embed/([\w-]{11})", html) + re.findall(r'data-yt="([\w-]{11})"', html)))
    try:
        official = json.loads(OFFICIAL.read_text(encoding="utf-8")).get("videos", {})
    except (OSError, ValueError):
        official = {}
    unrec = [i for i in ids if not (official.get(i, {}).get("official") and official[i].get("channel"))]
    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        from youtube_status import status_problems
        stat = status_problems(ids)
    except Exception as e:  # noqa: BLE001
        stat = [f"youtube_status unavailable: {e}"]
    probs = ([f"{len(unrec)} of {len(ids)} video(s) not recorded as official/label in data/official-videos.json "
              f"(e.g. {unrec[0]})"] if unrec else []) + stat[:2]
    rep.add("L3", not probs, "official uploads only: " + ("; ".join(probs) if probs else f"{len(ids)} video(s) official, status OK"))

    # N links
    my_pillar = pillar or pillar_for(path)
    pillar_url = PILLARS[my_pillar] if PILLARS.get(my_pillar) != path else "/"
    if ptype == "pillar":
        pillar_url = "/"
    rep.add("N1", pillar_url in paths, f"links up to its pillar ({my_pillar}, {pillar_url})")
    ip = [p for p in paths if p]
    if related_songs is None and ptype in ("band", "artist") and subject:
        stories = song_story_pages()
        st = " " + " ".join(tok(subject)) + " "
        related_songs = [p for p, h1 in stories.items() if st in " " + " ".join(tok(h1)) + " "]
    related_songs = [internal_path(p) for p in (related_songs or [])]
    missing = [p for p in related_songs if p not in ip]
    rep.add("N2", not missing, f"links down to every related song story ({len(related_songs)} found)"
            + (f": missing {missing[:4]}" if missing else ""))
    if ptype == "pillar":
        # a pillar sits under Home; its sideways links are the other pillars
        side = sorted({p for p in ip if p in PILLARS.values() and p not in ("/", path)})
    else:
        side = sorted({p for p in ip if p.startswith("/blog/") and p.count("/") == 4 and p != path and p != pillar_url
                       and p not in related_songs and pillar_for(p) == my_pillar and p not in PILLARS.values()})
    rep.add("N3", 2 <= len(side) <= 4, f"{len(side)} sideways link(s) within {my_pillar} (need 2 to 4): {side}")
    rt = [p for p in ip if p.split("?")[0] == "/radio/" or p.split("?")[0] in TOOLS]
    rep.add("N4", len(rt) >= 1, f"radio/tool link: {sorted(set(rt)) or 'none'}")
    seen, dup = set(), set()
    for p in ip:
        (dup if p in seen else seen).add(p)
    rep.add("N5", not dup, "each internal target once" + (f": repeated {sorted(dup)}" if dup else ""))
    cra = [h for h in links if "classicrockartists.com" in h.lower()] + (["(text)"] if "classicrockartists.com" in html.lower() else [])
    rep.add("N6", not cra, "no classicrockartists.com link" + (f": {cra[0]}" if cra else ""))

    # X1 schema
    has_video = bool(re.search(r"youtube(?:-nocookie)?\.com/embed/", html)) or "listen-btn" in html
    check_schema(html, ptype, has_video, rep)
    return rep


# ---------------------------------------------------------------- modes
def run_registered(paths=None):
    reg = load_registry()
    ok = True
    for rel, cfg in reg.items():
        if paths is not None and rel not in paths:
            continue
        f = ROOT / rel
        rep = check(f, cfg["keyword"], cfg["type"], cfg.get("subject"), cfg.get("secondary", []),
                    cfg.get("related_songs"), cfg.get("pillar"))
        rep.print(rel)
        ok = ok and rep.passed
    if not reg:
        print("No pages registered yet (scripts/article_standard_pages.json).")
    return ok


# Charlie's decision of Nov 9 (2026-11-09): keep the classicrockartists.com links (and the author
# Person schema sameAs) on these two pages only. The rule still applies to every article and every
# other page. Do not add to this list without Charlie's explicit OK.
CRA_EXEMPT = {"pages/about.html", "about/author/index.html"}


def site_scan():
    bad = []
    for f in ROOT.rglob("*.html"):
        if any(part.startswith(".") for part in f.relative_to(ROOT).parts):
            continue
        if f.relative_to(ROOT).as_posix() in CRA_EXEMPT:
            continue
        if re.search(r"classicrockartists\.com", f.read_text(encoding="utf-8", errors="ignore"), re.I):
            bad.append(f.relative_to(ROOT).as_posix())
    for b in bad:
        print(f"FAIL {b}: links to or names classicrockartists.com")
    print("Site scan:", "PASS" if not bad else "FAIL")
    return not bad


def staged():
    """Pre-commit: registered pages must pass; a NEW page under blog/, pages/ or radio/ must be registered."""
    out = subprocess.run(["git", "diff", "--cached", "--name-status", "--diff-filter=AM"], cwd=ROOT, timeout=60,
                         capture_output=True, text=True).stdout
    reg = load_registry()
    ok, check_paths = True, set()
    for line in out.splitlines():
        status, name = line.split("\t", 1)
        if not name.endswith(".html"):
            continue
        if name not in CRA_EXEMPT and "classicrockartists.com" in (ROOT / name).read_text(encoding="utf-8", errors="ignore").lower():
            print(f"FAIL {name}: links to or names classicrockartists.com")
            ok = False
        if name in reg:
            check_paths.add(name)
        elif status == "A" and re.match(r"^(blog/[^/]+/[^/]+/index\.html|pages/[^/]+\.html|radio/index\.html)$", name):
            print(f"FAIL {name}: new page is not registered in scripts/article_standard_pages.json, so the Article "
                  f"Standard gate cannot run on it. Register it (type, keyword, subject) and pass check_standard.py.")
            ok = False
    if "scripts/article_standard_pages.json" in out:
        check_paths |= set(reg)
    if check_paths:
        ok = run_registered(check_paths) and ok
    return ok


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("page", nargs="?")
    ap.add_argument("--keyword")
    ap.add_argument("--type", choices=TYPES)
    ap.add_argument("--subject")
    ap.add_argument("--secondary", default="")
    ap.add_argument("--related-songs")
    ap.add_argument("--pillar", choices=list(PILLARS))
    ap.add_argument("--registered", action="store_true")
    ap.add_argument("--site", action="store_true")
    ap.add_argument("--staged", action="store_true")
    a = ap.parse_args()
    if a.staged:
        return 0 if staged() else 1
    if a.site:
        return 0 if site_scan() else 1
    if a.registered:
        return 0 if run_registered() else 1
    if not a.page:
        ap.error("give a page, or --registered / --site / --staged")
    rel = Path(a.page).resolve().relative_to(ROOT).as_posix()
    cfg = load_registry().get(rel, {})
    keyword, ptype = a.keyword or cfg.get("keyword"), a.type or cfg.get("type")
    if not keyword or not ptype:
        ap.error("page not registered: pass --keyword and --type")
    rel_songs = a.related_songs.split(",") if a.related_songs else cfg.get("related_songs")
    rep = check(a.page, keyword, ptype, a.subject or cfg.get("subject"),
                [s.strip() for s in a.secondary.split(",") if s.strip()] or cfg.get("secondary", []),
                rel_songs, a.pillar or cfg.get("pillar"))
    rep.print(f"{rel} ({ptype}, \"{keyword}\")")
    return 0 if rep.passed else 1


if __name__ == "__main__":
    sys.exit(main())
