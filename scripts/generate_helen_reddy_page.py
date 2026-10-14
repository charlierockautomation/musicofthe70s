#!/usr/bin/env python3
"""Build the Helen Reddy Songs Artists post (blog/artists/helen-reddy-songs/index.html).

Data: data/radio/radio-songs.json (seven Helen Reddy rows of the 1971-1977 Year-End Hot 100, each with a YouTube ID),
data/radio/number-one-videos.json (I Am Woman, a Hot 100 number one on no 1970s year-end list),
data/billboard/hot100_weekly.json (I Am Woman, Delta Dawn and Angie Baby, the three Hot 100 number ones in the site's
1970-1979 weekly data), data/billboard/beyond_year_end.json (five further singles on the weekly Hot 100 but on no 1970s
year-end list: Keep on Singing, Emotion, Ain't No Way to Treat a Lady, Somewhere in the Night and I Can't Hear You No
More, peaks and Topic-channel YouTube IDs checked).
Year-End Rank is the year-end rank, never a peak. Hot 100 peaks, release dates, writers and story facts come from the
linked Wikipedia articles, checked 2026-10-14, and are credited to Wikipedia on the page.
The site JSON's fun_fact and trivia text for Helen Reddy is not used.

Run: python3 scripts/generate_helen_reddy_page.py
"""
import html
import json
from datetime import date

from genre_page_common import ROOT, read, play_button, write
from generate_country_page import p, tbl, pic

SLUG = "helen-reddy-songs"
PAGE = f"blog/artists/{SLUG}/"
URL = f"https://musicofthe70s.net/{PAGE}"
IMG = "helen-reddy-1975"
IMG2 = "helen-reddy-1976"
CHART = "helen-reddy-peaks"
PUBLISHED = date(2026, 10, 14)
ARTIST = "Helen Reddy"
NUM = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
       10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen"}

IDK, IAW, PEACE, DELTA, LEAVE = "I Don't Know How to Love Him", "I Am Woman", "Peaceful", "Delta Dawn", "Leave Me Alone (Ruby Red Dress)"
KEEP, YOUME, ANGIE, EMO = "Keep on Singing", "You and Me Against the World", "Angie Baby", "Emotion"
AINT, SOME, ICANT, WORLD = "Ain't No Way to Treat a Lady", "Somewhere in the Night", "I Can't Hear You No More", "You're My World"

# title -> (release year, Hot 100 peak, released text, album, written by)
# Every value read from the song's Wikipedia article or the Helen Reddy discography article, checked 2026-10-14.
INFO = {
    IDK: (1971, 13, "January 1971", "I Don't Know How to Love Him", "Andrew Lloyd Webber and Tim Rice"),
    IAW: (1972, 1, "May 1972", "I Am Woman", "Helen Reddy and Ray Burton"),
    PEACE: (1973, 12, "Early 1973", "I Am Woman", "Kenny Rankin"),
    DELTA: (1973, 1, "June 1973", "Long Hard Climb", "Larry Collins and Alex Harvey"),
    LEAVE: (1973, 3, "October 1973", "Long Hard Climb", "Linda Laurie"),
    KEEP: (1974, 15, "February 1974", "Love Song for Jeffrey", "Danny Janssen and Bobby Hart"),
    YOUME: (1974, 9, "May 1974", "Love Song for Jeffrey", "Paul Williams and Kenny Ascher"),
    ANGIE: (1974, 1, "1974", "Free and Easy", "Alan O'Day"),
    EMO: (1975, 22, "January 1975", "Free and Easy", "Patti Dahlstrom and Véronique Sanson"),
    AINT: (1975, 8, "August 1975", "No Way to Treat a Lady", "Harriet Schock"),
    SOME: (1975, 19, "December 1975", "No Way to Treat a Lady", "Richard Kerr and Will Jennings"),
    ICANT: (1976, 29, "1976", "Music, Music", "Gerry Goffin and Carole King"),
    WORLD: (1977, 18, "April 4, 1977", "Ear Candy", "Umberto Bindi, Gino Paoli and Carl Sigman"),
}
ORDER = list(INFO)
BEYOND = {KEEP, EMO, AINT, SOME, ICANT}
YE_SET = {IDK, PEACE, DELTA, LEAVE, YOUME, ANGIE, WORLD}


def main():
    radio = json.loads(read(ROOT / "data/radio/radio-songs.json"))
    weekly = json.loads(read(ROOT / "data/billboard/hot100_weekly.json"))
    nones = json.loads(read(ROOT / "data/radio/number-one-videos.json"))
    beyond = {s["title"]: s for s in json.loads(read(ROOT / "data/billboard/beyond_year_end.json"))["songs"]
              if s["page"] == PAGE}

    ye = {}
    for s in radio:
        if s["artist"] == ARTIST and s.get("youtube_id"):
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
    iaw_vid = [v for v in nones["videos"] if v["artist"] == ARTIST and v["title"] == IAW]
    assert len(iaw_vid) == 1, iaw_vid
    assert iaw_vid[0]["embeddable"] and not iaw_vid[0]["madeForKids"]

    # weekly number ones by Helen Reddy in the site's own 1970-1979 data
    wk = {}
    for yr in weekly:
        for w in weekly[yr]:
            if w["artist"] == ARTIST:
                wk.setdefault(w["title"], []).append(w)
    assert set(wk) == {IAW, DELTA, ANGIE}, set(wk)
    wks = {t: len(v) for t, v in wk.items()}
    assert wks == {IAW: 1, DELTA: 1, ANGIE: 1}, wks
    assert all(w["weeks_at_number_one"] == 1 for v in wk.values() for w in v)
    wk_start = {t: v[0]["week_start"] for t, v in wk.items()}
    assert wk_start == {IAW: "1972-12-09", DELTA: "1973-09-15", ANGIE: "1974-12-28"}, wk_start

    rk = {t: ye[t]["rank"] for t in ye}
    yr_of = {t: ye[t]["year"] for t in ye}
    n = len(INFO)
    assert n == 13
    top_ten = [t for t in INFO if INFO[t][1] <= 10]
    assert len(top_ten) == 6, top_ten
    yt = {t: (ye[t]["youtube_id"] if t in ye else beyond[t]["youtube_id"] if t in beyond else iaw_vid[0]["youtube_id"])
          for t in INFO}

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
    first_rows = [
        [IDK, "Written for the 1970 Jesus Christ Superstar album, sung there as Mary Magdalene"],
        [PEACE, "Kenny Rankin, on his 1967 album Mind Dusters; Georgie Fame had the first hit in 1969"],
        [DELTA, "Alex Harvey, on his 1971 album Alex Harvey; Tanya Tucker had a 1972 country hit"],
        [LEAVE, "Linda Laurie, for MCA Records in summer 1973"],
        [KEEP, "Austin Roberts, who reached number 50 on the Hot 100 in 1973"],
        [EMO, "Véronique Sanson, as the French song Amoureuse; Kiki Dee cut an English version in 1973"],
        [AINT, "Harriet Schock, on her 1974 album Hollywood Town"],
        [ICANT, "Betty Everett, as I Can't Hear You, recorded May 13, 1964"],
        [WORLD, "Umberto Bindi, as the Italian ballad Il mio mondo in 1963; Cilla Black sang the English words in 1964"],
    ]

    faq = [
        ("What is Helen Reddy's most famous song?",
         ["Helen Reddy's most famous song is I Am Woman, which she co-wrote with Ray Burton.",
          "It reached number one on the Billboard Hot 100 in December 1972.",
          "Wikipedia calls it an enduring feminist anthem, and it won her the Grammy for Best Female Pop Vocal Performance.",
          "Delta Dawn and Angie Baby also reached number one."]),
        ("How many number one songs did Helen Reddy have?",
         ["Helen Reddy had three Hot 100 number ones, all between 1972 and 1975.",
          "They are I Am Woman, Delta Dawn and Angie Baby.",
          "This site's weekly chart data gives each one week at the top, starting December 9, 1972, September 15, 1973 and December 28, 1974.",
          "Wikipedia counts six top ten hits and 15 top 40 singles for her."]),
        ("Who wrote I Am Woman by Helen Reddy?",
         ["Helen Reddy and Ray Burton wrote I Am Woman, according to Wikipedia.",
          "Reddy said she wrote the lyric the day after she could not find a song that said what being a woman was about.",
          "Burton set it to music.",
          "She first recorded it for her 1971 debut album, then cut it again in April 1972 for the single."]),
        ("Did Helen Reddy write her own songs?",
         ["Helen Reddy wrote only one of the thirteen hits on this page, I Am Woman, and recorded songs by other writers for the rest.",
          "Her biggest hits came from Alex Harvey, Alan O'Day and Linda Laurie.",
          "Several began as songs by other singers, including Austin Roberts, Harriet Schock and Betty Everett.",
          "The table near the end lists every writer."]),
        ("What is Angie Baby by Helen Reddy about?",
         ["Angie Baby tells the story of a lonely teenage girl who escapes into her radio, according to Wikipedia.",
          "A neighbor boy comes to seduce her, the music overwhelms him, and he is pulled into the radio.",
          "Alan O'Day wrote it, and Reddy never gave her own reading of it.",
          "It reached number one on the Hot 100 on December 28, 1974."]),
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

    TITLE = f"Helen Reddy Songs: {n} Hits Played, 3 at Number One"
    desc = (f"Helen Reddy songs of the 70s, all {n} playable: I Am Woman, Delta Dawn, Angie Baby and more. "
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

    toc = [("helen-reddy-songs-list", f"Helen Reddy Songs: Play All {n} Hits"),
           ("by-the-numbers", "Helen Reddy Songs on the Charts: Three Number Ones, Six Top Tens"),
           ("origins", "From Melbourne to Capitol Records: How Helen Reddy Got Her Start"),
           ("year-1971-72", "1971 and 1972: I Don't Know How to Love Him and I Am Woman"),
           ("year-1973", "1973: Peaceful, Delta Dawn and Leave Me Alone (Ruby Red Dress)"),
           ("year-1974", "1974: Keep on Singing, You and Me Against the World and Angie Baby"),
           ("year-1975-77", "1975 to 1977: Emotion, Ain't No Way to Treat a Lady and More"),
           ("beyond-the-charts", "Beyond the Charts: Television, Film and Awards"),
           ("outside-writers", "Songs from Outside Writers: Who Sang Each Helen Reddy Song First"),
           ("who-wrote-what", "Who Wrote and Released Each of the Helen Reddy Songs"),
           ("sources", "Sources"), ("faq", "Frequently Asked Questions")]
    toc_html = "\n".join(f'            <li><a href="#{i}">{t}</a></li>' for i, t in toc)

    feat_pic = pic(IMG, "Black and white 1975 publicity portrait of Helen Reddy, the singer behind the Helen Reddy songs of the 70s, resting her head on one hand",
                   "(max-width: 700px) 100vw, 669px", 669, 758, widths=(400, 669), lazy=False).replace(
        'class="post-featured-img"', 'class="post-featured-img" style="aspect-ratio:669/758;max-width:669px;height:auto;margin:1.5rem auto"', 1)
    pic2 = pic(IMG2, "Helen Reddy smiling and holding a microphone while singing on stage at the White House in January 1976, the voice behind Delta Dawn and Angie Baby",
               "(max-width: 700px) 100vw, 400px", 630, 910, widths=(400, 630)).replace(
        "<img\n", '<img style="display:block;width:100%;max-width:400px;height:auto;margin:1.5rem auto;border-radius:8px"\n', 1)
    chart_pic = pic(CHART, "Lollipop chart of thirteen Helen Reddy songs by Hot 100 peak, from I Am Woman, Delta Dawn and Angie Baby at number one to I Can't Hear You No More at number 29",
                    "(max-width: 700px) 100vw, 800px", 800, 450, widths=(400, 800, 1200)).replace(
        "<img\n", '<img style="display:block;width:100%;max-width:800px;height:auto;margin:1.5rem auto;border-radius:8px"\n', 1)

    body = f'''        <h2 id="helen-reddy-songs-list">Helen Reddy Songs: Play All {n} Hits</h2>
{p(f"Here are {NUM[n]} hits from 1971 to 1977, from I Don't Know How to Love Him to You're My World.",
   "Seven sit on a Billboard Year-End Hot 100, and six more charted weekly without making a year-end list.",
   "Press Play on any row to watch it here, and tap a heading to sort.")}

        <div class="data-table-wrap scroll-list">
          <table class="data-table sortable-table" id="helenReddySongsTable" data-inline-player>
            <caption>{n} Helen Reddy songs of the 70s, with release year, Billboard Year-End Hot 100 rank and Hot 100 peak</caption>
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

        <h2 id="by-the-numbers">Helen Reddy Songs on the Charts: Three Number Ones, Six Top Tens</h2>
{p("The Helen Reddy songs of the 70s were hits on the pop charts and even bigger hits on the adult contemporary chart.",
   "Three reached number one on the Hot 100, and this site's weekly data gives each of them one week at the top.",
   "I Am Woman held the top spot in the week starting December 9, 1972.",
   "Delta Dawn held it in the week starting September 15, 1973.",
   "Angie Baby held it in the week starting December 28, 1974.")}

{chart_pic}
        <p class="post-img-caption">Hot 100 peaks of the thirteen hits on this page, from each song's Wikipedia article.</p>

{tbl("Helen Reddy songs of the 70s ranked by weekly Hot 100 peak, with release date (Wikipedia)", ["Song", "Hot 100 Peak", "Released"], peak_rows)}

        <h3>What the Chart Numbers Say</h3>
{p(f"Six of the {NUM[n]} hits on this page reached the Hot 100's top ten.")}
        <ul>
          <li>I Am Woman, Delta Dawn and Angie Baby reached number one in 1972, 1973 and 1974.</li>
          <li>Leave Me Alone (Ruby Red Dress) came closest after that, stopping at number three in 1973.</li>
          <li>Ain't No Way to Treat a Lady stopped at number eight and You and Me Against the World at number nine.</li>
          <li>Delta Dawn ranks #{rk[DELTA]} on the 1973 Year-End Hot 100, the best year-end rank of any song here, ahead of Angie Baby at #{rk[ANGIE]} on the 1975 list.</li>
          <li>Wikipedia counts 15 top 40 singles on the Hot 100 for Reddy, and 25 Adult Contemporary entries with eight number ones.</li>
        </ul>

        <h2 id="origins">From Melbourne to Capitol Records: How Helen Reddy Got Her Start</h2>
{p("The story behind the Helen Reddy songs starts in Melbourne, Australia.",
   "Wikipedia says she was born Helen Maxine Reddy on October 25, 1941, into a show business family.",
   "She arrived in New York in 1966 after winning a talent contest on the TV show Bandstand.")}

        <h3>Los Angeles and a Manager</h3>
{p("In 1968 she married Jeff Wald, who became her manager.",
   "The couple moved to Chicago, then to Los Angeles around 1969.",
   "Wald pressed Capitol Records executive Artie Mogull for a single.",
   "Capitol was the label under which her stardom developed.")}

        <h3>The B-Side That Started Everything</h3>
{p("Capitol chose I Believe in Music as the A-side, with I Don't Know How to Love Him on the flip.",
   "The A-side flopped, but Canadian disc jockeys championed the B-side.",
   "Wikipedia says it reached number 13 in Canada in June 1971.")}

        <h2 id="year-1971-72">1971 and 1972: I Don't Know How to Love Him and I Am Woman</h2>
{p("Her first two big Helen Reddy songs show how different her starting points were.",
   "One came from a rock opera, and the other she wrote herself.")}

        <h3>I Don't Know How to Love Him</h3>
{p("I Don't Know How to Love Him was released in January 1971, as the B-side of I Believe in Music.",
   "Andrew Lloyd Webber wrote the music and Tim Rice the lyrics, for the 1970 rock opera Jesus Christ Superstar.",
   "In the show, Mary Magdalene sings it.",
   "Larry Marks produced Reddy's version, and Wikipedia says she did not care for the song.",
   "She agreed to record it only as the flip side to the song she wanted to cut.")}
{p(f"It reached number 13 on the Hot 100 and number 12 on the Adult Contemporary chart, and it ranks #{rk[IDK]} on the 1971 Year-End Hot 100.",
   "Yvonne Elliman's cast version reached number 28 the same year.")}

        <h3>I Am Woman</h3>
{p("Reddy and Ray Burton wrote I Am Woman, the best known of all the Helen Reddy songs.",
   "Reddy said she could not find any songs that said what being a woman was about.",
   "She wrote the lyric the next day and gave it to Burton, who set it to music.",
   "Burton remembers it differently, and says he reworked some lines.",
   "Reddy insists he did not change a word.")}
{p("She first recorded it for her 1971 debut album.",
   "She cut it again on April 23, 1972, with Jay Senter producing, and Capitol released that version as a single in May 1972.")}
        <h3>From Barely Charting to Number One</h3>
{p("The single entered the Hot 100 at number 99 in the June 24, 1972 issue.",
   "It re-entered at number 87 in the September 16, 1972 issue, after listeners made it an anthem.",
   "It reached number one in the December 9, 1972 issue, and this site's weekly data gives it one week at the top.")}
        <ul>
          <li>Wikipedia says it was the first number one for Capitol since 1967.</li>
          <li>It was the first Billboard number one by an Australian-born artist.</li>
          <li>It reached number two on the Adult Contemporary chart, number two in Australia and number one in Canada.</li>
          <li>The RIAA certified it gold for one million units.</li>
        </ul>
        <h3>The Grammy and the Anthem</h3>
{p("It won the Grammy for Best Female Pop Vocal Performance at the 15th Annual Grammy Awards, in 1973.",
   "In her acceptance speech she thanked God, &quot;because She makes everything possible.&quot;",
   "Betty Friedan wrote that at a 1973 National Organization for Women gala in Washington, the song was played and women danced and sang along.")}
{p("An instrumental arrangement of it was the exit music for Kathryn Bigelow at the 82nd Academy Awards, after she won Best Director.",
   "Wikipedia says the 1972 recording joined the US National Recording Registry in 2025.")}

        <h2 id="year-1973">1973: Peaceful, Delta Dawn and Leave Me Alone (Ruby Red Dress)</h2>
{p("1973 gave Helen Reddy songs two more Hot 100 hits and her second number one.",
   f"Delta Dawn ranks #{rk[DELTA]} on the 1973 Year-End Hot 100, and Peaceful ranks #{rk[PEACE]}.")}

        <h3>Peaceful</h3>
{p("Peaceful was released in early 1973, as the follow-up to I Am Woman, from the album I Am Woman.",
   "Kenny Rankin wrote it, and Tom Catalano produced Reddy's version.",
   "Rankin first put it on his 1967 album Mind Dusters, Bobbie Gentry recorded it in 1968, and Georgie Fame had the first hit in 1969.")}
{p("Reddy's version reached number 12 on the Hot 100 in May 1973, and number two on the Adult Contemporary chart.",
   "It was number one for two weeks on Canada's Adult Contemporary chart.",
   'For a random song from the same decade, try the <a href="/pages/random-70s-song">Random 70s Song Generator</a>.')}

        <h3>Delta Dawn</h3>
{p("Delta Dawn was released in June 1973, from the album Long Hard Climb.",
   "Larry Collins and Alex Harvey wrote it.",
   "Harvey recorded the first version, on his album Alex Harvey in November 1971.",
   "Tanya Tucker's version reached number six on the country chart in 1972, and Bette Midler recorded it for The Divine Miss M.")}
        <h3>The Story Behind the Song</h3>
{p("Harvey said he wrote it about his mother, who lived as if she were always about to leave.",
   "Years earlier he had told her not to attend one of his television performances.",
   "She died in a car crash that night, which Harvey believed was suicide caused by his rejection.",
   "He considered the song an apology and a thank-you.")}
        <h3>Number One on the Hot 100</h3>
{p("Reddy's version entered the Hot 100's top ten on August 18, 1973, and reached number one on September 15, 1973.",
   "This site's weekly data gives it one week at the top.",
   "It also topped the Adult Contemporary chart, the first of six in a row for her.",
   "The RIAA certified it gold, and Wikipedia says it went gold in Australia and New Zealand too.",
   'The week it rose is one of the stories on the page about <a href="/blog/songs/70s-number-one-hits/">70s number one hits</a>.')}

        <h3>Leave Me Alone (Ruby Red Dress)</h3>
{p("Leave Me Alone (Ruby Red Dress) was released in October 1973, from Long Hard Climb.",
   "Linda Laurie wrote it and first recorded it for MCA Records in summer 1973.",
   "Tom Catalano produced Reddy's version, and Capitol issued it as the follow-up to Delta Dawn.")}
{p("It reached number three on the Hot 100 and number one on the Adult Contemporary chart.",
   f"It ranks #{rk[LEAVE]} on the 1974 Year-End Hot 100.",
   "The RIAA certified it gold, her third gold single in the US.",
   "Wikipedia says Reddy felt it was too similar to Delta Dawn in theme and found the chorus monotonous.")}

        <h2 id="year-1974">1974: Keep on Singing, You and Me Against the World and Angie Baby</h2>
{p("Helen Reddy songs in 1974 included her third number one, and two that sat at the top of the adult contemporary chart.")}

        <h3>Keep on Singing</h3>
{p("Keep on Singing was released in February 1974, as the lead single from Love Song for Jeffrey.",
   "Danny Janssen and Bobby Hart wrote it, and Tom Catalano produced it.",
   "Austin Roberts recorded it first, and his single reached number 50 on the Hot 100 in 1973.")}
{p("Reddy's version reached number 15 on the Hot 100 in May 1974, and number one on the Adult Contemporary chart.",
   "It reached number 10 in Canada.",
   'To find the next artist to try, spin the <a href="/pages/random-artist-picker">Random Artist Picker</a>.')}

        <h3>You and Me Against the World</h3>
{p("You and Me Against the World was released in May 1974, the second single from Love Song for Jeffrey.",
   "Paul Williams and Kenny Ascher wrote it.",
   "It reached number nine on the Hot 100 in September 1974, and number one on the Adult Contemporary chart.",
   f"It ranks #{rk[YOUME]} on the 1974 Year-End Hot 100.")}
        <h3>A Voice Calling Mommy</h3>
{p("The voice of Reddy's daughter Traci calls &quot;Mommy&quot; at the start and end of the record.",
   "Wikipedia says Reddy sang it as a mother singing to her child.",
   "Gladys Knight and the Pips, Johnny Mathis, Vera Lynn and Paul Williams also recorded it.",
   'Find a mood for it with the <a href="/pages/mood-song-matcher">Mood Song Matcher</a>.')}

        <h3>Angie Baby</h3>
{p("Alan O'Day wrote Angie Baby, and Joe Wissert produced Reddy's version, from the album Free and Easy.",
   "The B-side was I Think I'll Write a Song.",
   "It reached number one on the Hot 100 on December 28, 1974, and this site's weekly data gives it one week at the top.",
   f"It ranks #{rk[ANGIE]} on the 1975 Year-End Hot 100, because most of its run came in 1975.")}
{pic2}
        <p class="post-img-caption">Helen Reddy singing at the White House on January 27, 1976.</p>
        <p class="post-img-caption">Image credit: Ricardo Thomas, Gerald R. Ford Presidential Library, public domain, via Wikimedia Commons.</p>
        <h3>A Story Song with Many Readings</h3>
{p("The song follows a teenage girl who is pulled out of school, has no friends and daydreams about lovers from the radio.",
   "A neighbor boy comes to seduce her, but the loud music disorients him.",
   "When she turns the volume down, he shrinks and is pulled into the radio.",
   "Nobody asks her what happened, and the song suggests he became her secret lover.")}
{p("O'Day said it took three months to write and was loosely based on the character in the Beatles' Lady Madonna.",
   "Reddy never said what her own reading was, and she enjoyed hearing the theories.",
   "She joked that the boy had become a sound wave.",
   "She also said it was the one song she never had to push radio stations to play.")}
        <h3>Number One Around the World</h3>
{p("It reached number five in the UK and in Ireland, number three in Canada and number one on Cash Box.",
   "It was also number one on the Adult Contemporary chart, her fifth.",
   "Wikipedia says it was her only UK top 40 hit.",
   'The page on <a href="/blog/genres/pop-songs-of-70s/">pop songs of the 70s</a> shows where it sits among the decade&#39;s pop hits.')}

        <h2 id="year-1975-77">1975 to 1977: Emotion, Ain't No Way to Treat a Lady and More</h2>
{p("The last years of the decade gave Helen Reddy songs five more Hot 100 hits, none of them number one.",
   "Four of them were on the Adult Contemporary chart's top two.")}

        <h3>Emotion</h3>
{p("Emotion was released in January 1975, from Free and Easy, with Joe Wissert producing.",
   "It started as Amoureuse, a French song by Véronique Sanson.",
   "Elektra executive Artie Wayne sent Sanson's album to Patti Dahlstrom, who wrote the English lyric.",
   "Dahlstrom has said it came to her quickly after she had carried the melody in her head for weeks.")}
{p("Kiki Dee had cut an English version in 1973.",
   "Reddy's version reached number 22 on the Hot 100 and number one on the Adult Contemporary chart.",
   "It is on no 1970s year-end list, so its peak above is a weekly peak only.")}

        <h3>Ain't No Way to Treat a Lady</h3>
{p("Ain't No Way to Treat a Lady was released in August 1975, as the title song of the album No Way to Treat a Lady.",
   "Harriet Schock wrote it, and Joe Wissert produced it.",
   "It reached number eight on the Hot 100, number one on the Adult Contemporary chart in October 1975 and number two in Canada.")}
        <h3>A Napkin on a Flight Home</h3>
{p("Schock wrote it as she was leaving a self-absorbed lover.",
   "She got the title and first verse on a napkin during a flight home from Las Vegas.",
   "She finished the song at her Los Angeles home, and put her own version on her 1974 album Hollywood Town.",
   'The softer side of the decade has its own page, <a href="/blog/genres/70s-soft-rock/">70s soft rock</a>.')}

        <h3>Somewhere in the Night</h3>
{p("Somewhere in the Night was released in December 1975, as the follow-up to Ain't No Way to Treat a Lady.",
   "Richard Kerr and Will Jennings wrote it, and Joe Wissert produced it.",
   "It reached number 19 on the Hot 100 and number two on the Adult Contemporary chart.")}
{p("Barry Manilow recorded it in 1978 for the album Even Now, and his single reached number nine on the Hot 100.",
   "It is on no 1970s year-end list for Reddy, so her peak above is a weekly peak only.",
   'His own hits are on the page for <a href="/blog/artists/barry-manilow-songs/">Barry Manilow songs</a>.')}

        <h3>I Can't Hear You No More</h3>
{p("I Can't Hear You No More was released in 1976, from the album Music, Music.",
   "Gerry Goffin and Carole King wrote it, and Joe Wissert produced it.",
   "Betty Everett recorded it first, as I Can't Hear You, on May 13, 1964.",
   "Lulu, Dusty Springfield and Carole King herself later recorded it too.")}
{p("Reddy's version reached number 29 on the Hot 100 and number one on the Adult Contemporary chart.",
   "It is on no 1970s year-end list, so its peak above is a weekly peak only.")}

        <h3>You're My World</h3>
{p("You're My World was released on April 4, 1977, from the album Ear Candy.",
   "It began as Il mio mondo, an Italian ballad by Umberto Bindi that he recorded in 1963.",
   "Carl Sigman wrote the English words, and Cilla Black had a hit with that version in 1964.",
   "Kim Fowley and Earle Mankey produced Reddy's remake.")}
{p("It reached number 18 on the Hot 100 in July 1977, and number five on the Adult Contemporary chart.",
   f"It ranks #{rk[WORLD]} on the 1977 Year-End Hot 100.",
   "Wikipedia names it as her last top 40 hit.",
   'Test your memory of the decade with the <a href="/pages/70s-trivia-quiz">70s Music Trivia Quiz</a>.')}

        <h2 id="beyond-the-charts">Beyond the Charts: Television, Film and Awards</h2>
{p("Reddy was a television host and film actor as well as a singer.",
   "Wikipedia lists these milestones from the decade, alongside the Helen Reddy songs above.")}
        <ul>
          <li>1973: The Helen Reddy Show, an eight-episode summer replacement for The Flip Wilson Show, with Reddy as hostess.</li>
          <li>1974: She won the American Music Award for Favorite Pop/Rock Female Artist at the first ceremony.</li>
          <li>1974: She received a star on the Hollywood Walk of Fame on July 23.</li>
          <li>1974: She played a nun in the film Airport 1975, and earned a Golden Globe nomination for Most Promising Newcomer, Female.</li>
          <li>1975: She toured East Asia, Australia and New Zealand, and collected 16 gold records.</li>
          <li>1975 and 1976: She was a semiregular host of The Midnight Special.</li>
          <li>1977: She starred in Pete's Dragon, and introduced the Oscar-nominated song Candle on the Water.</li>
        </ul>
{p("Wikipedia says she was the first Australian to host a weekly one-hour prime-time variety show on an American network.")}

        <h2 id="outside-writers">Songs from Outside Writers: Who Sang Each Helen Reddy Song First</h2>
{p("Reddy wrote one of the thirteen Helen Reddy songs on this page, and took the rest from other writers.",
   "Many of them began as records by other singers, as the table shows.",
   'For more voices from the decade, read the page on <a href="/blog/artists/70s-female-singers/">70s female singers</a>.')}

{tbl("Helen Reddy songs of the 70s that had an earlier version, and who recorded it first (Wikipedia)", ["Song", "First Recorded By"], first_rows)}

        <h3>Writers Behind the Hits</h3>
{p("Several of her hits came from writers with hits of their own.")}
        <ul>
          <li>Alex Harvey: Delta Dawn.</li>
          <li>Alan O'Day: Angie Baby.</li>
          <li>Paul Williams and Kenny Ascher: You and Me Against the World.</li>
          <li>Gerry Goffin and Carole King: I Can't Hear You No More.</li>
          <li>Andrew Lloyd Webber and Tim Rice: I Don't Know How to Love Him.</li>
        </ul>

        <h2 id="who-wrote-what">Who Wrote and Released Each of the Helen Reddy Songs</h2>
{p(f"The table lists when each of the {NUM[n]} Helen Reddy songs was released, on which album, and who wrote it.")}

{tbl("Helen Reddy songs of the 70s: release date, album and writers (Wikipedia)", ["Song", "Released", "Album", "Written By"], album_rows)}

        <h3>Keep Exploring</h3>
{p("Reddy gave the decade three number ones and a long run of adult contemporary hits.",
   "Six of the thirteen reached the top ten.",
   'The page on <a href="/blog/artists/elton-john/">Elton John</a> tells the story of another act that ruled the decade&#39;s pop charts.')}

        <h2 id="sources">Sources</h2>
{p("Year-end ranks come from this site's own Billboard data, described on the <a href='/about/methodology/'>methodology page</a>.",
   'Every list on <a href="/">Music of the 70s</a> plays inside the page.',
   "Peaks, dates and stories behind the Helen Reddy songs above can be checked against these outside sources:")}
        <ul>
          <li><a href="https://en.wikipedia.org/wiki/Helen_Reddy" rel="noopener">Wikipedia: Helen Reddy</a> and <a href="https://en.wikipedia.org/wiki/Helen_Reddy_discography" rel="noopener">her discography</a> for the biography, albums, singles and chart peaks.</li>
          <li><a href="https://en.wikipedia.org/wiki/I_Don%27t_Know_How_to_Love_Him" rel="noopener">Wikipedia: I Don't Know How to Love Him</a> and <a href="https://en.wikipedia.org/wiki/I_Am_Woman" rel="noopener">I Am Woman</a> for 1971 and 1972.</li>
          <li><a href="https://en.wikipedia.org/wiki/Peaceful_(song)" rel="noopener">Wikipedia: Peaceful</a>, <a href="https://en.wikipedia.org/wiki/Delta_Dawn" rel="noopener">Delta Dawn</a> and <a href="https://en.wikipedia.org/wiki/Leave_Me_Alone_(Ruby_Red_Dress)" rel="noopener">Leave Me Alone (Ruby Red Dress)</a> for 1973.</li>
          <li><a href="https://en.wikipedia.org/wiki/Keep_on_Singing" rel="noopener">Wikipedia: Keep on Singing</a>, <a href="https://en.wikipedia.org/wiki/You_and_Me_Against_the_World_(song)" rel="noopener">You and Me Against the World</a> and <a href="https://en.wikipedia.org/wiki/Angie_Baby" rel="noopener">Angie Baby</a> for 1974.</li>
          <li><a href="https://en.wikipedia.org/wiki/Emotion_(Helen_Reddy_song)" rel="noopener">Wikipedia: Emotion</a>, <a href="https://en.wikipedia.org/wiki/Ain%27t_No_Way_to_Treat_a_Lady" rel="noopener">Ain't No Way to Treat a Lady</a>, <a href="https://en.wikipedia.org/wiki/Somewhere_in_the_Night_(Helen_Reddy_song)" rel="noopener">Somewhere in the Night</a>, <a href="https://en.wikipedia.org/wiki/I_Can%27t_Hear_You_No_More" rel="noopener">I Can't Hear You No More</a> and <a href="https://en.wikipedia.org/wiki/You%27re_My_World" rel="noopener">You're My World</a> for 1975 to 1977.</li>
        </ul>

        <section class="faq-block" id="faq">
          <h2>Frequently Asked Questions</h2>
{faq_html}
        </section>'''

    related = [
        ("carpenters-1972", "Artists", "Carpenters Songs: 11 Hits Played, 3 at Number One", "/blog/artists/carpenters-songs/",
         "Another act that ruled the adult contemporary chart, with every hit playable.", "The Carpenters in 1972"),
        ("carole-king-1970s", "Artists", "Carole King: The Same Chart, Three Different Names", "/blog/artists/carole-king/",
         "The songwriter who co-wrote I Can't Hear You No More, and her own 70s hits.", "Carole King in the 1970s"),
        ("donna-1977", "Artists", "Donna Summer: The 1977 Hit Too Influential for the Charts", "/blog/artists/donna-summer/",
         "Another woman who ruled the decade's charts, from the disco side.", "Donna Summer in 1977"),
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
      {{"@type": "ListItem", "position": 4, "name": "Helen Reddy Songs", "item": "{URL}"}}
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
        Helen Reddy Songs
      </nav>

      <article class="section seo-content">
        <h1>{TITLE}</h1>

        <p class="post-byline">By <a href="https://musicofthe70s.net/about/author/">Charlie</a> &middot; Published {PUBLISHED.strftime('%B')} {PUBLISHED.day}, {PUBLISHED.year}</p>
        <p class="jump-to-list"><a class="btn-primary jump-btn" href="#helen-reddy-songs-list">&#9654; Jump to the playable list</a></p>

        <p class="post-intro">Helen Reddy songs were on the radio all through the first half of the 70s.</p>
        <p class="post-intro">Three of them, I Am Woman, Delta Dawn and Angie Baby, reached number one on the Hot 100.</p>
        <p class="post-intro">This page plays {NUM[n]} of them, from I Don't Know How to Love Him to You're My World.</p>
        <p class="post-intro">Six reached the Hot 100's top ten, and I Am Woman became an anthem of the women's movement.</p>
        <p class="post-intro">She wrote one of them herself, and found the rest in other singers' records.</p>
        <p class="post-intro">Press Play on every hit below, then read the story behind each one.</p>

{feat_pic}
        <p class="post-img-caption">Helen Reddy in a 1975 publicity portrait by Francesco Scavullo.</p>
        <p class="post-img-caption">Image credit: publicity photo, public domain, via Wikimedia Commons.</p>

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
