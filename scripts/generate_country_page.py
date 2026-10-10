#!/usr/bin/env python3
"""Build the 70s Country Songs pillar page (blog/genres/70s-country-songs/index.html).

Data: data/radio/radio-songs.json (country-tagged songs on a Year-End Hot 100, only rows
with a YouTube ID), data/billboard/country.json (weekly Hot Country Singles #1s, 1970-1979,
from Wikipedia's per-year lists), data/billboard/hot100_weekly.json (Hot 100 #1 flag).
Every number in the prose and tables is computed here, never typed. Year-End Rank is the
year-end rank, never a peak. Country chart weeks are counted from the weekly data.

Run: python3 scripts/generate_country_page.py
"""
import collections
import html
import json
import re
from datetime import date

from genre_page_common import ROOT, norm, read, play_button, song_post_slug, write

SLUG = "70s-country-songs"
URL = f"https://musicofthe70s.net/blog/genres/{SLUG}/"
TITLE = "70s Country Songs: Play 60 Hits, See Who Ruled #1"
DESC = "70s country songs, played here: 60 hits to watch, plus the acts that really ruled Billboard's country chart, and the few that crossed over."
PUBLISHED = date(2026, 10, 10)
IMG = "dolly-parton-1970s"


def p(*lines, indent=8):
    return "\n".join(" " * indent + f"<p>{l}</p>" for l in lines)


def tbl(caption, head, rows, indent=8):
    sp = " " * indent
    th = "".join(f"<th>{h}</th>" for h in head)
    body = "\n".join(f"{sp}    <tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return (f'{sp}<div class="data-table-wrap">\n{sp}  <table class="data-table">\n{sp}    <caption>{caption}</caption>\n'
            f'{sp}    <thead><tr>{th}</tr></thead>\n{sp}    <tbody>\n{body}\n{sp}    </tbody>\n{sp}  </table>\n{sp}</div>')


def pic(name, alt, sizes, w, h, lazy=True, widths=(400, 800, 1200), indent=8):
    sp = " " * indent
    srcset_w = ", ".join(f"/images/blog/srcset/{name}-{x}w.webp {x}w" for x in widths if x != 1000)
    srcset_j = ", ".join([f"/images/blog/srcset/{name}-{x}w.jpg {x}w" for x in widths[:-1]] + [f"/images/blog/{name}-{widths[-1]}w.jpg {widths[-1]}w"])
    cls = ' class="post-featured-img"' if not lazy else ""
    return (f'{sp}<picture>\n{sp}  <source type="image/webp" srcset="{srcset_w}" sizes="{sizes}">\n'
            f'{sp}  <img{cls}\n{sp}    src="/images/blog/{name}-{widths[-1]}w.jpg"\n{sp}    srcset="{srcset_j}"\n{sp}    sizes="{sizes}"\n'
            f'{sp}    width="{w}" height="{h}" loading="{"lazy" if lazy else "eager"}"\n{sp}    alt="{alt}">\n{sp}</picture>')


def fmt_date(iso):
    d = date.fromisoformat(iso)
    return f"{d.strftime('%b')} {d.day}, {d.year}"


def main():
    radio = json.loads(read(ROOT / "data/radio/radio-songs.json"))
    weekly = json.loads(read(ROOT / "data/billboard/hot100_weekly.json"))
    cn = json.loads(read(ROOT / "data/billboard/country.json"))

    hot_ones = {(norm(w["title"]), norm(w["artist"])) for wk in weekly.values() for w in wk}
    weeks = [w for y in sorted(cn) for w in cn[y]]
    songs = collections.OrderedDict()
    for w in weeks:
        d = songs.setdefault((w["title"], w["artist"]), {"first": w["week_start"], "weeks": 0})
        d["weeks"] += 1
    country_ones = {(norm(t), norm(a)) for t, a in songs}
    by_artist = collections.defaultdict(list)
    for (t, a), d in songs.items():
        by_artist[a].append((t, d))

    country = sorted((s for s in radio if s["genre"] == "country" and s.get("youtube_id")), key=lambda s: (s["year"], s["rank"]))
    song_slugs = {pth.parent.name for pth in (ROOT / "blog/songs").glob("*/index.html")}
    artist_slugs = {pth.parent.name for pth in (ROOT / "blog/artists").glob("*/index.html")}

    rows, n_c1, n_h1, both = [], 0, 0, []
    for s in country:
        key = (norm(s["title"]), norm(s["artist"]))
        c1, h1 = key in country_ones, key in hot_ones
        n_c1 += c1
        n_h1 += h1
        if c1 and h1:
            both.append(s)
        sslug = song_post_slug(s["title"], s["artist"], song_slugs)
        aslug = next((sl for sl in artist_slugs if norm(sl) == norm(s["artist"])), None)
        t, a = html.escape(s["title"]), html.escape(s["artist"])
        song_cell = f'<a href="/blog/songs/{sslug}/">{t}</a>' if sslug else t
        artist_cell = f'<a href="/blog/artists/{aslug}/">{a}</a>' if aslug else a
        rows.append(f'              <tr><td class="ohw-listen">{play_button(s["youtube_id"], s["title"], s["artist"])}</td>'
                    f'<td class="ohw-song">{song_cell}</td><td class="ohw-artist">{artist_cell}</td>'
                    f'<td>{s["year"]}</td><td>{s["rank"]}</td><td>{"Yes" if h1 else ""}</td><td>{"Yes" if c1 else ""}</td></tr>')
    N = len(country)
    n_songs, n_weeks = len(songs), len(weeks)

    # leaders table
    ye_by_artist = collections.Counter(norm(s["artist"]) for s in radio)
    leaders = sorted(by_artist.items(), key=lambda kv: (-len(kv[1]), -sum(d["weeks"] for _, d in kv[1])))
    top = [(a, v) for a, v in leaders if " and " not in a and " & " not in a][:12]
    lead_rows = [[html.escape(a), len(v), sum(d["weeks"] for _, d in v), ye_by_artist[norm(a)]] for a, v in top]
    zero_ye = [a for a, v in top if ye_by_artist[norm(a)] == 0]

    # longest runs
    long_runs = sorted(((d["weeks"], d["first"], t, a) for (t, a), d in songs.items() if d["weeks"] >= 5), key=lambda x: (-x[0], x[1]))
    run_rows = [[html.escape(t), html.escape(a), w, fmt_date(f)] for w, f, t, a in long_runs]
    six = [r for r in long_runs if r[0] == 6]

    # women of country
    women = ["Dolly Parton", "Tammy Wynette", "Loretta Lynn", "Donna Fargo", "Tanya Tucker", "Crystal Gayle", "Lynn Anderson"]
    women_items = []
    for a in sorted(women, key=lambda a: (-len(by_artist[a]), -sum(d["weeks"] for _, d in by_artist[a]))):
        v = by_artist[a]
        women_items.append(f"          <li>{a}: {len(v)} number ones, {sum(d['weeks'] for _, d in v)} weeks at the top.</li>")

    women_total = sum(len(by_artist[a]) for a in women)
    both_items = "\n".join(
        f'          <li>{html.escape(s["title"])} by {html.escape(s["artist"])} ({s["year"]})</li>' for s in both)

    def first(a, t):
        return fmt_date(dict(by_artist[a])[t]["first"])

    jolene_first = first("Dolly Parton", "Jolene")
    iwaly_first = first("Dolly Parton", "I Will Always Love You")
    hyca = dict(by_artist["Dolly Parton"])["Here You Come Again"]
    waylon = by_artist["Waylon Jennings"]
    waylon_n, waylon_w = len(waylon), sum(d["weeks"] for _, d in waylon)
    luck = dict(waylon)["Luckenbach, Texas (Back to the Basics of Love)"]
    mammas = dict(by_artist["Waylon Jennings and Willie Nelson"])["Mammas Don't Let Your Babies Grow Up to Be Cowboys"]
    willie_n = len(by_artist["Willie Nelson"])
    blue_first = first("Willie Nelson", "Blue Eyes Crying in the Rain")
    charley, conway = by_artist["Charley Pride"], by_artist["Conway Twitty"]
    c_w, t_w = sum(d["weeks"] for _, d in charley), sum(d["weeks"] for _, d in conway)
    first_wk, last_wk = weeks[0]["week_start"], weeks[-1]["week_end"]
    top_ye = sorted(country, key=lambda s: s["rank"])[:4]
    ye_text = ", ".join(f'{s["title"]} by {s["artist"]} ({s["year"]})' for s in top_ye[:3])
    six_text = "; ".join(f'{t} by {a} ({fmt_date(f)[-4:]})' for w, f, t, a in six)

    faq = [
        ("What were the most popular 70s country songs?",
         [f"The most popular 70s country songs on the pop year-end lists included {ye_text}.",
          "Those ranks measure pop-chart success, not the country chart.",
          "On Billboard's country chart, Charley Pride and Conway Twitty logged the most number ones."]),
        ("Who had the most number one country songs in the 1970s?",
         [f"Charley Pride and Conway Twitty each reached number one on Billboard's Hot Country Singles chart {len(charley)} times in the 1970s.",
          f"Pride spent {c_w} weeks on top and Twitty spent {t_w} weeks.",
          f"Merle Haggard followed with {len(by_artist['Merle Haggard'])} number ones, based on this site's weekly country chart data."]),
        ("What was the longest-running number one country song of the 70s?",
         ["Three songs tied for the longest country chart runs of the 1970s, at six weeks each.",
          f"They were {six_text}.",
          "These counts come from this site's weekly Hot Country Singles data, which follows Wikipedia's year-by-year number one lists."]),
        ("What is outlaw country?",
         ["Outlaw country is a 1970s country subgenre that grew as a reaction to the polished Nashville sound.",
          "Willie Nelson, Waylon Jennings, Jessi Colter, and Tompall Glaser appeared on the 1976 compilation Wanted! The Outlaws.",
          "Wikipedia says it was the first country album certified platinum."]),
        ("How many 70s country songs also reached number one on the pop chart?",
         [f"Of {N} country-tagged songs in this site's Year-End Hot 100 data, {n_h1} reached number one on the weekly Hot 100.",
          f"{len(both)} of those {n_h1} topped the country chart as well, so true double number ones were rare.",
          "Most country number ones never appeared on a pop year-end list at all."]),
    ]

    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": " ".join(a)}} for q, a in faq]}, indent=2, ensure_ascii=False)
    faq_ld = "\n".join("  " + l for l in faq_ld.split("\n"))
    faq_html = "\n".join(
        f'          <div class="faq-item">\n            <h3>{html.escape(q)}</h3>\n' + "\n".join(f"            <p>{html.escape(l)}</p>" for l in a) + "\n          </div>"
        for q, a in faq)
    faq_html = faq_html.replace("&#x27;", "'")

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

    toc = [("country-song-list", "70s Country Songs: Play the Songs"),
           ("what-counts", "What Counts as 70s Country Music"),
           ("country-number-ones", "Who Really Ruled the Country Chart"),
           ("two-charts", "When the Country and Pop Charts Agreed"),
           ("women-of-country", "The Women Who Ran the Country Chart"),
           ("sources", "Sources"), ("faq", "Frequently Asked Questions")]
    toc_html = "\n".join(f'            <li><a href="#{i}">{t}</a></li>' for i, t in toc)

    body = f'''        <h2 id="country-song-list">70s Country Songs: Play the Songs</h2>
{p(f"Here are {N} 70s country songs from this site's Year-End Hot 100 data, from {country[0]['year']} to {country[-1]['year']}.",
   "Each is tagged country. Press Play on any row to watch it here, and tap a heading to sort.")}

        <div class="data-table-wrap scroll-list">
          <table class="data-table sortable-table" id="countrySongsTable" data-inline-player>
            <caption>{N} country songs of the 70s, by year and Billboard Year-End Hot 100 rank, with Hot 100 and country chart number ones marked</caption>
            <thead>
              <tr>
                <th><span class="visually-hidden">Play</span></th>
                <th><button type="button" data-col="1" data-type="text">Song</button></th>
                <th><button type="button" data-col="2" data-type="text">Artist</button></th>
                <th aria-sort="ascending"><button type="button" data-col="3" data-type="num">Year</button></th>
                <th><button type="button" data-col="4" data-type="num">Year-End Rank</button></th>
                <th><button type="button" data-col="5" data-type="text">#1 Hit</button></th>
                <th><button type="button" data-col="6" data-type="text">Country #1</button></th>
              </tr>
            </thead>
            <tbody>
{chr(10).join(rows)}
            </tbody>
          </table>
        </div>
{p("Year-End Rank is the song's spot on that year's Billboard Year-End Hot 100.",
   "That list keeps only the top 100 songs of each year.",
   "The #1 Hit column marks songs that also reached number one on the weekly Hot 100.",
   "The Country #1 column marks songs that reached number one on the weekly Hot Country Singles chart.")}

        <h2 id="what-counts">What Counts as 70s Country Music</h2>
{p("70s country music was never one sound.",
   "The best 70s country songs came from three overlapping styles pulling in different directions.",
   "The table below sets them side by side, with a song from the playable list for each.")}

{tbl("Three paths through 70s country music", ["Style", "What defined it", "Acts named by Wikipedia", "Example on the list"], [
    ["Countrypolitan", "Smooth Nashville Sound offshoot with real orchestral strings", "Tammy Wynette, Charlie Rich, Charley Pride, Lynn Anderson, Glen Campbell", "Behind Closed Doors by Charlie Rich (1973)"],
    ["Outlaw country", "A 1970s reaction to Nashville's slick production", "Willie Nelson, Waylon Jennings, Jessi Colter, Kris Kristofferson", "I'm Not Lisa by Jessi Colter (1975)"],
    ["Country pop crossover", "Country singers and pop singers meeting on both charts", "Glen Campbell, John Denver, Olivia Newton-John, Anne Murray, Linda Ronstadt", "Rhinestone Cowboy by Glen Campbell (1975)"],
])}

        <h3>Countrypolitan: The Smooth Side</h3>
{p("Countrypolitan grew out of the Nashville Sound.",
   "Wikipedia describes it as a smoother sound with lush string arrangements played by a real orchestra.",
   "It sold best from the later 1960s into the mid-1970s.",
   "Producers Billy Sherrill and Glenn Sutton are tied to it there.",
   "Charlie Rich's Behind Closed Doors and Lynn Anderson's Rose Garden both sit on the list above.")}

        <h3>Outlaw Country: The Rough Side</h3>
{p("Outlaw country pushed back against that polish.",
   "Wikipedia dates its heyday to the mid-to-late 1970s, with signs of decline by 1978.",
   "The 1976 compilation Wanted! The Outlaws collected Waylon Jennings, Willie Nelson, Jessi Colter, and Tompall Glaser.",
   "Wikipedia calls it the first country album certified platinum.")}

        <h3>Waylon and Willie on the Country Chart</h3>
{p(f"In this site's weekly data, Waylon Jennings reached number one {waylon_n} times, for {waylon_w} weeks in all.",
   f"His Luckenbach, Texas held the top spot for {luck['weeks']} weeks starting {fmt_date(luck['first'])}.",
   f"Their duet Mammas Don't Let Your Babies Grow Up to Be Cowboys added {mammas['weeks']} more weeks in 1978.",
   f"Willie Nelson reached number one {willie_n} times under his own name.",
   f"The first was Blue Eyes Crying in the Rain on {blue_first}.")}
{pic("willie-nelson-1970s", "Willie Nelson in a black and white Atlantic Records publicity photo from the early 1970s, wearing a straw cowboy hat and singing into a microphone", "(max-width: 700px) 100vw, 700px", 1200, 670)}
        <p class="post-img-caption">Willie Nelson, Atlantic Records publicity photo, circa 1973.</p>
        <p class="post-img-caption">Image credit: Atlantic Records, public domain, via Wikimedia Commons.</p>
{p('The full story of that song is in <a href="/blog/songs/blue-eyes-crying-in-the-rain/">Blue Eyes Crying in the Rain</a>.')}

        <h3>Country Pop and Country Rock: The Crossover Side</h3>
{p("Country pop first emerged in the 1970s, according to Wikipedia.",
   "Glen Campbell, John Denver, Olivia Newton-John, Anne Murray, and Linda Ronstadt all had hits on the country charts.",
   "Dolly Parton's Here You Come Again topped the country chart.",
   "Wikipedia says it also reached No. 3 on the pop chart.",
   f"Among the 70s country songs on this site's list, Rhinestone Cowboy by Glen Campbell ranks highest, at #2 for 1975.",
   'The rock-leaning end of the crossover has its own page, <a href="/blog/genres/70s-country-rock/">70s country rock</a>.',
   'Want a country act picked for you? The <a href="/pages/random-artist-picker">Random Artist Picker</a> can do it.')}

        <h2 id="country-number-ones">Who Really Ruled the Country Chart</h2>
{p(f"Billboard's Hot Country Singles chart tells a different story about 70s country songs than the pop year-end lists do.",
   f"This site's weekly country data covers {n_weeks} charts, from {fmt_date(first_wk)} through {fmt_date(last_wk)}.",
   f"{n_songs} different songs reached number one in that stretch.")}

        <h3>The Acts With the Most Country Number Ones</h3>
{p("This table ranks the acts by number of country number ones.",
   "The last column counts how many songs each act placed on any 1970s Year-End Hot 100 list.",
   "Duets are credited separately, so they are left out here.")}

{tbl("The 12 acts with the most number ones on Billboard's Hot Country Singles chart, 1970 to 1979", ["Artist", "Country #1 songs", "Weeks at #1", "Songs on the Year-End Hot 100"], lead_rows)}
{p(f"{len(zero_ye)} of these 12 acts never placed a single song on any 1970s Year-End Hot 100 list.",
   f"Charley Pride and Conway Twitty each led with {len(charley)} number ones.",
   "The country chart and the pop chart were close to separate worlds.",
   "Many of the biggest 70s country songs never crossed over at all.")}

        <h3>The Longest Runs at the Top</h3>
{p("Most country number ones lasted one or two weeks.",
   f"Only {len(long_runs)} songs held the top spot for five weeks or longer.")}

{tbl("Country number ones that spent five or more weeks at the top, 1970 to 1979", ["Song", "Artist", "Weeks at #1", "Run began"], run_rows)}
{p(f"Three songs tied at six weeks.",
   "Convoy by C. W. McCall began its run in December 1975 and finished in 1976.",
   f"Dolly Parton's Here You Come Again spent {hyca['weeks']} weeks at number one.",
   f"That run began {fmt_date(hyca['first'])}.",
   'To hear something from anywhere in the decade, spin the <a href="/pages/random-70s-song">Random 70s Song Generator</a>.')}

        <h2 id="two-charts">When the Country and Pop Charts Agreed</h2>
{p(f"Of the {N} 70s country songs on the playable list, {n_c1} also reached number one on the country chart.",
   f"{n_h1} reached number one on the weekly Hot 100.",
   f"Only {len(both)} did both.",
   "These are the true double number ones in this site's data:")}
        <ul>
{both_items}
        </ul>
{p("Every other country number one stayed on the country side of the radio dial.",
   "Most 70s country songs followed that same path.",
   "That is why a country chart list and a pop year-end list look so different.",
   'The pop side of the story is covered in <a href="/blog/songs/70s-number-one-hits/">70s number one hits</a>.')}

        <h2 id="women-of-country">The Women Who Ran the Country Chart</h2>
{p(f"These seven women alone account for {women_total} of the decade's {n_songs} country number ones.",
   "Each reached number one at least six times:")}
        <ul>
{chr(10).join(women_items)}
        </ul>
{pic("porter-wagoner-dolly-parton-1969", "Porter Wagoner and Dolly Parton in a 1969 publicity photo, five years before she recorded I Will Always Love You", "(max-width: 700px) 100vw, 500px", 1000, 1200, widths=(400, 800, 1000))}
        <p class="post-img-caption">Porter Wagoner and Dolly Parton, publicity photo, 1969.</p>
        <p class="post-img-caption">Image credit: Moeller Talent, Inc. Nashville, public domain, via Wikimedia Commons.</p>
{p(f"Dolly Parton's run is the clearest example.",
   f"Jolene first hit number one on {jolene_first}.",
   f"I Will Always Love You followed on {iwaly_first}.",
   'The story of the first song is in <a href="/blog/songs/jolene/">Jolene</a>.',
   "That was the year she recorded I Will Always Love You as her farewell to Porter Wagoner's show.")}

        <h2 id="sources">Sources</h2>
{p("The year-end ranks and Hot 100 number ones come from this site's own Billboard data, described on the <a href='/about/methodology/'>methodology page</a>.",
   "Every list on <a href='/'>Music of the 70s</a> plays inside the page.",
   "The weekly country chart data follows Wikipedia's year-by-year lists of Hot Country Singles number ones.",
   "Background on the genre can be checked against these outside sources:")}
        <ul>
          <li><a href="https://en.wikipedia.org/wiki/Country_music" rel="noopener">Wikipedia: Country music</a> for the 1970s crossover and outlaw movements.</li>
          <li><a href="https://en.wikipedia.org/wiki/Outlaw_country" rel="noopener">Wikipedia: Outlaw country</a> for the movement and Wanted! The Outlaws.</li>
          <li><a href="https://en.wikipedia.org/wiki/Countrypolitan" rel="noopener">Wikipedia: Countrypolitan</a> for the smooth Nashville Sound offshoot.</li>
          <li><a href="https://en.wikipedia.org/wiki/Hot_Country_Songs" rel="noopener">Wikipedia: Hot Country Songs</a> for the chart's history and names.</li>
        </ul>

        <section class="faq-block" id="faq">
          <h2>Frequently Asked Questions</h2>
{faq_html}
        </section>'''

    related = [
        ("dolly-parton-1970s", "Artists", "Dolly Parton: The 1970s", "/blog/artists/dolly-parton/", "See how she went from Porter Wagoner's show to the top of both charts.", "Dolly Parton in a publicity photo from 1977"),
        ("willie-nelson-1970s", "Artists", "Willie Nelson: The 1970s", "/blog/artists/willie-nelson/", "Follow the ghostwriter who became an outlaw country star.", "Willie Nelson in an early 1970s Atlantic Records publicity photo"),
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
  <meta name="description" content="{DESC}">
  <link rel="canonical" href="{URL}">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <meta name="theme-color" content="#1a1a2e">

  <meta property="og:title" content="{TITLE}">
  <meta property="og:description" content="{DESC}">
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
      {{"@type": "ListItem", "position": 3, "name": "Genres", "item": "https://musicofthe70s.net/blog/genres/"}},
      {{"@type": "ListItem", "position": 4, "name": "70s Country Songs", "item": "{URL}"}}
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
        <a href="/blog/genres/">Genres</a> ›
        70s Country Songs
      </nav>

      <article class="section seo-content">
        <h1>{TITLE}</h1>

        <p class="post-byline">By <a href="https://musicofthe70s.net/about/author/">Charlie</a> &middot; Published {PUBLISHED.strftime('%B')} {PUBLISHED.day}, {PUBLISHED.year}</p>
        <p class="jump-to-list"><a class="btn-primary jump-btn" href="#country-song-list">&#9654; Jump to the playable list</a></p>

        <p class="post-intro">70s country songs lived on two charts at once, and the two rarely matched.</p>
        <p class="post-intro">Billboard's country chart crowned {n_songs} different number ones in the decade.</p>
        <p class="post-intro">Only {n_c1} of the {N} country-tagged songs on this site's pop year-end lists were among them.</p>
        <p class="post-intro">Most of the acts who ruled the country chart never touched the pop one.</p>
        <p class="post-intro">This page plays all {N} songs, then shows who really led the country chart.</p>

{pic(IMG, "Dolly Parton in a publicity photo from 1977, wearing a denim shirt with her hair styled in her signature big blonde curls", "(max-width: 700px) 100vw, 1100px", 1200, 670, lazy=False)}
        <p class="post-img-caption">Dolly Parton, publicity photo, March 1977.</p>
        <p class="post-img-caption">Image credit: Publicity photo by RCA Records, public domain, via Wikimedia Commons.</p>

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
    out = ROOT / "blog/genres" / SLUG / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    write(out, page)
    print(f"wrote {out}: {N} rows, {n_c1} country #1, {n_h1} Hot 100 #1, {len(both)} both; {n_songs} songs/{n_weeks} weeks; zero_ye={zero_ye}")


if __name__ == "__main__":
    main()
