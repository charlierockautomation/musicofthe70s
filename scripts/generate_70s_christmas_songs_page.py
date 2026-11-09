#!/usr/bin/env python3
"""Build /blog/songs/70s-christmas-songs/index.html (Article Standard page, type playlist).

Every fact below was checked on 2026-11-09 against the sources logged in
sources/log/70s-christmas-songs.json (Wikipedia song pages, Official Charts
song pages, Library of Congress newsroom). Every YouTube ID is an official
artist or label upload recorded in data/official-videos.json.

Run: python3 scripts/generate_70s_christmas_songs_page.py
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "blog/songs/70s-christmas-songs/index.html"
URL = "https://musicofthe70s.net/blog/songs/70s-christmas-songs/"
PUB = "2026-11-09"
PUB_H = "November 9, 2026"
TITLE = "70s Christmas Songs: 14 Holiday Classics to Play in Order"
DESC = ("70s Christmas songs from Feliz Navidad to Wonderful Christmastime: 14 holiday classics "
        "from 1970 to 1979, with writers, chart facts and one player.")
IMG = "https://musicofthe70s.net/images/blog/70s-christmas-songs-1200w.jpg"

# (title, artist, year, writers, video id, channel, chart fact, artist link or None, schema artist type)
SONGS = [
    ("Feliz Navidad", "José Feliciano", 1970, "José Feliciano", "N8NcQzMQN_U", "José Feliciano",
     "Released November 9, 1970, on RCA Victor; its all-time Hot 100 peak is No. 6, per Wikipedia.",
     None, "Person"),
    ("Merry Christmas, Darling", "Carpenters", 1970, "Richard Carpenter (music), Frank Pooler (lyrics)",
     "PB5c-KmxqQw", "Carpenters",
     "No. 1 on Billboard's Christmas singles chart in 1970, 1971 and 1973, per Wikipedia.",
     "/blog/artists/carpenters-songs/", "MusicGroup"),
    ("This Christmas", "Donny Hathaway", 1970, "Donny Hathaway, Nadine McKinnor", "PhKVSZsRxQM", "RHINO",
     "Released on Atco on December 9, 1970; it reached No. 34 on the Hot 100 in January 2024, per Wikipedia.",
     None, "Person"),
    ("Santa Claus Is Comin' to Town", "Jackson 5", 1970, "J. Fred Coots, Haven Gillespie", "HhiUOCo8LYQ",
     "Classic Motown",
     "From Jackson 5 Christmas Album, four weeks at No. 1 on Billboard's Christmas albums chart in December 1970, per Wikipedia.",
     "/blog/artists/jackson-5-songs/", "MusicGroup"),
    ("Happy Xmas (War Is Over)", "John Lennon and Yoko Ono", 1971, "John Lennon, Yoko Ono", "yN4Uu0OlmTg",
     "johnlennon",
     "Out in the US on December 1, 1971; No. 4 in the UK on its 1972 release, then No. 2 after Lennon's death in 1980, per Wikipedia. The video is the 2020 Ultimate Mix, a remix; the official johnlennon channel has no upload of the original 1971 mix.",
     None, "MusicGroup"),
    ("Merry Xmas Everybody", "Slade", 1973, "Noddy Holder, Jim Lea", "PTslBTBl1X8", "Slade Official",
     "UK No. 1 for 5 weeks from its first chart date, 15 December 1973, per Official Charts.",
     None, "MusicGroup"),
    ("I Wish It Could Be Christmas Everyday", "Wizzard", 1973, "Roy Wood", "IJPc7esgvsA", "RHINO",
     "Peaked at No. 4 in the UK, a spot it held for four weeks over Christmas 1973, per Wikipedia.",
     None, "MusicGroup"),
    ("Step Into Christmas", "Elton John", 1973, "Elton John, Bernie Taupin", "IbRtGMm96F8", "Elton John",
     "No. 24 in the UK in 1973 and No. 1 on Billboard's Christmas singles chart, per Wikipedia.",
     "/blog/artists/elton-john/", "Person"),
    ("Lonely This Christmas", "Mud", 1974, "Nicky Chinn, Mike Chapman", "NJ6kJ7GWtv0", "Mud",
     "UK No. 1 for 4 weeks from its first chart date, 30 November 1974, per Official Charts.",
     None, "MusicGroup"),
    ("I Believe in Father Christmas", "Greg Lake", 1975, "Greg Lake (music), Peter Sinfield (lyrics)",
     "yfY4b1NszpY", "OfficialGregLake",
     "Peaked at No. 2 in the UK, first charting 6 December 1975, per Official Charts.",
     None, "Person"),
    ("Father Christmas", "The Kinks", 1977, "Ray Davies", "fPPCPqDINEk", "The Kinks",
     "Released on Arista on 25 November 1977, with \"Prince of the Punks\" on the B-side, per Wikipedia.",
     None, "MusicGroup"),
    ("Please Come Home for Christmas", "Eagles", 1978, "Charles Brown, Gene Redd", "7Rv3wfwIVBc", "Eagles",
     "Released November 27, 1978; it peaked at No. 18 on the Hot 100, per Wikipedia.",
     None, "MusicGroup"),
    ("Mary's Boy Child / Oh My Lord", "Boney M.", 1978, "Jester Hairston (\"Mary's Boy Child\")", "cmm1gt_2SkQ",
     "Boney M.",
     "The UK Christmas number one of 1978, with 1.87 million UK copies sold as of November 2015, per Wikipedia.",
     None, "MusicGroup"),
    ("Wonderful Christmastime", "Paul McCartney", 1979, "Paul McCartney", "94Ye-3C1FC8", "PAUL McCARTNEY",
     "Peaked at No. 6 in the UK, first charting 1 December 1979, per Official Charts.",
     None, "Person"),
]

YEARS = {}
for s in SONGS:
    YEARS.setdefault(s[2], []).append(s[0])

e = lambda t: html.escape(t, quote=True)


def rows():
    out = []
    for t, a, y, w, vid, _, fact, link, _ in SONGS:
        art = f'<a href="{link}">{e(a)}</a>' if link else e(a)
        out.append(
            f'              <tr><td class="ohw-listen"><button type="button" class="ohw-play" data-yt="{vid}" '
            f'data-title="{e(t)} by {e(a)}" aria-label="Play {e(t)} by {e(a)} here">&#9654; Play</button></td>'
            f'<td class="ohw-song">{e(t)}</td><td class="ohw-artist">{art}</td><td data-sort="{y}">{y}</td>'
            f'<td>{e(w)}</td><td class="love-story">{e(fact)}</td></tr>')
    return "\n".join(out)


def year_rows():
    out = []
    for y in range(1970, 1980):
        titles = YEARS.get(y, [])
        cls = ' class="row-highlight"' if len(titles) == max(len(v) for v in YEARS.values()) else ""
        out.append(f'              <tr{cls}><td>{y}</td><td>{len(titles)}</td>'
                   f'<td>{e(", ".join(titles)) if titles else "None on this list"}</td></tr>')
    return "\n".join(out)


FAQ = [
    ("What is the most famous 70s Christmas song?",
     ["\"Feliz Navidad\" has the strongest claim among 70s Christmas songs, since the Grammy Hall of Fame inducted José Feliciano's recording in 2010.",
      "It joined the Library of Congress's preservation list for American sound recordings in May 2026, 56 years after its release.",
      "ASCAP has named it one of the 25 most played and recorded Christmas songs in the world."]),
    ("What was the UK Christmas number one in 1973?",
     ["Slade took it with \"Merry Xmas Everybody,\" keeping Wizzard's rival single off the top that December.",
      "It earned a silver disc on its release day from UK pre-orders of over 250,000 copies.",
      "It became Slade's sixth and final UK number one, and the band's best-selling single."]),
    ("Which 70s Christmas song went highest on the Billboard Hot 100 at the time?",
     ["The Eagles' \"Please Come Home for Christmas\" did, and it was the first Christmas song in the Hot 100 top 20 since Roy Orbison's \"Pretty Paper\" in 1963.",
      "Charles Brown's own 1960 recording had peaked at No. 76, well before the 70s Christmas songs here.",
      "It came back onto the Hot 100 at No. 45 on January 2, 2021, 42 years after it first charted."]),
    ("Did Paul McCartney play every instrument on Wonderful Christmastime?",
     ["McCartney played every instrument himself, from drums and guitars to sleigh bells, and built the backing track on a Yamaha CS-80 synthesizer.",
      "Wings appear in the music video but are not on the recording.",
      "He recorded it in mid-1979 at Lower Gate Farm in Peasmarsh, East Sussex, and at the Spirit of Ranachan Studio in Campbeltown, Scotland."]),
    ("Who sings with John Lennon on Happy Xmas (War Is Over)?",
     ["Yoko Ono sings with him, and the record is credited with the Plastic Ono Band and the Harlem Community Choir.",
      "The choir was 30 children aged four to twelve, recorded on October 31, 1971, at Record Plant East in New York.",
      "In ITV's 2012 poll of the nation's favourite Christmas song, it ranked tenth."]),
]

SOURCES = [
    ("https://en.wikipedia.org/wiki/Feliz_Navidad_(song)", "Wikipedia, \"Feliz Navidad (song)\""),
    ("https://newsroom.loc.gov/news/national-recording-registry-inducts-sounds-of-taylor-swift--beyonc---the-go-go-s--vince-gill--weezer/s/bc258688-e655-4ffb-9f91-f32b94956f36",
     "Library of Congress newsroom, National Recording Registry class of 2026 (May 14, 2026)"),
    ("https://www.officialcharts.com/songs/slade-merry-xmas-everybody/", "Official Charts, Slade \"Merry Xmas Everybody\""),
    ("https://www.officialcharts.com/songs/mud-lonely-this-christmas/", "Official Charts, Mud \"Lonely This Christmas\""),
    ("https://www.officialcharts.com/songs/greg-lake-i-believe-in-father-christmas/", "Official Charts, Greg Lake \"I Believe in Father Christmas\""),
    ("https://www.officialcharts.com/songs/paul-mccartney-wonderful-christmastime/", "Official Charts, Paul McCartney \"Wonderful Christmastime\""),
    ("https://en.wikipedia.org/wiki/Happy_Xmas_(War_Is_Over)", "Wikipedia, \"Happy Xmas (War Is Over)\""),
    ("https://en.wikipedia.org/wiki/Merry_Xmas_Everybody", "Wikipedia, \"Merry Xmas Everybody\""),
    ("https://en.wikipedia.org/wiki/I_Wish_It_Could_Be_Christmas_Everyday", "Wikipedia, \"I Wish It Could Be Christmas Everyday\""),
    ("https://en.wikipedia.org/wiki/Step_into_Christmas", "Wikipedia, \"Step into Christmas\""),
    ("https://en.wikipedia.org/wiki/Lonely_This_Christmas", "Wikipedia, \"Lonely This Christmas\""),
    ("https://en.wikipedia.org/wiki/I_Believe_in_Father_Christmas", "Wikipedia, \"I Believe in Father Christmas\""),
    ("https://en.wikipedia.org/wiki/Father_Christmas_(song)", "Wikipedia, \"Father Christmas (song)\""),
    ("https://en.wikipedia.org/wiki/Please_Come_Home_for_Christmas", "Wikipedia, \"Please Come Home for Christmas\""),
    ("https://en.wikipedia.org/wiki/Mary%27s_Boy_Child", "Wikipedia, \"Mary's Boy Child\""),
    ("https://en.wikipedia.org/wiki/Wonderful_Christmastime", "Wikipedia, \"Wonderful Christmastime\""),
    ("https://en.wikipedia.org/wiki/Merry_Christmas_Darling", "Wikipedia, \"Merry Christmas Darling\""),
    ("https://en.wikipedia.org/wiki/This_Christmas_(Donny_Hathaway_song)", "Wikipedia, \"This Christmas (Donny Hathaway song)\""),
    ("https://en.wikipedia.org/wiki/Jackson_5_Christmas_Album", "Wikipedia, \"Jackson 5 Christmas Album\""),
    ("https://en.wikipedia.org/wiki/Santa_Claus_Is_Comin%27_to_Town", "Wikipedia, \"Santa Claus Is Comin' to Town\""),
]


def schema():
    person = {"@type": "Person", "@id": "https://musicofthe70s.net/about/author/", "name": "Charlie",
              "url": "https://musicofthe70s.net/about/author/"}
    tracks = [{"@type": "MusicRecording", "name": t, "byArtist": {"@type": at, "name": a},
               "datePublished": str(y), "url": f"https://www.youtube.com/watch?v={vid}"}
              for t, a, y, _, vid, _, _, _, at in SONGS]
    post = {
        "@context": "https://schema.org", "@type": "BlogPosting", "headline": TITLE, "description": DESC,
        "datePublished": PUB, "dateModified": PUB, "author": person,
        "publisher": {"@type": "Organization", "@id": "https://musicofthe70s.net/#organization",
                      "name": "Music of the 70s", "url": "https://musicofthe70s.net/",
                      "logo": {"@type": "ImageObject", "url": "https://musicofthe70s.net/favicon-512.png",
                               "width": 512, "height": 512}},
        "image": IMG, "mainEntityOfPage": URL,
    }
    playlist = {"@context": "https://schema.org", "@type": "MusicPlaylist", "name": "70s Christmas Songs",
                "url": URL, "numTracks": len(tracks), "track": tracks}
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": " ".join(a)}} for q, a in FAQ]}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://musicofthe70s.net/"},
        {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://musicofthe70s.net/blog/"},
        {"@type": "ListItem", "position": 3, "name": "Songs", "item": "https://musicofthe70s.net/blog/songs/"},
        {"@type": "ListItem", "position": 4, "name": "70s Christmas Songs", "item": URL}]}
    return "\n".join(f'  <script type="application/ld+json">\n{json.dumps(n, ensure_ascii=False, indent=2)}\n  </script>'
                     for n in (post, playlist, faq, crumbs))


def faq_html():
    out = []
    for q, a in FAQ:
        out.append(f'          <div class="faq-item">\n          <h3>{e(q)}</h3>')
        out += [f"          <p>{html.escape(s, quote=False)}</p>" for s in a]
        out.append("          </div>")
    return "\n".join(out)


def sources_html():
    return "\n".join(f'            <li><a href="{e(u)}" target="_blank" rel="noopener">{e(n)}</a></li>' for u, n in SOURCES)


def card(href, img, alt, cat, h3, blurb):
    return f"""            <div class="card post-card">
              <picture>
                <source type="image/webp" srcset="/images/blog/srcset/{img}-400w.webp 400w, /images/blog/srcset/{img}-800w.webp 800w" sizes="(max-width: 700px) 100vw, 33vw">
                <img class="post-thumb" src="/images/blog/srcset/{img}-400w.jpg"
                  srcset="/images/blog/srcset/{img}-400w.jpg 400w, /images/blog/srcset/{img}-800w.jpg 800w"
                  sizes="(max-width: 700px) 100vw, 33vw" width="400" height="225" loading="lazy"
                  alt="{e(alt)}">
              </picture>
              <div class="post-card-body">
                <span class="post-cat">{cat}</span>
                <h3>{e(h3)}</h3>
                <p>{e(blurb)}</p>
                <a class="cta" href="{href}">Read post</a>
              </div>
            </div>"""


def picture(stub, alt, eager=False):
    return f"""        <picture>
          <source type="image/webp" srcset="/images/blog/srcset/{stub}-400w.webp 400w, /images/blog/srcset/{stub}-800w.webp 800w, /images/blog/srcset/{stub}-1200w.webp 1200w" sizes="(max-width: 700px) 100vw, 1100px">
          <img class="post-featured-img"
            src="/images/blog/{stub}-1200w.jpg"
            srcset="/images/blog/srcset/{stub}-400w.jpg 400w, /images/blog/srcset/{stub}-800w.jpg 800w, /images/blog/{stub}-1200w.jpg 1200w"
            sizes="(max-width: 700px) 100vw, 1100px"
            width="1200" height="675" loading="{'eager' if eager else 'lazy'}"
            alt="{e(alt)}">
        </picture>"""


BODY = """
        <h2 id="christmas-songs-list">The Playlist: 14 Holiday Records, Playable in Order</h2>
        <p>Press Play on any row and the list keeps going, song after song, until you press Stop.</p>

        <div class="data-table-wrap scroll-list">
          <table class="data-table sortable-table" id="christmasSongsTable" data-inline-player>
            <caption>14 Christmas songs released from 1970 to 1979, with writers and one checked chart fact each</caption>
            <thead>
              <tr>
                <th><span class="visually-hidden">Play</span></th>
                <th><button type="button" data-col="1" data-type="text">Song</button></th>
                <th><button type="button" data-col="2" data-type="text">Artist</button></th>
                <th aria-sort="ascending"><button type="button" data-col="3" data-type="num">Year</button></th>
                <th>Written by</th>
                <th>The chart fact</th>
              </tr>
            </thead>
            <tbody>
__ROWS__
            </tbody>
          </table>
        </div>
        <p>Year is when each song first came out, as a single or on an album.</p>
        <p>Every video is an official upload from the artist's or the label's own channel.</p>

        <h2 id="answer">The Short Answer: The 70s Christmas Songs Everyone Knows</h2>
        <p>Four of them reached a US or UK top 10.</p>
        <ul>
          <li><strong>Feliz Navidad</strong> (1970), written and sung by José Feliciano, No. 6 on the Hot 100.</li>
          <li><strong>Happy Xmas (War Is Over)</strong> (1971), the first original Christmas song from a former Beatle after the group split.</li>
          <li><strong>Merry Xmas Everybody</strong> (1973), the Slade single that went straight in at No. 1 in Britain.</li>
          <li><strong>Wonderful Christmastime</strong> (1979), Paul McCartney's first single credited to him alone since 1971.</li>
        </ul>

        <h2 id="uk-race">The UK Christmas Number One Race</h2>
        <p>Three songs on this list were UK Christmas number ones, by Slade, Mud and Boney M.</p>
        <h3>1973: Slade Against Wizzard</h3>
        <p>Slade and Wizzard both released Christmas singles in December 1973.</p>
        <p>Slade won the race, and Wizzard's record stopped at No. 4.</p>
        <h3>1974 and 1975: Mud, Then a Near Miss</h3>
        <p>Mud took "Lonely This Christmas" to No. 1 a year later, in the style of a late Elvis ballad.</p>
        <p>In 1975 Greg Lake's "I Believe in Father Christmas" climbed to No. 2.</p>
        <p>The record that kept it off the top was Queen's "<a href="/blog/songs/bohemian-rhapsody/">Bohemian Rhapsody</a>."</p>
        <p>Lake's song borrows its instrumental riff from the "Troika" section of Prokofiev's Lieutenant Kijé suite.</p>
        <h3>1978: Boney M. Brings Back a 1950s Carol</h3>
        <p>"Mary's Boy Child" had already been a UK number one for Harry Belafonte in 1957.</p>
        <p>Boney M.'s version, "Mary's Boy Child / Oh My Lord," took it back to No. 1 in 1978.</p>

        <h2 id="us-side">The American Side: Christmas Charts and the Hot 100</h2>
        <p>In the US, Billboard tracked 70s Christmas songs on separate Christmas charts.</p>
        <p>From 1963 to 1973, holiday albums could not appear on the Billboard 200 at all.</p>
        <p>The Carpenters, Elton John and the Jackson 5 all reached No. 1 on those Christmas charts.</p>
        <p>The Eagles broke through in 1978, taking a 1960 Charles Brown song to No. 18 on the Hot 100.</p>
        <p>Three 70s Christmas songs here first entered the Hot 100 between 2017 and 2020.</p>
        <p>They are "Feliz Navidad," "This Christmas" and "Wonderful Christmastime."</p>
        <p>Chart notes on this site follow the rules on the <a href="/about/methodology/">methodology page</a>.</p>

        <h2 id="by-year">Christmas Songs by Year, 1970 to 1979</h2>
        <p>1970 was the busiest year, with four of the 14 songs on this list.</p>
__FIG2__
        <p class="post-img-caption">Songs on this list per year of first release.</p>
        <p class="post-img-caption">Chart: Music of the 70s, from the 14 songs in the table above.</p>
        <div class="data-table-wrap">
          <table class="data-table">
            <caption>Songs on this list by year of first release</caption>
            <thead>
              <tr><th>Year</th><th>Songs</th><th>Titles</th></tr>
            </thead>
            <tbody>
__YEARS__
            </tbody>
          </table>
        </div>
        <p>No song on this list comes from 1972 or 1976.</p>
        <p>For slower, quieter songs from the same years, try this site's <a href="/blog/songs/70s-slow-songs/">70s slow songs</a> list.</p>

        <h2 id="keep-listening">After the Holidays: Keep the Music Going</h2>
        <p>Once the tree comes down, the <a href="/radio/">Listen Now 70s radio</a> plays the rest of the decade nonstop.</p>
        <p>For the big picture, the <a href="/blog/songs/best-songs-of-the-70s/">best songs of the 70s</a> page covers the whole decade's hits.</p>
"""


def build():
    rows_html = rows()
    fig1 = picture("70s-christmas-songs", "Timeline of 14 70s Christmas songs by release year, from Feliz Navidad in 1970 to Wonderful Christmastime in 1979", eager=True)
    fig2 = picture("70s-christmas-songs-years", "Bar chart of 70s Christmas songs on this list per year, led by 1970 with four songs")
    body = BODY.replace("__ROWS__", rows_html).replace("__YEARS__", year_rows()).replace("__FIG2__", fig2)
    cards = "\n".join([
        card("/blog/songs/70s-love-songs/", "70s-love-songs", "70s Love Songs, a companion playable list of 30 romantic songs from the decade",
             "Songs", "70s Love Songs", "Thirty romantic songs from the decade, playable in one list."),
        card("/blog/songs/70s-party-songs/", "70s-party-songs", "70s Party Songs, a playable list for getting a room dancing",
             "Songs", "70s Party Songs", "A playable list for the holiday party once the carols are done."),
        card("/blog/artists/eagles-the-band/", "eagles-1975", "The Eagles in 1975, the band behind Please Come Home for Christmas",
             "Artists", "Eagles", "The full story of the band that took a Christmas blues song into the Hot 100 top 20."),
    ])
    page = f"""<!DOCTYPE html>
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
  <title>{e(TITLE)}</title>
  <meta name="description" content="{e(DESC)}">
  <link rel="canonical" href="{URL}">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <meta name="theme-color" content="#1a1a2e">

  <meta property="og:title" content="{e(TITLE)}">
  <meta property="og:description" content="{e(DESC)}">
  <meta property="og:url" content="{URL}">
  <meta property="og:type" content="article">
  <meta property="og:image" content="{IMG}">
  <meta property="og:site_name" content="Music of the 70s">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{e(TITLE)}">
  <meta name="twitter:description" content="{e(DESC)}">
  <meta name="twitter:image" content="{IMG}">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@700;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/style.css">

{schema()}
</head>
<body>
  <header class="site-header">
    <div class="header-inner">
      <a href="/" class="site-logo"><span class="logo-vinyl">&#9834;</span> Music of the 70s</a>
      <nav class="main-nav">
        <a href="/">Home</a>
        <a href="/#tools">Tools</a>
        <a href="/radio/">Listen Now</a>
        <a href="/pages/about">About</a>
        <a href="/blog/">Blog</a>
      </nav>
      <button class="nav-toggle" aria-label="Menu">&#9776;</button>
    </div>
  </header>

  <main>
    <div class="container">
      <nav class="breadcrumb">
        <a href="/">Home</a> &rsaquo;
        <a href="/blog/">Blog</a> &rsaquo;
        <a href="/blog/songs/">Songs</a> &rsaquo;
        <span>70s Christmas Songs</span>
      </nav>

      <article class="section seo-content">
        <h1>{e(TITLE)}</h1>

        <p class="post-byline">By <a href="https://musicofthe70s.net/about/author/">Charlie</a> &middot; Published {PUB_H} &middot; Updated {PUB_H}</p>
        <p class="listen-row"><button type="button" class="btn-primary listen-btn" data-yt="N8NcQzMQN_U" data-title="Feliz Navidad - José Feliciano">&#9654; Listen to Feliz Navidad</button></p>

        <p class="post-intro">The best-known 70s Christmas songs are "Feliz Navidad" (1970), "Happy Xmas (War Is Over)" (1971), "Merry Xmas Everybody" (1973) and "Wonderful Christmastime" (1979).</p>
        <p class="post-intro">This list has 14 holiday records from 1970 to 1979, including three UK Christmas number ones.</p>
        <p class="post-intro">Every one plays from the table below, one after another.</p>

        <aside class="facts-box" aria-label="Quick facts">
          <dl>
            <div><dt>Songs</dt><dd>14, all playable here</dd></div>
            <div><dt>Years</dt><dd>1970 to 1979</dd></div>
            <div><dt>Oldest</dt><dd>Feliz Navidad, 1970</dd></div>
            <div><dt>Newest</dt><dd>Wonderful Christmastime, 1979</dd></div>
            <div><dt>UK Christmas No. 1s</dt><dd>Slade (1973), Mud (1974), Boney M. (1978)</dd></div>
            <div><dt>Highest Hot 100 peak at the time</dt><dd>Please Come Home for Christmas, No. 18 (1978)</dd></div>
          </dl>
        </aside>

{fig1}
        <p class="post-img-caption">The 14 songs on this list, placed by the year each was first released.</p>
        <p class="post-img-caption">Chart: Music of the 70s, from the table on this page.</p>

        <nav class="toc-block" aria-label="Table of contents">
          <details class="toc-details" open>
            <summary>Table of Contents</summary>
            <ol>
            <li><a href="#christmas-songs-list">The Playlist: 14 Holiday Records, Playable in Order</a></li>
            <li><a href="#answer">The Short Answer: The Songs Everyone Knows</a></li>
            <li><a href="#uk-race">The UK Christmas Number One Race</a></li>
            <li><a href="#us-side">The American Side: Christmas Charts and the Hot 100</a></li>
            <li><a href="#by-year">Christmas Songs by Year, 1970 to 1979</a></li>
            <li><a href="#keep-listening">After the Holidays: Keep the Music Going</a></li>
            <li><a href="#faq">Frequently Asked Questions</a></li>
            <li><a href="#sources">Sources</a></li>
          </ol>
          </details>
        </nav>
        <script>if(window.matchMedia("(max-width: 699px)").matches){{document.querySelector(".toc-details").open=false;}}</script>
{body}
        <section class="faq-block" id="faq">
          <h2>Frequently Asked Questions</h2>
{faq_html()}
        </section>

        <section class="sources" id="sources">
          <h2>Sources</h2>
          <p>Each fact about these 70s Christmas songs was checked against the sources below on {PUB_H}.</p>
          <ul>
{sources_html()}
          </ul>
        </section>

        <section class="related-posts">
          <h2>You Might Also Like</h2>
          <div class="post-grid">
{cards}
          </div>
        </section>
      </article>
    </div>
  </main>

  <footer class="site-footer">
    <p>&copy; 2026 Music of the 70s |
      <a href="/pages/privacy-policy">Privacy Policy</a> |
      <a href="/pages/terms-of-use">Terms of Use</a> |
      <a href="/pages/contact">Contact</a> |
      <a href="/pages/about">About</a> |
      <a href="/about/author/">About the Author</a> |
      <a href="/about/methodology/">How We Write</a>
    </p>
  </footer>

  <script src="/js/main.js"></script>
  <script src="/js/sortable-table.js"></script>
  <script src="/js/table-player.js"></script>
  <script src="/js/listen-button.js" defer></script>
</body>
</html>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    build()
