#!/usr/bin/env python3
"""
Runs the CLAUDE.md prose/SEO checklist against a blog post automatically:
word count, keyword density, sentence-length distribution, em-dash count,
banned words, FAQ schema/visible match, heading hierarchy, title/meta
length, keyword placement (title/meta/first-100-words/H2).

Built after the same manual checks (density, sentence length, em-dash)
were re-run by hand on four straight posts. Run this instead of
re-deriving the numbers from scratch each time.

Usage: python3 scripts/verify_post.py <path/to/post/index.html> "<focus keyword>"
"""
import json
import re
import sys

BANNED_WORDS = ["delve", "tapestry", "testament", "vibrant", "unveil",
                "groundbreaking", "seminal", "journey", "realm", "haunting",
                "sonic landscape", "stands the test of time"]


def load(path):
    return open(path, encoding="utf-8").read()


def get_article(html):
    m = re.search(r"<article.*?</article>", html, re.S)
    if not m:
        sys.exit("ERROR: no <article> found")
    return m.group(0)


def strip_related_posts(article):
    idx = article.find('<section class="related-posts">')
    return article if idx == -1 else article[:idx]


def clean_text(html_fragment):
    text = re.sub(r"<[^>]+>", " ", html_fragment)
    text = text.replace("&amp;", "&")
    return re.sub(r"\s+", " ", text).strip()


def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: verify_post.py <path/to/post/index.html> \"<focus keyword>\"")
    path, keyword = sys.argv[1], sys.argv[2].lower()
    html = load(path)
    article = get_article(html)
    body_only = strip_related_posts(article)

    text = clean_text(article)
    words = text.split()
    wc = len(words)
    kw_count = text.lower().count(keyword)
    density = kw_count / wc * 100 if wc else 0

    print(f"=== {path} ===")
    print(f"Word count: {wc}  {'PASS' if wc >= 1200 else 'FAIL (<1200)'}")
    print(f"Keyword '{keyword}': {kw_count} uses, density {density:.3f}%  "
          f"{'PASS' if 0.5 <= density <= 2.0 else 'FAIL (outside 0.5-2.0%)' if kw_count else 'FAIL (zero uses)'}")

    # sentence length, on body only (excludes reused related-posts card blurb)
    para_texts = re.findall(r"<p[^>]*>(.*?)</p>", body_only, re.S)
    sentences = [re.sub(r"<[^>]+>", "", p).strip().replace("&amp;", "&") for p in para_texts if p.strip()]
    long_sentences = [s for s in sentences if len(s.split()) >= 20]
    pct_under_20 = (1 - len(long_sentences) / len(sentences)) * 100 if sentences else 0
    print(f"Sentences: {len(sentences)}, {pct_under_20:.1f}% under 20 words  "
          f"{'PASS' if pct_under_20 >= 75 else 'FAIL (<75%)'}")
    for s in long_sentences:
        print(f"  LONG ({len(s.split())}w): {s[:90]}")

    # em-dash: allowed only as a numeric separator inside a bulleted <li>
    # (e.g. "Song Title" — #36), never in flowing prose <p> sentences.
    li_items = re.findall(r"<li[^>]*>(.*?)</li>", article, re.S)
    em_dash_in_li = sum(item.count("—") for item in li_items)
    em_dash_total = article.count("—")
    em_dash_outside_li = em_dash_total - em_dash_in_li
    print(f"Em-dashes: {em_dash_total} total ({em_dash_in_li} inside <li> numeric separators, "
          f"{em_dash_outside_li} elsewhere)  {'PASS' if em_dash_outside_li == 0 else 'FAIL (em-dash in prose)'}")

    # banned words
    found_banned = [b for b in BANNED_WORDS if b in text.lower()]
    print(f"Banned words: {found_banned or 'none'}  {'PASS' if not found_banned else 'FAIL'}")

    # keyword placement
    title_m = re.search(r"<title>(.*?)</title>", html)
    desc_m = re.search(r'<meta name="description" content="(.*?)">', html)
    title = title_m.group(1) if title_m else ""
    desc = desc_m.group(1) if desc_m else ""
    first100 = " ".join(words[:100]).lower()
    h2s = re.findall(r"<h2[^>]*>(.*?)</h2>", article)
    h2_has_kw = any(keyword in h.lower() for h in h2s)

    print(f"\nTitle ({len(title)} chars, {'PASS <=60' if len(title) <= 60 else 'FAIL >60'}): {title}")
    print(f"  keyword in title: {'PASS' if keyword in title.lower() else 'FAIL'}")
    print(f"Meta description ({len(desc)} chars, {'PASS <=155' if len(desc) <= 155 else 'FAIL >155'}): {desc}")
    print(f"  keyword in meta description: {'PASS' if keyword in desc.lower() else 'FAIL'}")
    print(f"Keyword in first 100 words: {'PASS' if keyword in first100 else 'FAIL'}")
    print(f"Keyword in an H2: {'PASS' if h2_has_kw else 'FAIL'}")

    # consecutive-sentence keyword check
    kw_idx = [i for i, s in enumerate(sentences) if keyword in s.lower()]
    consecutive = any(b - a == 1 for a, b in zip(kw_idx, kw_idx[1:]))
    print(f"Keyword in consecutive sentences: {consecutive}  {'FAIL' if consecutive else 'PASS'}")

    # heading hierarchy (no skipped levels going down)
    heads = re.findall(r"<(h[1-4])[ >]", article)
    levels = [int(h[1]) for h in heads]
    skipped = any(b - a > 1 for a, b in zip(levels, levels[1:]) if b > a)
    print(f"Heading sequence: {heads}")
    print(f"Heading hierarchy clean: {'PASS' if not skipped else 'FAIL (skipped level)'}")

    # FAQ schema vs visible match
    scripts = re.findall(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', html, re.S)
    faq_obj = None
    for s in scripts:
        obj = json.loads(s)
        if obj.get("@type") == "FAQPage":
            faq_obj = obj
            break
    print("\n--- FAQ schema vs visible ---")
    if not faq_obj:
        print("FAIL: no FAQPage schema found")
    else:
        all_ok = True
        for qa in faq_obj["mainEntity"]:
            q, a = qa["name"], qa["acceptedAnswer"]["text"]
            idx = html.find(f"<h3>{q}</h3>")
            if idx == -1:
                print(f"FAIL missing visible question: {q}")
                all_ok = False
                continue
            chunk = html[idx: idx + 3000]
            chunk = chunk[:chunk.find("</div>")]
            visible = " ".join(re.sub(r"<[^>]+>", "", p).strip() for p in re.findall(r"<p>(.*?)</p>", chunk, re.S))
            visible = re.sub(r"\s+", " ", visible).replace("&amp;", "&")
            a_norm = re.sub(r"\s+", " ", a)
            wc_ans = len(a.split())
            starts_yesno = a.strip().split()[0].rstrip(".").lower() in ("yes", "no")
            ok = visible == a_norm
            all_ok = all_ok and ok and 40 <= wc_ans <= 70 and not starts_yesno
            print(f"{'OK' if ok else 'MISMATCH'} ({wc_ans}w, "
                  f"{'startsYes/No FAIL' if starts_yesno else 'opener OK'}, "
                  f"{'len OK' if 40 <= wc_ans <= 70 else 'len FAIL'}): {q}")
        print(f"FAQ overall: {'PASS' if all_ok else 'FAIL'}")

    # internal links found
    links = re.findall(r'<a href="([^"]+)"', article)
    print(f"\nLinks in article: {links}")


if __name__ == "__main__":
    main()
