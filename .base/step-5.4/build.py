#!/usr/bin/env python3
"""Build /blog/artists/ac-dc-songs/ (rotation slot 5.4, bands-queue #2 AC/DC), 2026-11-23.
Peaks: Wikipedia "AC/DC discography" singles + albums tables (opened 2026-11-23).
Play IDs: data/official-videos.json (recorded 2026-11-23, see video-decisions.md).
Run: python3 .base/step-5.4/build.py
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "blog/artists/ac-dc-songs/index.html"
URL = "https://musicofthe70s.net/blog/artists/ac-dc-songs/"
PUB, PUB_H = "2026-11-23", "November 23, 2026"
TITLE = "AC/DC Songs of the 70s: 16 Tracks You Can Play in One List"
H1 = "AC/DC in the 70s: 16 Tracks You Can Play in One List"
DESC = ("AC/DC songs from 1975 to 1979, from It's a Long Way to the Top to Highway to Hell: "
        "16 tracks with chart peaks and one player for the whole list.")
IMG = "https://musicofthe70s.net/images/blog/acdc-album-peaks-1200w.jpg"

# (song, album, year, chart result, sort key, video id)
ROWS = [
    ("High Voltage", "T.N.T.", 1975, "UK No. 48", 48, "Nnjh-zp6pP4"),
    ("It's a Long Way to the Top (If You Wanna Rock 'n' Roll)", "T.N.T.", 1975, "UK No. 55", 55, "GChhRrU6BJU"),
    ("T.N.T.", "T.N.T.", 1975, "Single, did not chart in the US or UK", 999, "CiJeSSzu9Bo"),
    ("Jailbreak", "Dirty Deeds Done Dirt Cheap", 1976, "Single, did not chart in the US or UK", 999, "x7qQmpK9b1M"),
    ("Dirty Deeds Done Dirt Cheap", "Dirty Deeds Done Dirt Cheap", 1976, "UK No. 47", 47, "jsjdjWGDvFk"),
    ("Problem Child", "Dirty Deeds Done Dirt Cheap", 1976, "Single, did not chart in the US or UK", 999, "S4uwi5cUyco"),
    ("Let There Be Rock", "Let There Be Rock", 1977, "Single, did not chart in the US or UK", 999, "3f2g4RMfhS0"),
    ("Whole Lotta Rosie", "Let There Be Rock", 1977, "UK No. 36", 36, "BL58K-3XGKs"),
    ("Rock 'n' Roll Damnation", "Powerage", 1978, "UK No. 24", 24, "-0Oa5wvARSc"),
    ("Sin City", "Powerage", 1978, "Album track", 999, "pdnFm6uZSc8"),
    ("Riff Raff", "Powerage", 1978, "Album track", 999, "7S69xWkV4uM"),
    ("Highway to Hell", "Highway to Hell", 1979, "Hot 100 No. 47", 47, "l482T0yNkeo"),
    ("Girls Got Rhythm", "Highway to Hell", 1979, "Single, did not chart in the US or UK", 999, "YFMF4ZFmtnU"),
    ("Touch Too Much", "Highway to Hell", 1979, "Album track", 999, "JGftIcp2SC0"),
    ("Shot Down in Flames", "Highway to Hell", 1979, "Album track", 999, "UKwVvSleM6w"),
    ("Walk All Over You", "Highway to Hell", 1979, "Album track", 999, "_bP6aVG6L1w"),
]
E = html.escape
HALL = "The Rock and Roll Hall of Fame calls the early band a &ldquo;raw, proto-punk alternative to overblown '70s fare.&rdquo;"


def check_ids():
    vids = json.loads((ROOT / "data/official-videos.json").read_text())["videos"]
    missing = [r[5] for r in ROWS if r[5] not in vids]
    if missing:
        raise SystemExit(f"IDs not in data/official-videos.json: {missing}")


def table_rows():
    out = []
    for song, album, year, res, key, vid in ROWS:
        t = E(f"{song} by AC/DC")
        out.append(
            f'              <tr><td class="ohw-listen"><button type="button" class="ohw-play" data-yt="{vid}" '
            f'data-title="{t}" aria-label="Play {t} here">&#9654; Play</button></td>'
            f'<td class="ohw-song">{E(song)}</td><td>{E(album)}</td>'
            f'<td data-sort="{year}">{year}</td><td data-sort="{key}">{E(res)}</td></tr>')
    return "\n".join(out)


FAQ = [
    ("Where does the name AC/DC come from?",
     ["Malcolm and Angus Young took it from the AC/DC marking on their sister Margaret's sewing machine adapter.",
      "The letters stand for alternating current and direct current, and fans say them one at a time."]),
    ("Who designed the AC/DC logo?",
     ["American typographer Gerard Huerta designed the lightning-bolt logo in 1977.",
      "It first appeared on the Let There Be Rock album."]),
    ("Why did Atlantic wait until 1981 to release Dirty Deeds Done Dirt Cheap in the US?",
     ["Louder Sound reports that Atlantic executives in America had misgivings about Bon Scott's gritty vocal style.",
      "The album came out there in March 1981, after Back in Black had made the band a US act."]),
    ("What was Bon Scott's job before he sang for AC/DC?",
     ["Scott had sung in the Valentines and in Fraternity, and he worked as AC/DC's chauffeur before he auditioned.",
      "The band made him lead singer in 1974, and he sang lead on all 16 AC/DC songs in the list above."]),
    ("When was AC/DC inducted into the Rock and Roll Hall of Fame?",
     ["The band was inducted in 2003.",
      "The Hall's biography calls the early AC/DC a \"raw, proto-punk alternative to overblown '70s fare.\""]),
]

SOURCES = [
    ("https://www.loudersound.com/features/ac-dc-the-making-of-highway-to-hell", 'Louder Sound, "AC/DC: The Making of Highway to Hell"'),
    ("https://www.loudersound.com/features/cheap-thrills-how-acdc-were-repackaged-for-international-stardom", 'Louder Sound, "Cheap Thrills: How AC/DC Were Repackaged for International Stardom"'),
    ("https://www.rockhall.com/inductees/acdc", 'Rock and Roll Hall of Fame, "AC/DC"'),
    ("https://en.wikipedia.org/wiki/AC/DC", 'Wikipedia, "AC/DC"'),
    ("https://en.wikipedia.org/wiki/AC/DC_discography", 'Wikipedia, "AC/DC discography"'),
    ("https://en.wikipedia.org/wiki/Highway_to_Hell_(song)", 'Wikipedia, "Highway to Hell (song)"'),
    ("https://en.wikipedia.org/wiki/It%27s_a_Long_Way_to_the_Top_(If_You_Wanna_Rock_%27n%27_Roll)", 'Wikipedia, "It\'s a Long Way to the Top (If You Wanna Rock \'n\' Roll)"'),
    ("https://en.wikipedia.org/wiki/Whole_Lotta_Rosie", 'Wikipedia, "Whole Lotta Rosie"'),
    ("https://en.wikipedia.org/wiki/Dirty_Deeds_Done_Dirt_Cheap_(song)", 'Wikipedia, "Dirty Deeds Done Dirt Cheap (song)"'),
    ("https://en.wikipedia.org/wiki/Jailbreak_(AC/DC_song)", 'Wikipedia, "Jailbreak (AC/DC song)"'),
    ("https://en.wikipedia.org/wiki/T.N.T._(song)", 'Wikipedia, "T.N.T. (song)"'),
    ("https://musicbrainz.org/artist/66c662b6-6e2f-4930-8610-912e24c63ed1", 'MusicBrainz, "AC/DC"'),
]

SOURCE_LOG = [
    ("https://www.loudersound.com/features/ac-dc-the-making-of-highway-to-hell", "Mick Wall, Classic Rock 191, 6 Nov 2013: Atlantic meeting in New York January 1979 agreed AC/DC needed a new producer to crack America; George Young stepped aside; Mutt Lange, 31, had produced the Boomtown Rats' No. 1 hit; basic tracking began Saturday March 24 at Roundhouse Studios, recording completed three weeks later on April 14; Atlantic disliked the album title and tried to get it changed; first AC/DC album to crack the US Top 20, eventually selling more than seven million copies; no earlier AC/DC album had gained traction in America"),
    ("https://www.loudersound.com/features/cheap-thrills-how-acdc-were-repackaged-for-international-stardom", "Geoff Barton, 14 May 2018: Atlantic cherry-picked songs from the two Australia-only albums for the international High Voltage; majority from T.N.T., only Little Lover and She's Got Balls from High Voltage; first non-Albert Productions release; UK tour began June 11 1976 at Glasgow City Hall and ended July 7 at London Lyceum, 19 dates; international Dirty Deeds had subtly different versions; Dirty Deeds not released officially in the US until March 1981 because Atlantic execs had misgivings about Scott's gritty vocal style; Scott died February 1980"),
    ("https://www.rockhall.com/inductees/acdc", "bio: 'raw, proto-punk alternative to overblown '70s fare'; lists T.N.T. (1975) and Highway to Hell (1979); inducted 2003"),
    ("https://en.wikipedia.org/wiki/AC/DC", "formed Sydney November 1973 by Malcolm and Angus Young; name from sister Margaret and sewing machine AC adapter; Scott joined September 1974 after working as chauffeur; logo by Gerard Huerta 1977 first on Let There Be Rock; Vanda and George Young producers; Rock Hall 2003; Scott died seven months after Highway to Hell, Brian Johnson recruited, Back in Black 1980"),
    ("https://en.wikipedia.org/wiki/AC/DC_discography", "albums: High Voltage (Australasia) 17 Feb 1975; T.N.T. 1 Dec 1975; High Voltage (international) 14 May 1976 US peak 146; Dirty Deeds 20 Sep 1976; Let There Be Rock 21 Mar 1977 US 154; Powerage 5 May 1978 US 133; If You Want Blood 13 Oct 1978 US 113; Highway to Hell 27 Jul 1979 US 17, RIAA 8x Platinum. Singles: Highway to Hell US Hot 100 47; UK peaks High Voltage 48, Long Way to the Top 55, Dirty Deeds 47, Whole Lotta Rosie 36, Rock 'n' Roll Damnation 24; T.N.T., Jailbreak, Problem Child, Let There Be Rock, Girls Got Rhythm no UK or US chart entry"),
    ("https://en.wikipedia.org/wiki/Highway_to_Hell_(song)", "written by Angus Young, Malcolm Young and Bon Scott, Angus credited for the riff; single released 27 July 1979, same day as album; title from constant touring; produced by Mutt Lange"),
    ("https://en.wikipedia.org/wiki/It%27s_a_Long_Way_to_the_Top_(If_You_Wanna_Rock_%27n%27_Roll)", "Scott had been a drummer in a pipe band and taught himself bagpipes for the song, set bought for AU$479; video filmed 23 February 1976 on a flatbed truck on Swanston Street Melbourne with the Rats of Tobruk Pipe band"),
    ("https://en.wikipedia.org/wiki/Whole_Lotta_Rosie", "closes Let There Be Rock; single in 1977 backed by Dog Eat Dog; main riff from earlier recording Dirty Eyes, released on Volts in the Bonfire box set; live Glasgow recording of 30 April 1978 released as single in October 1978"),
    ("https://en.wikipedia.org/wiki/Dirty_Deeds_Done_Dirt_Cheap_(song)", "title from Beany and Cecil character Dishonest John's calling card; single Australia October 1976, UK February 1977"),
    ("https://en.wikipedia.org/wiki/Jailbreak_(AC/DC_song)", "only on the Australian edition of Dirty Deeds; not released in US, Canada, Japan until October 1984 on the '74 Jailbreak EP"),
    ("https://en.wikipedia.org/wiki/T.N.T._(song)", "single 1976; first UK headline tour named Lock Up Your Daughters after a line in the song"),
    ("https://musicbrainz.org/artist/66c662b6-6e2f-4930-8610-912e24c63ed1", "MusicBrainz ID for AC/DC (matches Wikidata P434 on Q27593), Australian rock band, begin 1973"),
]


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
        "about": {"@type": "MusicGroup", "name": "AC/DC", "genre": ["Hard rock"], "foundingDate": "1973",
                  "foundingLocation": {"@type": "Place", "name": "Sydney, Australia"},
                  "sameAs": ["https://en.wikipedia.org/wiki/AC/DC",
                             "https://musicbrainz.org/artist/66c662b6-6e2f-4930-8610-912e24c63ed1"]},
    }
    items = []
    for i, (song, album, year, res, key, vid) in enumerate(ROWS, 1):
        items.append({"@type": "ListItem", "position": i, "item": {
            "@type": "MusicRecording", "name": song,
            "byArtist": {"@type": "MusicGroup", "name": "AC/DC"},
            "inAlbum": {"@type": "MusicAlbum", "name": album},
            "datePublished": str(year),
            "url": f"https://www.youtube.com/watch?v={vid}"}})
    lst = {"@context": "https://schema.org", "@type": "ItemList", "@id": URL + "#songs",
           "name": "AC/DC songs of the 1970s", "numberOfItems": len(items), "itemListElement": items}
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": " ".join(a)}} for q, a in FAQ]}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://musicofthe70s.net/"},
        {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://musicofthe70s.net/blog/"},
        {"@type": "ListItem", "position": 3, "name": "Artists", "item": "https://musicofthe70s.net/blog/artists/"},
        {"@type": "ListItem", "position": 4, "name": "AC/DC Songs", "item": URL}]}
    return "\n".join(f'  <script type="application/ld+json">\n{json.dumps(s, indent=2, ensure_ascii=False)}\n  </script>'
                     for s in (post, lst, faq, crumbs))


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
    toc = [("acdc-song-list", "Play 16 AC/DC Tracks From 1975 to 1979"),
           ("bon-scott-years", "Bon Scott and the Australian Albums, 1975 to 1976"),
           ("rock-and-powerage", "Let There Be Rock and Powerage, 1977 to 1978"),
           ("highway-to-hell", "Highway to Hell and Mutt Lange, 1979"),
           ("after-1979", "What Came Right After the 70s"),
           ("keep-listening", "Keep Listening"),
           ("faq", "Frequently Asked Questions"),
           ("sources", "Sources")]
    toc_html = "\n".join(f'            <li><a href="#{a}">{t}</a></li>' for a, t in toc)
    faq_html = "\n".join(
        "          <div class=\"faq-item\">\n          <h3>" + E(q) + "</h3>\n"
        + "\n".join(f"          <p>{E(x)}</p>" for x in a) + "\n          </div>" for q, a in FAQ)
    src_html = "\n".join(f'            <li><a href="{u}" target="_blank" rel="noopener">{E(t)}</a></li>' for u, t in SOURCES)

    keep = P('AC/DC songs are missing from the <a href="/blog/artists/70s-rock-bands/">70s rock bands</a> ranking, which counts only acts with a Billboard year-end hit from 1970 to 1979.',
             'For more loud guitars from the same decade, play the <a href="/blog/genres/70s-hard-rock/">70s hard rock</a> page next.',
             'Every act on the site is listed on the <a href="/blog/artists/70s-bands/">70s bands and singers</a> page.',
             'Or let <a href="/radio/">Listen Now</a> run 70s hits back to back with no list at all.')
    body = f"""      <article class="section seo-content">
        <h1>{E(H1)}</h1>

        <p class="post-byline">By <a href="https://musicofthe70s.net/about/author/">Charlie</a> &middot; Published {PUB_H} &middot; Updated {PUB_H}</p>
        <p class="listen-row"><button type="button" class="btn-primary listen-btn" data-yt="{ROWS[0][5]}" data-playlist="#acdcSongsTable" data-title="AC/DC 1970s playlist">&#9654; Listen to the Whole AC/DC List</button></p>

        <p class="post-intro">AC/DC songs of the 70s are led by Highway to Hell, which reached No. 47 on the Billboard Hot 100 as a 1979 single.</p>
        <p class="post-intro">The Australian hard rock band formed in Sydney in 1973 and had no No. 1 hits in the 1970s.</p>
        <p class="post-intro">This page plays 16 tracks from the Bon Scott years, 1975 to 1979.</p>
        <p class="post-intro">Every one of them plays right here in one continuous list, from the band's own YouTube channel.</p>

        <aside class="facts-box" aria-label="Quick facts">
          <dl>
            <div><dt>Active</dt><dd>1973 to present</dd></div>
            <div><dt>Genre</dt><dd>Hard rock</dd></div>
            <div><dt>Biggest 70s hits</dt><dd>Highway to Hell (Hot 100 No. 47, 1979); Whole Lotta Rosie (UK No. 36, 1977)</dd></div>
            <div><dt>No. 1 hits</dt><dd>None in the 1970s</dd></div>
            <div><dt>Hot 100 singles, 1970s</dt><dd>1, Highway to Hell</dd></div>
            <div><dt>Label</dt><dd>Albert Productions (Australia), Atlantic (international)</dd></div>
          </dl>
        </aside>

{picture("acdc-album-peaks", "Chart of the US Billboard 200 peaks of the 1970s albums behind the AC/DC songs on this page, led by Highway to Hell at No. 17", eager=True)}
        <p class="post-img-caption">US Billboard 200 peaks of AC/DC's 1970s albums released in the United States.</p>
        <p class="post-img-caption">Chart: Music of the 70s, from the peaks in Wikipedia's AC/DC discography.</p>

        <nav class="toc-block" aria-label="Table of contents">
          <details class="toc-details" open>
            <summary>Table of Contents</summary>
            <ol>
{toc_html}
            </ol>
          </details>
        </nav>
        <script>if(window.matchMedia("(max-width: 699px)").matches){{document.querySelector(".toc-details").open=false;}}</script>

        <h2 id="acdc-song-list">Play 16 AC/DC Tracks From 1975 to 1979</h2>
{P("The list runs in release order, from the 1975 Australian albums to Highway to Hell in 1979.",
   "Only Highway to Hell reached the Billboard Hot 100, and five more singles made the UK Singles Chart.",
   "Another five of the sixteen were singles that missed both charts, and five are album tracks.",
   "Press Play on any row and the list keeps going, song after song, until you press Stop.",
   "Tap a column heading to sort the AC/DC songs by year or by chart result.")}

        <div class="data-table-wrap">
          <table class="data-table sortable-table" id="acdcSongsTable" data-inline-player>
            <caption>16 tracks by AC/DC from 1975 to 1979, with album and chart result</caption>
            <thead>
              <tr>
                <th><span class="visually-hidden">Play</span></th>
                <th><button type="button" data-col="1" data-type="text">Song</button></th>
                <th><button type="button" data-col="2" data-type="text">Album</button></th>
                <th aria-sort="ascending"><button type="button" data-col="3" data-type="num">Year</button></th>
                <th><button type="button" data-col="4" data-type="num">Chart Result</button></th>
              </tr>
            </thead>
            <tbody>
{table_rows()}
            </tbody>
          </table>
        </div>

        <h3>Which AC/DC Songs Were Hits in the 70s?</h3>
        <ul>
          <li>Highway to Hell is the only AC/DC single from the 1970s on the Billboard Hot 100, at No. 47.</li>
          <li>Rock 'n' Roll Damnation reached No. 24 on the UK Singles Chart in 1978, and Whole Lotta Rosie reached No. 36 in 1977.</li>
          <li>This site's Billboard year-end data from 1970 to 1979 has no AC/DC entry, so every peak here is a weekly peak.</li>
          <li>Album years follow the first release, and several 1976 songs came out in Australia before they reached the United States.</li>
        </ul>

        <h2 id="bon-scott-years">Bon Scott and the Australian Albums, 1975 to 1976</h2>
{P("Brothers Malcolm and Angus Young formed AC/DC in Sydney in November 1973.",
   "Singer Bon Scott joined in September 1974 after working as the band's chauffeur.",
   "Harry Vanda and George Young, an older brother of the Youngs, produced the early AC/DC songs.",
   HALL)}

        <h3>High Voltage and T.N.T. (1975)</h3>
{P("High Voltage came out in Australia and New Zealand on February 17, 1975.",
   "T.N.T. followed on December 1, 1975, and opened with It's a Long Way to the Top.",
   "Scott had been a drummer in a pipe band, so he taught himself the bagpipes for that song.",
   "The video was shot on a flatbed truck on Swanston Street in Melbourne on February 23, 1976.",
   "The Rats of Tobruk Pipe band rode along.")}

        <h3>The International High Voltage (1976)</h3>
{P("Atlantic Records built the international High Voltage, released on May 14, 1976, from songs on the two Australia-only albums.",
   "Louder Sound counts only two of them, Little Lover and She's Got Balls, from the original High Voltage, with the rest taken from T.N.T.",
   "The record reached No. 146 on the Billboard 200.",
   "The Lock Up Your Daughters UK tour ran from June 11 to July 7, 1976.",
   "Its name came from a line in T.N.T.")}

        <h3>Dirty Deeds and Jailbreak (1976)</h3>
{P("Dirty Deeds Done Dirt Cheap reached Australian stores in September 1976.",
   "Atlantic did not release it officially in the United States until March 1981.",
   "Angus Young took the title from the cartoon Beany and Cecil.",
   "Its character Dishonest John carries a card reading Dirty Deeds Done Dirt Cheap.",
   "Jailbreak was on the Australian edition only, and it did not reach US stores until the 1984 '74 Jailbreak EP.")}

        <h2 id="rock-and-powerage">Let There Be Rock and Powerage, 1977 to 1978</h2>
{P("Let There Be Rock arrived in Australia on March 21, 1977, and the international version followed that June.",
   "The album reached No. 154 in the United States.",
   "Two of its AC/DC songs, the title track and Whole Lotta Rosie, are in the list above.")}

        <h3>Whole Lotta Rosie</h3>
{P("Whole Lotta Rosie closes Let There Be Rock and was released as a single in 1977 with Dog Eat Dog on the B-side.",
   "Its main riff first appeared in an earlier recording called Dirty Eyes, which came out much later on the Volts disc of the Bonfire box set.",
   "A live version recorded in Glasgow on April 30, 1978, was released as a single that October.",
   "The studio single reached No. 36 on the UK Singles Chart.")}

{picture("acdc-uk-singles-peaks", "Chart of the UK Singles Chart peaks of five AC/DC singles from 1976 to 1978, led by Rock 'n' Roll Damnation at No. 24")}
        <p class="post-img-caption">UK Singles Chart peaks of five AC/DC singles from 1976 to 1978.</p>
        <p class="post-img-caption">Chart: Music of the 70s, from the peaks in Wikipedia's AC/DC discography.</p>

        <h3>Powerage and If You Want Blood (1978)</h3>
{P("Powerage was released on May 5, 1978, and reached No. 133 in the United States.",
   "Rock 'n' Roll Damnation, its single, climbed to No. 24 in the UK.",
   "The live album If You Want Blood You've Got It followed on October 13, 1978, and reached No. 113.",
   "It includes the Glasgow recording of Whole Lotta Rosie.")}

        <h2 id="highway-to-hell">Highway to Hell and Mutt Lange, 1979</h2>
{P("A meeting in New York in January 1979 ended with agreement that AC/DC needed a new producer to break America, according to Louder Sound.",
   "George Young stepped aside, and the job went to Mutt Lange, then 31 and fresh from producing a No. 1 hit for the Boomtown Rats.",
   "Basic tracking began on Saturday, March 24, at Roundhouse Studios, and recording finished three weeks later, on April 14.")}

        <h3>Highway to Hell</h3>
{P("Angus Young, Malcolm Young and Bon Scott wrote Highway to Hell, the best known of these AC/DC songs, with Angus credited for the guitar riff.",
   "The title came from the band's nonstop touring, and Atlantic disliked it enough to ask for a change.",
   "The album and the single were both released on July 27, 1979.",
   "The album reached No. 17, the first AC/DC record to reach the US top 20, and the RIAA has since certified it 8x Platinum.")}

        <h3>Girls Got Rhythm and the rest of the album</h3>
{P("Girls Got Rhythm was the other 1979 single, and it missed both the US and UK charts.",
   "Touch Too Much, Shot Down in Flames and Walk All Over You are album tracks in this list.",
   "Touch Too Much was released as a single in 1980.")}

        <h2 id="after-1979">What Came Right After the 70s</h2>
{P("Bon Scott died in February 1980, about seven months after Highway to Hell came out.",
   "Singer Brian Johnson replaced him, and the band recorded Back in Black later that year.",
   "Those records sit outside this site's decade, so the list above stops at Highway to Hell.")}

        <h2 id="keep-listening">Keep Listening</h2>
{keep}

        <section class="faq-block" id="faq">
          <h2>Frequently Asked Questions</h2>
{faq_html}
        </section>

        <section class="sources" id="sources">
          <h2>Sources</h2>
          <p>Hot 100, UK Singles Chart and Billboard 200 peaks come from Wikipedia's AC/DC discography, which cites Billboard and the Official Charts Company.</p>
          <p>This site's own Billboard year-end data has no AC/DC entry from 1970 to 1979 (<a href="/about/methodology/">how the site's chart data works</a>).</p>
          <p>Each other fact was checked against the sources below on {PUB_H}.</p>
          <ul>
{src_html}
          </ul>
        </section>

        <section class="related-posts">
          <h2>You Might Also Like</h2>
          <div class="post-grid">
{card("led-zeppelin-1971", 400, 277, "Led Zeppelin in 1971, a related Artists post covering 15 essential songs", "Artists", "Led Zeppelin Songs: Play 15 Essentials and Their Stories", "Another hard rock band that sold albums far better than singles.", "/blog/artists/led-zeppelin-songs/")}
{card("queen-1977", 400, 223, "Queen photographed in 1977 for their News of the World press kit", "Artists", "Queen Freddie Mercury: Two Nights That Defined Their 70s", "The other big rock band that crossed from the UK to US arenas in the 70s.", "/blog/artists/queen-freddie-mercury/")}
{card("70s-rock-infographic", 400, 223, "70s Rock, a related genre overview covering hard rock, arena rock and punk", "Genres", "70s Rock: The Sound That Defined a Decade", "Where AC/DC fits in the decade's full rock story.", "/blog/genres/70s-rock/")}
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
        <span>AC/DC Songs</span>
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
    (ROOT / "sources/log/ac-dc-songs.json").write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n")
    print("wrote", OUT)


if __name__ == "__main__":
    build()
