#!/usr/bin/env python3
"""Build /blog/artists/journey-songs/ (rotation slot 5.1, bands-queue #1 Journey), 2026-11-13.
Peaks: Wikipedia "Journey discography" singles + albums tables (opened 2026-11-13).
Play IDs: data/official-videos.json (recorded 2026-11-13, see video-decisions.md).
Run: python3 .base/step-5.1/build.py
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "blog/artists/journey-songs/index.html"
URL = "https://musicofthe70s.net/blog/artists/journey-songs/"
PUB, PUB_H = "2026-11-13", "November 13, 2026"
TITLE = "Journey Songs of the 70s: 12 Tracks You Can Play in One List"
DESC = ("Journey songs from 1975 to 1979, from To Play Some Music to Lovin', Touchin', Squeezin': "
        "12 tracks with Hot 100 peaks and one player that runs the whole list.")
IMG = "https://musicofthe70s.net/images/blog/journey-singles-peaks-1200w.jpg"

# (song, album, year, peak or None, video id, lead vocal)
ROWS = [
    ("To Play Some Music", "Journey", 1975, None, "riX_qDc9cGE"),
    ("Of a Lifetime", "Journey", 1975, None, "hc_q_zb7nts"),
    ("On a Saturday Nite", "Look into the Future", 1976, None, "nhtNRpwUxPA"),
    ("Look into the Future", "Look into the Future", 1976, None, "1l22HM-d5Zo"),
    ("Spaceman", "Next", 1977, None, "zhwbEj7bSyo"),
    ("Wheel in the Sky", "Infinity", 1978, 57, "MxGEVIvSFeY"),
    ("Lights", "Infinity", 1978, 68, "tNG62fULYgI"),
    ("Anytime", "Infinity", 1978, 83, "88T131rQCUc"),
    ("Feeling That Way", "Infinity", 1978, None, "vg5vziU-qIs"),
    ("Lovin', Touchin', Squeezin'", "Evolution", 1979, 16, "fTkHFQC3wow"),
    ("Just the Same Way", "Evolution", 1979, 58, "twC6FvDubLk"),
    ("Too Late", "Evolution", 1979, 70, "CV7CwbNs_Wg"),
]
E = html.escape
# singles per Wikipedia "Journey discography" with no Hot 100 entry
NONCHART_SINGLES = {"To Play Some Music", "On a Saturday Nite", "Spaceman"}


def check_ids():
    vids = json.loads((ROOT / "data/official-videos.json").read_text())["videos"]
    missing = [r[4] for r in ROWS if r[4] not in vids]
    if missing:
        raise SystemExit(f"IDs not in data/official-videos.json: {missing}")


def table_rows():
    out = []
    for i, (song, album, year, peak, vid) in enumerate(ROWS, 1):
        t = E(f"{song} by Journey")
        pk = f"No. {peak}" if peak else ("Single, did not chart" if song in NONCHART_SINGLES else "Album track")
        out.append(
            f'              <tr><td class="ohw-listen"><button type="button" class="ohw-play" data-yt="{vid}" '
            f'data-title="{t}" aria-label="Play {t} here">&#9654; Play</button></td>'
            f'<td class="ohw-song">{E(song)}</td><td>{E(album)}</td>'
            f'<td data-sort="{year}">{year}</td><td data-sort="{peak or 999}">{pk}</td></tr>')
    return "\n".join(out)


def schema():
    post = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": TITLE,
        "description": DESC,
        "datePublished": PUB,
        "dateModified": PUB,
        "author": {"@type": "Person", "@id": "https://musicofthe70s.net/about/author/", "name": "Charlie",
                   "url": "https://musicofthe70s.net/about/author/"},
        "publisher": {"@type": "Organization", "@id": "https://musicofthe70s.net/#organization",
                      "name": "Music of the 70s", "url": "https://musicofthe70s.net/",
                      "logo": {"@type": "ImageObject", "url": "https://musicofthe70s.net/favicon-512.png",
                               "width": 512, "height": 512}},
        "image": IMG,
        "mainEntityOfPage": URL,
        "about": {"@type": "MusicGroup", "name": "Journey", "genre": ["Rock"], "foundingDate": "1973",
                  "foundingLocation": {"@type": "Place", "name": "San Francisco, California"},
                  "sameAs": ["https://en.wikipedia.org/wiki/Journey_(band)",
                             "https://musicbrainz.org/artist/abd506e1-6f2b-4d6f-b937-92c267f6f88b"]},
    }
    items = []
    for i, (song, album, year, peak, vid) in enumerate(ROWS, 1):
        items.append({"@type": "ListItem", "position": i, "item": {
            "@type": "MusicRecording", "name": song,
            "byArtist": {"@type": "MusicGroup", "name": "Journey"},
            "inAlbum": {"@type": "MusicAlbum", "name": album},
            "datePublished": str(year),
            "url": f"https://www.youtube.com/watch?v={vid}"}})
    lst = {"@context": "https://schema.org", "@type": "ItemList", "@id": URL + "#songs",
           "name": "Journey songs of the 1970s", "numberOfItems": len(items), "itemListElement": items}
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": " ".join(a)}} for q, a in FAQ]}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://musicofthe70s.net/"},
        {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://musicofthe70s.net/blog/"},
        {"@type": "ListItem", "position": 3, "name": "Artists", "item": "https://musicofthe70s.net/blog/artists/"},
        {"@type": "ListItem", "position": 4, "name": "Journey Songs", "item": URL}]}
    return "\n".join(f'  <script type="application/ld+json">\n{json.dumps(s, indent=2, ensure_ascii=False)}\n  </script>'
                     for s in (post, lst, faq, crumbs))


FAQ = [
    ("What was Journey's original name?",
     ["The band started out in San Francisco in 1973 as the Golden Gate Rhythm Section.",
      "It was put together by Herbie Herbert, a former Santana manager, who went on to manage Journey."]),
    ("Was Aynsley Dunbar Journey's first drummer?",
     ["No, Prairie Prince of the Tubes played drums when the band formed.",
      "Dunbar was hired on February 1, 1974, and played on every album up to Infinity."]),
    ("Which Journey song do San Francisco Giants fans hear at the ballpark?",
     ["Lights is played often at Giants games, including Game 2 of the 2010 World Series, when Steve Perry led the crowd himself.",
      "It was played again at the 2012 and 2014 World Series games in San Francisco."]),
    ("Who replaced Gregg Rolie in Journey?",
     ["Jonathan Cain took his place on keyboards.",
      "Cain's first Journey album was Escape in 1981."]),
    ("Is Journey in the Rock and Roll Hall of Fame?",
     ["Yes, Journey was inducted in 2017, with Pat Monahan of Train giving the induction speech.",
      "The inductees were Steve Perry, Neal Schon, Gregg Rolie, Ross Valory, Aynsley Dunbar, Steve Smith and Jonathan Cain."]),
]

SOURCES = [
    ("https://en.wikipedia.org/wiki/Journey_(band)", 'Wikipedia, "Journey (band)"'),
    ("https://en.wikipedia.org/wiki/Journey_discography", 'Wikipedia, "Journey discography"'),
    ("https://en.wikipedia.org/wiki/Infinity_(Journey_album)", 'Wikipedia, "Infinity (Journey album)"'),
    ("https://en.wikipedia.org/wiki/Evolution_(Journey_album)", 'Wikipedia, "Evolution (Journey album)"'),
    ("https://en.wikipedia.org/wiki/Wheel_in_the_Sky", 'Wikipedia, "Wheel in the Sky"'),
    ("https://en.wikipedia.org/wiki/Lights_(Journey_song)", 'Wikipedia, "Lights (Journey song)"'),
    ("https://en.wikipedia.org/wiki/Lovin%27,_Touchin%27,_Squeezin%27", 'Wikipedia, "Lovin\', Touchin\', Squeezin\'"'),
    ("https://ultimateclassicrock.com/journey-evolution-35/", 'Ultimate Classic Rock, "Journey, Evolution" anniversary feature'),
    ("https://www.songfacts.com/facts/journey/lovin-touchin-squeezin", 'Songfacts, "Lovin\', Touchin\', Squeezin\' by Journey"'),
    ("https://www.rockhall.com/inductees/journey", 'Rockhall.com, "Journey"'),
    ("https://musicbrainz.org/artist/abd506e1-6f2b-4d6f-b937-92c267f6f88b", 'MusicBrainz, "Journey"'),
]

SOURCE_LOG = [
    ("https://en.wikipedia.org/wiki/Journey_(band)", "formed San Francisco 1973 as Golden Gate Rhythm Section; Schon and Rolie ex-Santana; Valory and Tickner ex-Frumious Bandersnatch; Prairie Prince of the Tubes; Herbie Herbert; Dunbar hired Feb 1 1974, fired after Sept 2 1978 Day on the Green; Columbia after Feb 1974 showcase; Fleischman May to Sept 1977; Perry hired Oct 10 1977, debut Old Waldorf Oct 28 1977; Steve Smith ex-Montrose; Rolie left after Departure tour, Jonathan Cain replaced; Rock Hall 2017"),
    ("https://en.wikipedia.org/wiki/Journey_discography", "single peaks: Wheel in the Sky 57, Anytime 83, Lights 68, Just the Same Way 58, Lovin' Touchin' Squeezin' 16, Too Late 70, Any Way You Want It 23; no Hot 100 entry for To Play Some Music, On a Saturday Night, Spaceman; album peaks Journey 138, Look into the Future 100, Next 85, Infinity 21, Evolution 20, Departure 8, Escape 1; Infinity/Evolution/Departure 3x Platinum, Escape Diamond; release dates Apr 1 1975, Jan 1976, Feb 9 1977, Feb 29 1980, Jul 20 1981"),
    ("https://en.wikipedia.org/wiki/Infinity_(Journey_album)", "released Jan 30 1978, produced by Roy Thomas Baker, first album with Steve Perry, peak 21, 3x Platinum; writers Lights (Perry, Schon), Feeling That Way (Perry, Rolie, Dunbar), Anytime (Rolie, Schon, Valory, Roger Silver, Fleischman), Wheel in the Sky (Schon, Fleischman, Diane Valory); Perry and Rolie duet on Feeling That Way; Rolie lead on Anytime"),
    ("https://en.wikipedia.org/wiki/Evolution_(Journey_album)", "released Mar 20 1979, Roy Thomas Baker, peak 20, 3x Platinum, first album with Steve Smith; writers Too Late (Perry, Schon), Lovin' Touchin' Squeezin' (Perry), Just the Same Way (Schon, Rolie, Valory); Rolie and Perry co-lead on Just the Same Way"),
    ("https://en.wikipedia.org/wiki/Wheel_in_the_Sky", "began as Diane Valory poem Wheels in My Mind; lead single from Infinity, released March 1978; first Journey song on the Hot 100, peak 57; 2x Platinum"),
    ("https://en.wikipedia.org/wiki/Lights_(Journey_song)", "Perry and Schon; Perry wrote most of it in Los Angeles about LA, moved setting to San Francisco after joining; US release Aug 1978; peak 68; 2x Platinum; played at Giants World Series games 2010 (Perry led it at Game 2), 2012, 2014"),
    ("https://en.wikipedia.org/wiki/Lovin%27,_Touchin%27,_Squeezin%27", "written by Steve Perry; US release June 25 1979; B-side Daydream; peak 16 in November 1979; Canada 12; Journey's first Top 40 hit in the US"),
    ("https://ultimateclassicrock.com/journey-evolution-35/", "Evolution produced by Roy Thomas Baker, peak 20, over three million sold; Steve Smith recruited from Ronnie Montrose's band"),
    ("https://www.songfacts.com/facts/journey/lovin-touchin-squeezin", "Perry wrote it about a real breakup, per the Time3 liner notes: he saw his girlfriend kiss another man goodbye; extended fade of na na's"),
    ("https://www.rockhall.com/inductees/journey", "inducted 2017, performer category, Pat Monahan of Train inducted; inductees Dunbar, Smith, Valory, Perry, Rolie, Schon, Cain"),
    ("https://musicbrainz.org/artist/abd506e1-6f2b-4d6f-b937-92c267f6f88b", "MusicBrainz ID for Journey, American rock band, begin 1973"),
]


def card(img, w, h, alt, cat, title, blurb, href, srcset_extra=True):
    two = f", /images/blog/srcset/{img}-800w.webp 800w" if srcset_extra else ""
    twoj = f", /images/blog/srcset/{img}-800w.jpg 800w" if srcset_extra else ""
    return f"""            <div class="card post-card">
              <picture>
                <source type="image/webp" srcset="/images/blog/srcset/{img}-400w.webp 400w{two}" sizes="(max-width: 700px) 100vw, 33vw">
                <img class="post-thumb" src="/images/blog/srcset/{img}-400w.jpg"
                  srcset="/images/blog/srcset/{img}-400w.jpg 400w{twoj}"
                  sizes="(max-width: 700px) 100vw, 33vw" width="{w}" height="{h}" loading="lazy"
                  alt="{alt}">
              </picture>
              <div class="post-card-body">
                <span class="post-cat">{cat}</span>
                <h3>{title}</h3>
                <p>{blurb}</p>
                <a class="cta" href="{href}">Read post</a>
              </div>
            </div>"""


def picture(stub, alt, eager=False, h=675):
    return f"""        <picture>
          <source type="image/webp" srcset="/images/blog/srcset/{stub}-400w.webp 400w, /images/blog/srcset/{stub}-800w.webp 800w, /images/blog/srcset/{stub}-1200w.webp 1200w" sizes="(max-width: 700px) 100vw, 1100px">
          <img class="post-featured-img"
            src="/images/blog/{stub}-1200w.jpg"
            srcset="/images/blog/srcset/{stub}-400w.jpg 400w, /images/blog/srcset/{stub}-800w.jpg 800w, /images/blog/{stub}-1200w.jpg 1200w"
            sizes="(max-width: 700px) 100vw, 1100px"
            width="1200" height="{h}" loading="{'eager' if eager else 'lazy'}"
            alt="{alt}">
        </picture>"""


def P(*lines):
    return "\n".join(f"        <p>{l}</p>" for l in lines)


def build():
    check_ids()
    toc = [("journey-song-list", "Play Journey's 1970s Songs in One List"),
           ("rolie-years", "The Gregg Rolie Years, 1975 to 1977"),
           ("infinity", "Steve Perry Arrives on Infinity, 1978"),
           ("evolution", "Evolution and the First Top 20 Hit, 1979"),
           ("after-1979", "What Came Right After the 70s"),
           ("keep-listening", "Keep Listening"),
           ("faq", "Frequently Asked Questions"),
           ("sources", "Sources")]
    toc_html = "\n".join(f'            <li><a href="#{a}">{t}</a></li>' for a, t in toc)
    faq_html = "\n".join(
        "          <div class=\"faq-item\">\n          <h3>" + E(q) + "</h3>\n"
        + "\n".join(f"          <p>{E(x)}</p>" for x in a) + "\n          </div>" for q, a in FAQ)
    src_html = "\n".join(f'            <li><a href="{u}" target="_blank" rel="noopener">{E(t)}</a></li>' for u, t in SOURCES)

    keep = P('Journey sits on this site\'s <a href="/blog/artists/70s-rock-bands/">70s rock bands</a> page among the big rock bands the year-end singles chart missed.',
   'For a West Coast band that did top the charts, play the <a href="/blog/artists/eagles-the-band/">Eagles</a> next.',
   'Every act on the site is listed on the <a href="/blog/artists/70s-bands/">70s bands and singers</a> page.',
   'Or let <a href="/radio/">Listen Now</a> run 70s hits back to back with no list at all.')
    body = f"""      <article class="section seo-content">
        <h1>{E(TITLE)}</h1>

        <p class="post-byline">By <a href="https://musicofthe70s.net/about/author/">Charlie</a> &middot; Published {PUB_H} &middot; Updated {PUB_H}</p>
        <p class="listen-row"><button type="button" class="btn-primary listen-btn" data-yt="{ROWS[0][4]}" data-playlist="#journeySongsTable" data-title="Journey 1970s playlist">&#9654; Listen to the Whole Journey List</button></p>

        <p class="post-intro">Journey's biggest 70s hits are Lovin', Touchin', Squeezin', which reached No. 16 on the Billboard Hot 100 in 1979, and Wheel in the Sky, which reached No. 57 in 1978.</p>
        <p class="post-intro">The San Francisco rock band has been active since 1973 and had no No. 1 hits in the 1970s.</p>
        <p class="post-intro">This page plays 12 tracks from the band's first five albums, from the Gregg Rolie years of 1975 to the first Steve Perry hits of 1978 and 1979.</p>
        <p class="post-intro">Every one of them plays right here in one continuous list.</p>

        <aside class="facts-box" aria-label="Quick facts">
          <dl>
            <div><dt>Active</dt><dd>1973 to present</dd></div>
            <div><dt>Genre</dt><dd>Rock</dd></div>
            <div><dt>Biggest 70s hits</dt><dd>Lovin', Touchin', Squeezin' (No. 16, 1979); Wheel in the Sky (No. 57, 1978)</dd></div>
            <div><dt>No. 1 hits</dt><dd>None in the 1970s</dd></div>
            <div><dt>Hot 100 entries, 1970s</dt><dd>6, all from 1978 and 1979</dd></div>
            <div><dt>Label</dt><dd>Columbia</dd></div>
          </dl>
        </aside>

{picture("journey-singles-peaks", "Chart of the weekly Billboard Hot 100 peaks of Journey's six 1970s singles, led by Lovin', Touchin', Squeezin' at No. 16", eager=True)}
        <p class="post-img-caption">Hot 100 peaks of Journey's six 1970s chart singles.</p>
        <p class="post-img-caption">Chart: Music of the 70s, from the peaks in Wikipedia's Journey discography.</p>

        <nav class="toc-block" aria-label="Table of contents">
          <details class="toc-details" open>
            <summary>Table of Contents</summary>
            <ol>
{toc_html}
            </ol>
          </details>
        </nav>
        <script>if(window.matchMedia("(max-width: 699px)").matches){{document.querySelector(".toc-details").open=false;}}</script>

        <h2 id="journey-song-list">Play Journey's 1970s Songs in One List</h2>
{P("The list runs in release order, from the 1975 debut album to Evolution in 1979.",
   "Six of the twelve made the weekly Hot 100, three were singles that missed it, and three are album tracks.",
   "Press Play on any row and the list keeps going, song after song, until you press Stop.",
   "Tap a column heading to sort by year or by peak.")}

        <div class="data-table-wrap">
          <table class="data-table sortable-table" id="journeySongsTable" data-inline-player>
            <caption>12 tracks by Journey from 1975 to 1979, with album and weekly Billboard Hot 100 peak</caption>
            <thead>
              <tr>
                <th><span class="visually-hidden">Play</span></th>
                <th><button type="button" data-col="1" data-type="text">Song</button></th>
                <th><button type="button" data-col="2" data-type="text">Album</button></th>
                <th aria-sort="ascending"><button type="button" data-col="3" data-type="num">Year</button></th>
                <th><button type="button" data-col="4" data-type="num">Hot 100 Peak</button></th>
              </tr>
            </thead>
            <tbody>
{table_rows()}
            </tbody>
          </table>
        </div>

        <h3>The Short Version</h3>
        <ul>
          <li>Journey made no Billboard Year-End Hot 100 list in the 1970s, so every peak here is a weekly peak.</li>
          <li>All six chart singles came after Steve Perry joined in October 1977.</li>
          <li>Lovin', Touchin', Squeezin' was the band's first Top 40 hit in the United States.</li>
          <li>Each album from 1975 to 1979 charted higher than the one before it.</li>
        </ul>

        <h2 id="rolie-years">The Gregg Rolie Years, 1975 to 1977</h2>
{P("Journey began in San Francisco in 1973 around two former members of Santana, guitarist Neal Schon and keyboard player Gregg Rolie.",
   "Bassist Ross Valory and rhythm guitarist George Tickner came from the Bay Area band Frumious Bandersnatch.",
   "Drummer Aynsley Dunbar joined in 1974, and Columbia Records signed the band after a showcase that February.",
   "Rolie sang lead on the first three albums.")}

        <h3>Journey (1975)</h3>
{P("The debut album came out on April 1, 1975, and peaked at No. 138 on the Billboard 200.",
   "To Play Some Music opened the record and was released as a single, but it did not reach the Hot 100.",
   "Of a Lifetime, written by Rolie, Schon and Tickner, runs close to seven minutes.")}

        <h3>Look into the Future (1976)</h3>
{P("The second album arrived in January 1976 and climbed to No. 100.",
   "On a Saturday Nite, written by Rolie, was the single, and the title track is an eight-minute piece by Schon, Rolie and Diane Valory.")}

        <h3>Next (1977)</h3>
{P("Next followed on February 9, 1977, and reached No. 85.",
   "Spaceman, credited to Rolie and Dunbar, was the single.",
   "None of the first three albums produced a Hot 100 single.")}

        <h2 id="infinity">Steve Perry Arrives on Infinity, 1978</h2>
{P("Singer Robert Fleischman joined in May 1977 and was gone by September.",
   "Steve Perry was hired on October 10, 1977, and played his first show with the band at the Old Waldorf in San Francisco on October 28.",
   "Infinity, released on January 30, 1978, was produced by Roy Thomas Baker and was the first Journey album with Perry.",
   "It reached No. 21 and has since been certified 3x Platinum by the RIAA.")}

        <h3>Wheel in the Sky</h3>
{P("Wheel in the Sky started as a poem called Wheels in My Mind by Diane Valory, Ross Valory's wife.",
   "Schon and Fleischman share the writing credit with her.",
   "It was the first Journey single to enter the Hot 100, peaking at No. 57 in 1978.")}

        <h3>Lights</h3>
{P("Perry wrote most of Lights in Los Angeles before he joined, and it was first about that city.",
   "Once he was in Journey, he moved the setting to San Francisco and finished it with Schon.",
   "It was only a minor hit at No. 68, but it has since been certified 2x Platinum.")}

        <h3>Anytime and Feeling That Way</h3>
{P("Perry and Rolie trade lead vocals on Feeling That Way, and Rolie sings lead on Anytime.",
   "Anytime went out as a single and stopped at No. 83.")}

        <h2 id="evolution">Evolution and the First Top 20 Hit, 1979</h2>
{P("Dunbar was let go after the Infinity tour ended on September 2, 1978.",
   "His replacement, Steve Smith, came from Ronnie Montrose's band.",
   "Evolution came out in spring 1979 with Roy Thomas Baker producing again, and it reached No. 20.",
   "Ultimate Classic Rock reports that it sold more than three million copies.")}

{picture("journey-album-peaks", "Bar chart of Journey's Billboard 200 album peaks from 1975 to 1981, rising from No. 138 for the debut to No. 1 for Escape")}
        <p class="post-img-caption">Billboard 200 peaks of Journey's studio albums, 1975 to 1981.</p>
        <p class="post-img-caption">Chart: Music of the 70s, from the peaks in Wikipedia's Journey discography.</p>

        <h3>Lovin', Touchin', Squeezin'</h3>
{P("Perry wrote Lovin', Touchin', Squeezin' alone, and it was released as a single on June 25, 1979.",
   "In the liner notes to the Time3 box set, he said it came from a real breakup, after he saw his girlfriend kiss another man goodbye.",
   "It reached No. 16 on the Hot 100 that November and No. 12 in Canada.",
   "The record closes on a long, wordless sing-along fade.")}

        <h3>Just the Same Way and Too Late</h3>
{P("Just the Same Way, by Schon, Rolie and Valory, puts Rolie and Perry on lead vocals together and peaked at No. 58.",
   "Too Late, by Perry and Schon, also charted, at No. 70.")}

        <h2 id="after-1979">What Came Right After the 70s</h2>
{P("Departure followed on February 29, 1980, and gave Journey its first Top 10 album at No. 8.",
   "Its single Any Way You Want It reached No. 23.",
   "Rolie left the band after the Departure tour.",
   "Escape, released on July 20, 1981, went to No. 1 on the Billboard 200 and has since been certified Diamond.",
   "Those 1980s records sit outside this site's decade, so the Journey songs above stop at Evolution.")}

        <h2 id="keep-listening">Keep Listening</h2>
{keep}

        <section class="faq-block" id="faq">
          <h2>Frequently Asked Questions</h2>
{faq_html}
        </section>

        <section class="sources" id="sources">
          <h2>Sources</h2>
          <p>Hot 100 and Billboard 200 peaks come from Wikipedia's Journey discography, which cites Billboard.</p>
          <p>This site's own Billboard year-end data has no Journey entry from 1970 to 1979 (<a href="/about/methodology/">how the site's chart data works</a>).</p>
          <p>Each other fact was checked against the sources below on {PUB_H}.</p>
          <ul>
{src_html}
          </ul>
        </section>

        <section class="related-posts">
          <h2>You Might Also Like</h2>
          <div class="post-grid">
{card("led-zeppelin-1971", 400, 277, "Led Zeppelin in 1971, a related Artists post covering 15 essential songs", "Artists", "Led Zeppelin Songs: Play 15 Essentials and Their Stories", "Another rock band that sold albums far better than singles.", "/blog/artists/led-zeppelin-songs/")}
{card("pink-floyd-1973", 400, 249, "Pink Floyd at Earls Court in 1973, a related Artists post covering 12 of their songs", "Artists", "Pink Floyd Songs of the 70s: 12 Playable Tracks", "Money, Time, Wish You Were Here and the No. 1 Another Brick in the Wall.", "/blog/artists/pink-floyd-songs/", srcset_extra=False)}
{card("70s-rock-infographic", 400, 223, "70s Rock, a related genre overview covering hard rock, arena rock and punk", "Genres", "70s Rock: The Sound That Defined a Decade", "Where Journey fits in the decade's full rock story.", "/blog/genres/70s-rock/")}
          </div>
        </section>
      </article>"""

    funk = (ROOT / "blog/genres/70s-funk/index.html").read_text()
    head_top = funk[:funk.index("  <title>")]
    header = funk[funk.index("<body>"):funk.index("  <main>")]
    footer = funk[funk.index("  <footer"):funk.index("  <script src=\"/js/main.js\">")]
    page = f"""{head_top}  <title>{E(TITLE)}</title>
  <meta name="description" content="{E(DESC)}">
  <link rel="canonical" href="{URL}">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <meta name="theme-color" content="#1a1a2e">

  <meta property="og:title" content="{E(TITLE)}">
  <meta property="og:description" content="{E(DESC)}">
  <meta property="og:url" content="{URL}">
  <meta property="og:type" content="article">
  <meta property="og:image" content="{IMG}">
  <meta property="og:site_name" content="Music of the 70s">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{E(TITLE)}">
  <meta name="twitter:description" content="{E(DESC)}">
  <meta name="twitter:image" content="{IMG}">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@700;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/style.css">

{schema()}
</head>
{header}  <main>
    <div class="container">
      <nav class="breadcrumb">
        <a href="/">Home</a> &rsaquo;
        <a href="/blog/">Blog</a> &rsaquo;
        <a href="/blog/artists/">Artists</a> &rsaquo;
        <span>Journey Songs</span>
      </nav>

{body}
    </div>
  </main>

{footer}  <script src="/js/main.js"></script>
  <script src="/js/table-player.js"></script>
  <script src="/js/listen-button.js" defer></script>
  <script src="/js/sortable-table.js"></script>
</body>
</html>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page)
    log = [{"url": u, "claim": c, "opened": PUB} for u, c in SOURCE_LOG]
    (ROOT / "sources/log/journey-songs.json").write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    build()
