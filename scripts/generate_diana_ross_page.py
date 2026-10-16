#!/usr/bin/env python3
"""Build the Diana Ross Songs Artists post (blog/artists/diana-ross-songs/index.html).

Data: data/radio/radio-songs.json (six Diana Ross rows of the 1970, 1973, 1974, 1976 and 1979 Year-End Hot 100, each with
a YouTube ID), data/billboard/hot100_weekly.json (four Hot 100 number ones in the site's 1970-1979 weekly data: Ain't No
Mountain High Enough, Touch Me in the Morning, Theme from Mahogany and Love Hangover), data/billboard/beyond_year_end.json
(six further singles on the weekly Hot 100 but on no 1970s year-end list: Reach Out and Touch, Remember Me, Surrender,
You're a Special Part of Me, Last Time I Saw Him and Gettin' Ready for Love; peaks and Topic YouTube IDs checked).
Year-End Rank is the year-end rank, never a peak. Hot 100 peaks, release dates, writers and story facts come from the
linked Wikipedia articles and the Diana Ross discography article, checked 2026-10-16, and are credited to Wikipedia.
The site JSON's fun_fact and trivia text for the artist is not used (it gives Touch Me in the Morning two weeks at
number one, and the weekly data and Wikipedia's chart table give one).

Run: python3 scripts/generate_diana_ross_page.py
"""
import html
import json
from datetime import date

from genre_page_common import ROOT, read, play_button, write
from generate_country_page import p, tbl, pic

SLUG = "diana-ross-songs"
PAGE = f"blog/artists/{SLUG}/"
URL = f"https://musicofthe70s.net/{PAGE}"
IMG = "diana-ross-1976"
IMG2 = "diana-ross-mahogany-1975"
CHART = "diana-ross-peaks"
PUBLISHED = date(2026, 10, 16)
ARTIST = "Diana Ross"
NUM = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
       10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen"}

REACH, MOUNTAIN, REMEMBER, SURRENDER = "Reach Out and Touch (Somebody's Hand)", "Ain't No Mountain High Enough", "Remember Me", "Surrender"
TOUCH, SPECIAL, LAST, MISTAKE = "Touch Me in the Morning", "You're a Special Part of Me", "Last Time I Saw Him", "My Mistake (Was to Love You)"
MAHOGANY, HANGOVER, READY, BOSS = "Theme from Mahogany (Do You Know Where You're Going To)", "Love Hangover", "Gettin' Ready for Love", "The Boss"
AS = "Nickolas Ashford and Valerie Simpson"

# title -> (release year, Hot 100 peak, released text, album it first appeared on, written by)
# Every value read from the song's Wikipedia article or the Diana Ross discography article, checked 2026-10-16.
INFO = {
    REACH: (1970, 20, "April 1970", "Diana Ross (1970)", AS),
    MOUNTAIN: (1970, 1, "July 19, 1970", "Diana Ross (1970)", AS),
    REMEMBER: (1970, 16, "December 8, 1970", "Surrender", AS),
    SURRENDER: (1971, 38, "July 6, 1971", "Surrender", AS),
    TOUCH: (1973, 1, "May 3, 1973", "Touch Me in the Morning", "Ron Miller and Michael Masser"),
    SPECIAL: (1973, 12, "September 1973", "Diana &amp; Marvin", "Harold Johnson, Andrew Porter and Greg Wright"),
    LAST: (1973, 14, "December 6, 1973", "Last Time I Saw Him", "Michael Masser and Pam Sawyer"),
    MISTAKE: (1974, 19, "February 1974", "Diana &amp; Marvin", "Gloria Jones and Pam Sawyer"),
    MAHOGANY: (1975, 1, "September 24, 1975", "Mahogany soundtrack and Diana Ross (1976)", "Michael Masser and Gerry Goffin"),
    HANGOVER: (1976, 1, "March 16, 1976", "Diana Ross (1976)", "Marilyn McLeod and Pam Sawyer"),
    READY: (1977, 27, "October 16, 1977", "Baby It's Me", "Tom Snow and Franne Golde"),
    BOSS: (1979, 19, "May 22, 1979", "The Boss", AS),
}
ORDER = list(INFO)
BEYOND = {REACH, REMEMBER, SURRENDER, SPECIAL, LAST, READY}
YE_SET = {MOUNTAIN, TOUCH, MISTAKE, MAHOGANY, HANGOVER, BOSS}
SHORT = {MAHOGANY: "Theme from Mahogany"}

# Hot 100 singles from the discography that are not on the playable list (peak 100 or better)
OTHERS = [("Reach Out I'll Be There", 1971, 29), ("I'm Still Waiting", 1971, 63), ("Good Morning Heartache", 1972, 34),
          ("Sleepin'", 1974, 70), ("Don't Knock My Love (with Marvin Gaye)", 1974, 46),
          ("One Love in My Lifetime", 1976, 25), ("I Thought It Took a Little Time (But Today I Fell in Love)", 1976, 47),
          ("Your Love Is So Good for Me", 1978, 49), ("You Got It", 1978, 49),
          ("Ease On down the Road (with Michael Jackson)", 1978, 41)]


def main():
    radio = json.loads(read(ROOT / "data/radio/radio-songs.json"))
    weekly = json.loads(read(ROOT / "data/billboard/hot100_weekly.json"))
    beyond = {s["title"]: s for s in json.loads(read(ROOT / "data/billboard/beyond_year_end.json"))["songs"]
              if s["page"] == PAGE}

    ye = {}
    for s in radio:
        if s["artistId"] in ("diana-ross", "diana-ross-marvin-gaye") and s.get("youtube_id"):
            title = next(t for t in INFO if t.lower() == s["title"].lower())
            ye[title] = s
    assert set(ye) == YE_SET, set(ye) ^ YE_SET
    assert set(beyond) == BEYOND, set(beyond)
    for t in BEYOND:
        assert beyond[t]["weekly_peak"] == INFO[t][1], t
        assert beyond[t]["released"] == INFO[t][0], t
    for t, s in ye.items():
        assert s["year"] in (INFO[t][0], INFO[t][0] + 1), (t, s["year"])
        assert s["billboard_peak"] == s["rank"], t

    # weekly number ones by the artist in the site's own 1970-1979 data
    wk = {}
    for yr in weekly:
        for w in weekly[yr]:
            if w["artist"] == ARTIST:
                wk.setdefault(w["title"], []).append(w)
    assert set(wk) == {MOUNTAIN, TOUCH, MAHOGANY, HANGOVER}, set(wk)
    assert [w["week_start"] for w in wk[MOUNTAIN]] == ["1970-09-19", "1970-09-26", "1970-10-03"]
    assert [w["week_start"] for w in wk[TOUCH]] == ["1973-08-18"]
    assert [w["week_start"] for w in wk[MAHOGANY]] == ["1976-01-24"]
    assert [w["week_start"] for w in wk[HANGOVER]] == ["1976-05-29", "1976-06-05"]
    weeks_total = 3 + 1 + 1 + 2
    assert weeks_total == 7

    rk = {t: ye[t]["rank"] for t in ye}
    yr_of = {t: ye[t]["year"] for t in ye}
    n = len(INFO)
    assert n == 12
    top_ten = [t for t in INFO if INFO[t][1] <= 10]
    assert len(top_ten) == 4, top_ten
    top_twenty = [t for t in INFO if INFO[t][1] <= 20]
    assert len(top_twenty) == 10, top_twenty
    yt = {t: (ye[t]["youtube_id"] if t in ye else beyond[t]["youtube_id"]) for t in INFO}
    who = {t: (ye[t]["artist"] if t in ye else beyond[t]["artist"]) for t in INFO}

    rows = []
    for t in ORDER:
        y, pk, rel, alb, wr = INFO[t]
        ye_year = yr_of[t] if t in ye else ""
        ye_rank = rk[t] if t in ye else ""
        rows.append(f'              <tr><td class="ohw-listen">{play_button(yt[t], t, who[t])}</td>'
                    f'<td class="ohw-song">{html.escape(t)}</td>'
                    f'<td>{y}</td><td>{ye_year}</td><td>{ye_rank}</td><td>{pk}</td></tr>')

    peak_rows = sorted(([html.escape(t), INFO[t][1], INFO[t][2]] for t in ORDER), key=lambda r: (r[1], r[0]))
    album_rows = [[html.escape(t), INFO[t][2], INFO[t][3], html.escape(INFO[t][4]).replace("&amp;amp;", "&amp;")] for t in ORDER]
    other_rows = [[html.escape(t), y, pk] for t, y, pk in sorted(OTHERS, key=lambda r: (r[1], r[2]))]

    faq = [
        ("How many number one songs did Diana Ross have in the 1970s?",
         ["Diana Ross had four Billboard Hot 100 number ones in the 1970s, according to Wikipedia.",
          "They were Ain't No Mountain High Enough, Touch Me in the Morning, Theme from Mahogany and Love Hangover.",
          "This site's weekly chart data gives them seven weeks at the top between them.",
          "Ain't No Mountain High Enough held the spot for three of those weeks."]),
        ("What was Diana Ross's first solo number one?",
         ["Ain't No Mountain High Enough was Diana Ross's first solo number one on the Billboard Hot 100, according to Wikipedia.",
          "Motown released it on July 19, 1970, and it held the top spot for three weeks in September and October 1970.",
          "Ashford and Simpson wrote it, and Marvin Gaye and Tammi Terrell took their version to number 19 in 1967."]),
        ("Who wrote Love Hangover?",
         ["Marilyn McLeod and Pam Sawyer wrote Love Hangover, and Hal Davis produced it, according to Wikipedia.",
          "Motown released it as a single on March 16, 1976.",
          "It reached number one on May 29, 1976.",
          "That week Casey Kasem said on American Top 40 that Ross had broken the record for most number ones by a female vocalist."]),
        ("Did Diana Ross sing Touch Me in the Morning with Marvin Gaye?",
         ["No, Touch Me in the Morning was a solo single written by Ron Miller and Michael Masser, according to Wikipedia.",
          "Motown released it on May 3, 1973, and it became her second solo number one.",
          "Her duets with Marvin Gaye came from the album Diana and Marvin, and they included You're a Special Part of Me and My Mistake."]),
        ("When did Diana Ross leave the Supremes?",
         ["Diana Ross made her final appearance with the Supremes at the Frontier Hotel in Las Vegas on January 14, 1970, according to Wikipedia.",
          "She released her debut solo album in May 1970.",
          "Its first single, Reach Out and Touch (Somebody's Hand), peaked at number 20 on the Hot 100.",
          "The second, Ain't No Mountain High Enough, went to number one."]),
    ]
    for q, a in faq:
        wc = len(" ".join(a).split())
        assert 40 <= wc <= 70, (q, wc)
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": " ".join(a)}} for q, a in faq]},
        indent=2, ensure_ascii=False)
    faq_ld = "\n".join("  " + l for l in faq_ld.split("\n"))
    faq_html = "\n".join(
        f'          <div class="faq-item">\n            <h3>{html.escape(q)}</h3>\n' + "\n".join(f"            <p>{html.escape(l)}</p>" for l in a) + "\n          </div>"
        for q, a in faq).replace("&#x27;", "'")

    TITLE = f"Diana Ross Songs: {n} Hits Played, 4 at No. 1"
    desc = (f"Diana Ross songs of the 70s, all {n} playable: Ain't No Mountain High Enough, Love Hangover and more. "
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
    "image": "https://musicofthe70s.net/images/blog/{IMG}-800w.jpg",
    "mainEntityOfPage": "{URL}"
  }}'''

    toc = [("diana-ross-songs-list", f"Diana Ross Songs: Play All {n} Hits"),
           ("by-the-numbers", "Diana Ross Songs on the Charts: Four Number Ones"),
           ("origins", "From the Supremes to Solo: Where the Diana Ross Songs Began"),
           ("year-1970-71", "1970 and 1971: Reach Out and Touch, Ain't No Mountain High Enough, Remember Me and Surrender"),
           ("year-1973-74", "1973 and 1974: Touch Me in the Morning and the Marvin Gaye Duets"),
           ("year-1975-76", "1975 and 1976: Theme from Mahogany and Love Hangover"),
           ("year-1977-79", "1977 to 1979: Gettin' Ready for Love and The Boss"),
           ("other-singles", "The Other Diana Ross Singles on the 70s Hot 100"),
           ("beyond-the-charts", "Beyond the Charts: Films, Awards and Later Honors"),
           ("who-wrote-what", "Who Wrote and Released Each of the Diana Ross Songs"),
           ("sources", "Sources"), ("faq", "Frequently Asked Questions")]
    toc_html = "\n".join(f'            <li><a href="#{i}">{t}</a></li>' for i, t in toc)

    feat_pic = pic(IMG, "Diana Ross in a 1976 Motown publicity portrait, the singer behind the Diana Ross songs of the 70s",
                   "(max-width: 700px) 100vw, 420px", 800, 935, widths=(400, 800), lazy=False).replace(
        'class="post-featured-img"', 'class="post-featured-img" style="aspect-ratio:800/935;max-width:420px;width:100%;height:auto;margin:1.5rem auto"', 1)
    pic2 = pic(IMG2, "Anthony Perkins photographing Diana Ross on stone steps in a still from the 1975 Mahogany film trailer",
               "(max-width: 700px) 100vw, 800px", 800, 344, widths=(400, 800)).replace(
        "<img\n", '<img style="display:block;width:100%;max-width:800px;height:auto;margin:1.5rem auto;border-radius:8px"\n', 1)
    chart_pic = pic(CHART, "Lollipop chart of twelve Diana Ross songs by Hot 100 peak, from four number ones to Surrender at number 38",
                    "(max-width: 700px) 100vw, 800px", 800, 450, widths=(400, 800, 1200)).replace(
        "<img\n", '<img style="display:block;width:100%;max-width:800px;height:auto;margin:1.5rem auto;border-radius:8px"\n', 1)

    body = f'''        <h2 id="diana-ross-songs-list">Diana Ross Songs: Play All {n} Hits</h2>
{p(f"Here are {NUM[n]} hits from 1970 to 1979, from Reach Out and Touch to The Boss.",
   "Six sit on a Billboard Year-End Hot 100, and six more charted weekly without making a year-end list.",
   "Press Play on any row to watch it here, and tap a heading to sort.")}

        <div class="data-table-wrap scroll-list">
          <table class="data-table sortable-table" id="dianaRossSongsTable" data-inline-player>
            <caption>{n} Diana Ross songs of the 70s, with release year, Billboard Year-End Hot 100 rank and Hot 100 peak</caption>
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
{p("Released is the year each song came out as a single, per Wikipedia.",
   "Year-End List and Year-End Rank show which year-end list a song is on, and its rank there.",
   "A blank means it is on none.",
   "Hot 100 Peak is the weekly peak, from each song's Wikipedia article or the Diana Ross discography article.",
   "All four number ones are Hot 100 chart toppers in this site's weekly chart data.",
   "You're a Special Part of Me and My Mistake are duets with Marvin Gaye.")}

        <h2 id="by-the-numbers">Diana Ross Songs on the Charts: Four Number Ones</h2>
{p("The four number ones came in three separate bursts across the decade.",
   "Ain't No Mountain High Enough held the top spot for three weeks, starting September 19, 1970.",
   "Touch Me in the Morning did it for one week, starting August 18, 1973.",
   "Theme from Mahogany did it for one week, starting January 24, 1976.",
   "Love Hangover followed for two weeks, starting May 29, 1976.")}

{chart_pic}
        <p class="post-img-caption">Hot 100 peaks of the twelve hits on this page, per Wikipedia's song and discography articles.</p>

{tbl("Diana Ross songs of the 70s ranked by weekly Hot 100 peak, with release date (Wikipedia)", ["Song", "Hot 100 Peak", "Released"], peak_rows)}

        <h3>What the Chart Numbers Say</h3>
{p(f"Ten of the {NUM[n]} hits on this page reached the Hot 100's top 20.")}
        <ul>
          <li>Ain't No Mountain High Enough, Touch Me in the Morning, Theme from Mahogany and Love Hangover all reached number one, for seven weeks in this site's weekly data.</li>
          <li>You're a Special Part of Me, with Marvin Gaye, reached number 12, and Last Time I Saw Him reached number 14.</li>
          <li>Ain't No Mountain High Enough ranks #{rk[MOUNTAIN]} on the 1970 Year-End Hot 100, the highest of her six year-end songs.</li>
          <li>Touch Me in the Morning ranks #{rk[TOUCH]} on the 1973 list, and Love Hangover ranks #{rk[HANGOVER]} on the 1976 list.</li>
          <li>Theme from Mahogany ranks #{rk[MAHOGANY]} on the 1976 list, My Mistake ranks #{rk[MISTAKE]} on the 1974 list, and The Boss ranks #{rk[BOSS]} on the 1979 list.</li>
          <li>Wikipedia says she made twelve top ten singles in a fifteen-year span, and that six of them reached number one.</li>
        </ul>

        <h2 id="origins">From the Supremes to Solo: Where the Diana Ross Songs Began</h2>
{p("The Diana Ross songs of the 70s came from the lead singer of the best-charting female group in history.",
   "She was born on March 26, 1944, in Detroit, Michigan.",
   "At fifteen she joined the Primettes, who were renamed the Supremes in 1961.",
   "Berry Gordy made her the group's lead singer at the end of 1963.")}

        <h3>Twelve Supremes Number Ones and a Last Night in Las Vegas</h3>
{p("Wikipedia credits the Supremes with twelve Hot 100 number ones.",
   "Someday We'll Be Together was the last of them, and the final number one of the 1960s.",
   "Ross made her final appearance with the group at the Frontier Hotel in Las Vegas on January 14, 1970.",
   "She released her first solo album, Diana Ross, in May 1970.")}

        <h3>The Songwriters Who Built Her Solo Sound</h3>
{p("Ashford and Simpson wrote her first solo single and her first solo number one.",
   "Michael Masser wrote the ballads that carried her through 1973 and 1974.",
   "Masser, Ashford and Simpson, or Pam Sawyer wrote or co-wrote ten of the twelve hits on this page.",
   'Spin the dial on more voices from the decade with the <a href="/pages/random-artist-picker">Random Artist Picker</a>.')}

        <h2 id="year-1970-71">1970 and 1971: Reach Out and Touch, Ain't No Mountain High Enough, Remember Me and Surrender</h2>
{p("The first four Diana Ross songs on this page all came from the Ashford and Simpson team.")}

        <h3>Reach Out and Touch (Somebody's Hand)</h3>
{p("Reach Out and Touch (Somebody's Hand) was her debut solo single, released in April 1970.",
   "Ashford and Simpson wrote and produced it, and Paul Riser arranged it.",
   "Wikipedia says it carried a heavy gospel influence.",
   "It was one of the few songs she recorded to express her social conscience.")}
{p("It peaked at number 20 on the Hot 100, number 10 on the Cash Box Top 100 and number seven on the R&amp;B chart.",
   "Cash Box said she took a slow blues-waltz message ballad and turned it into something all her own.",
   "In concert she often had the whole crowd turn to their neighbors and reach out and touch their hands.",
   "She also sang it as the finale of the Nobel Peace Prize Concert in Oslo in 2008.")}

        <h3>Ain't No Mountain High Enough</h3>
{p("Ashford and Simpson wrote Ain't No Mountain High Enough in 1966.",
   "Marvin Gaye and Tammi Terrell took it to number 19 on the Hot 100 in 1967.",
   "In early 1970 the writers had Ross record it again, and she was apprehensive at first.",
   "The remake added spoken-word passages, strings, horns and a gospel-style backing chorus.")}
        <h3>The Record Berry Gordy Did Not Want to Release</h3>
{p("Wikipedia says Berry Gordy did not like the record when he first heard it.",
   "He hated the spoken-word passages and wanted it to begin with the climactic chorus.",
   "Radio stations then began editing their own versions and adding them to their playlists.",
   "That let Ashford and Simpson convince him to release an edited three-minute single.")}
{p("Motown released it on July 19, 1970, as the second single from her debut album.",
   "It reached number one on both the pop and R&amp;B charts, higher than the Gaye and Terrell version.",
   "This site's weekly data gives it three weeks at the top, starting September 19, 1970.",
   f"It ranks #{rk[MOUNTAIN]} on the 1970 Year-End Hot 100, and it earned her a Grammy nomination for Best Female Pop Vocal Performance.",
   'Its year-end company is on the page for <a href="/blog/years/top-songs-of-1970/">top songs of 1970</a>.')}

        <h3>Remember Me</h3>
{p("Remember Me was released on December 8, 1970, as the first single from her second album, Surrender.",
   "Ashford and Simpson wrote and produced it.",
   "It is told from the view of a spurned woman who asks an ex to remember the good she brought to his life.")}
{p("It peaked at number 16 on the Hot 100 and number 10 on the soul chart.",
   "Wikipedia calls it her third top 40 pop hit within a year.",
   "It reached number seven in the UK.")}

        <h3>Surrender</h3>
{p("Surrender was the third single from the album of the same name, released on July 6, 1971.",
   "Ashford and Simpson wrote and produced it, and the Funk Brothers played on it.",
   "It peaked at number 38 on the Hot 100 and number 16 on the R&amp;B chart.",
   "In the UK it reached number 10, her fourth straight top ten hit there.")}
{p("Her soul ballad I'm Still Waiting reached number one in the UK in 1971.",
   "Wikipedia calls it her first solo number one there.",
   "It stalled at number 63 on the Hot 100, so it sits in the table of other singles below.")}

        <h2 id="year-1973-74">1973 and 1974: Touch Me in the Morning and the Marvin Gaye Duets</h2>
{p("Lady Sings the Blues, her film debut, opened in October 1972 and earned her an Academy Award nomination.",
   "The next single returned her to number one.")}

        <h3>Touch Me in the Morning</h3>
{p("Touch Me in the Morning was written by Ron Miller and Michael Masser, and produced by Masser and Tom Baird.",
   "Motown released it on May 3, 1973, as the first single from the album of the same name.",
   "Masser said she pushed hard to get the vocal right and called it a draining experience.",
   "She recorded it in the early morning hours, as was her custom after she began raising her children.")}
        <h3>Her Second Solo Number One</h3>
{p("It reached number one on the Hot 100, her second solo chart-topper.",
   "This site's weekly data puts that in the week starting August 18, 1973, for one week.",
   "It also spent a week at number one on the adult contemporary chart, her first on that chart.",
   f"It ranks #{rk[TOUCH]} on the 1973 Year-End Hot 100.")}
{p("Wikipedia says it stayed on the chart for 21 weeks, her longest run until 1980.",
   "Sherlie Matthews, Clydie King and Venetta Fields sang backing vocals, and Gene Page arranged it.",
   'Find more songs with the same late-night mood in the <a href="/pages/mood-song-matcher">Mood Song Matcher</a>.')}

        <h3>You're a Special Part of Me</h3>
{p("You're a Special Part of Me was a duet with her Motown label mate Marvin Gaye, released in September 1973.",
   "It came from their album Diana &amp; Marvin, and Berry Gordy produced it.",
   "Harold Johnson, Andrew Porter and Greg Wright wrote it.",
   "It reached number 12 on the Hot 100 and number four on the R&amp;B chart.")}
{p("Record World said the combination of the two voices was beautiful.",
   'More of his own story is on the page for <a href="/blog/artists/marvin-gaye/">Marvin Gaye</a>.')}

        <h3>Last Time I Saw Him</h3>
{p("Last Time I Saw Him was written by Michael Masser and Pam Sawyer.",
   "Motown released it on December 6, 1973, as the first single from the album of the same name.",
   "The narrator waved a man off on a Greyhound bus and has heard nothing for six months, so she sets out to find him.")}
{p("It peaked at number 14 on the Hot 100 in February 1974, her seventh top 40 hit.",
   "It spent three weeks at number one on the Easy Listening chart.",
   "Wikipedia says it was the biggest Easy Listening hit of 1974.",
   "Billboard called it a light romp in the Tony Orlando and Dawn style.")}
{p("Dottie West covered it for the country market, and her version reached number eight on the country chart in February 1974.")}

        <h3>My Mistake (Was to Love You)</h3>
{p("My Mistake (Was to Love You) was the second single from Diana &amp; Marvin, released in February 1974.",
   "Gloria Jones and Pam Sawyer wrote it, and Hal Davis produced it.",
   "It peaked at number 19 on the Hot 100 and number 15 on the R&amp;B chart.",
   f"It ranks #{rk[MISTAKE]} on the 1974 Year-End Hot 100.")}
{p("Sawyer also co-wrote Last Time I Saw Him and, two years later, Love Hangover.")}

        <h2 id="year-1975-76">1975 and 1976: Theme from Mahogany and Love Hangover</h2>
{p("1976 was the year the Diana Ross songs hit the top twice, and Casey Kasem noticed.")}

        <h3>Theme from Mahogany (Do You Know Where You're Going To)</h3>
{p("Michael Masser and Gerry Goffin wrote Theme from Mahogany.",
   "Thelma Houston recorded it first, in 1973.",
   "Ross cut it as the theme to her 1975 film Mahogany, and Motown released it on September 24, 1975.",
   "It was the lead single for both the film soundtrack and her album Diana Ross.")}
        <h3>Number One in January 1976</h3>
{p("It reached number one on the Hot 100, her third.",
   "This site's weekly data puts that in the week starting January 24, 1976, for one week.",
   f"It ranks #{rk[MAHOGANY]} on the 1976 Year-End Hot 100.")}
{p("Masser and Goffin received an Academy Award nomination for Best Original Song.",
   "Ross sang it at the 48th Academy Awards ceremony by satellite from Amsterdam.",
   "Mariah Carey later included it as a promotional single on international versions of her compilation #1's.")}
{pic2}
        <p class="post-img-caption">Anthony Perkins photographing Diana Ross in a still from the 1975 Mahogany film trailer.</p>
        <p class="post-img-caption">Image credit: Paramount Pictures, public domain, via Wikimedia Commons.</p>
        <h3>A Troubled Film Behind the Theme</h3>
{p("Wikipedia says the film was a troubled production.",
   "The original director, Tony Richardson, was fired, and Berry Gordy took over.",
   "Ross had designed the costumes herself.")}

        <h3>Love Hangover</h3>
{p("Marilyn McLeod and Pam Sawyer wrote Love Hangover, and Hal Davis produced it.",
   "Motown released it as a single on March 16, 1976.",
   "Davis had engineer Russ Terrana install a strobe light so that Ross would be in a disco mindset.",
   "As the song changed from ballad to uptempo, she hummed, laughed, danced and even imitated Billie Holiday.")}
        <h3>A Hangover Race Against the 5th Dimension</h3>
{p("The 5th Dimension released their own version of Love Hangover, and both versions entered the chart the same day.",
   "By the time Ross reached number one, the 5th Dimension had peaked at number 80.",
   "Hers reached number one on the Hot 100 on May 29, 1976, for two weeks in this site's weekly data.",
   f"It ranks #{rk[HANGOVER]} on the 1976 Year-End Hot 100.")}
        <h3>A Record Fourth Number One</h3>
{p("That week Casey Kasem reported on American Top 40 that Ross had broken the record for most number ones by a female vocalist.",
   "Her fourth passed Connie Francis, Helen Reddy, Roberta Flack and Cher, who each had three.",
   "It also earned a Grammy nomination for Best Female R&amp;B Vocal Performance.",
   'The beat behind it is explored in the page on <a href="/blog/genres/disco-music-of-the-70s/">70s disco music</a>.')}
{p("Janet Jackson sampled it on My Need in 1997, and Monica sampled it on The First Night in 1998.",
   "A 2020 remix by Eric Kupper reached number one on the Dance Club Songs chart.",
   "Wikipedia says that was the final number one single on that chart.")}

        <h2 id="year-1977-79">1977 to 1979: Gettin' Ready for Love and The Boss</h2>
{p("The last two Diana Ross songs on this page came after the decade's biggest run, and both went in new directions.")}

        <h3>Gettin' Ready for Love</h3>
{p("Gettin' Ready for Love was released on October 16, 1977, as the first single from Baby It's Me.",
   "Tom Snow and Franne Golde wrote it, and Richard Perry produced it.",
   "It reached number 27 on the Hot 100 and number eight on the adult contemporary chart.")}
{p("Wikipedia's personnel list includes Steve Lukather on guitar, Jeff Porcaro on drums and Tom Scott on the saxophone solo.",
   "Gene Page arranged the strings.",
   "In the UK it reached number 23.")}

        <h3>The Boss</h3>
{p("The Boss was written and produced by Ashford and Simpson.",
   "Motown released it on May 22, 1979, a day before the album of the same name.",
   "It reached number 19 on the Hot 100 and number 12 on the soul chart.",
   "It went to number one on the dance club chart.")}
{p("Wikipedia calls it her first top 20 pop hit since Love Hangover.",
   f"It ranks #{rk[BOSS]} on the 1979 Year-End Hot 100.",
   "The album gave her her first gold-certified album.",
   "She performed the song in the Macy's Thanksgiving Day Parade in November 1979.")}
{p("The next chapter was Diana in 1980, with Upside Down and I'm Coming Out.",
   "Those fall just outside this decade.")}

        <h2 id="other-singles">The Other Diana Ross Singles on the 70s Hot 100</h2>
{p("Not every one of the Diana Ross songs fit on the playable list.",
   "Wikipedia's discography shows ten more singles on the Hot 100 in the decade.",
   "Among them are I'm Still Waiting, which reached number one in the UK, and the Michael Jackson duet Ease On down the Road from The Wiz.")}

{tbl("Diana Ross singles on the 1970s Hot 100 that are not on the playable list (Wikipedia discography)", ["Single", "Released", "Hot 100 Peak"], other_rows)}

        <h2 id="beyond-the-charts">Beyond the Charts: Films, Awards and Later Honors</h2>
{p("The Diana Ross songs above sit beside a film career and a stack of honors.",
   "Wikipedia lists these milestones.")}
        <ul>
          <li>1972: Lady Sings the Blues, her film debut as Billie Holiday, brought an Academy Award nomination for Best Actress.</li>
          <li>1972: The Lady Sings the Blues soundtrack reached number one on the Billboard 200 for two weeks and sold two million copies.</li>
          <li>1974: She became the first African-American woman to co-host the Academy Awards.</li>
          <li>1975: Mahogany reunited her with her Lady Sings the Blues co-star Billy Dee Williams.</li>
          <li>1976: She launched her An Evening with Diana Ross tour, and its success earned her a Special Tony Award.</li>
          <li>1978: She played Dorothy in The Wiz, and Ease On down the Road with Michael Jackson earned a Grammy nomination.</li>
          <li>1988: The Supremes were inducted into the Rock and Roll Hall of Fame.</li>
        </ul>
{p("Wikipedia says she has sold more than 100 million records worldwide as a solo artist.",
   "Counting her time with the Supremes, she has 18 number one singles.",
   "Six of those came as a solo artist, with Upside Down and Endless Love still to come after this decade.")}

        <h2 id="who-wrote-what">Who Wrote and Released Each of the Diana Ross Songs</h2>
{p(f"The table lists the release date, first album and writers for each of the {NUM[n]} hits.",
   "Ashford and Simpson wrote five of them, and Pam Sawyer co-wrote three.")}

{tbl("Diana Ross songs of the 70s: release date, album and writers (Wikipedia)", ["Song", "Released", "First Appeared On", "Written By"], album_rows)}

        <h3>Keep Exploring</h3>
{p("These Diana Ross songs gave the decade four number ones and a long run of polished Motown hits.",
   "Ten of the twelve reached the top 20.",
   'Another act with a Motown start is covered on the page for <a href="/blog/artists/jackson-5-songs/">Jackson 5 songs</a>.')}

        <h2 id="sources">Sources</h2>
{p("Year-end ranks come from this site's own Billboard data, described on the <a href='/about/methodology/'>methodology page</a>.",
   'Every list on <a href="/">Music of the 70s</a> plays inside the page.',
   "Peaks, dates and stories behind the Diana Ross songs above can be checked against these outside sources:")}
        <ul>
          <li><a href="https://en.wikipedia.org/wiki/Diana_Ross" rel="noopener">Wikipedia: Diana Ross</a> and <a href="https://en.wikipedia.org/wiki/Diana_Ross_discography" rel="noopener">her discography</a> for the biography, honors, singles and chart peaks.</li>
          <li><a href="https://en.wikipedia.org/wiki/Reach_Out_and_Touch_(Somebody%27s_Hand)" rel="noopener">Wikipedia: Reach Out and Touch (Somebody's Hand)</a>, <a href="https://en.wikipedia.org/wiki/Ain%27t_No_Mountain_High_Enough" rel="noopener">Ain't No Mountain High Enough</a>, <a href="https://en.wikipedia.org/wiki/Remember_Me_(Diana_Ross_song)" rel="noopener">Remember Me</a> and <a href="https://en.wikipedia.org/wiki/Surrender_(Diana_Ross_song)" rel="noopener">Surrender</a> for 1970 and 1971.</li>
          <li><a href="https://en.wikipedia.org/wiki/Touch_Me_in_the_Morning_(song)" rel="noopener">Wikipedia: Touch Me in the Morning</a>, <a href="https://en.wikipedia.org/wiki/You%27re_a_Special_Part_of_Me" rel="noopener">You're a Special Part of Me</a>, <a href="https://en.wikipedia.org/wiki/Last_Time_I_Saw_Him_(song)" rel="noopener">Last Time I Saw Him</a> and <a href="https://en.wikipedia.org/wiki/My_Mistake_(Was_to_Love_You)" rel="noopener">My Mistake (Was to Love You)</a> for 1973 and 1974.</li>
          <li><a href="https://en.wikipedia.org/wiki/Theme_from_Mahogany_(Do_You_Know_Where_You%27re_Going_To)" rel="noopener">Wikipedia: Theme from Mahogany</a> and <a href="https://en.wikipedia.org/wiki/Love_Hangover" rel="noopener">Love Hangover</a> for 1975 and 1976.</li>
          <li><a href="https://en.wikipedia.org/wiki/Gettin%27_Ready_for_Love" rel="noopener">Wikipedia: Gettin' Ready for Love</a> and <a href="https://en.wikipedia.org/wiki/The_Boss_(Diana_Ross_song)" rel="noopener">The Boss</a> for 1977 and 1979.</li>
        </ul>

        <section class="faq-block" id="faq">
          <h2>Frequently Asked Questions</h2>
{faq_html}
        </section>'''


    related = [
        ("marvin-gaye-1973-publicity", "Artists", "Marvin Gaye: The Party Tape That Ended Up in Federal Court", "/blog/artists/marvin-gaye/",
         "Her duet partner on You're a Special Part of Me and My Mistake.", "Marvin Gaye in a 1973 publicity photo"),
        ("jackson-5-1972", "Artists", "Jackson 5 Songs: 13 Hits Played, 4 at Number One", "/blog/artists/jackson-5-songs/",
         "Another act that started out at Motown.", "The Jackson 5 in 1972"),
        ("gladys-knight-1974", "Artists", "Gladys Knight Songs: 12 Hits Played, 1 at Number One", "/blog/artists/gladys-knight-songs/",
         "Another Motown-era voice with a number one in the 70s.", "Gladys Knight in 1974"),
    ]

    cards = []
    for img, cat, title, href, blurb, alt in related:
        big = {"jackson-5-1972": 669, "gladys-knight-1974": 668}.get(img, 800)
        bigjpg = f"/images/blog/{img}-{big}w.jpg" if big != 800 else f"/images/blog/srcset/{img}-{big}w.jpg"
        cards.append(f'''            <div class="card post-card">
              <picture>
                <source type="image/webp" srcset="/images/blog/srcset/{img}-400w.webp 400w, /images/blog/srcset/{img}-{big}w.webp {big}w" sizes="(max-width: 700px) 100vw, 33vw">
                <img class="post-thumb" src="/images/blog/srcset/{img}-400w.jpg"
                  srcset="/images/blog/srcset/{img}-400w.jpg 400w, {bigjpg} {big}w"
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
  <meta property="og:image" content="https://musicofthe70s.net/images/blog/{IMG}-800w.jpg">
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
      {{"@type": "ListItem", "position": 4, "name": "Diana Ross Songs", "item": "{URL}"}}
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
        Diana Ross Songs
      </nav>

      <article class="section seo-content">
        <h1>{TITLE}</h1>

        <p class="post-byline">By <a href="https://musicofthe70s.net/about/author/">Charlie</a> &middot; Published {PUBLISHED.strftime('%B')} {PUBLISHED.day}, {PUBLISHED.year}</p>
        <p class="jump-to-list"><a class="btn-primary jump-btn" href="#diana-ross-songs-list">&#9654; Jump to the playable list</a></p>

        <p class="post-intro">Diana Ross songs turned a Supremes lead singer into a solo star with four Billboard Hot 100 number ones in the 1970s.</p>
        <p class="post-intro">Ain't No Mountain High Enough, Touch Me in the Morning, Theme from Mahogany and Love Hangover all got there.</p>
        <p class="post-intro">Between them they held the top spot for seven weeks.</p>
        <p class="post-intro">This page plays {NUM[n]} of her hits, from Reach Out and Touch in 1970 to The Boss in 1979.</p>
        <p class="post-intro">Ten of the twelve reached the Hot 100's top 20, and two are duets with Marvin Gaye.</p>
        <p class="post-intro">Press Play on every hit below, then read the story behind each one.</p>

{feat_pic}
        <p class="post-img-caption">Diana Ross in a 1976 Motown publicity photo.</p>
        <p class="post-img-caption">Image credit: Motown Records, public domain, via Wikimedia Commons.</p>

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
