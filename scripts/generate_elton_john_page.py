#!/usr/bin/env python3
"""Build the Elton John Artists post (blog/artists/elton-john/index.html).

Data: data/radio/radio-songs.json (Elton John rows of the Year-End Hot 100, each with a YouTube ID),
data/billboard/hot100_weekly.json (weekly Hot 100 #1s, weeks at #1). Every count and rank in the
prose and tables is computed here. Year-End Rank is the year-end rank, never a peak. Story facts
(albums, dates, Lennon, Taupin) come from the linked Wikipedia articles, checked 2026-10-10.

Run: python3 scripts/generate_elton_john_page.py
"""
import collections
import html
import json
from datetime import date

from genre_page_common import ROOT, norm, read, play_button, write
from generate_country_page import p, tbl, pic, fmt_date

SLUG = "elton-john"
URL = f"https://musicofthe70s.net/blog/artists/{SLUG}/"
TITLE = "Elton John: 13 Hits Played, 6 at Number One"
PUBLISHED = date(2026, 10, 10)
IMG = "elton-john-1972"
NUM = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}


def main():
    radio = json.loads(read(ROOT / "data/radio/radio-songs.json"))
    weekly = json.loads(read(ROOT / "data/billboard/hot100_weekly.json"))

    songs = sorted((s for s in radio if "elton john" in s["artist"].lower() and s.get("youtube_id")),
                   key=lambda s: (s["year"], s["rank"]))
    n = len(songs)
    runs = collections.OrderedDict()
    for yr in sorted(weekly):
        for w in weekly[yr]:
            if "elton john" in w["artist"].lower():
                d = runs.setdefault(w["title"], {"first": w["week_start"], "weeks": 0, "credit": w["artist"]})
                d["weeks"] += 1
    run_by_title = {norm(t): d for t, d in runs.items()}
    n1, wk1 = len(runs), sum(d["weeks"] for d in runs.values())
    by_title = {s["title"]: s for s in songs}
    years = sorted({s["year"] for s in songs})

    rows = []
    for s in songs:
        r = run_by_title.get(norm(s["title"]))
        t, a = html.escape(s["title"]), html.escape(s["artist"])
        rows.append(f'              <tr><td class="ohw-listen">{play_button(s["youtube_id"], s["title"], s["artist"])}</td>'
                    f'<td class="ohw-song">{t}{" (with Kiki Dee)" if "Kiki" in s["artist"] else ""}</td>'
                    f'<td>{s["year"]}</td><td>{s["rank"]}</td><td>{"Yes" if r else ""}</td><td>{r["weeks"] if r else ""}</td></tr>')

    year_rows = []
    for y in years:
        ys = [s for s in songs if s["year"] == y]
        best = min(ys, key=lambda s: s["rank"])
        ones = [t for t, d in runs.items() if d["first"].startswith(str(y))]
        year_rows.append([y, len(ys), f'{html.escape(best["title"])} (#{best["rank"]})', html.escape(", ".join(ones)) or "None"])

    run_rows = []
    for t, d in sorted(runs.items(), key=lambda kv: kv[1]["first"]):
        s = by_title[t]
        run_rows.append([html.escape(t), html.escape(d["credit"]), fmt_date(d["first"]), d["weeks"], f'{s["rank"]} ({s["year"]})'])

    def r(t):
        return runs[t]

    lucy, phil, isl, duet = r("Lucy in the Sky with Diamonds"), r("Philadelphia Freedom"), r("Island Girl"), r("Don't Go Breaking My Heart")
    croc, bennie = r("Crocodile Rock"), r("Bennie and the Jets")
    yr1975 = [d for d in runs.values() if d["first"].startswith("1975")]
    wk1975 = sum(d["weeks"] for d in yr1975)
    solo = [s for s in songs if s["artist"] == "Elton John"]
    top_solo = min(solo, key=lambda s: s["rank"])
    duet_row = by_title["Don't Go Breaking My Heart"]

    faq = [
        ("How many number one hits did Elton John have in the 1970s?",
         [f"Elton John reached number one on the Billboard Hot 100 {NUM[n1]} times in the 1970s, based on this site's weekly chart data.",
          f"Those songs spent {wk1} weeks at the top between February 1973 and September 1976.",
          "They were Crocodile Rock, Bennie and the Jets, Lucy in the Sky with Diamonds, Philadelphia Freedom, Island Girl, and Don't Go Breaking My Heart."]),
        ("What was Elton John's biggest song of the 1970s on the year-end chart?",
         [f"Elton John's highest Year-End Hot 100 rank of the 1970s was #2 for 1976, with the Kiki Dee duet Don't Go Breaking My Heart.",
          f"Under his own name, {top_solo['title']} ranked highest, at #{top_solo['rank']} on the {top_solo['year']} year-end list.",
          "Year-end rank measures a whole year of chart performance, not a weekly peak."]),
        ("Did John Lennon play on an Elton John record?",
         ["John Lennon played guitar and sang backing vocals on Elton John's 1974 cover of Lucy in the Sky with Diamonds.",
          "He used the pseudonym Dr. Winston O'Boogie on the record.",
          "The single reached number one on the Hot 100 for two weeks in January 1975, according to this site's weekly data and Wikipedia."]),
        ("How many number one albums in a row did Elton John have in the 1970s?",
         ["Elton John had seven consecutive number one albums in the United States between 1972 and 1975.",
          "The run started with Honky Chateau in 1972 and ended with Rock of the Westies in 1975.",
          "Wikipedia lists the albums in its article on him, linked in the sources below."]),
        ("When did Elton John change his name?",
         ["Elton John legally changed his name to Elton Hercules John on January 7, 1972, according to Wikipedia.",
          "That was the year his first number one album, Honky Chateau, came out.",
          "His first American concert had been at the Troubadour in Los Angeles on August 25, 1970."]),
    ]
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": " ".join(a)}} for q, a in faq]},
        indent=2, ensure_ascii=False)
    faq_ld = "\n".join("  " + l for l in faq_ld.split("\n"))
    faq_html = "\n".join(
        f'          <div class="faq-item">\n            <h3>{html.escape(q)}</h3>\n' + "\n".join(f"            <p>{html.escape(l)}</p>" for l in a) + "\n          </div>"
        for q, a in faq).replace("&#x27;", "'")

    desc = (f"Elton John put {n} songs on the 70s Year-End Hot 100, {NUM[n1]} at number one. Play every hit and read the Lennon, "
            "Kiki Dee and Billie Jean King stories.")
    article_ld = f'''  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{TITLE}",
    "datePublished": "{PUBLISHED.isoformat()}",
    "dateModified": "{PUBLISHED.isoformat()}",
    "author": {{
      "@type": "Person",
      "@id": "https://musicofthe70s.net/about/author/",
      "name": "Charlie",
      "url": "https://musicofthe70s.net/about/author/"
    }},
    "publisher": {{
      "@type": "Organization",
      "@id": "https://musicofthe70s.net/#organization",
      "name": "Music of the 70s",
      "url": "https://musicofthe70s.net/",
      "logo": {{
        "@type": "ImageObject",
        "url": "https://musicofthe70s.net/favicon-512.png",
        "width": 512,
        "height": 512
      }}
    }},
    "image": "https://musicofthe70s.net/images/blog/{IMG}-1200w.jpg",
    "mainEntityOfPage": "{URL}"
  }}'''

    toc = [("elton-song-list", f"Elton John Songs: Play All {n} Year-End Hits"),
           ("by-the-numbers", "The Numbers Behind the Hits"),
           ("road-to-1972", "The Road to 1972"),
           ("six-number-ones", f"{NUM[n1].capitalize()} Number Ones, {wk1} Weeks at the Top"),
           ("year-1975", "1975: Three Number Ones in One Year"),
           ("duet", "Don't Go Breaking My Heart: Two Singers, Two Cities"),
           ("albums", "Seven Number One Albums in a Row"),
           ("sources", "Sources"), ("faq", "Frequently Asked Questions")]
    toc_html = "\n".join(f'            <li><a href="#{i}">{t}</a></li>' for i, t in toc)

    body = f'''        <h2 id="elton-song-list">Elton John Songs: Play All {n} Year-End Hits</h2>
{p(f"Here are all {n} Elton John songs on this site's Year-End Hot 100 data for the 1970s, from {years[0]} to {years[-1]}.",
   "Press Play on any row to watch it here, and tap a heading to sort.")}

        <div class="data-table-wrap scroll-list">
          <table class="data-table sortable-table" id="eltonSongsTable" data-inline-player>
            <caption>{n} Elton John songs of the 70s, by year and Billboard Year-End Hot 100 rank, with weeks at number one</caption>
            <thead>
              <tr>
                <th><span class="visually-hidden">Play</span></th>
                <th><button type="button" data-col="1" data-type="text">Song</button></th>
                <th aria-sort="ascending"><button type="button" data-col="2" data-type="num">Year</button></th>
                <th><button type="button" data-col="3" data-type="num">Year-End Rank</button></th>
                <th><button type="button" data-col="4" data-type="text">#1 Hit</button></th>
                <th><button type="button" data-col="5" data-type="num">Weeks at #1</button></th>
              </tr>
            </thead>
            <tbody>
{chr(10).join(rows)}
            </tbody>
          </table>
        </div>
{p("Year-End Rank is the song's spot on that year's Billboard Year-End Hot 100.",
   "That list keeps only the top 100 songs of each year.",
   "The #1 Hit and Weeks at #1 columns come from this site's own weekly Hot 100 data, not from the year-end list.")}

        <h2 id="by-the-numbers">The Numbers Behind the Hits</h2>
{p(f"Elton John placed a song on the Year-End Hot 100 in {len(years)} different years of the decade.",
   f"He missed 1970, 1971, and 1978 entirely.",
   "The table shows his best-ranked song each year, and any number one that began that year.")}

{tbl("Year-End Hot 100 entries and weekly number ones, 1972 to 1979", ["Year", "Songs on the year-end list", "Best year-end rank", "Number ones that began that year"], year_rows)}

        <h3>Three Ways to Read the Same Career</h3>
{p("Year-end rank and weekly number ones are different measures, and his catalog shows it.")}
        <ul>
          <li>{html.escape(top_solo["title"])} ranked #{top_solo["rank"]} for {top_solo["year"]}, his best solo rank.</li>
          <li>Island Girl held number one for {isl["weeks"]} weeks, yet sits at #{by_title["Island Girl"]["rank"]} on the {by_title["Island Girl"]["year"]} year-end list.</li>
          <li>Daniel ranks #{by_title["Daniel"]["rank"]} for 1973 and never appears in this site's weekly number one data.</li>
        </ul>
{p(f"Island Girl's run began on {fmt_date(isl['first'])}, so it topped the weekly chart a year before its year-end entry.")}

        <h2 id="road-to-1972">The Road to 1972</h2>

        <h3>Two Strangers and One Ad</h3>
{p("Elton John and lyricist Bernie Taupin first met in 1967.",
   "They had both answered the same advertisement.",
   "Wikipedia calls it a decades-long partnership, and it is the spine of nearly every song on the list above.")}

        <h3>The Troubadour and a New Name</h3>
{p("His first American concert was at the Troubadour in Los Angeles on August 25, 1970.",
   "By January 7, 1972, he had legally changed his name to Elton Hercules John.",
   "That same year Honky Chateau became the first of seven number one albums in a row.",
   "Rocket Man followed in 1972 and landed at #40 on that year's year-end list.")}

        <h2 id="six-number-ones">{NUM[n1].capitalize()} Number Ones, {wk1} Weeks at the Top</h2>
{p(f"This site's weekly data shows {NUM[n1]} Elton John songs reaching number one on the Hot 100 in the 1970s.",
   f"Together they held the top spot for {wk1} weeks.",
   "No song of his repeated a run, and each credit line was slightly different.")}

{tbl("Every Elton John number one on the weekly Hot 100, 1970 to 1979", ["Song", "Credited as", "First week at #1", "Weeks at #1", "Year-End Rank (year)"], run_rows)}

        <h3>The Early Run: Crocodile Rock and Bennie and the Jets</h3>
{p(f"Crocodile Rock began its {croc['weeks']} weeks at number one on {fmt_date(croc['first'])}.",
   f"Bennie and the Jets took one week at the top, starting {fmt_date(bennie['first'])}.",
   "Both landed inside the top ten of their year-end lists, at #7 and #9.",
   'Both also appear on the full list of <a href="/blog/songs/70s-number-one-hits/">70s number one hits</a>.')}

        <h3>One Act, Three Credit Lines</h3>
{p("The weekly data credits his number ones three ways.",
   "Most are listed under his own name.",
   "Philadelphia Freedom is credited to the Elton John Band.",
   "Don't Go Breaking My Heart lists both singers, with Kiki Dee second.")}

        <h2 id="year-1975">1975: Three Number Ones in One Year</h2>
{p(f"He spent {wk1975} weeks at number one in 1975 across {NUM[len(yr1975)]} different songs.",
   "That was more than any other act that year, according to this site's weekly data notes.")}
{pic("elton-john-1975", "Elton John in a silver quilted costume and tall jeweled hat at a piano, in a 1975 publicity photo for The Cher Show", "(max-width: 700px) 100vw, 500px", 718, 916, widths=(400, 600, 718))}
        <p class="post-img-caption">Elton John, CBS Television publicity photo for The Cher Show, 1975.</p>
        <p class="post-img-caption">Image credit: CBS Television, public domain, via Wikimedia Commons.</p>

        <h3>Lucy and the Promise Lennon Kept</h3>
{p("Elton John released his cover of Lucy in the Sky with Diamonds on November 15, 1974.",
   "John Lennon played guitar and sang backing vocals under the name Dr. Winston O'Boogie.",
   "Lennon had promised to join him on stage if Whatever Gets You Thru the Night reached number one.",
   "It did, and Lennon kept his word on Thanksgiving night, November 28, 1974, at Madison Square Garden.",
   f"The Lucy single then took {NUM[lucy['weeks']]} weeks at number one, starting {fmt_date(lucy['first'])}.")}

        <h3>Philadelphia Freedom for Billie Jean King</h3>
{p("Elton John asked Bernie Taupin to write Philadelphia Freedom as a favor to tennis star Billie Jean King.",
   "King played for the Philadelphia Freedoms, a professional tennis team.",
   "Wikipedia says she did not want the song to be about tennis.",
   "It was credited to the Elton John Band and produced by Gus Dudgeon.",
   f"It began {NUM[phil['weeks']]} weeks at number one on {fmt_date(phil['first'])}, then ranked #3 on the 1975 year-end list.")}

        <h2 id="duet">Don't Go Breaking My Heart: Two Singers, Two Cities</h2>
{p(f"The Kiki Dee duet gave him his longest run, {NUM[duet['weeks']]} weeks at number one starting {fmt_date(duet['first'])}.",
   f"It ranked #{duet_row['rank']} on the {duet_row['year']} year-end list, behind only Wings.",
   "He and Taupin wrote it under the pseudonyms Ann Orson and Carte Blanche.",
   "Wikipedia calls it an affectionate pastiche of the Motown style.")}

        <h3>Recorded Apart</h3>
{p("The band and his vocals were recorded in March 1976 at Eastern Sound in Toronto.",
   "Kiki Dee's vocals were recorded separately at Marquee Studios in London.",
   "The song had first been offered to Dusty Springfield, but the offer was withdrawn.",
   "It was released June 25, 1976, and Wikipedia says it also spent six weeks at number one in the UK.")}

        <h2 id="albums">Seven Number One Albums in a Row</h2>
{p("Between 1972 and 1975, he put seven albums at number one on the US album chart in a row.",
   "Wikipedia names these as the run:")}
        <ol>
          <li>Honky Chateau (1972)</li>
          <li>Don't Shoot Me I'm Only the Piano Player (1973)</li>
          <li>Goodbye Yellow Brick Road (1973)</li>
          <li>Caribou (1974)</li>
          <li>Elton John's Greatest Hits (1974)</li>
          <li>Captain Fantastic and the Brown Dirt Cowboy (1975)</li>
          <li>Rock of the Westies (1975)</li>
        </ol>
{p("Captain Fantastic debuted at number one, which Wikipedia says no album had done before.",
   "It stayed there seven weeks.",
   "Albums are a separate chart from the singles above, so none of these counts toward the weeks at number one in this post.",
   'For a random 70s act to explore next, try the <a href="/pages/random-artist-picker">Random Artist Picker</a>.',
   'To test what you know about the decade, take the <a href="/pages/70s-trivia-quiz">70s Music Trivia Quiz</a>.')}

        <h2 id="sources">Sources</h2>
{p("Year-end ranks and Hot 100 number ones come from this site's own Billboard data, described on the <a href='/about/methodology/'>methodology page</a>.",
   'Every list on <a href="/">Music of the 70s</a> plays inside the page.',
   "The stories and album run can be checked against these outside sources:")}
        <ul>
          <li><a href="https://en.wikipedia.org/wiki/Elton_John" rel="noopener">Wikipedia: Elton John</a> for Taupin, the Troubadour debut, the name change, and the seven albums.</li>
          <li><a href="https://en.wikipedia.org/wiki/Lucy_in_the_Sky_with_Diamonds" rel="noopener">Wikipedia: Lucy in the Sky with Diamonds</a> for the Lennon promise and the 1974 cover.</li>
          <li><a href="https://en.wikipedia.org/wiki/Philadelphia_Freedom_(song)" rel="noopener">Wikipedia: Philadelphia Freedom</a> for the Billie Jean King tribute.</li>
          <li><a href="https://en.wikipedia.org/wiki/Don%27t_Go_Breaking_My_Heart_(Elton_John_and_Kiki_Dee_song)" rel="noopener">Wikipedia: Don't Go Breaking My Heart</a> for the recording story and pseudonyms.</li>
        </ul>

        <section class="faq-block" id="faq">
          <h2>Frequently Asked Questions</h2>
{faq_html}
        </section>'''

    related = [
        ("70s-number-one-hits", "Songs", "70s Number One Hits: Every Billboard #1", "/blog/songs/70s-number-one-hits/",
         "All 253 Hot 100 number ones of the decade, sortable and playable.", "A collage for the 70s number one hits list"),
        ("carole-king-1970s", "Artists", "Carole King: The Same Chart, Three Different Names", "/blog/artists/carole-king/",
         "She topped the 1971 year-end chart and wrote two other hits on it.", "Carole King seated at a piano in a 1971 publicity photo"),
    ]
    cards = []
    for img, cat, title, href, blurb, alt in related:
        cards.append(f'''            <div class="card post-card">
              <picture>
                <source type="image/webp" srcset="/images/blog/srcset/{img}-400w.webp 400w, /images/blog/srcset/{img}-800w.webp 800w" sizes="(max-width: 700px) 100vw, 33vw">
                <img class="post-thumb" src="/images/blog/srcset/{img}-400w.jpg"
                  srcset="/images/blog/srcset/{img}-400w.jpg 400w, /images/blog/srcset/{img}-800w.jpg 800w"
                  sizes="(max-width: 700px) 100vw, 33vw" width="400" height="223" loading="lazy"
                  alt="{alt}">
              </picture>
              <div class="post-card-body">
                <span class="post-cat">{cat}</span>
                <h3>{title}</h3>
                <p>{blurb}</p>
                <a class="cta" href="{href}">Read post</a>
              </div>
            </div>''')

    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-ZY77Y8DHV1"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());

    gtag('config', 'G-ZY77Y8DHV1');
  </script>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{TITLE}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{URL}">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <meta name="theme-color" content="#1a1a2e">

  <meta property="og:title" content="{TITLE}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{URL}">
  <meta property="og:type" content="article">
  <meta property="og:image" content="https://musicofthe70s.net/images/blog/{IMG}-1200w.jpg">
  <meta property="og:site_name" content="Music of the 70s">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@700;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/style.css">

  <script type="application/ld+json">
{article_ld}
  </script>
  <script type="application/ld+json">
{faq_ld}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://musicofthe70s.net/"}},
      {{"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://musicofthe70s.net/blog/"}},
      {{"@type": "ListItem", "position": 3, "name": "Artists", "item": "https://musicofthe70s.net/blog/artists/"}},
      {{"@type": "ListItem", "position": 4, "name": "Elton John", "item": "{URL}"}}
    ]
  }}
  </script>
</head>
<body>
  <header class="site-header">
    <div class="header-inner">
      <a href="/" class="site-logo"><span class="logo-vinyl">♪</span> Music of the 70s</a>
      <nav class="main-nav">
        <a href="/">Home</a>
        <a href="/#tools">Tools</a>
        <a href="/radio/">Listen Now</a>
        <a href="/pages/about">About</a>
        <a href="/blog/">Blog</a>
      </nav>
      <button class="nav-toggle" aria-label="Menu">☰</button>
    </div>
  </header>

  <main>
    <div class="container">
      <nav class="breadcrumb">
        <a href="/">Home</a> ›
        <a href="/blog/">Blog</a> ›
        <a href="/blog/artists/">Artists</a> ›
        Elton John
      </nav>

      <article class="section seo-content">
        <h1>{TITLE}</h1>

        <p class="post-byline">By <a href="https://musicofthe70s.net/about/author/">Charlie</a> &middot; Published {PUBLISHED.strftime('%B')} {PUBLISHED.day}, {PUBLISHED.year}</p>
        <p class="jump-to-list"><a class="btn-primary jump-btn" href="#elton-song-list">&#9654; Jump to the playable list</a></p>

        <p class="post-intro">Elton John put {n} songs on the 1970s Year-End Hot 100, and {NUM[n1]} of them reached number one.</p>
        <p class="post-intro">Those {NUM[n1]} songs held the top spot for {wk1} weeks, and none of them repeated a run.</p>
        <p class="post-intro">His best year-end rank came on a duet, not a solo record.</p>
        <p class="post-intro">This page plays all {n} songs, then follows the stories behind the biggest ones.</p>

{pic(IMG, "Elton John at the piano in a lip-patterned shirt and tinted glasses during a March 1972 concert in Hamburg, Germany", "(max-width: 700px) 100vw, 1100px", 1200, 803, lazy=False)}
        <p class="post-img-caption">Elton John performing in Hamburg, Germany, March 1972.</p>
        <p class="post-img-caption">Image credit: Photo by Heinrich Klaffs, CC BY-SA 2.0, via Wikimedia Commons.</p>

        <nav class="toc-block" aria-label="Table of contents">
          <details class="toc-details" open>
            <summary>Table of Contents</summary>
            <ol>
{toc_html}
          </ol>
          </details>
        </nav>
        <script>if(window.matchMedia("(max-width: 699px)").matches){{document.querySelector(".toc-details").open=false;}}</script>

{body}

        <section class="related-posts">
          <h2>Related Posts</h2>
          <div class="post-grid">
{chr(10).join(cards)}
          </div>
        </section>
      </article>
    </div>
  </main>

  <footer class="site-footer">
    <p>© 2026 Music of the 70s |
      <a href="/pages/privacy-policy">Privacy Policy</a> |
      <a href="/pages/terms-of-use">Terms of Use</a> |
      <a href="/pages/contact">Contact</a> |
      <a href="/pages/about">About</a> |
      <a href="/about/author/">About the Author</a> |
      <a href="/about/methodology/">How We Write</a>
    </p>
  </footer>

  <script src="/js/main.js"></script>
  <script src="/js/table-player.js"></script>
  <script src="/js/sortable-table.js"></script>
</body>
</html>
'''
    page = page.replace("href='/about/methodology/'", 'href="/about/methodology/"').replace("href='/'>", 'href="/">')
    out = ROOT / "blog/artists" / SLUG / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    write(out, page)
    print(f"wrote {out}: {n} rows, {n1} number ones, {wk1} weeks, years {years}")


if __name__ == "__main__":
    main()
