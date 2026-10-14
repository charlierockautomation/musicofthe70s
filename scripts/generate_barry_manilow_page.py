#!/usr/bin/env python3
"""Build the Barry Manilow Songs Artists post (blog/artists/barry-manilow-songs/index.html).

Data: data/radio/radio-songs.json (nine Barry Manilow rows of the 1975-1979 Year-End Hot 100, each with a YouTube ID),
data/billboard/hot100_weekly.json (Mandy, I Write the Songs and Looks Like We Made It, the three Hot 100 number ones in
the site's 1970-1979 weekly data), data/billboard/beyond_year_end.json (three further singles on the weekly Hot 100 but
on no 1970s year-end list: It's a Miracle, Even Now and Ships, peaks and official-channel YouTube IDs checked).
Year-End Rank is the year-end rank, never a peak. Hot 100 and Adult Contemporary peaks, release dates, writers and
story facts come from the linked Wikipedia articles, checked 2026-10-14, and are credited to Wikipedia on the page.
The site JSON's fun_fact and trivia text for Barry Manilow is not used.

Run: python3 scripts/generate_barry_manilow_page.py
"""
import html
import json
from datetime import date

from genre_page_common import ROOT, read, play_button, write
from generate_country_page import p, tbl, pic

SLUG = "barry-manilow-songs"
PAGE = f"blog/artists/{SLUG}/"
URL = f"https://musicofthe70s.net/{PAGE}"
IMG = "barry-manilow-1975"
IMG2 = "barry-manilow-1979"
CHART = "barry-manilow-peaks"
PUBLISHED = date(2026, 10, 14)
ARTIST = "Barry Manilow"
NUM = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
       10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen"}

# title -> (release year, Hot 100 peak, Adult Contemporary peak, released text, album, written by)
# Every value read from the song's Wikipedia article, checked 2026-10-14.
INFO = {
    "Mandy": (1974, 1, 1, "October 7, 1974", "Barry Manilow II", "Scott English and Richard Kerr"),
    "It's a Miracle": (1975, 12, 1, "February 1975", "Barry Manilow II", "Barry Manilow and Marty Panzer"),
    "Could It Be Magic": (1975, 6, 4, "1975 (single)", "Barry Manilow (1973), reissued as Barry Manilow I",
                          "Barry Manilow and Adrienne Anderson, from a Chopin prelude"),
    "I Write the Songs": (1975, 1, 1, "November 1975", "Tryin' to Get the Feeling", "Bruce Johnston"),
    "Tryin' to Get the Feeling Again": (1976, 10, 1, "March 1976", "Tryin' to Get the Feeling", "David Pomeranz"),
    "Weekend in New England": (1976, 10, 1, "November 1976", "This One's for You", "Randy Edelman"),
    "Looks Like We Made It": (1977, 1, 1, "April 20, 1977", "This One's for You", "Richard Kerr and Will Jennings"),
    "Can't Smile Without You": (1978, 3, 1, "January 1978", "Even Now", "Christian Arnold, Geoff Morrow and David Martin"),
    "Even Now": (1978, 19, 1, "April 1978", "Even Now", "Barry Manilow and Marty Panzer"),
    "Copacabana": (1978, 8, 6, "June 1978", "Even Now", "Barry Manilow, Jack Feldman and Bruce Sussman"),
    "Somewhere in the Night": (1978, 9, 4, "1978", "Even Now", "Richard Kerr and Will Jennings"),
    "Ships": (1979, 9, 4, "October 1979", "One Voice", "Ian Hunter"),
}
ORDER = list(INFO)
BEYOND = {"It's a Miracle", "Even Now", "Ships"}
TRYIN, CANT = "Tryin' to Get the Feeling Again", "Can't Smile Without You"


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
    assert len(ye) == 9, len(ye)
    assert set(beyond) == BEYOND, set(beyond)
    assert set(ye) | BEYOND == set(INFO), (set(ye) | BEYOND) ^ set(INFO)
    for t in BEYOND:
        assert beyond[t]["weekly_peak"] == INFO[t][1], t
        assert beyond[t]["released"] == INFO[t][0], t
    for t, s in ye.items():
        assert s["year"] in (INFO[t][0], INFO[t][0] + 1), (t, s["year"])
        assert s["billboard_peak"] == s["rank"], t

    # weekly number ones by Barry Manilow in the site's own 1970-1979 data
    wk = {}
    for yr in weekly:
        for w in weekly[yr]:
            if w["artist"] == ARTIST:
                wk.setdefault(w["title"], []).append(w)
    assert set(wk) == {"Mandy", "I Write the Songs", "Looks Like We Made It"}, set(wk)
    assert all(len(v) == 1 and v[0]["weeks_at_number_one"] == 1 for v in wk.values())
    wk_start = {t: v[0]["week_start"] for t, v in wk.items()}
    assert wk_start == {"Mandy": "1975-01-18", "I Write the Songs": "1976-01-17",
                        "Looks Like We Made It": "1977-07-23"}, wk_start

    rk = {t: ye[t]["rank"] for t in ye}
    n = len(INFO)
    assert n == 12
    top_ten = [t for t in INFO if INFO[t][1] <= 10]
    assert len(top_ten) == 10, top_ten
    ac_ones = [t for t in INFO if INFO[t][2] == 1]
    assert len(ac_ones) == 8, ac_ones
    manilow_wrote = [t for t in INFO if "Barry Manilow" in INFO[t][5]]
    assert len(manilow_wrote) == 4, manilow_wrote
    yt = {t: (ye[t]["youtube_id"] if t in ye else beyond[t]["youtube_id"]) for t in INFO}

    rows = []
    for t in ORDER:
        y, pk, ac, rel, alb, wr = INFO[t]
        ye_year = ye[t]["year"] if t in ye else ""
        ye_rank = ye[t]["rank"] if t in ye else ""
        rows.append(f'              <tr><td class="ohw-listen">{play_button(yt[t], t, ARTIST)}</td>'
                    f'<td class="ohw-song">{html.escape(t)}</td>'
                    f'<td>{y}</td><td>{ye_year}</td><td>{ye_rank}</td><td>{pk}</td></tr>')

    peak_rows = sorted(([html.escape(t), INFO[t][1], INFO[t][2], INFO[t][3]] for t in ORDER), key=lambda r: (r[1], r[2], r[0]))
    album_rows = [[html.escape(t), INFO[t][3], html.escape(INFO[t][4]), html.escape(INFO[t][5])] for t in ORDER]

    faq = [
        ("What is Barry Manilow's biggest hit?",
         ["Barry Manilow's biggest hits of the 70s are his three Hot 100 number ones.",
          "They are Mandy, I Write the Songs and Looks Like We Made It.",
          f"I Write the Songs ranks highest on a year-end list, at #{rk['I Write the Songs']} on the 1976 Year-End Hot 100.",
          "Wikipedia calls Looks Like We Made It his third and final Billboard number one."]),
        ("How many number one songs did Barry Manilow have in the 1970s?",
         ["Barry Manilow had three Hot 100 number ones in the 1970s.",
          "This site's weekly chart data gives each one week at the top.",
          "Mandy started its week on January 18, 1975.",
          "I Write the Songs followed on January 17, 1976, and Looks Like We Made It on July 23, 1977.",
          "Eight of the twelve songs on this page also reached number one on the Adult Contemporary chart, according to Wikipedia."]),
        ("Who wrote I Write the Songs?",
         ["Bruce Johnston wrote I Write the Songs, not Barry Manilow, according to Wikipedia.",
          "Captain & Tennille recorded it first.",
          "David Cassidy's version was the first single, reaching number 11 in the UK in August 1975.",
          "Manilow's version was released in November 1975.",
          "It reached number one on the Hot 100 on January 17, 1976, and won the Grammy for Song of the Year."]),
        ("Did Barry Manilow write Mandy?",
         ["No, Scott English and Richard Kerr wrote Mandy, which English first recorded in 1971 under the title Brandy.",
          "Manilow slowed the song down and changed the title to Mandy.",
          "That avoided confusion with Looking Glass's number one Brandy (You're a Fine Girl) from 1972.",
          "It was released on October 7, 1974, and it was his first number one on the Hot 100."]),
        ("Which Barry Manilow song won a Grammy?",
         ["Copacabana (At the Copa) won Manilow his first and only Grammy, per Wikipedia.",
          "It was for Best Male Pop Vocal Performance, in February 1979.",
          "He wrote it with Jack Feldman and Bruce Sussman, and it reached number eight on the Hot 100.",
          "It was his first gold single for a song he wrote or co-wrote."]),
    ]
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": " ".join(a)}} for q, a in faq]},
        indent=2, ensure_ascii=False)
    faq_ld = "\n".join("  " + l for l in faq_ld.split("\n"))
    faq_html = "\n".join(
        f'          <div class="faq-item">\n            <h3>{html.escape(q)}</h3>\n' + "\n".join(f"            <p>{html.escape(l)}</p>" for l in a) + "\n          </div>"
        for q, a in faq).replace("&#x27;", "'")

    TITLE = f"Barry Manilow Songs: {n} Hits Played, 3 at Number One"
    desc = (f"Barry Manilow songs of the 70s, all {n} playable: Mandy, I Write the Songs, Copacabana and more. "
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

    toc = [("barry-manilow-songs-list", f"Barry Manilow Songs: Play All {n} Hits"),
           ("by-the-numbers", "Barry Manilow Songs on the Charts: Three Number Ones, Eight Adult Contemporary Chart-Toppers"),
           ("origins", "From Brooklyn Jingles to Clive Davis: How Barry Manilow Got His Start"),
           ("mandy-years", "1974 and 1975: Mandy, It's a Miracle and Could It Be Magic"),
           ("tryin-years", "1975 and 1976: I Write the Songs, Tryin' to Get the Feeling Again and Weekend in New England"),
           ("one-voice", "1977: Looks Like We Made It"),
           ("even-now-years", "1978: Can't Smile Without You, Even Now, Copacabana and Somewhere in the Night"),
           ("ships-year", "1979: Ships"),
           ("who-wrote-what", "Who Wrote and Released Each of the Barry Manilow Songs"),
           ("sources", "Sources"), ("faq", "Frequently Asked Questions")]
    toc_html = "\n".join(f'            <li><a href="#{i}">{t}</a></li>' for i, t in toc)

    feat_pic = pic(IMG, "Barry Manilow in a black and white 1975 press photo, shoulder-length hair and an open-collared shirt, the face behind the Barry Manilow songs of the 70s",
                   "(max-width: 700px) 100vw, 669px", 669, 440, widths=(400, 669), lazy=False).replace(
        'class="post-featured-img"', 'class="post-featured-img" style="aspect-ratio:669/440;max-width:669px;height:auto;margin:1.5rem auto"', 1)
    pic2 = pic(IMG2, "Barry Manilow in profile in a dark suit with a red rose on the lapel, photographed in November 1979 at the premiere of The Rose",
               "(max-width: 700px) 100vw, 669px", 669, 440, widths=(400, 669)).replace(
        "<img\n", '<img style="display:block;width:100%;max-width:669px;height:auto;margin:1.5rem auto;border-radius:8px"\n', 1)
    chart_pic = pic(CHART, "Dumbbell chart of twelve Barry Manilow songs, each with its Hot 100 peak and Adult Contemporary peak, from Mandy at number one on both to Even Now at number 19 and number one",
                    "(max-width: 700px) 100vw, 800px", 800, 450, widths=(400, 800, 1200)).replace(
        "<img\n", '<img style="display:block;width:100%;max-width:800px;height:auto;margin:1.5rem auto;border-radius:8px"\n', 1)

    body = f'''        <h2 id="barry-manilow-songs-list">Barry Manilow Songs: Play All {n} Hits</h2>
{p(f"Here are {NUM[n]} Barry Manilow songs from 1974 to 1979, from Mandy to Ships.",
   "Nine sit on a Billboard Year-End Hot 100, and three more charted weekly without making a year-end list.",
   "Press Play on any row to watch it here, and tap a heading to sort.")}

        <div class="data-table-wrap scroll-list">
          <table class="data-table sortable-table" id="barryManilowSongsTable" data-inline-player>
            <caption>{n} Barry Manilow songs of the 70s, with release year, Billboard Year-End Hot 100 rank and Hot 100 peak</caption>
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

        <h2 id="by-the-numbers">Barry Manilow Songs on the Charts: Three Number Ones, Eight Adult Contemporary Chart-Toppers</h2>
{p("His hits of the 70s were as big on the Adult Contemporary chart as on the Hot 100.",
   "Three reached number one on the Hot 100, and this site's weekly data gives each one week at the top.",
   "Mandy started its week on January 18, 1975.",
   "I Write the Songs followed on January 17, 1976, and Looks Like We Made It on July 23, 1977.",
   "Eight of the songs on this page also reached number one on the Adult Contemporary chart, according to Wikipedia.")}

{chart_pic}
        <p class="post-img-caption">Hot 100 and Adult Contemporary peaks of the twelve hits on this page, from each song's Wikipedia article.</p>

{tbl("Barry Manilow songs of the 70s ranked by weekly Hot 100 peak, with the Adult Contemporary peak and release date (Wikipedia)", ["Song", "Hot 100 Peak", "Adult Contemporary Peak", "Released"], peak_rows)}

        <h3>What the Chart Numbers Say</h3>
{p(f"Ten of the {NUM[n]} Barry Manilow songs on this page reached the Hot 100's top ten.")}
        <ul>
          <li>Mandy, I Write the Songs and Looks Like We Made It reached number one on the Hot 100, in 1975, 1976 and 1977.</li>
          <li>Can't Smile Without You came closest after that, stopping at number three in 1978.</li>
          <li>Only It's a Miracle (number 12) and Even Now (number 19) missed the top ten.</li>
          <li>I Write the Songs ranks #{rk['I Write the Songs']} on the 1976 Year-End Hot 100, the best year-end rank of any song here, ahead of Can't Smile Without You at #{rk[CANT]}.</li>
          <li>Even Now reached only number 19 on the Hot 100, yet spent three weeks at number one on the Adult Contemporary chart.</li>
        </ul>
{p('To see who else ruled the decade&#39;s number one spots, read the page on <a href="/blog/songs/70s-number-one-hits/">70s number one hits</a>.')}

        <h3>Written by Others, Sung by Manilow</h3>
{p(f"Barry Manilow wrote or co-wrote only {NUM[len(manilow_wrote)]} of the {NUM[n]} songs on this page.",
   "Those four are It's a Miracle, Could It Be Magic, Even Now and Copacabana.",
   "The song with the title I Write the Songs was written by Bruce Johnston.",
   "The table near the end of this page lists the writer of every hit.")}

        <h2 id="origins">From Brooklyn Jingles to Clive Davis: How Barry Manilow Got His Start</h2>
{p("The story behind the Barry Manilow songs starts in Brooklyn, New York.",
   "Wikipedia says he was born Barry Alan Pincus on June 17, 1943.",
   "Through the 1960s he wrote and sang commercial jingles, including State Farm, Band-Aid, McDonald's and Dr Pepper.",
   "In 1971 Bette Midler chose him as her pianist at the Continental Baths.",
   "He worked with her until 1975.")}
{p("He produced her albums The Divine Miss M and Bette Midler.",
   "He was nominated for Album of the Year at the 1973 Grammys for the first one.",
   "His own debut album, Barry Manilow, came out on Bell Records in July 1973.")}

        <h3>Clive Davis and Arista</h3>
{p("In 1974 Clive Davis became temporary president of Bell, and Arista was introduced in November 1974.",
   "Davis insisted on including Mandy on Barry Manilow II.",
   "That single became Bell's last number one, in January 1975.",
   "The debut album was later reissued on Arista as Barry Manilow I.",
   'For more of the same era, spin the <a href="/pages/random-artist-picker">Random Artist Picker</a>.')}

        <h2 id="mandy-years">1974 and 1975: Mandy, It's a Miracle and Could It Be Magic</h2>
{p("The first three Barry Manilow songs on this page all came from the Arista launch.",
   f"Mandy and Could It Be Magic rank on the 1975 Year-End Hot 100, at #{rk['Mandy']} and #{rk['Could It Be Magic']}.")}

        <h3>Mandy</h3>
{p("Mandy was released on October 7, 1974, from Barry Manilow II.",
   "Scott English and Richard Kerr wrote it, and English first recorded it in 1971 as Brandy.",
   "Wikipedia says Davis suggested Manilow record it, and that Davis heard the first take and said it was terrible.")}
{p("Manilow agreed, went back to the studio, slowed the song down and changed the title to Mandy.",
   "The new title avoided confusion with Looking Glass's Brandy (You're a Fine Girl), which reached number one in 1972.",
   "It was his first number one on the Hot 100 and on the Easy Listening chart.",
   "It was also his first gold single, and it reached number 11 in the UK.")}
{p(f"It ranks #{rk['Mandy']} on the 1975 Year-End Hot 100.")}

        <h3>It's a Miracle</h3>
{p("It's a Miracle was released in February 1975, from Barry Manilow II, and Manilow and Marty Panzer wrote it.",
   "It reached number 12 on the Hot 100.",
   "It spent one week at number one on the Adult Contemporary chart in April 1975.",
   "It is on no 1970s year-end list, so its peak above is a weekly peak only.")}
{p("The song describes a long concert tour across America, and the miracle is coming home to a love rediscovered.",
   "Wikipedia says it is traditionally the first song at Manilow's concerts.",
   "It was a number one hit in Canada for two weeks.")}

        <h3>Could It Be Magic</h3>
{p("Could It Be Magic began on Manilow's 1973 debut album.",
   "A reworked version was released as an Arista single in 1975.",
   "Manilow wrote the music and Adrienne Anderson wrote the lyrics.",
   "The song is inspired by Chopin's Prelude in C minor, Op. 28, No. 20.",
   "The recording quotes the prelude's first eight bars at the start and the end.")}
{p("The 1975 single reached number six on the Hot 100 and number four on the Adult Contemporary chart.",
   f"It ranks #{rk['Could It Be Magic']} on the 1975 Year-End Hot 100.",
   "Donna Summer released a cover on January 11, 1976.",
   "It reached number 52 on the Hot 100 and number three on the Dance chart.",
   'Read the story of another soft hitmaker in the page on <a href="/blog/artists/carpenters-songs/">Carpenters songs</a>.')}

        <h2 id="tryin-years">1975 and 1976: I Write the Songs, Tryin' to Get the Feeling Again and Weekend in New England</h2>
{p("Three more hits followed in less than a year.",
   "Manilow wrote none of them.",
   "Two reached number one on the Adult Contemporary chart, and I Write the Songs topped the Hot 100.")}

        <h3>I Write the Songs</h3>
{p("I Write the Songs was released in November 1975, from the album Tryin' to Get the Feeling.",
   "Bruce Johnston wrote it, and Captain & Tennille recorded it before Manilow did.",
   "David Cassidy's version, produced by Johnston, was the first single.",
   "It reached number 11 in the UK in August 1975.")}
        <h3>Why Manilow Hesitated</h3>
{p("Manilow was reluctant to record it, because he worried that listeners would hear it as an ego trip.",
   "Davis persuaded him.",
   "Johnston has said the I in the song is God, and that it is not about Brian Wilson.",
   "It reached number one on the Hot 100 on January 17, 1976, nine weeks after it first charted.")}
{p(f"It ranks #{rk['I Write the Songs']} on the 1976 Year-End Hot 100, and it won the Grammy for Song of the Year.",
   "It was also nominated for Record of the Year at the 1977 Grammys.",
   "Frank Sinatra covered it as I Sing the Songs.")}

        <h3>Tryin' to Get the Feeling Again</h3>
{p("Tryin' to Get the Feeling Again was released in March 1976, and David Pomeranz wrote it.",
   "It reached number 10 on the Hot 100 and number one on the Adult Contemporary chart.",
   f"It ranks #{rk[TRYIN]} on the 1976 Year-End Hot 100.")}
{p("Pomeranz wrote it during a time of stress in his marriage, and he rewrote it several times.",
   "The Carpenters recorded it in 1975 but shelved it as one too many ballads.",
   "Richard Carpenter released it in 1994.",
   "Manilow's single cut the original bridge for timing reasons.")}

        <h3>Weekend in New England</h3>
{p("Weekend in New England was released in November 1976, as the second single from This One's for You.",
   "Randy Edelman wrote it, and he first recorded it in 1975 as the B-side of Concrete and Clay.",
   "It reached number 10 on the Hot 100 and number one on the Adult Contemporary chart, and it ranks #" + str(rk["Weekend in New England"]) + " on the 1977 Year-End Hot 100.")}
{p("Wikipedia says Davis asked Edelman to rework the verse melody, and that Edelman delivered a new one about a week later.",
   "The title phrase does not appear in the lyrics.",
   "Reba McEntire's Whoever's in New England (1986) and Sugarland's Stay (2007) were inspired by it.")}

        <h2 id="one-voice">1977: Looks Like We Made It</h2>
{p("Looks Like We Made It was released on April 20, 1977, from This One's for You, and it was Manilow's third gold record of five.",
   "Richard Kerr wrote the music and Will Jennings wrote the lyrics.",
   "It reached number one on the Hot 100 and the Adult Contemporary chart.")}
{pic2}
        <p class="post-img-caption">Barry Manilow in November 1979, photo by Alan Light, licensed CC BY 2.0.</p>
{p(f"This site's weekly data puts its week at number one at July 23, 1977, and it ranks #{rk['Looks Like We Made It']} on the 1977 Year-End Hot 100.",
   "Wikipedia calls it his third and final Billboard number one.",
   "Jennings said listeners often took it as upbeat, but he considered the lyric sad and ironic.")}
{p("The same year, The Barry Manilow Special, shown on March 2, 1977, drew an audience of 37 million, and it won the Emmy for Outstanding Special, Comedy, Variety or Music.",
   'Test your memory of the decade with the <a href="/pages/70s-trivia-quiz">70s Music Trivia Quiz</a>.')}

        <h2 id="even-now-years">1978: Can't Smile Without You, Even Now, Copacabana and Somewhere in the Night</h2>
{p("The album Even Now gave the Barry Manilow songs their biggest run of singles.",
   "Wikipedia says it contained four singles that became major US hits, and that it was his breakthrough in Britain.",
   "Ready to Take a Chance Again, from the film Foul Play, also charted in 1978, and it is not on this page.")}

        <h3>Can't Smile Without You</h3>
{p("Can't Smile Without You was released in January 1978, and Christian Arnold, Geoff Morrow and David Martin wrote it.",
   "David Martin released it as a solo single on July 25, 1975, and the Carpenters recorded it in February 1976.",
   "Manilow recorded it in 1977.")}
{p(f"It reached number three on the Hot 100, number one on the Adult Contemporary chart and number 43 in the UK, and it ranks #{rk[CANT]} on the 1978 Year-End Hot 100.",
   "Martin wrote it about a woman named Debbie, who appears on the cover of his single.",
   "Tottenham Hotspur fans have sung it since the late 1970s, according to Wikipedia.")}

        <h3>Even Now</h3>
{p("Even Now was released in April 1978, as the second single and title track of the album.",
   "Manilow wrote the music, Marty Panzer wrote the words, and they produced it with Ron Dante.",
   "It reached number 19 on the Hot 100 in June 1978.",
   "It spent three weeks at number one on the Adult Contemporary chart, starting May 27, 1978.")}
{p("In his autobiography Sweet Life, Manilow called it one of his personal favorites.",
   "The lyric describes a lyricist who regrets leaving a loving relationship for a better life with someone else.",
   "It is on no 1970s year-end list, so its peak above is a weekly peak only.")}

        <h3>Copacabana (At the Copa)</h3>
{p("Copacabana was released in June 1978, as the third single from Even Now.",
   "Manilow, Jack Feldman and Bruce Sussman wrote it.",
   "The idea came from a conversation between Manilow and Sussman at the Copacabana Hotel in Rio de Janeiro.",
   "Lola Falana inspired the showgirl character.")}
{p("It reached number eight on the Hot 100 and number six on the Adult Contemporary chart.",
   f"It ranks #{rk['Copacabana']} on the 1978 Year-End Hot 100.",
   "It won Manilow his first and only Grammy, for Best Male Pop Vocal Performance, in February 1979.",
   "In 1985 he, Feldman and Sussman expanded the song into a made-for-television musical.")}

        <h3>Somewhere in the Night</h3>
{p("Richard Kerr wrote the music of Somewhere in the Night, and Will Jennings wrote the lyrics.",
   "It was their first song as a team.",
   "Batdorf & Rodney's version came out first, in October 1975, and it reached number 69 on the Hot 100.",
   "Helen Reddy's version reached number 19 in 1975.")}
{p("Manilow's version, on Even Now, reached number nine on the Hot 100 and number four on the Adult Contemporary chart.",
   f"It ranks #{rk['Somewhere in the Night']} on the 1979 Year-End Hot 100.",
   'For more pop hits of the decade, read the page on <a href="/blog/genres/pop-songs-of-70s/">pop songs of the 70s</a>.')}

        <h2 id="ships-year">1979: Ships</h2>
{p("Ships is the last of the Barry Manilow songs on this page, released in October 1979, from One Voice.",
   "Ian Hunter wrote it.",
   "Hunter first recorded it on his March 1979 album You're Never Alone with a Schizophrenic.",
   "His single, issued in August 1979, never charted.",
   "Manilow's version reached number nine on the Hot 100 and number four on the Adult Contemporary chart.")}
{p("The song is said to be about Hunter's relationship with his father.",
   "Manilow chose it because his own father had been absent since he was two.",
   "In 1975, after a concert, a man entered his dressing room and said he was his father.",
   "It is on no 1970s year-end list, so its peak above is a weekly peak only.")}
{p('The soft side of the decade has its own page, <a href="/blog/genres/70s-soft-rock/">70s soft rock</a>.')}

        <h2 id="who-wrote-what">Who Wrote and Released Each of the Barry Manilow Songs</h2>
{p(f"The table lists when each of the {NUM[n]} songs was released, on which album, and who wrote it.",
   f"Manilow shared a writing credit on {NUM[len(manilow_wrote)]} of them.")}

{tbl("Barry Manilow songs of the 70s: release date, album and writers (Wikipedia)", ["Song", "Released", "Album", "Written By"], album_rows)}

        <h3>Keep Exploring</h3>
{p("Barry Manilow songs turned a Brooklyn jingle writer into one of the biggest voices on 70s radio.",
   "Three reached number one on the Hot 100, and ten reached the top ten.",
   'The page on <a href="/blog/artists/elton-john/">Elton John</a> tells the story of another act that ruled the decade&#39;s pop charts.')}

        <h2 id="sources">Sources</h2>
{p("Year-end ranks come from this site's own Billboard data, described on the <a href='/about/methodology/'>methodology page</a>.",
   'Every list on <a href="/">Music of the 70s</a> plays inside the page.',
   "Peaks, dates and stories behind the Barry Manilow songs above can be checked against these outside sources:")}
        <ul>
          <li><a href="https://en.wikipedia.org/wiki/Barry_Manilow" rel="noopener">Wikipedia: Barry Manilow</a> and <a href="https://en.wikipedia.org/wiki/Barry_Manilow_discography" rel="noopener">his discography</a> for the biography, albums, singles and chart peaks.</li>
          <li><a href="https://en.wikipedia.org/wiki/Mandy_(Barry_Manilow_song)" rel="noopener">Wikipedia: Mandy</a>, <a href="https://en.wikipedia.org/wiki/It%27s_a_Miracle_(Barry_Manilow_song)" rel="noopener">It's a Miracle</a> and <a href="https://en.wikipedia.org/wiki/Could_It_Be_Magic" rel="noopener">Could It Be Magic</a> for 1974 and 1975.</li>
          <li><a href="https://en.wikipedia.org/wiki/I_Write_the_Songs" rel="noopener">Wikipedia: I Write the Songs</a>, <a href="https://en.wikipedia.org/wiki/Tryin%27_to_Get_the_Feeling_Again" rel="noopener">Tryin' to Get the Feeling Again</a> and <a href="https://en.wikipedia.org/wiki/Weekend_in_New_England" rel="noopener">Weekend in New England</a> for 1975 and 1976.</li>
          <li><a href="https://en.wikipedia.org/wiki/Looks_Like_We_Made_It" rel="noopener">Wikipedia: Looks Like We Made It</a> for 1977.</li>
          <li><a href="https://en.wikipedia.org/wiki/Can%27t_Smile_Without_You" rel="noopener">Wikipedia: Can't Smile Without You</a>, <a href="https://en.wikipedia.org/wiki/Even_Now_(Barry_Manilow_song)" rel="noopener">Even Now</a>, <a href="https://en.wikipedia.org/wiki/Copacabana_(At_the_Copa)" rel="noopener">Copacabana</a> and <a href="https://en.wikipedia.org/wiki/Somewhere_in_the_Night_(Barry_Manilow_song)" rel="noopener">Somewhere in the Night</a> for 1978.</li>
          <li><a href="https://en.wikipedia.org/wiki/Ships_(song)" rel="noopener">Wikipedia: Ships</a> for 1979.</li>
        </ul>

        <section class="faq-block" id="faq">
          <h2>Frequently Asked Questions</h2>
{faq_html}
        </section>'''

    related = [
        ("carpenters-1972", "Artists", "Carpenters Songs: 11 Hits Played, 3 at Number One", "/blog/artists/carpenters-songs/",
         "Another soft-pop act with playable hits and a Can't Smile Without You connection.", "The Carpenters in 1972"),
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
      {{"@type": "ListItem", "position": 4, "name": "Barry Manilow Songs", "item": "{URL}"}}
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
        Barry Manilow Songs
      </nav>

      <article class="section seo-content">
        <h1>{TITLE}</h1>

        <p class="post-byline">By <a href="https://musicofthe70s.net/about/author/">Charlie</a> &middot; Published {PUBLISHED.strftime('%B')} {PUBLISHED.day}, {PUBLISHED.year}</p>
        <p class="jump-to-list"><a class="btn-primary jump-btn" href="#barry-manilow-songs-list">&#9654; Jump to the playable list</a></p>

        <p class="post-intro">Barry Manilow songs ruled the Adult Contemporary chart in the 70s.</p>
        <p class="post-intro">Three of them, Mandy, I Write the Songs and Looks Like We Made It, reached number one on the Hot 100.</p>
        <p class="post-intro">This page plays {NUM[n]} of them, from Mandy to Ships.</p>
        <p class="post-intro">Ten reached the Hot 100's top ten, and eight reached number one on the Adult Contemporary chart.</p>
        <p class="post-intro">Manilow wrote only four of the twelve, and Clive Davis pushed him to record Mandy.</p>
        <p class="post-intro">Press Play on every hit below, then read the story behind each one.</p>

{feat_pic}
        <p class="post-img-caption">Barry Manilow in a 1975 press photo from the William Morris Agency.</p>
        <p class="post-img-caption">Image credit: William Morris Agency press photo dated December 15, 1975, public domain in the United States, via Wikimedia Commons.</p>

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
