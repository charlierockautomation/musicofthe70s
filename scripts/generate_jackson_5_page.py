#!/usr/bin/env python3
"""Build the Jackson 5 Songs Artists post (blog/artists/jackson-5-songs/index.html).

Data: data/radio/radio-songs.json (seven Jackson 5 rows of the 1970, 1971 and 1974 Year-End Hot 100 plus two Jacksons rows
of 1977 and 1979, each with a YouTube ID), data/billboard/hot100_weekly.json (the four Jackson 5 number ones and their
weeks at #1, 1970), data/billboard/beyond_year_end.json (four further Jackson 5 singles on the weekly Hot 100 but on no
1970s year-end list: Sugar Daddy, Little Bitty Pretty One, Lookin' Through the Windows and I Am Love, peaks and YouTube IDs
checked). Year-End Rank is the year-end rank, never a peak. Hot 100 and UK peaks, release dates, writers, certifications
and story facts come from the linked Wikipedia articles, checked 2026-10-13, and are credited to Wikipedia on the page.
The site JSON's fun_fact text for the Jackson 5 is not used.

Run: python3 scripts/generate_jackson_5_page.py
"""
import html
import json
from datetime import date

from genre_page_common import ROOT, read, play_button, write
from generate_country_page import p, tbl, pic

SLUG = "jackson-5-songs"
PAGE = f"blog/artists/{SLUG}/"
URL = f"https://musicofthe70s.net/{PAGE}"
IMG = "jackson-5-1972"
IMG2 = "jackson-5-1974"
PUBLISHED = date(2026, 10, 13)
NUM = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
       10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen"}

# title -> (release year, Hot 100 peak, UK peak or None, released text, album, billed as)
# Every value read from the song's Wikipedia article, checked 2026-10-13.
INFO = {
    "I Want You Back": (1969, 1, 2, "October 1969", "Diana Ross Presents The Jackson 5", "The Jackson 5"),
    "ABC": (1970, 1, 8, "February 24, 1970", "ABC", "The Jackson 5"),
    "The Love You Save": (1970, 1, 7, "May 13, 1970", "ABC", "The Jackson 5"),
    "I'll Be There": (1970, 1, 4, "August 28, 1970", "Third Album", "The Jackson 5"),
    "Mama's Pearl": (1971, 2, 25, "January 7, 1971", "Third Album", "The Jackson 5"),
    "Never Can Say Goodbye": (1971, 2, 33, "March 16, 1971", "Maybe Tomorrow", "The Jackson 5"),
    "Sugar Daddy": (1971, 10, None, "November 23, 1971", "Greatest Hits (1971)", "The Jackson 5"),
    "Little Bitty Pretty One": (1972, 13, None, "April 4, 1972", "Lookin' Through the Windows", "The Jackson 5"),
    "Lookin' Through the Windows": (1972, 16, None, "June 23, 1972", "Lookin' Through the Windows", "The Jackson 5"),
    "Dancing Machine": (1974, 2, None, "February 19, 1974", "Dancing Machine", "The Jackson 5"),
    "I Am Love": (1974, 15, None, "December 23, 1974", "Dancing Machine", "The Jackson 5"),
    "Enjoy Yourself": (1976, 6, None, "October 22, 1976", "The Jacksons", "The Jacksons"),
    "Shake Your Body (Down to the Ground)": (1979, 7, 4, "January 18, 1979", "Destiny", "The Jacksons"),
}
ORDER = list(INFO)
BEYOND = {"Sugar Daddy", "Little Bitty Pretty One", "Lookin' Through the Windows", "I Am Love"}
NUMBER_ONES = ["I Want You Back", "ABC", "The Love You Save", "I'll Be There"]


def main():
    radio = json.loads(read(ROOT / "data/radio/radio-songs.json"))
    weekly = json.loads(read(ROOT / "data/billboard/hot100_weekly.json"))
    beyond = {s["title"]: s for s in json.loads(read(ROOT / "data/billboard/beyond_year_end.json"))["songs"]
              if s["page"] == PAGE}

    ye = {s["title"]: s for s in radio
          if s["artist"] in ("The Jackson 5", "The Jacksons") and s.get("youtube_id")}
    assert len(ye) == 9, len(ye)
    assert set(beyond) == BEYOND, set(beyond)
    assert set(ye) | BEYOND == set(INFO), (set(ye) | BEYOND) ^ set(INFO)
    for t in BEYOND:
        assert beyond[t]["weekly_peak"] == INFO[t][1], t
        assert beyond[t]["released"] == INFO[t][0], t
    for t, s in ye.items():
        assert s["year"] in (INFO[t][0], INFO[t][0] + 1), (t, s["year"])

    # weekly number ones by The Jackson 5 in the site's own 1970-1979 data
    wk = {}
    for yr in weekly:
        for w in weekly[yr]:
            if w["artist"] == "The Jackson 5":
                wk.setdefault(w["title"], []).append(w)
    assert list(wk) and set(wk) == set(NUMBER_ONES), set(wk)
    weeks = {t: len(v) for t, v in wk.items()}
    assert weeks == {"I Want You Back": 1, "ABC": 2, "The Love You Save": 2, "I'll Be There": 5}, weeks
    total_weeks = sum(weeks.values())
    assert total_weeks == 10
    first_week = {t: v[0]["week_start"] for t, v in wk.items()}

    rk = {t: ye[t]["rank"] for t in ye}
    r_dm, r_ibt, r_mp = rk["Dancing Machine"], rk["I'll Be There"], rk["Mama's Pearl"]
    n = len(INFO)
    assert n == 13
    top_ten = [t for t in INFO if INFO[t][1] <= 10]
    assert len(top_ten) == 10, top_ten
    yt = {t: (ye[t]["youtube_id"] if t in ye else beyond[t]["youtube_id"]) for t in INFO}

    rows = []
    for t in ORDER:
        y, pk, uk, rel, alb, billed = INFO[t]
        ye_year = ye[t]["year"] if t in ye else ""
        ye_rank = ye[t]["rank"] if t in ye else ""
        rows.append(f'              <tr><td class="ohw-listen">{play_button(yt[t], t, billed)}</td>'
                    f'<td class="ohw-song">{html.escape(t)}</td>'
                    f'<td>{y}</td><td>{ye_year}</td><td>{ye_rank}</td><td>{pk}</td></tr>')

    us_rows = sorted(([html.escape(t), INFO[t][1], INFO[t][3]] for t in ORDER), key=lambda r: (r[1], r[0]))
    uk_rows = sorted(([html.escape(t), INFO[t][1], INFO[t][2], INFO[t][3]] for t in ORDER if INFO[t][2] is not None),
                     key=lambda r: r[2])
    assert len(uk_rows) == 7
    one_rows = [[html.escape(t), weeks[t], first_week[t], INFO[t][3]] for t in NUMBER_ONES]
    album_rows = [[html.escape(t), INFO[t][3], html.escape(INFO[t][4]), INFO[t][5]] for t in ORDER]

    faq = [
        ("How many number one songs did the Jackson 5 have?",
         ["The Jackson 5 had four number one songs on the Billboard Hot 100: I Want You Back, ABC, The Love You Save and I'll Be There.",
          "All four came in 1970, and together they spent ten weeks at number one in this site's weekly chart data.",
          "Wikipedia says the Jackson 5 were the first recording act whose first four singles all reached number one."]),
        ("What was the Jackson 5's biggest hit?",
         ["I'll Be There was the Jackson 5's biggest hit, with five weeks at number one on the Billboard Hot 100 in late 1970.",
          "Wikipedia says it replaced I Heard It Through the Grapevine as the most successful Motown single in the US, a record it held until 1981.",
          "It ranks #7 on the 1970 Year-End Hot 100."]),
        ("Who wrote the Jackson 5's early hits?",
         ["The Corporation wrote I Want You Back, ABC and The Love You Save, according to Wikipedia.",
          "Berry Gordy set up the team in September 1969 to write exclusively for the group.",
          "Its members were Gordy, Freddie Perren, Alphonzo Mizell and Deke Richards.",
          "I'll Be There was written by Gordy, Hal Davis, Bob West and Willie Hutch."]),
        ("Why did the Jackson 5 become The Jacksons?",
         ["The Jackson 5 became The Jacksons in 1976 because Motown owned the name Jackson 5, according to Wikipedia.",
          "The brothers signed with Epic Records in June 1975, and Motown allowed the Epic recordings on the condition that the name change.",
          "Jermaine stayed at Motown, and Randy Jackson replaced him."]),
        ("When did Michael Jackson do the robot dance in Dancing Machine?",
         ["Michael Jackson performed the robot dance on Soul Train on October 27, 1973, and Wikipedia says it was fully caught on camera.",
          "The song, Dancing Machine, was released on February 19, 1974.",
          "It reached number two on the Hot 100, number one on the soul chart, and ranks #5 on the 1974 Year-End Hot 100."]),
    ]
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": " ".join(a)}} for q, a in faq]},
        indent=2, ensure_ascii=False)
    faq_ld = "\n".join("  " + l for l in faq_ld.split("\n"))
    faq_html = "\n".join(
        f'          <div class="faq-item">\n            <h3>{html.escape(q)}</h3>\n' + "\n".join(f"            <p>{html.escape(l)}</p>" for l in a) + "\n          </div>"
        for q, a in faq).replace("&#x27;", "'")

    TITLE = f"Jackson 5 Songs: {n} Hits Played, 4 at Number One"
    desc = (f"Jackson 5 songs of the 70s, all {n} playable: I Want You Back, ABC, I'll Be There and more. "
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

    toc = [("jackson-5-songs-list", f"Jackson 5 Songs: Play All {n} Hits"),
           ("by-the-numbers", "Jackson 5 Songs on the Charts: Four Number Ones in 1970"),
           ("origins", "Gary, Indiana to Hitsville: How the Jackson 5 Began"),
           ("number-ones", "The Four Number Ones: I Want You Back, ABC, The Love You Save and I'll Be There"),
           ("after-number-ones", "After the Number Ones: Mama's Pearl, Never Can Say Goodbye and Sugar Daddy"),
           ("window-years", "1972: Little Bitty Pretty One and Lookin' Through the Windows"),
           ("dancing-machine", "Dancing Machine and I Am Love: The Last Motown Hits"),
           ("the-jacksons", "From Jackson 5 to The Jacksons: Enjoy Yourself and Shake Your Body"),
           ("who-wrote-what", "Who Wrote and Released Each of the Jackson 5 Songs"),
           ("sources", "Sources"), ("faq", "Frequently Asked Questions")]
    toc_html = "\n".join(f'            <li><a href="#{i}">{t}</a></li>' for i, t in toc)

    feat_pic = pic(IMG, "The Jackson 5 performing on stage in 1972 in matching white outfits, the Jackson 5 songs live on television",
                   "(max-width: 700px) 100vw, 669px", 669, 509, widths=(400, 669), lazy=False).replace(
        'class="post-featured-img"', 'class="post-featured-img" style="aspect-ratio:669/509;max-width:669px;height:auto;margin:1.5rem auto"', 1)
    band_pic = pic(IMG2, "Black and white 1974 portrait of the six Jackson brothers, with Michael Jackson at the center, from the Dancing Machine era",
                   "(max-width: 700px) 100vw, 400px", 669, 733, widths=(400, 669)).replace(
        "<img\n", '<img style="display:block;width:100%;max-width:400px;height:auto;margin:1.5rem auto;border-radius:8px"\n', 1)

    body = f'''        <h2 id="jackson-5-songs-list">Jackson 5 Songs: Play All {n} Hits</h2>
{p(f"Here are {NUM[n]} Jackson 5 songs from 1969 to 1979, from I Want You Back to Shake Your Body.",
   "Nine sit on a Billboard Year-End Hot 100, and four more charted weekly without making a year-end list.",
   "The last two were released after the group became The Jacksons.",
   "Press Play on any row to watch it here, and tap a heading to sort.")}

        <div class="data-table-wrap scroll-list">
          <table class="data-table sortable-table" id="jackson5SongsTable" data-inline-player>
            <caption>{n} Jackson 5 songs of the 70s, with release year, Billboard Year-End Hot 100 rank and Hot 100 peak</caption>
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
   "The number ones are the four Hot 100 chart toppers in this site's weekly chart data.")}

        <h2 id="by-the-numbers">Jackson 5 Songs on the Charts: Four Number Ones in 1970</h2>
{p("The Jackson 5 songs of 1970 are among the fastest starts in chart history.",
   "I Want You Back, ABC, The Love You Save and I'll Be There all reached number one on the Hot 100 that year.",
   f"This site's weekly chart data gives them {total_weeks} weeks at number one between them, the most of any act in 1970.",
   "Wikipedia says the Jackson 5 were the first recording act whose first four singles all reached number one.")}

{tbl("The four Jackson 5 number ones: weeks at number one and first week at the top, from this site's weekly Hot 100 data", ["Song", "Weeks at #1", "First Week at #1 Began", "Released"], one_rows)}

        <h3>What the Chart Numbers Say</h3>
{p(f"Ten of the {NUM[n]} Jackson 5 songs on this page reached the Hot 100's top ten.")}
        <ul>
          <li>I Want You Back, ABC, The Love You Save and I'll Be There all reached number one in 1970.</li>
          <li>Mama's Pearl, Never Can Say Goodbye and Dancing Machine all stalled at number two.</li>
          <li>Enjoy Yourself and Shake Your Body reached number six and number seven, under the name The Jacksons.</li>
          <li>Sugar Daddy reached number ten, the last top ten for the group until Dancing Machine nearly three years later, per Wikipedia.</li>
          <li>Dancing Machine ranks #{r_dm} on the 1974 Year-End Hot 100, the best year-end rank of any song here, ahead of I'll Be There at #{r_ibt}.</li>
        </ul>
{p('To see which groups charted the most, read the page on <a href="/blog/artists/70s-bands/">70s bands</a>, ranked by year-end hits.')}

        <h3>The UK Chart Told a Similar Story</h3>
{p(f"{NUM[len(uk_rows)].capitalize()} of these songs have a UK peak in the Wikipedia articles used for this page.",
   "I Want You Back did best, reaching number two in the UK.",
   "Mama's Pearl and Never Can Say Goodbye did much better in the US than in the UK.")}

{tbl("Jackson 5 songs of the 70s with a UK Singles Chart peak next to the Hot 100 peak (Wikipedia)", ["Song", "Hot 100 Peak", "UK Peak", "Released"], uk_rows)}

        <h2 id="origins">Gary, Indiana to Hitsville: How the Jackson 5 Began</h2>
{p("The story behind the Jackson 5 songs starts in Gary, Indiana.",
   "Wikipedia says the group formed in 1964 as the Jackson Brothers, with Jackie, Tito and Jermaine, managed by their father Joe.",
   "Marlon joined in August 1965, and Michael joined soon after.",
   "The average age of the five was 12 when they turned professional.",
   'To meet more voices from the decade, spin the <a href="/pages/random-artist-picker">Random Artist Picker</a>.')}

        <h3>The Motown Audition and The Corporation</h3>
{p("Bobby Taylor set up a Motown audition after the brothers opened for his group in July 1968.",
   "The audition took place on July 23, 1968, and Berry Gordy signed them to a first year-long contract on July 26.",
   "Motown's publicity team, led by Suzanne de Passe, then presented the group as discovered by Diana Ross.",
   "Wikipedia describes that as a PR strategy, not an established fact.")}
{p("In September 1969, Gordy set up The Corporation, a writing and production team, to write exclusively for the group.",
   "Wikipedia says The Corporation made most of their hit singles before the team split in 1973.")}
{band_pic}
        <p class="post-img-caption">The Jackson 5 in a 1974 publicity portrait.</p>
        <p class="post-img-caption">Image credit: Photo by The Jackson 5, public domain in the United States, via Wikimedia Commons.</p>

        <h2 id="number-ones">The Four Number Ones: I Want You Back, ABC, The Love You Save and I'll Be There</h2>
{p("The four Jackson 5 number ones came out between October 1969 and August 1970.",
   "The first three were written by The Corporation, and the fourth by Berry Gordy and three co-writers.")}

        <h3>I Want You Back</h3>
{p("I Want You Back came out in October 1969, and it was written by The Corporation.",
   "It was recorded between July and September 1969 at The Sound Factory in Los Angeles, and 11-year-old Michael Jackson sang lead.",
   "Wikipedia says the song was first meant for Gladys Knight and the Pips, then for Diana Ross, under the working title I Wanna Be Free.",
   "It reached number one on the Hot 100 dated January 31, 1970, and it was number one on the soul chart for four weeks.")}
{p(f"It ranks #{rk['I Want You Back']} on the 1970 Year-End Hot 100.",
   "It reached number two in the UK, and the RIAA certified it Platinum.",
   "Rolling Stone ranks it number 104 on its list of the 500 greatest songs, and it entered the Grammy Hall of Fame in 1999.")}
{p("The group's first TV appearance was on The Hollywood Palace on October 18, 1969.",
   "They sang it on The Ed Sullivan Show on December 14, 1969.")}

        <h3>ABC</h3>
{p("ABC was released on February 24, 1970, and it was recorded in December 1969.",
   "It reached number one on the Hot 100 for two weeks in April 1970, and number eight in the UK.",
   f"It ranks #{rk['ABC']} on the 1970 Year-End Hot 100.",
   "The Grammy Hall of Fame inducted it in 2016, and Sigala interpolated it in the 2015 single Easy Love.")}

        <h3>The Love You Save</h3>
{p("The Love You Save was released on May 13, 1970, and it was recorded in March 1970 at Hitsville West in Los Angeles.",
   "It reached number one on the Hot 100 for two weeks, and it spent six weeks at number one on the soul chart.",
   f"It ranks #{rk['The Love You Save']} on the 1970 Year-End Hot 100, and it reached number seven in the UK.")}

        <h3>I'll Be There</h3>
{p("I'll Be There was released on August 28, 1970, and it was written by Berry Gordy, Hal Davis, Bob West and Willie Hutch.",
   "Michael and Jermaine Jackson shared the lead vocal, and it was recorded in June 1970 at Hitsville West.",
   "It spent five weeks at number one on the Hot 100, from October 17 to November 14, 1970.",
   f"It ranks #{r_ibt} on the 1970 Year-End Hot 100, and it reached number four in the UK.")}
{p("Wikipedia says it replaced I Heard It Through the Grapevine as the most successful Motown single in the US.",
   "It held that record until 1981.",
   "Mariah Carey and Trey Lorenz took their 1992 MTV Unplugged cover of it to number one on the Hot 100.")}

        <h2 id="after-number-ones">After the Number Ones: Mama's Pearl, Never Can Say Goodbye and Sugar Daddy</h2>
{p("The next two singles came within one place of a fifth number one.",
   "Mama's Pearl and Never Can Say Goodbye both stalled at number two.")}

        <h3>Mama's Pearl</h3>
{p("Mama's Pearl was released on January 7, 1971, from Third Album, and The Corporation wrote and produced it.",
   "It reached number two on the Hot 100 for two weeks, behind One Bad Apple by The Osmonds.",
   f"It ranks #{r_mp} on the 1971 Year-End Hot 100, and it reached number two on the soul chart.")}
{p("It was first titled Guess Who's Making Whoopie (with Your Girlfriend).",
   "Wikipedia says producer Deke Richards reportedly changed the title and lyrics to protect Michael Jackson's youthful image.")}

        <h3>Never Can Say Goodbye</h3>
{p("Clifton Davis wrote Never Can Say Goodbye, and Wikipedia says it was originally written for the Supremes.",
   "The Jackson 5 version was released on March 16, 1971, and it reached number two on the Hot 100 for three weeks, behind Joy to the World by Three Dog Night.",
   "It was number one on the soul chart, and it reached number 33 in the UK.",
   f"It ranks #{rk['Never Can Say Goodbye']} on the 1971 Year-End Hot 100.")}
{p("Wikipedia says it sold 1.2 million copies in its first week.",
   "Clifton Davis once sang a bit of it on The Hollywood Squares, and when he was asked who wrote it, he answered, I did.")}
{p("Gloria Gaynor's disco version in 1974 reached number nine on the Hot 100 and number one on the first Billboard dance chart.",
   "Isaac Hayes reached number 22 with his 1971 cover.",
   'See the page on <a href="/blog/genres/disco-music-of-the-70s/">70s disco music</a> for more of that sound.')}

        <h3>Sugar Daddy</h3>
{p("Sugar Daddy was released on November 23, 1971, and it reached number ten on the Hot 100 and number three on the soul chart.",
   "The Corporation wrote and produced it, and Michael and Jermaine Jackson shared the lead.",
   "Wikipedia says it was recorded between April and October 1971.",
   "It is on no 1970s year-end list, so its peak above is a weekly peak only.")}

        <h2 id="window-years">1972: Little Bitty Pretty One and Lookin' Through the Windows</h2>
{p("By 1972, the Jackson 5 songs were still on the radio, but the chart peaks had slipped below the top ten.",
   "Two singles from the album Lookin' Through the Windows show the group in that more settled phase.")}

        <h3>Little Bitty Pretty One</h3>
{p("Little Bitty Pretty One was released on April 4, 1972, and it reached number 13 on the Hot 100.",
   "It was a cover, and Wikipedia says Bobby Day wrote it and first recorded it in 1957.",
   "Thurston Harris made it a hit the same year, with number six on the best sellers chart and number two on the R&B chart.",
   "Mel Larson and Jerry Marcellino produced the Jackson 5 version, which runs 2:22.")}

        <h3>Lookin' Through the Windows</h3>
{p("Clifton Davis wrote Lookin' Through the Windows too, and Hal Davis produced it.",
   "It was released on June 23, 1972, as the second single and title track of the album.",
   "It reached number 16 on the Hot 100 and number five on the soul chart.",
   'Test your memory of the decade with the <a href="/pages/70s-trivia-quiz">70s Music Trivia Quiz</a>.')}

        <h2 id="dancing-machine">Dancing Machine and I Am Love: The Last Motown Hits</h2>
{p("Dancing Machine brought the Jackson 5 back to the top of the chart in 1974.",
   "Wikipedia says it was the group's first top ten since Sugar Daddy, nearly three years earlier.")}

        <h3>Dancing Machine</h3>
{p("Dancing Machine was released on February 19, 1974, and Hal Davis, Don Fletcher and Dean Parks wrote it.",
   "It was recorded for G.I.T.: Get It Together, and it became the title track of the 1974 album Dancing Machine.",
   "It reached number two on the Hot 100, behind The Streak by Ray Stevens, and number one on the soul chart.",
   f"It ranks #{rk['Dancing Machine']} on the 1974 Year-End Hot 100, and the RIAA certified it Gold.")}
{p("Michael Jackson performed the robot dance on Soul Train on October 27, 1973.",
   "Wikipedia says it was fully caught on camera.",
   "The song earned a Grammy nomination at the 1975 awards, and it lost to Tell Me Something Good by Rufus and Chaka Khan.")}

        <h3>I Am Love</h3>
{p("I Am Love was released on December 23, 1974, and it was recorded in June 1974 at Hitsville West.",
   "It reached number 15 on the Hot 100 and number three on the soul chart.",
   "Wikipedia calls it the group's last top 20 hit.",
   "The full version runs 7:30, with Part I at 5:31 and Part II at 3:01.")}
{p("The first half is a soul ballad led by Jermaine, and the second half is a funk dance anthem led mostly by Michael.")}

        <h2 id="the-jacksons">From Jackson 5 to The Jacksons: Enjoy Yourself and Shake Your Body</h2>
{p("Wikipedia says Joe Jackson signed the group with Epic Records in June 1975.",
   "The brothers had learned they earned 2.8% in royalties at Motown, against 20% at Epic.",
   "Jermaine stayed at Motown after marrying Hazel Gordy, and Randy Jackson replaced him.",
   "Motown owned the name Jackson 5, so the group became The Jacksons.",
   "They stayed under Motown contract until March 1976.")}

        <h3>Enjoy Yourself</h3>
{p("Enjoy Yourself was released on October 22, 1976, on Epic and Philadelphia International Records.",
   "Gamble and Huff wrote and produced it at Sigma Sound Studios in Philadelphia, and Michael and Jackie Jackson sang lead.",
   "It was the first single after the group left Motown, and the first to feature Randy.",
   f"It reached number six on the Hot 100 and number two on the soul chart, and it ranks #{rk['Enjoy Yourself']} on the 1977 Year-End Hot 100.")}

        <h3>Shake Your Body (Down to the Ground)</h3>
{p("Michael and Randy Jackson wrote Shake Your Body, and it was released on January 18, 1979, from the album Destiny.",
   "Wikipedia says it was first demoed as Shake a Body.",
   "It reached number seven on the Hot 100 in May 1979, number three on the soul chart and number four in the UK.",
   f"It ranks #{rk['Shake Your Body (Down to the Ground)']} on the 1979 Year-End Hot 100, and the RIAA certified it Platinum.")}

        <h3>The Solo Years Begin</h3>
{p("This site's weekly chart data also shows two number ones for Michael Jackson alone.",
   "Ben reached number one in October 1972, for one week, and Don't Stop 'Til You Get Enough did the same in October 1979.",
   'To compare, the page on <a href="/blog/artists/marvin-gaye/">Marvin Gaye</a> tells another Motown story.')}

        <h2 id="who-wrote-what">Who Wrote and Released Each of the Jackson 5 Songs</h2>
{p(f"The table lists when each of the {NUM[n]} songs was released, on which album, and under which name.",
   "The Corporation wrote the early hits, and later songs came from other writers and producers.")}

{tbl("Jackson 5 songs of the 70s: release date, album and billing (Wikipedia)", ["Song", "Released", "Album", "Billed As"], album_rows)}

{tbl("Jackson 5 songs of the 70s ranked by Hot 100 peak, with release date (Wikipedia)", ["Song", "Hot 100 Peak", "Released"], us_rows)}

        <h3>Keep Exploring</h3>
{p("Jackson 5 songs turned a family act from Gary into the defining pop group of 1970.",
   "Four reached number one, and ten reached the top ten.",
   'The page on <a href="/blog/artists/carpenters-songs/">Carpenters songs</a> covers another brother and sibling act at the top of the chart.')}

        <h2 id="sources">Sources</h2>
{p("Year-end ranks come from this site's own Billboard data, described on the <a href='/about/methodology/'>methodology page</a>.",
   'Every list on <a href="/">Music of the 70s</a> plays inside the page.',
   "Peaks, dates and stories behind the Jackson 5 songs above can be checked against these outside sources:")}
        <ul>
          <li><a href="https://en.wikipedia.org/wiki/The_Jackson_5" rel="noopener">Wikipedia: The Jackson 5</a> and <a href="https://en.wikipedia.org/wiki/The_Jackson_5_discography" rel="noopener">its discography</a> for the group history, singles and chart peaks.</li>
          <li><a href="https://en.wikipedia.org/wiki/I_Want_You_Back_(Jackson_5_song)" rel="noopener">Wikipedia: I Want You Back</a>, <a href="https://en.wikipedia.org/wiki/ABC_(The_Jackson_5_song)" rel="noopener">ABC</a> and <a href="https://en.wikipedia.org/wiki/The_Love_You_Save" rel="noopener">The Love You Save</a> for the early number ones.</li>
          <li><a href="https://en.wikipedia.org/wiki/I%27ll_Be_There_(Jackson_5_song)" rel="noopener">Wikipedia: I'll Be There</a> and <a href="https://en.wikipedia.org/wiki/Mama%27s_Pearl" rel="noopener">Mama's Pearl</a> for Third Album.</li>
          <li><a href="https://en.wikipedia.org/wiki/Never_Can_Say_Goodbye" rel="noopener">Wikipedia: Never Can Say Goodbye</a> and <a href="https://en.wikipedia.org/wiki/Sugar_Daddy_(The_Jackson_5_song)" rel="noopener">Sugar Daddy</a> for 1971.</li>
          <li><a href="https://en.wikipedia.org/wiki/Little_Bitty_Pretty_One" rel="noopener">Wikipedia: Little Bitty Pretty One</a> and <a href="https://en.wikipedia.org/wiki/Lookin%27_Through_the_Windows_(song)" rel="noopener">Lookin' Through the Windows</a> for 1972.</li>
          <li><a href="https://en.wikipedia.org/wiki/Dancing_Machine" rel="noopener">Wikipedia: Dancing Machine</a> and <a href="https://en.wikipedia.org/wiki/I_Am_Love_(Jackson_5_song)" rel="noopener">I Am Love</a> for 1974.</li>
          <li><a href="https://en.wikipedia.org/wiki/Enjoy_Yourself_(The_Jacksons_song)" rel="noopener">Wikipedia: Enjoy Yourself</a> and <a href="https://en.wikipedia.org/wiki/Shake_Your_Body_(Down_to_the_Ground)" rel="noopener">Shake Your Body (Down to the Ground)</a> for the Epic years.</li>
        </ul>

        <section class="faq-block" id="faq">
          <h2>Frequently Asked Questions</h2>
{faq_html}
        </section>'''

    related = [
        ("marvin-gaye-1973-publicity", "Artists", "Marvin Gaye: The Party Tape That Ended Up in Federal Court", "/blog/artists/marvin-gaye/",
         "Another Motown story, from Hitsville to the Let's Get It On sessions.", "Marvin Gaye in a 1973 publicity photo"),
        ("carpenters-1972", "Artists", "Carpenters Songs: 11 Hits Played, 3 at Number One", "/blog/artists/carpenters-songs/",
         "Another sibling act, with every Carpenters hit playable.", "The Carpenters in 1972"),
        ("70s-bands", "Artists", "70s Bands: The Biggest Groups of the Decade, by the Charts", "/blog/artists/70s-bands/",
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
      {{"@type": "ListItem", "position": 4, "name": "Jackson 5 Songs", "item": "{URL}"}}
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
        Jackson 5 Songs
      </nav>

      <article class="section seo-content">
        <h1>{TITLE}</h1>

        <p class="post-byline">By <a href="https://musicofthe70s.net/about/author/">Charlie</a> &middot; Published {PUBLISHED.strftime('%B')} {PUBLISHED.day}, {PUBLISHED.year}</p>
        <p class="jump-to-list"><a class="btn-primary jump-btn" href="#jackson-5-songs-list">&#9654; Jump to the playable list</a></p>

        <p class="post-intro">Jackson 5 songs ruled the Hot 100 in 1970, when four of them reached number one in a single year.</p>
        <p class="post-intro">This page plays {NUM[n]} of them, from I Want You Back to Shake Your Body.</p>
        <p class="post-intro">I'll Be There spent five weeks at number one, and Dancing Machine got to number two in 1974.</p>
        <p class="post-intro">The Corporation wrote the early hits, and a young Michael Jackson sang them.</p>
        <p class="post-intro">Press Play on every hit below, then read the story behind each one.</p>

{feat_pic}
        <p class="post-img-caption">The Jackson 5 in a CBS Television publicity photo, 1972.</p>
        <p class="post-img-caption">Image credit: Photo by CBS Television, public domain in the United States, via Wikimedia Commons.</p>

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
