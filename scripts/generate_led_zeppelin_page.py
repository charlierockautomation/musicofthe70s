#!/usr/bin/env python3
"""Build the Led Zeppelin Artists post (blog/artists/led-zeppelin-songs/index.html).

Led Zeppelin has no rows in data/billboard/*.json or data/radio/radio-songs.json (the band
refused to chase singles), so unlike the Elton John page nothing here comes from the site's
chart JSON. Every chart peak, album date, certification and story fact is taken from the
linked Wikipedia articles, read 2026-10-11, and the page credits them that way. Hot 100 peaks
are Wikipedia's, never year-end ranks. YouTube IDs are the band's official channel uploads
(channel checked with yt-dlp 2026-10-11); embeddable/madeForKids status is recorded by
scripts/youtube_status.py.

Run: python3 scripts/generate_led_zeppelin_page.py
"""
import html
import json
from datetime import date

from genre_page_common import ROOT, read, play_button, write
from generate_country_page import p, tbl, pic as _pic


def pic(*a, **k):
    """pic() plus inline height:auto on in-body images (no global rule exists, so the fixed height
    attribute would stretch them at mobile widths)."""
    out = _pic(*a, **k)
    if k.get("lazy", True):
        cap = ";max-width:420px" if a[0] == "jimmy-page-1977" else ""
        out = out.replace("<img\n", f'<img style="height:auto;margin:1.5rem auto{cap}"\n', 1)
    return out

SLUG = "led-zeppelin-songs"
URL = f"https://musicofthe70s.net/blog/artists/{SLUG}/"
TITLE = "Led Zeppelin Songs: Play 15 Essentials and Their Stories"
PUBLISHED = date(2026, 10, 11)
IMG = "led-zeppelin-1971"

# (title, album, album year, Wikipedia US Hot 100 peak or None, official-channel YouTube ID)
SONGS = [
    ("Immigrant Song", "Led Zeppelin III", 1970, 16, "P3Y8OWkiUts"),
    ("Whole Lotta Love", "Led Zeppelin II", 1969, 4, "HibBnC6SVk8"),
    ("Black Dog", "Led Zeppelin IV", 1971, 15, "2KPEHohJMuw"),
    ("Rock and Roll", "Led Zeppelin IV", 1971, 47, "D2lSwosw9xY"),
    ("Stairway to Heaven", "Led Zeppelin IV", 1971, None, "QkF3oxziUI4"),
    ("Going to California", "Led Zeppelin IV", 1971, None, "NrUIJY_Xu2s"),
    ("Since I've Been Loving You", "Led Zeppelin III", 1970, None, "vcIem-L398w"),
    ("The Song Remains the Same", "Houses of the Holy", 1973, None, "MTRgvPrUuU8"),
    ("Dancing Days", "Houses of the Holy", 1973, None, "mbsCo7TvzRQ"),
    ("D'yer Mak'er", "Houses of the Holy", 1973, 20, "rwy07azI8nc"),
    ("Over the Hills and Far Away", "Houses of the Holy", 1973, 51, "Am9gu4wkY9E"),
    ("Kashmir", "Physical Graffiti", 1975, None, "ww9484EM2OQ"),
    ("Trampled Under Foot", "Physical Graffiti", 1975, 38, "2KdymN0xDQQ"),
    ("Fool in the Rain", "In Through the Out Door", 1979, 21, "I57nIP0vc44"),
    ("All My Love", "In Through the Out Door", 1979, None, "vwFz3EThGMU"),
]

# Wikipedia "Led Zeppelin discography": 1970s studio albums, release date, Billboard 200 peak, RIAA.
ALBUMS = [
    ("Led Zeppelin III", "Oct 5, 1970", 1, "6× Platinum"),
    ("Led Zeppelin IV", "Nov 8, 1971", 2, "2× Diamond (24× Platinum)"),
    ("Houses of the Holy", "Mar 28, 1973", 1, "Diamond (11× Platinum)"),
    ("Physical Graffiti", "Feb 24, 1975", 1, "Diamond (16× Platinum)"),
    ("Presence", "Mar 31, 1976", 1, "3× Platinum"),
    ("In Through the Out Door", "Aug 22, 1979", 1, "6× Platinum"),
]

NUM = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}


def main():
    n = len(SONGS)
    peaks = [s for s in SONGS if s[3]]
    peaks_sorted = sorted(peaks, key=lambda s: s[3])
    best = peaks_sorted[0]
    n_ones = sum(1 for a in ALBUMS if a[2] == 1)
    n_alb = len(ALBUMS)
    no_single = [s for s in SONGS if not s[3]]

    rows = []
    for t, alb, yr, pk, yt in SONGS:
        rows.append(f'              <tr><td class="ohw-listen">{play_button(yt, t, "Led Zeppelin")}</td>'
                    f'<td class="ohw-song">{html.escape(t)}</td><td>{html.escape(alb)}</td><td>{yr}</td>'
                    f'<td data-sort="{pk or 0}">{pk if pk else "None listed"}</td></tr>')

    single_rows = [[html.escape(t), html.escape(alb), yr, pk] for t, alb, yr, pk, _ in sorted(peaks, key=lambda s: s[3])]
    album_rows = [[html.escape(a), d, f"#{pk}", c] for a, d, pk, c in ALBUMS]

    faq = [
        ("What are the most famous Led Zeppelin songs?",
         ["The most famous Led Zeppelin songs include Stairway to Heaven, Whole Lotta Love, Kashmir, Black Dog, and Immigrant Song.",
          "Wikipedia says Stairway to Heaven was the most requested song on US FM radio in the 1970s, even though it was never a US single.",
          "All five are in the playable list at the top of this page."]),
        ("What was the highest-charting Led Zeppelin single in the US?",
         ["Whole Lotta Love was the highest-charting Led Zeppelin single in the US, peaking at number four on the Billboard Hot 100.",
          "Wikipedia calls it the band's only US top-10 single, and it was certified gold.",
          "It came from Led Zeppelin II, released in 1969."]),
        ("Why did Led Zeppelin never release Stairway to Heaven as a single?",
         ["Led Zeppelin never released Stairway to Heaven as a US single because manager Peter Grant refused label requests in 1972 and 1973.",
          "In 1975, Jimmy Page told Rolling Stone, \"We were careful to never release it as a single.\"",
          "The band preferred albums to be heard as complete listening experiences."]),
        ("How many number one albums did Led Zeppelin have in the 1970s?",
         [f"Led Zeppelin had {NUM[n_ones]} number one albums on the Billboard 200 among its {NUM[n_alb]} studio albums of the 1970s.",
          "Led Zeppelin III, Houses of the Holy, Physical Graffiti, Presence, and In Through the Out Door all reached number one.",
          "Led Zeppelin IV peaked at number two, according to Wikipedia's discography."]),
        ("When did Led Zeppelin break up?",
         ["Led Zeppelin announced its breakup on December 4, 1980, after drummer John Bonham died on September 25, 1980.",
          "Bonham's death was ruled accidental, caused by asphyxiation from vomit.",
          "The band formed in London in 1968 and was inducted into the Rock and Roll Hall of Fame in 1995."]),
    ]
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": " ".join(a)}} for q, a in faq]},
        indent=2, ensure_ascii=False)
    faq_ld = "\n".join("  " + l for l in faq_ld.split("\n"))
    faq_html = "\n".join(
        f'          <div class="faq-item">\n            <h3>{html.escape(q)}</h3>\n' + "\n".join(f"            <p>{html.escape(l)}</p>" for l in a) + "\n          </div>"
        for q, a in faq).replace("&#x27;", "'").replace("&quot;", '"')

    desc = (f"Led Zeppelin songs to play here: {n} essentials, the {len(peaks)} that charted on the Hot 100, and the albums that ruled instead. "
            "Stairway, Kashmir and more.")
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

    toc = [("zeppelin-song-list", f"Led Zeppelin Songs: Play All {n} Essentials"),
           ("albums-not-singles", "Albums, Not Singles"),
           ("hot-100", "Led Zeppelin Songs on the Hot 100"),
           ("stairway", "Stairway to Heaven: The Song They Never Released"),
           ("iv", "Led Zeppelin IV: No Title, Four Symbols"),
           ("graffiti", "Physical Graffiti and Kashmir"),
           ("holy", "Houses of the Holy: A Reggae Joke and a Cover"),
           ("four-players", "Four Players, One Sound"),
           ("end", "1979 to 1980: Knebworth and the End"),
           ("sources", "Sources"), ("faq", "Frequently Asked Questions")]
    toc_html = "\n".join(f'            <li><a href="#{i}">{t}</a></li>' for i, t in toc)

    body = f'''        <h2 id="zeppelin-song-list">Led Zeppelin Songs: Play All {n} Essentials</h2>
{p(f"Here are {n} Led Zeppelin songs, from the 1970 single Immigrant Song to the 1979 album track All My Love.",
   "Press Play on any row to watch it here, and tap a heading to sort.")}

        <div class="data-table-wrap scroll-list">
          <table class="data-table sortable-table" id="zeppelinSongsTable" data-inline-player>
            <caption>{n} Led Zeppelin songs by album, with each song's US Billboard Hot 100 peak where Wikipedia lists one</caption>
            <thead>
              <tr>
                <th><span class="visually-hidden">Play</span></th>
                <th><button type="button" data-col="1" data-type="text">Song</button></th>
                <th><button type="button" data-col="2" data-type="text">Album</button></th>
                <th aria-sort="ascending"><button type="button" data-col="3" data-type="num">Album Year</button></th>
                <th><button type="button" data-col="4" data-type="num">US Hot 100 Peak</button></th>
              </tr>
            </thead>
            <tbody>
{chr(10).join(rows)}
            </tbody>
          </table>
        </div>
{p("Album Year is the year the album came out.",
   "Whole Lotta Love is on a 1969 album, but it was a US single that climbed the Hot 100 and fits the band's 1970s story.",
   "US Hot 100 Peak comes from Wikipedia's Led Zeppelin discography, and &quot;None listed&quot; means no US Hot 100 single appears there.")}

        <h2 id="albums-not-singles">Albums, Not Singles</h2>
{p("Most Led Zeppelin songs never had a US single behind them.",
   f"Of the {n} songs above, {NUM[len(no_single)]} have no Hot 100 peak listed.",
   "That was a choice, not an accident.")}

        <h3>Why the Band Avoided 45s</h3>
{p("Wikipedia says the band viewed albums as complete listening experiences.",
   "They disliked re-editing tracks to fit a single.",
   "Some songs were still issued as singles without the band's consent, mostly in the US.")}

        <h3>The Deal That Made It Possible</h3>
{p("In November 1968, Atlantic Records signed the band with a $143,000 advance.",
   "Wikipedia says it was the biggest deal of its kind for a new band at the time.",
   "The band kept control over release timing, touring, and what went on each album.")}
        <ul>
          <li>Autonomy over when albums came out.</li>
          <li>Autonomy over tour schedules.</li>
          <li>Autonomy over album contents.</li>
        </ul>
{p('That freedom is why <a href="/blog/genres/70s-hard-rock/">70s hard rock</a> radio played whole album sides of Led Zeppelin instead of one single at a time.')}

        <h2 id="hot-100">Led Zeppelin Songs on the Hot 100</h2>
{p(f"Wikipedia lists {NUM[len(peaks)]} Led Zeppelin songs from this list on the US Hot 100.",
   f"{best[0]} climbed highest, to number {NUM[best[3]]}.",
   "It is the band's only US top-10 single, and the RIAA certified it gold.")}

{tbl("Led Zeppelin songs on the US Billboard Hot 100, by peak position (Wikipedia)", ["Song", "Album", "Album year", "Hot 100 peak"], single_rows)}

        <h3>Whole Lotta Love and the Willie Dixon Credit</h3>
{p("Whole Lotta Love was released in the US on November 7, 1969, and spent 15 weeks on the Hot 100.",
   "It opens Led Zeppelin II, and Jimmy Page played theremin on it.",
   "Muddy Waters recorded Willie Dixon's You Need Love in 1962, and the Led Zeppelin song was first credited without him.",
   "A 1985 lawsuit was settled out of court, and Dixon's name now appears in the credits.")}

        <h3>Immigrant Song and the Reykjavik Show</h3>
{p("Immigrant Song opens Led Zeppelin III and runs just 2:26.",
   "It was written during the summer 1970 tour that opened in Reykjavik, and that Iceland stop inspired Robert Plant's lyrics.",
   "The band first played it live six days later at the Bath Festival.",
   "Atlantic issued it as a US single on November 5, 1970, and it reached number 16 on the Hot 100.",
   "The B-side, Hey, Hey, What Can I Do, never appeared on an album.")}
{pic("led-zeppelin-acoustic-1973", "Robert Plant seated and clapping beside Jimmy Page with an acoustic guitar during an acoustic set in Hamburg, Germany, in 1973", "(max-width: 700px) 100vw, 800px", 800, 537, widths=(400, 600, 800))}
        <p class="post-img-caption">Robert Plant and Jimmy Page playing an acoustic set in Hamburg, Germany, 1973.</p>
        <p class="post-img-caption">Image credit: Photo by Heinrich Klaffs, CC BY-SA 2.0, via Wikimedia Commons.</p>

        <h2 id="stairway">Stairway to Heaven: The Song They Never Released</h2>
{p("Stairway to Heaven is the best-known of all Led Zeppelin songs, and it was never a US single.",
   "Wikipedia says Atlantic wanted one, but manager Peter Grant refused the requests in 1972 and 1973.",
   "In 1975, Page told Rolling Stone, &quot;We were careful to never release it as a single.&quot;")}

        <h3>A Song in Three Parts</h3>
{p("The song runs 8:02 and builds in three sections, each faster and louder than the last.",
   "It opens with acoustic guitar and recorders, then brings in electric instruments.",
   "The final section is an uptempo hard rock arrangement, and Page's guitar solo sits just before it.",
   "It was recorded between December 1970 and February 1971.")}

        <h3>Radio Made It Anyway</h3>
{p("Wikipedia calls it the most requested song on US FM radio of its time.",
   "US radio sources estimated 2,874,000 plays by its 20th anniversary.",
   "By 2000, the estimate was over three million broadcasts.")}
        <ul>
          <li>Rolling Stone ranked it number 31 in 2004 and number 61 in 2021.</li>
          <li>VH1 ranked it number three on its 2000 list of the 100 greatest rock songs.</li>
          <li>The Library of Congress added it to the National Recording Registry in 2023.</li>
        </ul>

        <h3>The Taurus Lawsuit</h3>
{p("In May 2014, the Spirit bassist Mark Andes and a trust for Randy California sued over a similarity to the song Taurus.",
   "A jury found no infringement on June 23, 2016, and an appeals court ordered a new trial in 2018.",
   "On March 9, 2020, the full Ninth Circuit ruled for Led Zeppelin.",
   "The Supreme Court declined to hear the case on October 5, 2020, which ended it.")}

        <h2 id="iv">Led Zeppelin IV: No Title, Four Symbols</h2>
{p("Led Zeppelin IV came out on November 8, 1971, and Page produced it.",
   "After the lukewarm reception of Led Zeppelin III, Page decided the next album would carry no title.",
   "Each member picked a hand-drawn symbol for the inner sleeve and the record label instead.")}

        <h3>The Fight With Atlantic</h3>
{p("Atlantic Records strongly opposed the idea.",
   "The band refused to hand over the master tapes until the label agreed.",
   "A press agent warned that a release with no written information would be professional suicide.",
   "The front and back covers carry no text at all.")}

        <h3>Headley Grange and the Stairwell Drums</h3>
{p("Sessions began at Island Studios in London on December 5, 1970, with Black Dog.",
   "The band then moved to Headley Grange, a country house in Hampshire, with the Rolling Stones Mobile Studio.",
   "John Bonham's drums on When the Levee Breaks were recorded in the lobby, with two microphones hung above a flight of stairs.",
   "Black Dog was named after a dog that hung around the house, and Wikipedia says the riff was written by Page and John Paul Jones.",
   "Going to California, a quiet acoustic song by Page and Plant, was inspired by Joni Mitchell.")}
{p("The album peaked at number two on the Billboard 200, behind Carole King's Music and Sly and the Family Stone.",
   "It later sold over 37 million copies worldwide, and the RIAA lists it at 24× Platinum.")}

        <h2 id="graffiti">Physical Graffiti and Kashmir</h2>
{p("Physical Graffiti arrived on February 24, 1975, as a double album on the band's own Swan Song label.",
   "It debuted at number three on the Billboard Pop Albums chart and reached number one the next week.",
   "It stayed there for six weeks, and all of the band's earlier albums re-entered the top 200 at the same time.")}

        <h3>The Sleeve With Windows</h3>
{p("The cover shows a New York tenement block, photographed at 96 and 98 St. Mark's Place.",
   "Windows were die-cut so the inner sleeves showed through.",
   "That design was hard to manufacture and delayed the release.")}

        <h3>Kashmir: Built Over Three Years</h3>
{p("Kashmir runs 8:37, and Page, Plant, and Bonham share the writing credit.",
   "Plant wrote the lyrics in 1973, right after the band's US tour.",
   "None of them had visited Kashmir, and Plant was inspired by a drive through a desolate desert in southern Morocco.",
   "In early 1974, John Paul Jones added orchestration, with session players on strings and horns, plus a Mellotron part.",
   "Page used a Danelectro guitar in DADGAD tuning.")}

        <h2 id="holy">Houses of the Holy: A Reggae Joke and a Cover</h2>
{p("Houses of the Holy was released on March 28, 1973, after cover delays pushed it back from January.",
   "It topped the Billboard 200 for two weeks and spent 39 weeks on the chart.",
   "The RIAA lists it at 11× Platinum, and awarded Diamond status in 1999.")}

        <h3>The Title Song Left Off</h3>
{p("The song Houses of the Holy was recorded for the album and left off, because the tracks already filled two sides of an LP.",
   "It finally appeared on Physical Graffiti in 1975.")}

        <h3>D'yer Mak'er: Say It Fast</h3>
{p("D'yer Mak'er combines reggae with 1950s doo-wop, with a short off-beat that was Bonham's idea.",
   "The title comes from an old British joke: said quickly, &quot;D'yer Mak'er&quot; sounds like Jamaica.",
   "The reply is &quot;No, she went of her own accord.&quot;",
   "The song reached number 20 on the Hot 100.")}

        <h3>Dancing Days and the Cover Shoot</h3>
{p("Dancing Days grew out of the enjoyable Stargroves sessions, and its lyrics lean optimistic.",
   "The Hipgnosis cover used photographs from the Giant's Causeway in Northern Ireland.",
   "Two child models were printed several times over to make 11 figures.",
   "The shoot lasted 10 days and was hampered by rain and clouds.")}

        <h2 id="four-players">Four Players, One Sound</h2>
{p("The band formed in London in 1968 with four members.",
   "Each one shows up in the songs above in a specific, audible way.")}

{tbl("The four members of Led Zeppelin and where each is audible on this page", ["Member", "Role", "Heard on"],
     [["Robert Plant", "Vocals", "Immigrant Song lyrics, Kashmir lyrics"],
      ["Jimmy Page", "Guitar, producer", "Stairway to Heaven solo, Whole Lotta Love theremin"],
      ["John Paul Jones", "Bass, keyboards", "Kashmir orchestration and Mellotron"],
      ["John Bonham", "Drums", "When the Levee Breaks, Kashmir"]])}
{pic("jimmy-page-1977", "Jimmy Page on one knee with a Gibson Les Paul guitar, one arm raised toward the ceiling, performing live in 1977", "(max-width: 700px) 100vw, 420px", 700, 1089, widths=(400, 600, 700))}
        <p class="post-img-caption">Jimmy Page performing live with Led Zeppelin, 1977.</p>
        <p class="post-img-caption">Image credit: APA-Agency for the Performing Arts, public domain, via Wikimedia Commons.</p>

        <h2 id="end">1979 to 1980: Knebworth and the End</h2>
{p("In 1979, the band headlined two concerts at Knebworth.",
   "Wikipedia says the first night drew about 104,000 people.",
   "In Through the Out Door came out on August 22, 1979, and reached number one.",
   "Fool in the Rain, from that album, climbed to number 21 on the Hot 100.")}

        <h3>September 25, 1980</h3>
{p("John Bonham died on September 25, 1980.",
   "The cause was asphyxiation from vomit, and it was ruled accidental.",
   "On December 4, 1980, the band announced its breakup in a statement.",
   "It was inducted into the Rock and Roll Hall of Fame in 1995.")}
{p('For a random 70s act to explore next, try the <a href="/pages/random-artist-picker">Random Artist Picker</a>.',
   'To test what you know about the decade, take the <a href="/pages/70s-trivia-quiz">70s Music Trivia Quiz</a>.')}

        <h2 id="sources">Sources</h2>
{p("Every chart peak, album date, and story on this page comes from the outside articles below, because Led Zeppelin does not appear in this site's own Billboard data files.",
   'The way this site handles data is described on the <a href="/about/methodology/">methodology page</a>.',
   'Every list on <a href="/">Music of the 70s</a> plays inside the page.')}
        <ul>
          <li><a href="https://en.wikipedia.org/wiki/Led_Zeppelin" rel="noopener">Wikipedia: Led Zeppelin</a> for the band's history, the Atlantic deal, Knebworth, and the breakup.</li>
          <li><a href="https://en.wikipedia.org/wiki/Led_Zeppelin_discography" rel="noopener">Wikipedia: Led Zeppelin discography</a> for album chart peaks, certifications, and the singles table.</li>
          <li><a href="https://en.wikipedia.org/wiki/Stairway_to_Heaven" rel="noopener">Wikipedia: Stairway to Heaven</a> for the single refusal, radio plays, and the lawsuit.</li>
          <li><a href="https://en.wikipedia.org/wiki/Led_Zeppelin_IV" rel="noopener">Wikipedia: Led Zeppelin IV</a> for the untitled cover and the Headley Grange sessions.</li>
          <li><a href="https://en.wikipedia.org/wiki/Physical_Graffiti" rel="noopener">Wikipedia: Physical Graffiti</a> for the die-cut sleeve and chart run.</li>
          <li><a href="https://en.wikipedia.org/wiki/Kashmir_(song)" rel="noopener">Wikipedia: Kashmir</a> for the writing and recording details.</li>
          <li><a href="https://en.wikipedia.org/wiki/Houses_of_the_Holy" rel="noopener">Wikipedia: Houses of the Holy</a> for D'yer Mak'er and the cover.</li>
          <li><a href="https://en.wikipedia.org/wiki/Immigrant_Song" rel="noopener">Wikipedia: Immigrant Song</a> for the Reykjavik origin and chart peaks.</li>
          <li><a href="https://en.wikipedia.org/wiki/Whole_Lotta_Love" rel="noopener">Wikipedia: Whole Lotta Love</a> for the single release, chart run, and Dixon credit.</li>
        </ul>

        <section class="faq-block" id="faq">
          <h2>Frequently Asked Questions</h2>
{faq_html}
        </section>'''

    related = [
        ("gfr-1971", "Genres", "70s Hard Rock: The Genre That Actually Hit #1", "/blog/genres/70s-hard-rock/",
         "28 hard rock songs to play, and the one that reached number one.", "Grand Funk Railroad on stage in 1971"),
        ("elton-john-1972", "Artists", "Elton John: 13 Hits Played, 6 at Number One", "/blog/artists/elton-john/",
         "Every Elton John hit of the decade, playable, with the Lennon and Kiki Dee stories.", "Elton John at the piano in 1972"),
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
      {{"@type": "ListItem", "position": 4, "name": "Led Zeppelin Songs", "item": "{URL}"}}
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
        Led Zeppelin Songs
      </nav>

      <article class="section seo-content">
        <h1>{TITLE}</h1>

        <p class="post-byline">By <a href="https://musicofthe70s.net/about/author/">Charlie</a> &middot; Published {PUBLISHED.strftime('%B')} {PUBLISHED.day}, {PUBLISHED.year}</p>
        <p class="jump-to-list"><a class="btn-primary jump-btn" href="#zeppelin-song-list">&#9654; Jump to the playable list</a></p>

        <p class="post-intro">Led Zeppelin songs ruled 1970s rock radio, yet {NUM[len(peaks)]} of the {n} on this page ever charted on the Hot 100.</p>
        <p class="post-intro">The band refused to chase singles, and {NUM[n_ones]} of its {NUM[n_alb]} studio albums of the decade went to number one instead.</p>
        <p class="post-intro">The biggest hit was Whole Lotta Love, at number four, and Stairway to Heaven was never a US single at all.</p>
        <p class="post-intro">This page plays all {n} songs, then follows the stories behind the albums.</p>

{pic(IMG, "Led Zeppelin in a 1971 black and white promotional photo, with bassist John Paul Jones, guitarist Jimmy Page, drummer John Bonham and singer Robert Plant posed against a plain wall", "(max-width: 700px) 100vw, 1100px", 1200, 830, lazy=False)}
        <p class="post-img-caption">Led Zeppelin in a 1971 Atlantic Records promotional photograph.</p>
        <p class="post-img-caption">Image credit: Atlantic Records, public domain, via Wikimedia Commons.</p>

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
    out = ROOT / "blog/artists" / SLUG / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    write(out, page)
    print(f"wrote {out}: {n} rows, {len(peaks)} Hot 100 peaks, {n_ones} number one albums")


if __name__ == "__main__":
    main()
