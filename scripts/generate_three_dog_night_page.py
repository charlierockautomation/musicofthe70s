#!/usr/bin/env python3
"""Build the Three Dog Night Songs Artists post (blog/artists/three-dog-night-songs/index.html).

Data: data/radio/radio-songs.json (seven Three Dog Night rows of the 1970-1974 Year-End Hot 100, each with a YouTube ID),
data/billboard/hot100_weekly.json (Mama Told Me (Not to Come), Joy to the World and Black and White, the three Hot 100
number ones in the site's 1970-1979 weekly data), data/billboard/beyond_year_end.json (five further singles on the weekly
Hot 100 but on no 1970s year-end list: Celebrate, Out in the Country, An Old Fashioned Love Song, The Family of Man and
Let Me Serenade You, peaks and Topic-channel YouTube IDs checked).
Year-End Rank is the year-end rank, never a peak. Hot 100 peaks, release dates, writers and story facts come from the
linked Wikipedia articles, checked 2026-10-14, and are credited to Wikipedia on the page.
The site JSON's fun_fact and trivia text for Three Dog Night is not used.

Run: python3 scripts/generate_three_dog_night_page.py
"""
import html
import json
from datetime import date

from genre_page_common import ROOT, read, play_button, write
from generate_country_page import p, tbl, pic

SLUG = "three-dog-night-songs"
PAGE = f"blog/artists/{SLUG}/"
URL = f"https://musicofthe70s.net/{PAGE}"
IMG = "three-dog-night-1975"
IMG2 = "three-dog-night-1972"
CHART = "three-dog-night-peaks"
PUBLISHED = date(2026, 10, 14)
ARTIST = "Three Dog Night"
NUM = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
       10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen"}

# title -> (release year, Hot 100 peak, released text, album, written by)
# Every value read from the song's Wikipedia article, checked 2026-10-14.
INFO = {
    "Celebrate": (1970, 15, "January 1970", "Suitable for Framing", "Gary Bonner and Alan Gordon"),
    "Mama Told Me (Not to Come)": (1970, 1, "May 1970", "It Ain't Easy", "Randy Newman"),
    "Out in the Country": (1970, 15, "August 1970", "It Ain't Easy", "Paul Williams and Roger Nichols"),
    "Joy to the World": (1971, 1, "February 1971", "Naturally", "Hoyt Axton"),
    "Liar": (1971, 7, "July 1971", "Naturally", "Russ Ballard"),
    "An Old Fashioned Love Song": (1971, 4, "November 1971", "Harmony", "Paul Williams"),
    "Never Been to Spain": (1971, 5, "1971", "Harmony", "Hoyt Axton"),
    "The Family of Man": (1972, 12, "March 1972", "Harmony", "Paul Williams and Jack Conrad"),
    "Black and White": (1972, 1, "August 1972", "Seven Separate Fools", "David Arkin and Earl Robinson"),
    "Shambala": (1973, 3, "May 11, 1973", "Cyan", "Daniel Moore"),
    "Let Me Serenade You": (1973, 17, "November 3, 1973", "Cyan", "John Finley"),
    "The Show Must Go On": (1974, 4, "March 16, 1974", "Hard Labor", "Leo Sayer and David Courtney"),
}
ORDER = list(INFO)
BEYOND = {"Celebrate", "Out in the Country", "An Old Fashioned Love Song", "The Family of Man", "Let Me Serenade You"}
MAMA, JOY, BW, SHOW = "Mama Told Me (Not to Come)", "Joy to the World", "Black and White", "The Show Must Go On"
OLD, SPAIN = "An Old Fashioned Love Song", "Never Been to Spain"


def main():
    radio = json.loads(read(ROOT / "data/radio/radio-songs.json"))
    weekly = json.loads(read(ROOT / "data/billboard/hot100_weekly.json"))
    beyond = {s["title"]: s for s in json.loads(read(ROOT / "data/billboard/beyond_year_end.json"))["songs"]
              if s["page"] == PAGE}

    ye = {}
    for s in radio:
        if s["artist"] == ARTIST and s.get("youtube_id"):
            title = next(t for t in INFO if t.lower() == s["title"].lower())
            ye[title] = s
    assert len(ye) == 7, len(ye)
    assert set(beyond) == BEYOND, set(beyond)
    assert set(ye) | BEYOND == set(INFO), (set(ye) | BEYOND) ^ set(INFO)
    for t in BEYOND:
        assert beyond[t]["weekly_peak"] == INFO[t][1], t
        assert beyond[t]["released"] == INFO[t][0], t
    for t, s in ye.items():
        assert s["year"] in (INFO[t][0], INFO[t][0] + 1), (t, s["year"])
        assert s["billboard_peak"] == s["rank"], t

    # weekly number ones by Three Dog Night in the site's own 1970-1979 data
    wk = {}
    for yr in weekly:
        for w in weekly[yr]:
            if w["artist"] == ARTIST:
                wk.setdefault(w["title"], []).append(w)
    assert set(wk) == {MAMA, JOY, BW}, set(wk)
    wks = {t: len(v) for t, v in wk.items()}
    assert wks == {MAMA: 2, JOY: 6, BW: 1}, wks
    assert all(w["weeks_at_number_one"] == wks[t] for t, v in wk.items() for w in v)
    wk_start = {t: v[0]["week_start"] for t, v in wk.items()}
    assert wk_start == {MAMA: "1970-07-11", JOY: "1971-04-17", BW: "1972-09-16"}, wk_start
    assert sum(wks.values()) == 9

    rk = {t: ye[t]["rank"] for t in ye}
    yr_of = {t: ye[t]["year"] for t in ye}
    n = len(INFO)
    assert n == 12
    top_ten = [t for t in INFO if INFO[t][1] <= 10]
    assert len(top_ten) == 8, top_ten
    williams = [t for t in INFO if "Paul Williams" in INFO[t][4]]
    assert len(williams) == 3, williams
    axton = [t for t in INFO if "Hoyt Axton" in INFO[t][4]]
    assert len(axton) == 2, axton
    yt = {t: (ye[t]["youtube_id"] if t in ye else beyond[t]["youtube_id"]) for t in INFO}

    rows = []
    for t in ORDER:
        y, pk, rel, alb, wr = INFO[t]
        ye_year = yr_of[t] if t in ye else ""
        ye_rank = rk[t] if t in ye else ""
        rows.append(f'              <tr><td class="ohw-listen">{play_button(yt[t], t, ARTIST)}</td>'
                    f'<td class="ohw-song">{html.escape(t)}</td>'
                    f'<td>{y}</td><td>{ye_year}</td><td>{ye_rank}</td><td>{pk}</td></tr>')

    peak_rows = sorted(([html.escape(t), INFO[t][1], INFO[t][2]] for t in ORDER), key=lambda r: (r[1], r[0]))
    album_rows = [[html.escape(t), INFO[t][2], html.escape(INFO[t][3]), html.escape(INFO[t][4])] for t in ORDER]
    lead_rows = [
        ["Cory Wells", "Mama Told Me (Not to Come), Never Been to Spain"],
        ["Danny Hutton", "Liar, Black and White"],
        ["Chuck Negron", "An Old Fashioned Love Song, The Show Must Go On"],
        ["All three", "The Family of Man"],
        ["All seven members", "Joy to the World"],
    ]

    faq = [
        ("What is Three Dog Night's biggest hit?",
         ["Three Dog Night's biggest hit is Joy to the World, which Billboard named the number one single of 1971.",
          "This site's weekly chart data gives it six weeks at number one, starting April 17, 1971.",
          "It ranks #1 on the 1971 Year-End Hot 100.",
          "Wikipedia says it sold five million copies worldwide."]),
        ("How many number one songs did Three Dog Night have?",
         ["Three Dog Night had three Hot 100 number ones, all between 1970 and 1972.",
          "They are Mama Told Me (Not to Come), Joy to the World and Black and White.",
          "This site's weekly data gives them two, six and one weeks at the top, nine weeks in all.",
          "Wikipedia counts 21 top 40 hits for the band between 1969 and 1975."]),
        ("Who wrote Joy to the World by Three Dog Night?",
         ["Hoyt Axton wrote Joy to the World, not the band, according to Wikipedia.",
          "Axton and his mother, Mae Axton, became the first mother and son to each write a rock-era number one pop single.",
          "Three Dog Night released it as a single in February 1971, from the album Naturally.",
          "Axton also wrote Never Been to Spain."]),
        ("Who wrote Mama Told Me (Not to Come)?",
         ["Randy Newman wrote Mama Told Me (Not to Come), and Eric Burdon and the Animals recorded it before Three Dog Night did.",
          "Newman's own version appeared on his 1970 album 12 Songs.",
          "Three Dog Night released its version in May 1970, with Cory Wells singing lead.",
          "It reached number one on the Hot 100 for two weeks in July 1970."]),
        ("Did Three Dog Night write their own songs?",
         ["Three Dog Night mostly recorded songs by outside writers, according to Wikipedia.",
          "The band helped introduce mainstream listeners to Harry Nilsson, Randy Newman, Paul Williams, Laura Nyro and Hoyt Axton.",
          "Of the twelve hits on this page, Paul Williams wrote or co-wrote three and Hoyt Axton wrote two.",
          "Every song's writers are listed in the table near the end."]),
    ]
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": " ".join(a)}} for q, a in faq]},
        indent=2, ensure_ascii=False)
    faq_ld = "\n".join("  " + l for l in faq_ld.split("\n"))
    faq_html = "\n".join(
        f'          <div class="faq-item">\n            <h3>{html.escape(q)}</h3>\n' + "\n".join(f"            <p>{html.escape(l)}</p>" for l in a) + "\n          </div>"
        for q, a in faq).replace("&#x27;", "'")

    TITLE = f"Three Dog Night Songs: {n} Hits Played, 3 at Number One"
    desc = (f"Three Dog Night songs of the 70s, all {n} playable: Joy to the World, Black and White, Shambala and more. "
            "Read the story behind each hit.")
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

    toc = [("three-dog-night-songs-list", f"Three Dog Night Songs: Play All {n} Hits"),
           ("by-the-numbers", "Three Dog Night Songs on the Charts: Three Number Ones, Eight Top Tens"),
           ("origins", "From Redwood to Three Dog Night: How the Band Began"),
           ("year-1970", "1970: Celebrate, Mama Told Me (Not to Come) and Out in the Country"),
           ("year-1971", "1971: Joy to the World, Liar, An Old Fashioned Love Song and Never Been to Spain"),
           ("year-1972", "1972: The Family of Man and Black and White"),
           ("year-1973-74", "1973 and 1974: Shambala, Let Me Serenade You and The Show Must Go On"),
           ("three-voices", "Three Lead Voices: Who Sang Which Three Dog Night Song"),
           ("who-wrote-what", "Who Wrote and Released Each of the Three Dog Night Songs"),
           ("sources", "Sources"), ("faq", "Frequently Asked Questions")]
    toc_html = "\n".join(f'            <li><a href="#{i}">{t}</a></li>' for i, t in toc)

    feat_pic = pic(IMG, "Three Dog Night singers Danny Hutton, Chuck Negron and Cory Wells at microphones on an NBC television stage in 1975, the voices behind the Three Dog Night songs of the 70s",
                   "(max-width: 700px) 100vw, 669px", 669, 465, widths=(400, 669), lazy=False).replace(
        'class="post-featured-img"', 'class="post-featured-img" style="aspect-ratio:669/465;max-width:669px;height:auto;margin:1.5rem auto"', 1)
    pic2 = pic(IMG2, "Black and white 1972 portrait of the seven members of Three Dog Night posed together against a dark backdrop, the group behind Black and White and Joy to the World",
               "(max-width: 700px) 100vw, 400px", 630, 879, widths=(400, 630)).replace(
        "<img\n", '<img style="display:block;width:100%;max-width:400px;height:auto;margin:1.5rem auto;border-radius:8px"\n', 1)
    chart_pic = pic(CHART, "Lollipop chart of twelve Three Dog Night songs by Hot 100 peak, from Mama Told Me (Not to Come), Joy to the World and Black and White at number one to Let Me Serenade You at number 17",
                    "(max-width: 700px) 100vw, 800px", 800, 450, widths=(400, 800, 1200)).replace(
        "<img\n", '<img style="display:block;width:100%;max-width:800px;height:auto;margin:1.5rem auto;border-radius:8px"\n', 1)

    body = f'''        <h2 id="three-dog-night-songs-list">Three Dog Night Songs: Play All {n} Hits</h2>
{p(f"Here are {NUM[n]} Three Dog Night songs from 1970 to 1974, from Celebrate to The Show Must Go On.",
   "Seven sit on a Billboard Year-End Hot 100, and five more charted weekly without making a year-end list.",
   "Press Play on any row to watch it here, and tap a heading to sort.")}

        <div class="data-table-wrap scroll-list">
          <table class="data-table sortable-table" id="threeDogNightSongsTable" data-inline-player>
            <caption>{n} Three Dog Night songs of the 70s, with release year, Billboard Year-End Hot 100 rank and Hot 100 peak</caption>
            <thead>
              <tr>
                <th><span class="visually-hidden">Play</span></th>
                <th><button type="button" data-col="1" data-type="text">Song</button></th>
                <th aria-sort="ascending"><button type="button" data-col="2" data-type="num">Released</button></th>
                <th><button type="button" data-col="3" data-type="num">Year-End List</button></th>
                <th><button type="button" data-col="4" data-type="num">Year-End Rank</button></th>
                <th><button type="button" data-col="5" data-type="num">Hot 100 Peak</button></th>
              </tr>
            </thead>
            <tbody>
{chr(10).join(rows)}
            </tbody>
          </table>
        </div>
{p("Released is the year each song came out, per Wikipedia.",
   "Year-End List and Year-End Rank show which year-end list a song is on, and its rank there.",
   "A blank means it is on none.",
   "Hot 100 Peak is the weekly peak, from each song's Wikipedia article.",
   "The three number ones are the Hot 100 chart toppers in this site's weekly chart data.")}

        <h2 id="by-the-numbers">Three Dog Night Songs on the Charts: Three Number Ones, Eight Top Tens</h2>
{p("The Three Dog Night songs of the 70s were hits on the pop charts and in Canada.",
   "Three reached number one on the Hot 100, and this site's weekly data counts nine weeks at the top between them.",
   "Mama Told Me (Not to Come) held the top spot for two weeks, starting July 11, 1970.",
   "Joy to the World held it for six weeks, starting April 17, 1971.",
   "Black and White held it for one week, starting September 16, 1972.")}

{chart_pic}
        <p class="post-img-caption">Hot 100 peaks of the twelve hits on this page, from each song's Wikipedia article.</p>

{tbl("Three Dog Night songs of the 70s ranked by weekly Hot 100 peak, with release date (Wikipedia)", ["Song", "Hot 100 Peak", "Released"], peak_rows)}

        <h3>What the Chart Numbers Say</h3>
{p(f"Eight of the {NUM[n]} Three Dog Night songs on this page reached the Hot 100's top ten.")}
        <ul>
          <li>Mama Told Me (Not to Come), Joy to the World and Black and White reached number one in 1970, 1971 and 1972.</li>
          <li>Shambala came closest after that, stopping at number three in 1973.</li>
          <li>An Old Fashioned Love Song and The Show Must Go On both stopped at number four.</li>
          <li>Joy to the World ranks #{rk[JOY]} on the 1971 Year-End Hot 100, the best year-end rank of any song here, ahead of Mama Told Me (Not to Come) at #{rk[MAMA]} on the 1970 list.</li>
          <li>Wikipedia counts 21 top 40 hits for the band between 1969 and 1975, and 13 straight top ten hits in Canada from 1969 to 1972.</li>
        </ul>
{p('To see who else ruled the decade&#39;s number one spots, read the page on <a href="/blog/songs/70s-number-one-hits/">70s number one hits</a>.')}

        <h2 id="origins">From Redwood to Three Dog Night: How the Band Began</h2>
{p("The story behind the Three Dog Night songs starts in Los Angeles in 1967.",
   "Wikipedia says three singers founded the band: Chuck Negron, Cory Wells and Danny Hutton.",
   "They first played as Redwood, in 1967 and 1968.")}

        <h3>Where the Name Came From</h3>
{p("The name has two stories, and Wikipedia gives both.",
   "According to the Celebrate CD commentary, Hutton's girlfriend, the actress June Fairchild, suggested it.",
   "She had read that Aboriginal Australians slept beside dingoes on cold nights.",
   "A very cold night was a three dog night.",
   "Van Dyke Parks, an arranger at Warner Bros. Records, disputed that and said he coined the name himself.")}

        <h3>Seven Players, Three Singers</h3>
{p("The three vocalists were joined by Jimmy Greenspoon on keyboards, Joe Schermie on bass and Floyd Sneed on drums.",
   "Guitarist Ron Morgan left before the first album was recorded, and Michael Allsup replaced him.",
   "The band played from 1967 to 1976, and again from 1981.",
   "The first run ended with a show at the Greek Theatre in Los Angeles on July 26, 1976.",
   'For a random song from the same decade, try the <a href="/pages/random-70s-song">Random 70s Song Generator</a>.')}

        <h2 id="year-1970">1970: Celebrate, Mama Told Me (Not to Come) and Out in the Country</h2>
{p("Three Dog Night opened the decade with three hits, and one of them reached number one.",
   f"Mama Told Me (Not to Come) ranks #{rk[MAMA]} on the 1970 Year-End Hot 100.")}

        <h3>Celebrate</h3>
{p("Celebrate was released in January 1970, from the album Suitable for Framing.",
   "Gary Bonner and Alan Gordon wrote it, and Gabriel Mekler produced it.",
   "It reached number 15 on the Hot 100, and number eight in Canada.",
   "It is on no 1970s year-end list, so its peak above is a weekly peak only.")}
{p("The horn section on the record is from the band then known as the Chicago Transit Authority.",
   "Its B-side was Feeling Alright?")}

        <h3>Mama Told Me (Not to Come)</h3>
{p("Mama Told Me (Not to Come) was released in May 1970, from It Ain't Easy.",
   "Randy Newman wrote it for Eric Burdon's first solo album in 1966.",
   "The Animals recorded it first, and Newman put his own version on 12 Songs in 1970.",
   "Newman said the song grew from a light-hearted look at the late-1960s Los Angeles music scene.")}
{p("Cory Wells sang lead on the Three Dog Night version.",
   "He had played the song with his earlier group, the Enemies, and the rest of the band at first resisted it.",
   "It topped the Hot 100 for two weeks in July 1970, and the RIAA certified it gold on July 14, 1970.",
   "It reached number three in the UK, and number two in Canada.",
   "The record turns up in the films Boogie Nights and Fear and Loathing in Las Vegas.")}

        <h3>Out in the Country</h3>
{p("Out in the Country was released in August 1970, from It Ain't Easy, and Paul Williams and Roger Nichols wrote it.",
   "It was recorded in 1969.",
   "It reached number 15 on the Hot 100 in the weeks of October 17 and 24, 1970.",
   "It reached number 11 on the Adult Contemporary chart.",
   "Wikipedia calls it an early environmental advocacy song, released in the first year of Earth Day.")}
{p("R.E.M. covered it in 2003, as a B-side to their single Bad Day.",
   "It is on no 1970s year-end list, so its peak above is a weekly peak only.")}

        <h2 id="year-1971">1971: Joy to the World, Liar, An Old Fashioned Love Song and Never Been to Spain</h2>
{p("1971 brought the band's biggest hit and three more on this list.",
   f"Joy to the World ranks #{rk[JOY]}, Liar ranks #{rk['Liar']}, and Never Been to Spain ranks #{rk[SPAIN]} on the 1972 list.")}

        <h3>Joy to the World</h3>
{p("Joy to the World was released as a single in February 1971.",
   "It first appeared on the album Naturally in November 1970.",
   "Hoyt Axton wrote it, and Wikipedia says all seven band members sang on the recording.",
   "Drummer Floyd Sneed sings the low line near the end.")}
        <h3>How Joy to the World Came Together</h3>
{p("Joy to the World is the best known of all the Three Dog Night songs, and its story starts with a melody that Axton offered to the band's producers.",
   "They asked him to sing any words to it.",
   "Hutton and Wells rejected the song.",
   "Negron felt the band needed a silly song to bring them back together.")}
        <h3>Six Weeks at Number One</h3>
{p("This site's weekly data gives it six weeks at number one, from April 17 to May 22, 1971.",
   "It ranks #1 on the 1971 Year-End Hot 100.",
   "The RIAA certified it gold on April 9, 1971, and Wikipedia says it sold five million copies worldwide.",
   "It was nominated for a Grammy at the 14th Grammy Awards.")}
{p("Axton and his mother, Mae Axton, became the first mother and son to each write a rock-era number one pop single.",
   "The song plays in Forrest Gump and The Big Chill, and after Denver Broncos home wins.",
   'Find a mood for it with the <a href="/pages/mood-song-matcher">Mood Song Matcher</a>.')}

        <h3>Liar</h3>
{p("Liar was released in July 1971, from Naturally.",
   "Russ Ballard of Argent wrote it, and Argent released it first on their 1970 album Argent.",
   "That single did not chart.",
   "Danny Hutton sang lead on the Three Dog Night version, and Richard Podolor produced it.")}
{p(f"It reached number seven on the Hot 100 and number four in Canada, and it ranks #{rk['Liar']} on the 1971 Year-End Hot 100.")}

        <h3>An Old Fashioned Love Song</h3>
{p("An Old Fashioned Love Song was released in November 1971, as the first single from Harmony.",
   "Paul Williams wrote it, and Chuck Negron sang lead.",
   "It reached number four on the Hot 100 in December 1971, and number one on the Adult Contemporary chart.",
   "Wikipedia says that made it the band's first record to top the easy listening chart.")}
{p("According to a biography of Karen Carpenter, Williams first wrote it with the Carpenters in mind.",
   "Richard Carpenter turned it down, so Williams offered it to Three Dog Night.",
   "The Carpenters never recorded it, though they performed it live on television with Carol Burnett.",
   "It is on no 1970s year-end list, so its peak above is a weekly peak only.",
   'The duo have their own page on <a href="/blog/artists/carpenters-songs/">Carpenters songs</a>.')}

        <h3>Never Been to Spain</h3>
{p("Never Been to Spain was released in 1971, from Harmony, and Hoyt Axton wrote it.",
   "Axton first released it on his 1971 album Joy to the World.",
   "Cory Wells sang lead on the Three Dog Night version.")}
{p("It reached number five on the Hot 100, number 18 on the Adult Contemporary chart and number three in Canada.",
   f"It ranks #{rk[SPAIN]} on the 1972 Year-End Hot 100.",
   "Ronnie Sessions took a cover to number 36 on the country chart in 1972.")}

        <h2 id="year-1972">1972: The Family of Man and Black and White</h2>
{p("1972 brought two Three Dog Night songs, one that stalled in the teens and one that went to number one.")}

        <h3>The Family of Man</h3>
{p("The Family of Man was released in March 1972, from Harmony, and Paul Williams and Jack Conrad wrote it.",
   "Three members shared the lead vocal.",
   "Danny Hutton sang the first verse, Chuck Negron the second verse and the fade-out, and Cory Wells the third verse.")}
{p("It reached number 12 on the Hot 100, number 27 on the Adult Contemporary chart and number five in Canada.",
   "The B-side was Going in Circles.",
   "Williams released his own version on his 1974 album A Little Bit of Love.",
   "It is on no 1970s year-end list, so its peak above is a weekly peak only.")}

        <h3>Black and White</h3>
{p("Black and White was released in August 1972, from Seven Separate Fools, and Danny Hutton sang lead.",
   "It is older than the band.",
   "David Arkin wrote the words and Earl Robinson wrote the music in 1954, and Pete Seeger made the first recording in 1956.")}
{pic2}
        <p class="post-img-caption">Three Dog Night in a 1972 television special photo from ABC Television.</p>
        <p class="post-img-caption">Image credit: ABC Television photo, public domain, via Wikimedia Commons.</p>
        <h3>From Brown v. Board of Education to Number One</h3>
{p("The song was inspired by the 1954 Supreme Court decision in Brown v. Board of Education.",
   "That ruling outlawed racial segregation in public schools.",
   "The original lyrics opened with a verse about the court, and the Three Dog Night version dropped it.",
   "Wikipedia says that made the song more universal and less historically specific.")}
{p("It reached number one on the Hot 100 and on the Easy Listening chart.",
   "This site's weekly data gives it one week at number one, starting September 16, 1972.",
   f"It ranks #{rk[BW]} on the 1972 Year-End Hot 100.",
   "The UK band Greyhound took a version to number six in 1971.",
   'Test your memory of the decade with the <a href="/pages/70s-trivia-quiz">70s Music Trivia Quiz</a>.')}

        <h2 id="year-1973-74">1973 and 1974: Shambala, Let Me Serenade You and The Show Must Go On</h2>
{p("The last three Three Dog Night songs on this page show a band leaning on other people's songs as much as ever.")}

        <h3>Shambala</h3>
{p("Shambala was released on May 11, 1973, from Cyan, the band's ninth album.",
   "Wikipedia says it was the first song the group cut specifically as a single.",
   "Daniel Moore wrote it, and B. W. Stevenson recorded it first, in April 1973.",
   "Stevenson's version stopped at number 66 on the Hot 100.")}
{p("Three Dog Night's version reached number three on the Hot 100 and number three on the Adult Contemporary chart.",
   f"It ranks #{rk['Shambala']} on the 1973 Year-End Hot 100.",
   "It also reached number one on Cash Box.")}
        <h3>The Kingdom Behind the Title</h3>
{p("The title comes from Shambhala, a mythical kingdom said to lie in or beyond the Himalayas.",
   "Moore pronounces the first syllable to rhyme with ham, while both later versions rhyme it with mom.",
   'For more pop hits of the decade, read the page on <a href="/blog/genres/pop-songs-of-70s/">pop songs of the 70s</a>.')}

        <h3>Let Me Serenade You</h3>
{p("Let Me Serenade You was released on November 3, 1973, from Cyan, and John Finley wrote it.",
   "Rhinoceros recorded it first, as I Will Serenade You, on the B-side of a November 1968 single.",
   "It was the closing track on Rhinoceros's debut album.")}
{p("Richard Podolor produced the cover, and he and the band arranged it together.",
   "They recorded it at American Recording Co. in Studio City, Los Angeles.",
   "It reached number 17 on the Hot 100 and number 11 in Canada.",
   "It is on no 1970s year-end list, so its peak above is a weekly peak only.")}

        <h3>The Show Must Go On</h3>
{p("The Show Must Go On was released on March 16, 1974, from Hard Labor.",
   "Leo Sayer and David Courtney wrote it.",
   "Sayer's own version came out in the UK in 1973, from his debut album Silverbird.",
   "It was his first hit, and it reached number two on the UK chart.")}
{p("Chuck Negron sang lead on the Three Dog Night version.",
   "It reached number four on the Hot 100, and it ranks #" + str(rk[SHOW]) + " on the 1974 Year-End Hot 100.",
   "The song uses a circus as a metaphor for the difficulties and wrong choices of life.",
   "Early in his career Sayer sang it dressed as a pierrot clown.")}
        <h3>Circus Metaphor, Changed Chorus</h3>
{p("Both versions quote Julius Fučík's Entrance of the Gladiators.",
   "Three Dog Night changed the final chorus line, and Sayer has criticized the change.",
   'The soft side of the decade has its own page, <a href="/blog/genres/70s-soft-rock/">70s soft rock</a>.')}

        <h2 id="three-voices">Three Lead Voices: Who Sang Which Three Dog Night Song</h2>
{p("Three singers shared the front of the band, and Wikipedia names the lead on most of the hits above.",
   "The table lists the songs where the lead singer is named.",
   "Wikipedia names no single lead for Celebrate, Out in the Country, Shambala or Let Me Serenade You.")}

{tbl("Lead vocalists on Three Dog Night songs of the 70s where Wikipedia names them", ["Lead Vocal", "Songs"], lead_rows)}

        <h3>Songs from Outside Writers</h3>
{p("The band took its hits from other writers.",
   f"Paul Williams wrote or co-wrote {NUM[len(williams)]} of the {NUM[n]} songs on this page, and Hoyt Axton wrote {NUM[len(axton)]}.",
   "Wikipedia says the band also helped introduce mainstream listeners to Harry Nilsson, Randy Newman and Laura Nyro.")}
        <ul>
          <li>Paul Williams: Out in the Country, An Old Fashioned Love Song and The Family of Man.</li>
          <li>Hoyt Axton: Joy to the World and Never Been to Spain.</li>
          <li>Randy Newman: Mama Told Me (Not to Come).</li>
          <li>Russ Ballard of Argent: Liar.</li>
          <li>Leo Sayer and David Courtney: The Show Must Go On.</li>
        </ul>

        <h2 id="who-wrote-what">Who Wrote and Released Each of the Three Dog Night Songs</h2>
{p(f"The table lists when each of the {NUM[n]} songs was released, on which album, and who wrote it.")}

{tbl("Three Dog Night songs of the 70s: release date, album and writers (Wikipedia)", ["Song", "Released", "Album", "Written By"], album_rows)}

        <h3>Keep Exploring</h3>
{p("Three Dog Night songs gave the decade three number ones and a run of hits written by other people.",
   "Eight of the twelve reached the top ten.",
   'The page on <a href="/blog/artists/elton-john/">Elton John</a> tells the story of another act that ruled the decade&#39;s pop charts.')}

        <h2 id="sources">Sources</h2>
{p("Year-end ranks come from this site's own Billboard data, described on the <a href='/about/methodology/'>methodology page</a>.",
   'Every list on <a href="/">Music of the 70s</a> plays inside the page.',
   "Peaks, dates and stories behind the Three Dog Night songs above can be checked against these outside sources:")}
        <ul>
          <li><a href="https://en.wikipedia.org/wiki/Three_Dog_Night" rel="noopener">Wikipedia: Three Dog Night</a> and <a href="https://en.wikipedia.org/wiki/Three_Dog_Night_discography" rel="noopener">their discography</a> for the biography, albums, singles and chart peaks.</li>
          <li><a href="https://en.wikipedia.org/wiki/Celebrate_(Three_Dog_Night_song)" rel="noopener">Wikipedia: Celebrate</a>, <a href="https://en.wikipedia.org/wiki/Mama_Told_Me_(Not_to_Come)" rel="noopener">Mama Told Me (Not to Come)</a> and <a href="https://en.wikipedia.org/wiki/Out_in_the_Country" rel="noopener">Out in the Country</a> for 1970.</li>
          <li><a href="https://en.wikipedia.org/wiki/Joy_to_the_World_(Three_Dog_Night_song)" rel="noopener">Wikipedia: Joy to the World</a>, <a href="https://en.wikipedia.org/wiki/Liar_(Russ_Ballard_song)" rel="noopener">Liar</a>, <a href="https://en.wikipedia.org/wiki/An_Old_Fashioned_Love_Song" rel="noopener">An Old Fashioned Love Song</a> and <a href="https://en.wikipedia.org/wiki/Never_Been_to_Spain" rel="noopener">Never Been to Spain</a> for 1971.</li>
          <li><a href="https://en.wikipedia.org/wiki/The_Family_of_Man_(Three_Dog_Night_song)" rel="noopener">Wikipedia: The Family of Man</a> and <a href="https://en.wikipedia.org/wiki/Black_and_White_(Three_Dog_Night_song)" rel="noopener">Black and White</a> for 1972.</li>
          <li><a href="https://en.wikipedia.org/wiki/Shambala_(song)" rel="noopener">Wikipedia: Shambala</a>, <a href="https://en.wikipedia.org/wiki/Let_Me_Serenade_You" rel="noopener">Let Me Serenade You</a> and <a href="https://en.wikipedia.org/wiki/The_Show_Must_Go_On_(Leo_Sayer_song)" rel="noopener">The Show Must Go On</a> for 1973 and 1974.</li>
        </ul>

        <section class="faq-block" id="faq">
          <h2>Frequently Asked Questions</h2>
{faq_html}
        </section>'''

    related = [
        ("carpenters-1972", "Artists", "Carpenters Songs: 11 Hits Played, 3 at Number One", "/blog/artists/carpenters-songs/",
         "The duo Paul Williams first wrote An Old Fashioned Love Song for, with every hit playable.", "The Carpenters in 1972"),
        ("elton-john-1972", "Artists", "Elton John: 13 Hits Played, 6 at Number One", "/blog/artists/elton-john/",
         "The pop-crossover giant of the decade, with every hit playable.", "Elton John in 1972"),
        ("carole-1971", "Genres", "70s Soft Rock: The Sound Built to Calm the Decade Down", "/blog/genres/70s-soft-rock/",
         "The quieter side of the decade, with a full playable list.", "Carole King at a piano in 1971, representing 70s soft rock"),
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
      {{"@type": "ListItem", "position": 4, "name": "Three Dog Night Songs", "item": "{URL}"}}
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
        Three Dog Night Songs
      </nav>

      <article class="section seo-content">
        <h1>{TITLE}</h1>

        <p class="post-byline">By <a href="https://musicofthe70s.net/about/author/">Charlie</a> &middot; Published {PUBLISHED.strftime('%B')} {PUBLISHED.day}, {PUBLISHED.year}</p>
        <p class="jump-to-list"><a class="btn-primary jump-btn" href="#three-dog-night-songs-list">&#9654; Jump to the playable list</a></p>

        <p class="post-intro">Three Dog Night songs were on the radio all through the early 70s.</p>
        <p class="post-intro">Three of them, Mama Told Me (Not to Come), Joy to the World and Black and White, reached number one on the Hot 100.</p>
        <p class="post-intro">This page plays {NUM[n]} of them, from Celebrate to The Show Must Go On.</p>
        <p class="post-intro">Eight reached the Hot 100's top ten, and Joy to the World was the number one song of 1971.</p>
        <p class="post-intro">Three singers shared the lead, and the hits came from outside writers.</p>
        <p class="post-intro">Press Play on every hit below, then read the story behind each one.</p>

{feat_pic}
        <p class="post-img-caption">Danny Hutton, Chuck Negron and Cory Wells of Three Dog Night in an NBC television special, 1975.</p>
        <p class="post-img-caption">Image credit: NBC Television photo, public domain, via Wikimedia Commons.</p>

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
