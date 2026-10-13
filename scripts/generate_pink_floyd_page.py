#!/usr/bin/env python3
"""Build the Pink Floyd Songs Artists post (blog/artists/pink-floyd-songs/index.html).

Data: data/radio/radio-songs.json (Money, the only Pink Floyd row on a 1970s Year-End Hot 100, rank 92 for 1973),
data/billboard/hot100_weekly.json (checked: no Pink Floyd weekly #1 in 1970-1979). Pink Floyd's US singles
career is two Hot 100 hits (Money, Another Brick in the Wall Part 2), so the other ten rows are album tracks chosen
as the band's best-known 1970s songs. Every Hot 100 peak, release date, writer and story fact comes from the linked
Wikipedia articles, checked 2026-10-12, and is credited to Wikipedia on the page. Another Brick in the Wall (Part 2)
was released November 1979 and reached number one in March 1980, so its weeks at number one come from Wikipedia's
1980 number-ones list, not from the site's 1970-1979 weekly file. Year-End Rank is the year-end rank, never a peak.
The site JSON's fun_fact text for Money is not used.

Run: python3 scripts/generate_pink_floyd_page.py
"""
import html
import json
from datetime import date

from genre_page_common import ROOT, read, play_button, write
from generate_country_page import p, tbl, pic

SLUG = "pink-floyd-songs"
PAGE = f"blog/artists/{SLUG}/"
URL = f"https://musicofthe70s.net/{PAGE}"
IMG = "pink-floyd-1973"
IMG2 = "pink-floyd-1971"
PUBLISHED = date(2026, 10, 12)
NUM = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
       10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen"}

# (title, album year, album, Hot 100 peak or None, YouTube id). Money's id is read from radio-songs.json.
SONGS = [
    ("One of These Days", 1971, "Meddle", None, "raV_A8YcBu0"),
    ("Echoes", 1971, "Meddle", None, "OcDiOUQBFd4"),
    ("Breathe (In the Air)", 1973, "The Dark Side of the Moon", None, "jcz0YxYl6Ac"),
    ("Time", 1973, "The Dark Side of the Moon", None, "Qr0-7Ds79zo"),
    ("Money", 1973, "The Dark Side of the Moon", 13, None),
    ("Us and Them", 1973, "The Dark Side of the Moon", None, "HoLhKJuGhK0"),
    ("Shine On You Crazy Diamond", 1975, "Wish You Were Here", None, "Tu7oq3VNgpY"),
    ("Welcome to the Machine", 1975, "Wish You Were Here", None, "Jh20cMEgvqc"),
    ("Have a Cigar", 1975, "Wish You Were Here", None, "Eq8ZiZ9xiLw"),
    ("Wish You Were Here", 1975, "Wish You Were Here", None, "-0MQXbcw-co"),
    ("Another Brick in the Wall, Part 2", 1979, "The Wall", 1, "A6iqfDrQ0_o"),
    ("Comfortably Numb", 1979, "The Wall", None, "7f3EGjRxxNI"),
]

WRITER = {
    "One of These Days": "Gilmour, Mason, Waters, Wright",
    "Echoes": "Gilmour, Wright (music), Waters (lyrics)",
    "Breathe (In the Air)": "Gilmour, Wright (music), Waters (lyrics)",
    "Time": "Mason, Waters, Wright, Gilmour (music), Waters (lyrics)",
    "Money": "Roger Waters",
    "Us and Them": "Richard Wright (music), Roger Waters (lyrics)",
    "Shine On You Crazy Diamond": "Gilmour, Wright, Waters (lyrics by Waters)",
    "Welcome to the Machine": "Roger Waters",
    "Have a Cigar": "Roger Waters",
    "Wish You Were Here": "David Gilmour and Roger Waters",
    "Another Brick in the Wall, Part 2": "Roger Waters",
    "Comfortably Numb": "David Gilmour (music), Roger Waters (lyrics)",
}
LEAD = {
    "One of These Days": "Instrumental, one spoken line by Nick Mason",
    "Echoes": "David Gilmour and Richard Wright",
    "Breathe (In the Air)": "David Gilmour",
    "Time": "David Gilmour and Richard Wright",
    "Money": "David Gilmour",
    "Us and Them": "David Gilmour, with Wright on harmony",
    "Shine On You Crazy Diamond": "Roger Waters (credited on parts 6 to 9)",
    "Welcome to the Machine": "David Gilmour",
    "Have a Cigar": "Roy Harper",
    "Wish You Were Here": "David Gilmour",
    "Another Brick in the Wall, Part 2": "Roger Waters and David Gilmour in unison, with a school choir",
    "Comfortably Numb": "Roger Waters (verses), David Gilmour (chorus)",
}


def main():
    radio = json.loads(read(ROOT / "data/radio/radio-songs.json"))
    weekly = json.loads(read(ROOT / "data/billboard/hot100_weekly.json"))

    money = [s for s in radio if s["artist"] == "Pink Floyd" and s.get("youtube_id")]
    assert len(money) == 1 and money[0]["title"] == "Money" and money[0]["rank"] == 92 and money[0]["year"] == 1973, money
    ye_rank = {"Money": money[0]["rank"]}
    songs = [(t, y, a, pk, yt or money[0]["youtube_id"]) for t, y, a, pk, yt in SONGS]
    n = len(songs)
    assert set(WRITER) == set(LEAD) == {s[0] for s in songs}

    # No Pink Floyd row may appear in the 1970-1979 weekly number-one file (Another Brick hit number one in 1980).
    assert not [w for yr in weekly for w in weekly[yr] if "Pink Floyd" in w["artist"]]

    rows = []
    for t, y, alb, pk, yt in songs:
        rows.append(f'              <tr><td class="ohw-listen">{play_button(yt, t, "Pink Floyd")}</td>'
                    f'<td class="ohw-song">{html.escape(t)}</td>'
                    f'<td>{y}</td><td>{html.escape(alb)}</td><td>{ye_rank.get(t, "")}</td><td>{pk if pk else ""}</td>'
                    f'<td>{"Yes" if t.startswith("Another Brick") else ""}</td></tr>')

    chart_rows = [
        ["Money", "May 7, 1973 (US single)", "Billboard Hot 100", "13", "Ranks #92 on the 1973 Year-End Hot 100"],
        ["Us and Them", "February 4, 1974 (US single)", "Cash Box Top 100", "72", "March 1974; on Billboard it only reached 101 on Bubbling Under; Time was the B-side"],
        ["Have a Cigar", "November 1975 (US single)", "Cash Box Looking Ahead", "119", "Also Record World singles 101-150 at 126"],
        ["Another Brick in the Wall, Part 2", "November 23, 1979 (single)", "Billboard Hot 100", "1",
         "Four weeks at number one from the issue dated March 22, 1980"],
    ]

    writer_rows = [[html.escape(t), WRITER[t], LEAD[t], y, html.escape(alb)] for t, y, alb, pk, yt in songs]

    faq = [
        ("What is Pink Floyd's biggest song on the Billboard Hot 100?",
         ["Another Brick in the Wall, Part 2 is Pink Floyd's biggest Hot 100 song, because it reached number one.",
          "It held the top spot for four weeks, starting with the issue dated March 22, 1980.",
          "Billboard's 1980 year-end list ranks it second, according to Wikipedia.",
          "Money, at number 13 in 1973, is the band's other Hot 100 hit."]),
        ("Did Pink Floyd have any Hot 100 hits in the 1970s?",
         ["Pink Floyd had one Hot 100 hit that peaked inside the 1970s calendar: Money, which reached number 13 in 1973.",
          "Another Brick in the Wall, Part 2 was released on November 23, 1979, but it reached number one in March 1980.",
          "Most of the band's best-known 70s music came from albums, not singles."]),
        ("Who sings lead on Money by Pink Floyd?",
         ["David Gilmour sings lead and plays guitar on Money, which Roger Waters wrote.",
          "Dick Parry added the tenor saxophone solo on October 27, and the song is in 7/4 time.",
          "The US single came out on May 7, 1973, in a shortened edit, and it reached number 13 on the Hot 100, according to Wikipedia."]),
        ("Who sang Have a Cigar on Wish You Were Here?",
         ["Roy Harper sang the lead vocal on Have a Cigar, not a member of Pink Floyd.",
          "Roger Waters and David Gilmour were unhappy with their own attempts, and Harper was recording his album HQ at Abbey Road at the same time.",
          "Waters wrote the song as a critique of greed and cynicism in the music business, according to Wikipedia."]),
        ("What are the clocks at the start of Time by Pink Floyd?",
         ["The clocks that open Time were recorded by engineer Alan Parsons in an antique shop.",
          "He recorded each clock separately as a quadrophonic test, not specifically for the album.",
          "Time is on The Dark Side of the Moon, and David Gilmour and Richard Wright share the lead vocals, according to Wikipedia."]),
    ]
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": " ".join(a)}} for q, a in faq]},
        indent=2, ensure_ascii=False)
    faq_ld = "\n".join("  " + l for l in faq_ld.split("\n"))
    faq_html = "\n".join(
        f'          <div class="faq-item">\n            <h3>{html.escape(q)}</h3>\n' + "\n".join(f"            <p>{html.escape(l)}</p>" for l in a) + "\n          </div>"
        for q, a in faq).replace("&#x27;", "'")

    TITLE = f"Pink Floyd Songs: {n} Tracks Played, 1 at Number One"
    desc = (f"Pink Floyd songs of the 70s, all {n} playable: Money, Time, Wish You Were Here and the number one Another Brick in the Wall. "
            "Read the stories behind each.")
    assert len(TITLE) <= 60, len(TITLE)
    assert len(desc) <= 155, len(desc)

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
    "image": "https://musicofthe70s.net/images/blog/{IMG}-669w.jpg",
    "mainEntityOfPage": "{URL}"
  }}'''

    toc = [("pink-floyd-songs-list", f"Pink Floyd Songs: Play All {n} Tracks"),
           ("by-the-numbers", "Pink Floyd Songs on the Charts: Two Hits and Four Albums"),
           ("meddle", "Meddle: One of These Days and Echoes"),
           ("dark-side", "The Dark Side of the Moon: Breathe, Time, Money and Us and Them"),
           ("wish-you-were-here", "Wish You Were Here: Four Songs and a Missing Friend"),
           ("the-wall", "The Wall: Another Brick in the Wall, Part 2 and Comfortably Numb"),
           ("who-wrote-what", "Who Wrote and Sang Each Song"),
           ("sources", "Sources"), ("faq", "Frequently Asked Questions")]
    toc_html = "\n".join(f'            <li><a href="#{i}">{t}</a></li>' for i, t in toc)

    feat_pic = pic(IMG, "Pink Floyd performing The Dark Side of the Moon at Earls Court in May 1973, the era of the Pink Floyd songs Money and Time",
                   "(max-width: 700px) 100vw, 669px", 669, 416, widths=(400, 669), lazy=False).replace(
        'class="post-featured-img"', 'class="post-featured-img" style="aspect-ratio:669/416;max-width:669px;height:auto;margin:1.5rem auto"', 1)
    ad_pic = pic(IMG2, "Roger Waters, Nick Mason, David Gilmour and Richard Wright in the 1971 Meddle trade advertisement, from the year of Echoes",
                 "(max-width: 700px) 100vw, 682px", 682, 247, widths=(400, 682)).replace(
        "<img\n", '<img style="display:block;width:100%;max-width:682px;height:auto;margin:1.5rem auto;border-radius:8px"\n', 1)

    body = f'''        <h2 id="pink-floyd-songs-list">Pink Floyd Songs: Play All {n} Tracks</h2>
{p(f"Here are {NUM[n]} Pink Floyd songs from 1971 to 1979.",
   "Only two were big Hot 100 singles, so the rest are the album tracks the band is known for.",
   "Press Play on any row to watch it here, and tap a heading to sort.")}

        <div class="data-table-wrap scroll-list">
          <table class="data-table sortable-table" id="pinkFloydSongsTable" data-inline-player>
            <caption>{n} Pink Floyd songs of the 70s, with album, Billboard Year-End Hot 100 rank, Hot 100 peak and number one status</caption>
            <thead>
              <tr>
                <th><span class="visually-hidden">Play</span></th>
                <th><button type="button" data-col="1" data-type="text">Song</button></th>
                <th aria-sort="ascending"><button type="button" data-col="2" data-type="num">Year</button></th>
                <th><button type="button" data-col="3" data-type="text">Album</button></th>
                <th><button type="button" data-col="4" data-type="num">Year-End Rank</button></th>
                <th><button type="button" data-col="5" data-type="num">Hot 100 Peak</button></th>
                <th><button type="button" data-col="6" data-type="text">#1 Hit</button></th>
              </tr>
            </thead>
            <tbody>
{chr(10).join(rows)}
            </tbody>
          </table>
        </div>
{p("Year is the year of the album the song came from.",
   "Year-End Rank is the song's spot on that year's Billboard Year-End Hot 100, and only Money has one in this site's data.",
   "Hot 100 Peak and the number one flag come from each song's Wikipedia article.",
   "A blank means the song was not a Hot 100 hit.")}

        <h2 id="by-the-numbers">Pink Floyd Songs on the Charts: Two Hits and Four Albums</h2>
{p("Pink Floyd songs rarely lived on the singles chart in the 1970s.",
   "The band built its decade on four albums, and two singles carried it onto the Hot 100.",
   "The table lists every US single from this page that charted anywhere, and which chart it was.")}

{tbl("Pink Floyd's charting US singles of the 70s: release, chart and peak (Wikipedia and this site's Year-End data)", ["Song", "Released", "Chart", "Peak", "Note"], chart_rows)}

        <h3>What the Chart Numbers Say</h3>
{p("The two Hot 100 hits among these Pink Floyd songs sit about six years apart.")}
        <ul>
          <li>Money reached number 13 in 1973 and ranks #{ye_rank["Money"]} on that year's Year-End Hot 100, the only Pink Floyd song on any 1970s year-end list in this site's data.</li>
          <li>Us and Them and Have a Cigar charted only on Cash Box and Record World lists, and Us and Them reached just 101 on Billboard's Bubbling Under chart.</li>
          <li>Another Brick in the Wall, Part 2 reached number one in the issue dated March 22, 1980, so it is a 1980 number one with a 1979 release.</li>
          <li>It is the band's only number one, and Wikipedia says Billboard ranked it second for 1980.</li>
        </ul>
{p('For another act whose catalogue lived on albums, read the page on <a href="/blog/artists/led-zeppelin-songs/">Led Zeppelin songs</a>.')}

        <h2 id="meddle">Meddle: One of These Days and Echoes</h2>
{p("Meddle came out on October 30, 1971, and it holds two of the best-loved Pink Floyd songs of the decade.",
   'It sits at the heart of the turn toward long-form music, which this site covers in its guide to <a href="/blog/genres/70s-progressive-rock/">70s progressive rock</a>.')}

        <h3>One of These Days</h3>
{p("The four members of the band share the writing credit for One of These Days, which opens Meddle.",
   "It was recorded between March 15 and July 22, 1971, at AIR, Abbey Road and Morgan Studios in London.",
   "The central riff began as a guitar part by David Gilmour, and Roger Waters suggested it for bass instead.",
   "The band recorded two bass parts, double-tracked and panned hard to separate stereo channels.",
   "One of them sounds muted, which Gilmour blamed on old strings.")}
        <h3>A Spoken Line and a Ring Modulator</h3>
{p("The only vocal is a spoken phrase by Nick Mason, run through a ring modulator and slowed down.",
   "Mason said it was aimed at the DJ Jimmy Young.",
   "A US single came out on November 29, 1971, with Fearless on the B-side, but Wikipedia lists no US chart position for it.")}
{ad_pic}
        <p class="post-img-caption">Roger Waters, Nick Mason, David Gilmour and Richard Wright in a 1971 trade advertisement for Meddle.</p>
        <p class="post-img-caption">Image credit: Capitol Records, public domain, via Wikimedia Commons (Billboard, October 30, 1971).</p>

        <h3>Echoes</h3>
{p("Echoes fills all of side two of Meddle, and the album version runs 23 minutes and 29 seconds.",
   "Richard Wright and David Gilmour wrote most of the music, and Waters wrote the lyrics.",
   "The famous opening ping came from an experiment early in the sessions.",
   "Wright's grand piano was amplified and sent through a Leslie speaker and a Binson Echorec.")}
        <h3>The Working Titles and the Pompeii Film</h3>
{p("The piece began life under the working title Nothing, Parts 1 to 24.",
   "Later tapes were labelled The Son of Nothing, and it was not called Echoes until a tour of Japan that began on August 6, 1971.",
   "The sessions ran from March 7 to May 1, 1971.",
   "The band later filmed it at the Amphitheatre of Pompeii, and the song was split in two to open and close that film.",
   "Wikipedia does not say that Echoes was a US single.")}

        <h2 id="dark-side">The Dark Side of the Moon: Breathe, Time, Money and Us and Them</h2>
{p("Four Pink Floyd songs on this page come from The Dark Side of the Moon, released in 1973.",
   "The band recorded it between June 1972 and January 1973 at EMI Studios, the Abbey Road building in London.")}

        <h3>Breathe (In the Air)</h3>
{p("David Gilmour and Richard Wright wrote the music for Breathe, and Roger Waters wrote the words.",
   "Gilmour sings it, and he plays a lap steel guitar with a volume pedal and several overdubs.",
   "A one-minute reprise closes Time, without the slide guitar.",
   "Breathe came out as a single in France in 1974, as the B-side to Time, and not internationally.")}

        <h3>Time</h3>
{p("Waters wrote the lyrics for Time, and all four members share the music credit.",
   "Gilmour sings the verses, and Wright sings the bridges.",
   "Doris Troy, Lesley Duncan, Liza Strike and Barry St. John sing backing vocals.",
   "The clocks that open the song were recorded by engineer Alan Parsons in an antique shop, as a quadrophonic test and not for the album.",
   "Each clock was captured separately.")}
{p("Time was the B-side of Us and Them on the US Harvest single released on February 4, 1974.",
   "It was recorded between June 3, 1972 and February 1, 1973.")}

        <h3>Money</h3>
{p("Roger Waters wrote Money, and David Gilmour sings it and plays the guitar.",
   "The song is in 7/4 time, although Gilmour and Waters first said 7/8, and Richard Wright confirmed 7/4 in a 2000 interview.",
   "Dick Parry added the tenor saxophone solo on October 27.",
   "The cash register sound is a tape loop that Waters spliced from coins, tearing paper and a counting machine.",
   "The loop was a seven-beat pattern, and some of the sounds came from sound libraries.")}
{p("The US single, in a shortened edit, came out on May 7, 1973, with Any Colour You Like as the B-side.",
   "It reached number 13 on the Hot 100.",
   f"It ranks #{ye_rank['Money']} on the 1973 Year-End Hot 100, the band's only year-end entry of the decade in this site's data.",
   'To meet more acts like this, spin the <a href="/pages/random-artist-picker">Random Artist Picker</a>.')}

        <h3>Us and Them</h3>
{p("Richard Wright first wrote the tune in 1969 for the film Zabriskie Point, under the title The Violent Sequence.",
   "Director Michelangelo Antonioni rejected it, and the piece was shelved.",
   "It returned on Dark Side as Us and Them, with lyrics by Waters.",
   "Gilmour sings it, with harmony vocals by Wright, and Dick Parry plays tenor saxophone.")}
{p("It was the album's second US single, released on February 4, 1974, with Time on the B-side.",
   "It reached number 72 on the Cash Box Top 100 in March 1974.",
   "It did not enter the Billboard Hot 100, and it peaked at number 101 on the Bubbling Under chart.")}

        <h2 id="wish-you-were-here">Wish You Were Here: Four Songs and a Missing Friend</h2>
{p("Wish You Were Here came out on September 12, 1975, and four Pink Floyd songs on this page come from it.",
   "The sessions ran at Abbey Road from January to July 1975.")}

        <h3>Shine On You Crazy Diamond</h3>
{p("David Gilmour, Richard Wright and Roger Waters share the music credit, and Waters wrote the lyrics.",
   "The full piece runs 25 minutes and 57 seconds.",
   "It was planned as a side-long track, and the band split it into two parts that bookend the album, with new songs placed between them.")}
{p("On June 5, 1975, Syd Barrett wandered into the studio while the band were recording.",
   "The band did not recognise him at first, and Waters was reduced to tears at his appearance.",
   "This page plays the first half of one of the longest Pink Floyd songs of the decade, parts one to five.")}

        <h3>Welcome to the Machine and Have a Cigar</h3>
{p("Roger Waters wrote Welcome to the Machine, and it is built on a throbbing EMS VCS 3 synthesiser sound.",
   "Gilmour plays six and 12-string acoustic guitars and sings it.",
   "He had trouble with one line, so he sang it at a lower pitch and the tape speed was raised back to normal.")}
{p("Waters wrote Have a Cigar as a critique of greed and cynicism in the music business.",
   "Neither he nor Gilmour was happy with their own lead vocal.",
   "So the band asked Roy Harper, who was recording HQ at Abbey Road at the same time, to sing it.",
   "Harper agreed partly to repay a favour to Gilmour.")}
{p("The US single came out in November 1975, with Welcome to the Machine on the B-side.",
   "It reached number 119 on the Cash Box Looking Ahead chart and number 126 on the Record World singles chart.",
   "Waters has called it a follow-up to Money, with the lyrics a record executive's demands after Dark Side became a huge success.")}

        <h3>Wish You Were Here</h3>
{p("Gilmour and Waters wrote the title track, and Gilmour sings it.",
   "The opening was played on a twelve-string guitar, processed to sound like an AM radio, and then overdubbed with a fuller acoustic part.",
   "The sound of a radio dial moving through stations was recorded from Gilmour's car radio.")}
{p("The jazz violinist Stéphane Grappelli was recording downstairs, and Gilmour invited him to add a country fiddle at the end.",
   "He was paid £300.",
   "In the mix his part was almost removed, and it can barely be heard around 5:21.",
   "Waters said that crediting him for such a small part would be insulting.")}

        <h2 id="the-wall">The Wall: Another Brick in the Wall, Part 2 and Comfortably Numb</h2>
{p("The Wall came out on November 30, 1979, and it gave the band its only number one.",
   "Two Pink Floyd songs from it are on this page.")}

        <h3>Another Brick in the Wall, Part 2</h3>
{p("Roger Waters wrote Another Brick in the Wall, Part 2, and it was released as a single on November 23, 1979.",
   "It was the Christmas number one of 1979 in the UK, and the last UK number one of the decade.",
   "In the US it reached number one in the issue dated March 22, 1980, and held it for four weeks.",
   "Blondie's Call Me replaced it on April 19.",
   "Wikipedia says it ranks second on Billboard's 1980 year-end list.")}

        <h3>The Children's Choir and the Disco Beat</h3>
        <ul>
          <li>Producer Bob Ezrin had engineer Nick Griffiths record children from Islington Green School, near the band's studio.</li>
          <li>The school gave the session 40 minutes, and a choir of 23 students rehearsed for about a week.</li>
          <li>The school received £1,000, and the children had no royalty arrangement at first.</li>
          <li>Ezrin pushed the band to add a disco beat, and Gilmour at first disliked the idea.</li>
          <li>The single and the album were banned in South Africa in 1980, after the song was adopted by a school boycott.</li>
        </ul>

        <h3>Comfortably Numb</h3>
{p("David Gilmour wrote the music for Comfortably Numb, and Roger Waters wrote the lyrics.",
   "Gilmour recorded a wordless demo in 1978 while working on his debut solo album.",
   "Waters wrote the words after he was injected with tranquilizers before a 1977 show in Philadelphia.",
   "Waters sings the verses, and Gilmour sings the chorus.")}
{p("Waters wanted an orchestral arrangement, and Gilmour preferred something stripped down.",
   "The band used the orchestral parts for the main section and Gilmour's mix for the final solo.",
   "A Guitar World reader poll rated that solo the fourth best of all time.",
   "It came out as a single on June 23, 1980, with Hey You on the B-side.",
   "Wikipedia gives no US Hot 100 position for it.",
   'Test what you know about the decade with the <a href="/pages/70s-trivia-quiz">70s Music Trivia Quiz</a>.')}

        <h2 id="who-wrote-what">Who Wrote and Sang Each Song</h2>
{p(f"Roger Waters wrote the lyrics for most of the {NUM[n]} Pink Floyd songs on this page.",
   "David Gilmour sings lead or shares it on most of them, and Roy Harper sings one.",
   "The table shows who wrote and sang each song, and which album it came from.")}

{tbl("Pink Floyd songs of the 70s: writers, lead vocal, year and album (Wikipedia)", ["Song", "Written by", "Lead vocal", "Year", "Album"], writer_rows)}

        <h3>Keep Exploring</h3>
{p("Pink Floyd songs of the 70s are the sound of a band that let its albums, not its singles, carry the decade.",
   "Only two reached the Hot 100, and one of them reached number one.")}

        <h2 id="sources">Sources</h2>
{p("Money's year-end rank comes from this site's own Billboard data, described on the <a href='/about/methodology/'>methodology page</a>.",
   'Every list on <a href="/">Music of the 70s</a> plays inside the page.',
   "Peaks, dates and stories behind the Pink Floyd songs above can be checked against these outside sources:")}
        <ul>
          <li><a href="https://en.wikipedia.org/wiki/Pink_Floyd_discography" rel="noopener">Wikipedia: Pink Floyd discography</a> for the singles, albums and chart peaks.</li>
          <li><a href="https://en.wikipedia.org/wiki/Money_(Pink_Floyd_song)" rel="noopener">Wikipedia: Money</a> and <a href="https://en.wikipedia.org/wiki/Time_(Pink_Floyd_song)" rel="noopener">Time</a> for the Dark Side singles.</li>
          <li><a href="https://en.wikipedia.org/wiki/Us_and_Them_(song)" rel="noopener">Wikipedia: Us and Them</a> for the Zabriskie Point origin and the Cash Box peak.</li>
          <li><a href="https://en.wikipedia.org/wiki/One_of_These_Days_(Pink_Floyd_song)" rel="noopener">Wikipedia: One of These Days</a> and <a href="https://en.wikipedia.org/wiki/Echoes_(Pink_Floyd_song)" rel="noopener">Echoes</a> for the Meddle songs.</li>
          <li><a href="https://en.wikipedia.org/wiki/Breathe_(Pink_Floyd_song)" rel="noopener">Wikipedia: Breathe</a> for the writers and the French single.</li>
          <li><a href="https://en.wikipedia.org/wiki/Shine_On_You_Crazy_Diamond" rel="noopener">Wikipedia: Shine On You Crazy Diamond</a>, <a href="https://en.wikipedia.org/wiki/Welcome_to_the_Machine" rel="noopener">Welcome to the Machine</a>, <a href="https://en.wikipedia.org/wiki/Have_a_Cigar" rel="noopener">Have a Cigar</a> and <a href="https://en.wikipedia.org/wiki/Wish_You_Were_Here_(Pink_Floyd_song)" rel="noopener">Wish You Were Here</a> for the 1975 album.</li>
          <li><a href="https://en.wikipedia.org/wiki/Another_Brick_in_the_Wall" rel="noopener">Wikipedia: Another Brick in the Wall</a> and <a href="https://en.wikipedia.org/wiki/Comfortably_Numb" rel="noopener">Comfortably Numb</a> for The Wall.</li>
          <li><a href="https://en.wikipedia.org/wiki/List_of_Billboard_Hot_100_number_ones_of_1980" rel="noopener">Wikipedia: Billboard Hot 100 number ones of 1980</a> for the weeks at number one.</li>
        </ul>

        <section class="faq-block" id="faq">
          <h2>Frequently Asked Questions</h2>
{faq_html}
        </section>'''

    related = [
        ("led-zeppelin-1971", "Artists", "Led Zeppelin Songs: Play 15 Essentials and Their Stories", "/blog/artists/led-zeppelin-songs/",
         "Stairway, Kashmir and every Led Zeppelin song playable.", "Led Zeppelin on stage in 1971"),
        ("genesis-1974", "Genres", "70s Progressive Rock: The Genre That Rarely Made the Top 100", "/blog/genres/70s-progressive-rock/",
         "Why concept albums, not singles, built prog's legacy.", "Genesis performing The Lamb Lies Down on Broadway in 1974"),
        ("70s-bands", "Artists", "70s Bands: The Groups That Ruled the Hot 100", "/blog/artists/70s-bands/",
         "Every band ranked by year-end Hot 100 hits, sortable and playable.", "Bar chart of the top ten 70s bands by year-end Hot 100 hits"),
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
  <meta property="og:image" content="https://musicofthe70s.net/images/blog/{IMG}-669w.jpg">
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
      {{"@type": "ListItem", "position": 4, "name": "Pink Floyd Songs", "item": "{URL}"}}
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
        Pink Floyd Songs
      </nav>

      <article class="section seo-content">
        <h1>{TITLE}</h1>

        <p class="post-byline">By <a href="https://musicofthe70s.net/about/author/">Charlie</a> &middot; Published {PUBLISHED.strftime('%B')} {PUBLISHED.day}, {PUBLISHED.year}</p>
        <p class="jump-to-list"><a class="btn-primary jump-btn" href="#pink-floyd-songs-list">&#9654; Jump to the playable list</a></p>

        <p class="post-intro">Pink Floyd songs of the 1970s were built for albums, and this page plays {NUM[n]} of the best known.</p>
        <p class="post-intro">Only two reached the Hot 100: Money at number 13 in 1973, and Another Brick in the Wall, Part 2 at number one in 1980.</p>
        <p class="post-intro">The rest come from four albums, Meddle, The Dark Side of the Moon, Wish You Were Here and The Wall.</p>
        <p class="post-intro">Press Play on every track below, then read the story behind each one.</p>

{feat_pic}
        <p class="post-img-caption">Pink Floyd performing The Dark Side of the Moon at Earls Court, London, in May 1973.</p>
        <p class="post-img-caption">Image credit: Photo by TimDuncan, CC BY 3.0, via Wikimedia Commons.</p>

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
    print(f"wrote {out}: {n} rows")


if __name__ == "__main__":
    main()
