#!/usr/bin/env python3
"""Build the KC and the Sunshine Band Songs Artists post (blog/artists/kc-and-the-sunshine-band-songs/index.html).

Data: data/radio/radio-songs.json (five KC and the Sunshine Band rows of the 1975-1977 Year-End Hot 100, each with a
YouTube ID), data/billboard/hot100_weekly.json (four Hot 100 number ones in the site's 1970-1979 weekly data: Get Down
Tonight, That's the Way (I Like It), (Shake, Shake, Shake) Shake Your Booty and I'm Your Boogie Man),
data/billboard/beyond_year_end.json (seven further singles on the weekly Hot 100 but on no 1970s year-end list: Queen of
Clubs, I Like to Do It, Wrap Your Arms Around Me, Boogie Shoes, It's the Same Old Song, Do You Wanna Go Party and Please
Don't Go; peaks and Topic YouTube IDs checked).
Year-End Rank is the year-end rank, never a peak. Hot 100 peaks, release dates, writers and story facts come from the
linked Wikipedia articles and the band's discography article, checked 2026-10-15, and are credited to Wikipedia.
Please Don't Go reached number one in January 1980 (Wikipedia), outside the site's 1970-1979 weekly data.
The site JSON's fun_fact and trivia text for the band is not used.

Run: python3 scripts/generate_kc_sunshine_band_page.py
"""
import html
import json
from datetime import date

from genre_page_common import ROOT, read, play_button, write
from generate_country_page import p, tbl, pic

SLUG = "kc-and-the-sunshine-band-songs"
PAGE = f"blog/artists/{SLUG}/"
URL = f"https://musicofthe70s.net/{PAGE}"
IMG = "kc-sunshine-band-1980"
IMG2 = "kc-sunshine-band-2006"
CHART = "kc-sunshine-band-peaks"
PUBLISHED = date(2026, 10, 15)
ARTIST = "KC and the Sunshine Band"
NUM = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
       10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen"}

QUEEN, GDT, TTW, SHAKE, ILTDI = "Queen of Clubs", "Get Down Tonight", "That's the Way (I Like It)", "(Shake, Shake, Shake) Shake Your Booty", "I Like to Do It"
BOOGIE, KEEP, WRAP = "I'm Your Boogie Man", "Keep It Comin' Love", "Wrap Your Arms Around Me"
SHOES, SAME, PARTY, PLEASE = "Boogie Shoes", "It's the Same Old Song", "Do You Wanna Go Party", "Please Don't Go"
CF = "Harry Wayne Casey and Richard Finch"

# title -> (release year, Hot 100 peak, released text, album, written by)
# Every value read from the song's Wikipedia article, the album's article or the band's discography article, checked
# 2026-10-15. Album and writers are "" where none of those states them.
INFO = {
    QUEEN: (1974, 66, "1974", "", ""),
    GDT: (1975, 1, "February 11, 1975", "KC and the Sunshine Band", CF),
    TTW: (1975, 1, "June 10, 1975", "KC and the Sunshine Band", CF),
    SHAKE: (1976, 1, "May 28, 1976", "Part 3", CF),
    ILTDI: (1976, 37, "1976", "", ""),
    BOOGIE: (1977, 1, "February 3, 1977", "Part 3", CF),
    KEEP: (1977, 2, "May 16, 1977", "Part 3", CF),
    WRAP: (1977, 48, "1977", "", ""),
    SHOES: (1978, 35, "January 1978", "KC and the Sunshine Band", CF),
    SAME: (1978, 35, "1978", "Who Do Ya Love", "Holland, Dozier and Holland"),
    PARTY: (1979, 50, "1979", "Do You Wanna Go Party", CF),
    PLEASE: (1979, 1, "July 12, 1979", "Do You Wanna Go Party", CF),
}
ORDER = list(INFO)
BEYOND = {QUEEN, ILTDI, WRAP, SHOES, SAME, PARTY, PLEASE}
YE_SET = {GDT, TTW, SHAKE, BOOGIE, KEEP}


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
    assert set(ye) == YE_SET, set(ye) ^ YE_SET
    assert set(beyond) == BEYOND, set(beyond)
    for t in BEYOND:
        assert beyond[t]["weekly_peak"] == INFO[t][1], t
        assert beyond[t]["released"] == INFO[t][0], t
    for t, s in ye.items():
        assert s["year"] in (INFO[t][0], INFO[t][0] + 1), (t, s["year"])
        assert s["billboard_peak"] == s["rank"], t

    # weekly number ones by the band in the site's own 1970-1979 data
    wk = {}
    for yr in weekly:
        for w in weekly[yr]:
            if w["artist"] == ARTIST:
                wk.setdefault(w["title"], []).append(w)
    assert set(wk) == {GDT, TTW, SHAKE, BOOGIE}, set(wk)
    assert len(wk[GDT]) == 1 and wk[GDT][0]["week_start"] == "1975-08-30"
    assert [w["week_start"] for w in wk[TTW]] == ["1975-11-22", "1975-12-20"]
    assert len(wk[SHAKE]) == 1 and wk[SHAKE][0]["week_start"] == "1976-09-11"
    assert len(wk[BOOGIE]) == 1 and wk[BOOGIE][0]["week_start"] == "1977-06-11"
    weeks_total = 1 + 2 + 1 + 1
    assert weeks_total == 5

    rk = {t: ye[t]["rank"] for t in ye}
    yr_of = {t: ye[t]["year"] for t in ye}
    n = len(INFO)
    assert n == 12
    top_ten = [t for t in INFO if INFO[t][1] <= 10]
    assert len(top_ten) == 6, top_ten
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
    album_rows = [[html.escape(t), INFO[t][2], html.escape(INFO[t][3]), html.escape(INFO[t][4])]
                  for t in ORDER if INFO[t][3] and INFO[t][4]]
    assert len(album_rows) == 9, len(album_rows)
    bside_rows = [
        [GDT, "You Don't Know", "February 1975"],
        [TTW, "What Makes You Happy", "June 1975"],
        [SHAKE, "Boogie Shoes", "May 1976"],
        [BOOGIE, "Wrap Your Arms Around Me", "February 1977"],
        [KEEP, "Baby I Love You", "May 1977"],
        [PLEASE, "I Betcha Didn't Know That", "July 1979"],
    ]
    bside_rows = [[html.escape(a), html.escape(b), c] for a, b, c in bside_rows]

    faq = [
        ("How many number one songs did KC and the Sunshine Band have?",
         ["KC and the Sunshine Band had five Billboard Hot 100 number ones, according to Wikipedia: four in the 1970s and the first of the 1980s.",
          "The four 70s chart-toppers were Get Down Tonight, That's the Way (I Like It), (Shake, Shake, Shake) Shake Your Booty and I'm Your Boogie Man.",
          "The fifth, Please Don't Go, reached number one for one week in January 1980."]),
        ("Who wrote the KC and the Sunshine Band songs?",
         ["Harry Wayne Casey and Richard Finch wrote and produced almost all of the KC and the Sunshine Band songs on this page, according to Wikipedia.",
          "Casey is the KC of the name, and Finch was a bassist and engineer at TK Records.",
          "The exception here is It's the Same Old Song, a cover of the 1965 Four Tops hit that Holland, Dozier and Holland wrote."]),
        ("Was Boogie Shoes in Saturday Night Fever?",
         ["Boogie Shoes was on the 1977 Saturday Night Fever soundtrack, according to Wikipedia.",
          "It had first been the B-side of (Shake, Shake, Shake) Shake Your Booty in 1976.",
          "TK Records released it as a single in January 1978, and it reached number 35 on the Hot 100."]),
        ("Did KC write Rock Your Baby?",
         ["Harry Wayne Casey wrote Rock Your Baby while working on demos for the band, and guitarist Jerome Smith played on it, according to Wikipedia.",
          "George McCrae recorded it, and Wikipedia says it became a number one hit in 51 countries in mid-1974.",
          "It is a McCrae record, so it is not one of the songs on this page."]),
        ("What was KC and the Sunshine Band's last number one hit?",
         ["Please Don't Go was the band's last number one hit, according to Wikipedia.",
          "KC and the Sunshine Band released it on July 12, 1979, and it held the top spot for one week in January 1980.",
          "It was the band's first ballad, and Wikipedia says the group broke up shortly after, when Casey began a solo career."]),
        ("Where was KC and the Sunshine Band from?",
         ["KC and the Sunshine Band came from South Florida, where Harry Wayne Casey formed the group in 1973 while working at TK Records in Hialeah, according to Wikipedia.",
          "It was first called KC & The Sunshine Junkanoo Band.",
          "The Sunshine Band part of the name refers to Florida, the Sunshine State."]),
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

    TITLE = f"KC and the Sunshine Band Songs: {n} Hits Played, 5 at No. 1"
    desc = (f"KC and the Sunshine Band songs of the 70s, all {n} playable: Get Down Tonight, Boogie Shoes and more. "
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

    toc = [("kc-and-the-sunshine-band-songs-list", f"KC and the Sunshine Band Songs: Play All {n} Hits"),
           ("by-the-numbers", "KC and the Sunshine Band Songs on the Charts: Five Number Ones, Six Top Tens"),
           ("origins", "Hialeah and TK Records: Where the KC and the Sunshine Band Songs Began"),
           ("year-1974-75", "1974 and 1975: Queen of Clubs, Get Down Tonight and That's the Way (I Like It)"),
           ("year-1976", "1976: (Shake, Shake, Shake) Shake Your Booty and I Like to Do It"),
           ("year-1977", "1977: I'm Your Boogie Man, Keep It Comin' Love and Wrap Your Arms Around Me"),
           ("year-1978-79", "1978 and 1979: Boogie Shoes, It's the Same Old Song and Please Don't Go"),
           ("beyond-the-charts", "Beyond the Charts: Grammy Nominations and Later Honors"),
           ("b-sides", "B-Sides and Covers: The Songs Behind the KC and the Sunshine Band Hits"),
           ("who-wrote-what", "Who Wrote and Released Each of the KC and the Sunshine Band Songs"),
           ("sources", "Sources"), ("faq", "Frequently Asked Questions")]
    toc_html = "\n".join(f'            <li><a href="#{i}">{t}</a></li>' for i, t in toc)

    feat_pic = pic(IMG, "KC and the Sunshine Band on stage in Chile in September 1980, the band behind the KC and the Sunshine Band songs of the 70s",
                   "(max-width: 700px) 100vw, 800px", 800, 562, widths=(400, 800), lazy=False).replace(
        'class="post-featured-img"', 'class="post-featured-img" style="aspect-ratio:800/562;max-width:800px;height:auto;margin:1.5rem auto"', 1)
    pic2 = pic(IMG2, "Harry Wayne Casey of KC and the Sunshine Band performing at the Del Mar Fairgrounds in California in 2006",
               "(max-width: 700px) 100vw, 775px", 775, 600, widths=(400, 775)).replace(
        "<img\n", '<img style="display:block;width:100%;max-width:775px;height:auto;margin:1.5rem auto;border-radius:8px"\n', 1)
    chart_pic = pic(CHART, "Lollipop chart of twelve KC and the Sunshine Band songs by Hot 100 peak, from five number ones to Queen of Clubs at number 66",
                    "(max-width: 700px) 100vw, 800px", 800, 450, widths=(400, 800, 1200)).replace(
        "<img\n", '<img style="display:block;width:100%;max-width:800px;height:auto;margin:1.5rem auto;border-radius:8px"\n', 1)

    body = f'''        <h2 id="kc-and-the-sunshine-band-songs-list">KC and the Sunshine Band Songs: Play All {n} Hits</h2>
{p(f"Here are {NUM[n]} hits from 1974 to 1979, from Queen of Clubs to Please Don't Go.",
   "Five sit on a Billboard Year-End Hot 100, and seven more charted weekly without making a year-end list.",
   "Press Play on any row to watch it here, and tap a heading to sort.")}

        <div class="data-table-wrap scroll-list">
          <table class="data-table sortable-table" id="kcSunshineBandSongsTable" data-inline-player>
            <caption>{n} KC and the Sunshine Band songs of the 70s, with release year, Billboard Year-End Hot 100 rank and Hot 100 peak</caption>
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
   "Hot 100 Peak is the weekly peak, from each song's Wikipedia article or the band's discography article.",
   "Four number ones are Hot 100 chart toppers in this site's weekly chart data, and Please Don't Go reached number one in January 1980.")}

        <h2 id="by-the-numbers">KC and the Sunshine Band Songs on the Charts: Five Number Ones, Six Top Tens</h2>
{p("The band's run was a steady climb from 1975 to 1977.",
   "Five songs reached number one on the Hot 100, and this site's weekly data gives the first four five weeks at the top between them.",
   "Get Down Tonight held the top spot in the week starting August 30, 1975.",
   "That's the Way (I Like It) held it in the weeks starting November 22 and December 20, 1975.",
   "(Shake, Shake, Shake) Shake Your Booty did it in the week starting September 11, 1976, and I'm Your Boogie Man in the week starting June 11, 1977.")}

{chart_pic}
        <p class="post-img-caption">Hot 100 peaks of the twelve hits on this page, from each song's Wikipedia article and the band's discography article.</p>

{tbl("KC and the Sunshine Band songs of the 70s ranked by weekly Hot 100 peak, with release date (Wikipedia)", ["Song", "Hot 100 Peak", "Released"], peak_rows)}

        <h3>What the Chart Numbers Say</h3>
{p(f"Six of the {NUM[n]} hits on this page reached the Hot 100's top ten.")}
        <ul>
          <li>Get Down Tonight, That's the Way (I Like It), Shake Your Booty and I'm Your Boogie Man all reached number one in 1975 to 1977.</li>
          <li>Keep It Comin' Love stopped at number two in 1977, and Please Don't Go reached number one in January 1980.</li>
          <li>I'm Your Boogie Man ranks #{rk[BOOGIE]} on the 1977 Year-End Hot 100, the highest of the band's five year-end songs.</li>
          <li>(Shake, Shake, Shake) Shake Your Booty ranks #{rk[SHAKE]} on the 1976 list, and That's the Way (I Like It) ranks #{rk[TTW]} on it.</li>
          <li>Get Down Tonight ranks #{rk[GDT]} on the 1975 list, and Keep It Comin' Love ranks #{rk[KEEP]} on the 1977 list.</li>
          <li>Four songs on this page reached number one on the R&B chart, per Wikipedia.</li>
        </ul>

        <h2 id="origins">Hialeah and TK Records: Where the KC and the Sunshine Band Songs Began</h2>
{p("The KC and the Sunshine Band songs of the 70s came out of one Florida record label.",
   "Harry Wayne Casey formed the band in 1973 while working in a record store and part time at TK Records in Hialeah, Florida.",
   "It was first called KC & The Sunshine Junkanoo Band, and Sunshine refers to Florida, the Sunshine State.")}

        <h3>Casey, Finch and the Studio Players</h3>
{p("Bassist Richard Finch was engineering records at TK, and that led to his partnership with Casey.",
   "Guitarist Jerome Smith and drummer Robert Johnson, both TK studio musicians, joined soon after.",
   "Casey and Finch wrote and produced most of the band's hits on this page.")}

        <h3>Rock Your Baby: A Hit for Someone Else</h3>
{p("Casey wrote Rock Your Baby while working on demos for the band, and Smith played guitar on it.",
   "George McCrae recorded it, and Wikipedia says it became a number one hit in 51 countries in mid-1974.",
   "It is a McCrae record, so it is not on the playable list above.",
   'For the genre it helped launch, read the page on <a href="/blog/genres/disco-music-of-the-70s/">disco music of the 70s</a>.')}

        <h2 id="year-1974-75">1974 and 1975: Queen of Clubs, Get Down Tonight and That's the Way (I Like It)</h2>
{p("The band's first Hot 100 entry came in 1974, and its first number one followed a year later.")}

        <h3>Queen of Clubs</h3>
{p("Queen of Clubs came out in 1974, and the discography lists it at number 66 on the Hot 100 and number 25 on the R&B chart.",
   "It is on no 1970s year-end list, so its peak above is a weekly peak only.")}

        <h3>Get Down Tonight</h3>
{p("Get Down Tonight was released on February 11, 1975 by TK Records, as the first single from the band's self-titled album.",
   "Casey and Finch wrote and produced it, and it was first titled What You Want Is What You Get.",
   "Its introduction features a guitar solo played at double speed.")}
{p("It reached number one on the Soul chart in April 1975 and on the Hot 100 in August 1975.",
   "This site's weekly data gives it one week at the top, starting August 30.",
   f"It ranks #{rk[GDT]} on the 1975 Year-End Hot 100, and Wikipedia gives it a platinum certification from the RIAA.")}
{p("VH1 ranked it number 12 on its 100 Greatest Dance Songs list in 2000, and Rolling Stone ranked it number 100 on its 200 Greatest Dance Songs of All Time list in 2022.",
   "The house act Bamboo sampled it in Bamboogie, which reached number two in the UK in 1998.",
   'See where it landed among that year&#39;s hits on the page for <a href="/blog/years/top-songs-of-1975/">top songs of 1975</a>.')}

        <h3>That's the Way (I Like It)</h3>
{p("That's the Way (I Like It) came out on June 10, 1975, on the same self-titled album.",
   "Casey and Finch wrote and produced it, with What Makes You Happy on the flip.",
   "Wikipedia says its sexual overtones may have helped it in the discos.")}
        <h3>Number One Twice in a Month</h3>
{p("It reached number one for one week, and then Silver Convention's Fly, Robin, Fly replaced it.",
   "After that song spent three weeks at the top, it returned for one more week.",
   "Wikipedia calls it one of the few songs to reach number one more than once in a one-month span.",
   f"This site's weekly data matches, with weeks starting November 22 and December 20, 1975, and it ranks #{rk[TTW]} on the 1976 Year-End Hot 100.")}
{p("It also reached number four in the UK, and the RIAA certified it platinum.",
   "Dead or Alive covered it in 1984, and their version reached number 22 in the UK.",
   "Clock covered it in 1997, and their version reached number 11 in the UK.",
   'Find the right mood for it with the <a href="/pages/mood-song-matcher">Mood Song Matcher</a>.')}

        <h2 id="year-1976">1976: (Shake, Shake, Shake) Shake Your Booty and I Like to Do It</h2>
{p("1976 gave the band its third number one, from the album Part 3.")}

        <h3>(Shake, Shake, Shake) Shake Your Booty</h3>
{p("(Shake, Shake, Shake) Shake Your Booty was released on May 28, 1976, from Part 3.",
   "Casey and Finch wrote and produced it, and its chorus repeats the word shake eight times.",
   "Its B-side was Boogie Shoes, which became a hit of its own two years later.")}
{p("It reached number one on the Hot 100 and on the soul chart, and this site's weekly data gives it one week at the top, starting September 11.",
   f"It ranks #{rk[SHAKE]} on the 1976 Year-End Hot 100, and Wikipedia lists it at #218 on the all-time Hot 100.",
   "The RIAA certified it gold, and it earned a Grammy nomination at the 19th Annual Grammy Awards.",
   'Pick a random decade tune with the <a href="/pages/random-70s-song">Random 70s Song Generator</a>.')}

        <h3>I Like to Do It</h3>
{p("I Like to Do It was a 1976 single that reached number 37 on the Hot 100 and number four on the R&B chart, according to the discography.",
   "It is on no 1970s year-end list, so its peak above is a weekly peak only.")}

        <h2 id="year-1977">1977: I'm Your Boogie Man, Keep It Comin' Love and Wrap Your Arms Around Me</h2>
{p("1977 was the band's biggest year on the year-end list.",
   f"I'm Your Boogie Man ranks #{rk[BOOGIE]} on it, and Keep It Comin' Love ranks #{rk[KEEP]}.")}

        <h3>I'm Your Boogie Man</h3>
{p("I'm Your Boogie Man was released on February 3, 1977, from Part 3, with Wrap Your Arms Around Me on the flip.",
   "Casey and Finch wrote and produced it.",
   "Finch said it was written about the Miami disc jockey Robert W. Walker, who first played Get Down Tonight.")}
{p("It reached number one on the Hot 100 and number three on the soul chart.",
   "This site's weekly data gives it one week at the top, starting June 11, 1977.",
   "It also reached number one in Canada, and the RIAA certified it gold.",
   'Its year-end rank is on the page for <a href="/blog/years/top-songs-of-1977/">top songs of 1977</a>.')}
{p("White Zombie covered it as I'm Your Boogieman in 1996, for The Crow: City of Angels soundtrack.",
   "That version earned a Grammy nomination for Best Metal Performance at the 1997 ceremony.")}

        <h3>Keep It Comin' Love</h3>
{p("Keep It Comin' Love was released on May 16, 1977, from Part 3, with Baby I Love You on the flip.",
   "Casey and Finch wrote and produced it.",
   "It reached number one on the soul chart and number one in Canada.")}
{p("On the Hot 100, it stopped at number two.",
   "Wikipedia says Meco's Star Wars Theme/Cantina Band and Debby Boone's You Light Up My Life kept it from the top.",
   f"It ranks #{rk[KEEP]} on the 1977 Year-End Hot 100.",
   "Wikipedia says that, like That's the Way (I Like It), it succeeded partly through its sexual double entendres.")}

        <h3>Wrap Your Arms Around Me</h3>
{p("Wrap Your Arms Around Me was the B-side of I'm Your Boogie Man.",
   "It reached number 48 on the Hot 100 and number 24 on the R&B chart in 1977, according to the discography.",
   "It is on no 1970s year-end list, so its peak above is a weekly peak only.")}

        <h2 id="year-1978-79">1978 and 1979: Boogie Shoes, It's the Same Old Song and Please Don't Go</h2>
{p("The last two years of the decade brought a film hit, a flop, a party song and one more number one.")}

        <h3>Boogie Shoes</h3>
{p("Boogie Shoes was recorded in 1975 and first appeared on the band's self-titled album.",
   "It was the B-side of Shake Your Booty in 1976, and then it appeared on the 1977 Saturday Night Fever soundtrack.",
   "TK Records released it as a single in January 1978, and it reached number 35 on the Hot 100 and number 29 on the soul chart.")}
{p("It is on no 1970s year-end list, so its peak above is a weekly peak only.",
   "The RIAA has certified it two times platinum, and Wikipedia lists it in the films Boogie Nights and Mallrats.",
   "Alex Newell sang it in a 2012 Glee episode, and the Bloodhound Gang, Trick Daddy and Icandy sampled it.",
   'Test your memory of the decade with the <a href="/pages/70s-trivia-quiz">70s Music Trivia Quiz</a>.')}

        <h3>It's the Same Old Song</h3>
{p("It's the Same Old Song was a 1978 cover of the Four Tops hit that Holland, Dozier and Holland wrote.",
   "The Four Tops' original came out on July 9, 1965, and reached number five on the Hot 100.",
   "The band's version was the lead single from the album Who Do Ya Love.")}
{p("It reached number 35 on the Hot 100.",
   "Wikipedia calls it a relative flop for a disco cover that was expected to be a major hit.",
   "Casey blamed poor R&B airplay, and the band played it on the TV special Happy Birthday, Bob on May 29, 1978.")}

        <h3>Do You Wanna Go Party</h3>
{p("Do You Wanna Go Party was the title track of the band's 1979 album, which came out on June 22, 1979.",
   "Casey and Finch wrote it, and it reached number 50 on the Hot 100 and number eight on the R&B chart, per the discography.",
   "It is on no 1970s year-end list, so its peak above is a weekly peak only.")}

        <h3>Please Don't Go</h3>
{p("Please Don't Go was released on July 12, 1979, as the second single from Do You Wanna Go Party.",
   "Casey and Finch wrote and produced it, and Wikipedia calls it the band's first ballad.",
   "It reached number one in the US, Australia and Canada, and number three in the UK.")}
{p("Wikipedia says it held number one in the US for one week in January 1980, and that it was the first number one of the 1980s.",
   "The group broke up shortly after, and Casey began a solo career.",
   "Its B-side, I Betcha Didn't Know That, reached number 25 on the R&B chart.",
   'The band&#39;s run is also part of the story on the page for <a href="/blog/songs/70s-number-one-hits/">70s number one hits</a>.')}

        <h3>A Song That Kept Being Covered</h3>
{p("Other acts took Please Don't Go back up the charts.",
   "Double You covered it in 1992 and reached number one in Belgium, the Netherlands and Spain.",
   "KWS covered it in 1992, and their version spent five weeks at number one in the UK.",
   "It also reached number six on the US Hot 100 in October 1992.")}
{pic2}
        <p class="post-img-caption">Harry Wayne Casey of KC and the Sunshine Band performing at the Del Mar Fairgrounds in California in 2006.</p>
        <p class="post-img-caption">Image credit: BradP, CC BY-SA 3.0, via Wikimedia Commons.</p>

        <h2 id="beyond-the-charts">Beyond the Charts: Grammy Nominations and Later Honors</h2>
{p("The band's work did not stop at the singles chart.",
   "Wikipedia lists these milestones, alongside the KC and the Sunshine Band songs above.")}
        <ul>
          <li>1973: Casey formed the band in Hialeah, Florida.</li>
          <li>1974: George McCrae's Rock Your Baby, written by Casey, became a number one hit in 51 countries.</li>
          <li>1976: The band received two nominations at the 18th Annual Grammy Awards, in February 1976.</li>
          <li>1977: Shake Your Booty earned a nomination at the 19th Annual Grammy Awards.</li>
          <li>1979: Please Don't Go became the band's last number one.</li>
          <li>2002: The band received a star on the Hollywood Walk of Fame on August 2.</li>
          <li>2013: The band received a Palm Springs Golden Palm Star on July 6.</li>
        </ul>
{p("Wikipedia's article lists nominations for the 1970s Grammys, and it does not list a win.")}

        <h2 id="b-sides">B-Sides and Covers: The Songs Behind the KC and the Sunshine Band Hits</h2>
{p("Several KC and the Sunshine Band songs started life on the flip side of a single.",
   "Boogie Shoes and Wrap Your Arms Around Me are the two on this page.",
   'For more voices from the decade, try the <a href="/pages/random-artist-picker">Random Artist Picker</a>.')}

{tbl("KC and the Sunshine Band singles of the 70s and their B-sides (Wikipedia)", ["Single", "B-Side", "Released"], bside_rows)}

        <h3>Writers Behind the Hits</h3>
{p("Almost every song here came from the same two writers.")}
        <ul>
          <li>Harry Wayne Casey and Richard Finch: eight songs on this page, from Get Down Tonight to Please Don't Go.</li>
          <li>Holland, Dozier and Holland: It's the Same Old Song, first recorded by the Four Tops in 1965.</li>
          <li>Sources do not name the writers of Queen of Clubs, I Like to Do It or Wrap Your Arms Around Me.</li>
        </ul>

        <h2 id="who-wrote-what">Who Wrote and Released Each of the KC and the Sunshine Band Songs</h2>
{p(f"The table lists when nine of the {NUM[n]} hits were released, on which album, and who wrote them.",
   "The other three have no writers or albums stated in the sources used.")}

{tbl("KC and the Sunshine Band songs of the 70s: release date, album and writers (Wikipedia)", ["Song", "Released", "Album", "Written By"], album_rows)}

        <h3>Keep Exploring</h3>
{p("These KC and the Sunshine Band songs gave the decade five number ones and a long run of dance floor hits.",
   "Six of the twelve reached the top ten.",
   'Another act with a rise through the same years is covered on the page for <a href="/blog/artists/earth-wind-and-fire-songs/">Earth, Wind & Fire songs</a>.')}

        <h2 id="sources">Sources</h2>
{p("Year-end ranks come from this site's own Billboard data, described on the <a href='/about/methodology/'>methodology page</a>.",
   'Every list on <a href="/">Music of the 70s</a> plays inside the page.',
   "Peaks, dates and stories behind the KC and the Sunshine Band songs above can be checked against these outside sources:")}
        <ul>
          <li><a href="https://en.wikipedia.org/wiki/KC_and_the_Sunshine_Band" rel="noopener">Wikipedia: KC and the Sunshine Band</a> and <a href="https://en.wikipedia.org/wiki/KC_and_the_Sunshine_Band_discography" rel="noopener">their discography</a> for the lineup, honors, singles and chart peaks.</li>
          <li><a href="https://en.wikipedia.org/wiki/Get_Down_Tonight" rel="noopener">Wikipedia: Get Down Tonight</a> and <a href="https://en.wikipedia.org/wiki/That%27s_the_Way_(I_Like_It)" rel="noopener">That's the Way (I Like It)</a> for 1975.</li>
          <li><a href="https://en.wikipedia.org/wiki/(Shake,_Shake,_Shake)_Shake_Your_Booty" rel="noopener">Wikipedia: (Shake, Shake, Shake) Shake Your Booty</a> for 1976.</li>
          <li><a href="https://en.wikipedia.org/wiki/I%27m_Your_Boogie_Man" rel="noopener">Wikipedia: I'm Your Boogie Man</a> and <a href="https://en.wikipedia.org/wiki/Keep_It_Comin%27_Love" rel="noopener">Keep It Comin' Love</a> for 1977.</li>
          <li><a href="https://en.wikipedia.org/wiki/Boogie_Shoes" rel="noopener">Wikipedia: Boogie Shoes</a>, <a href="https://en.wikipedia.org/wiki/It%27s_the_Same_Old_Song" rel="noopener">It's the Same Old Song</a> and <a href="https://en.wikipedia.org/wiki/Please_Don%27t_Go_(KC_and_the_Sunshine_Band_song)" rel="noopener">Please Don't Go</a> for 1978 and 1979.</li>
        </ul>

        <section class="faq-block" id="faq">
          <h2>Frequently Asked Questions</h2>
{faq_html}
        </section>'''

    related = [
        ("earth-wind-and-fire-1977", "Artists", "Earth Wind and Fire Songs: 12 Hits Played, 1 at No. 1", "/blog/artists/earth-wind-and-fire-songs/",
         "Another act that ruled the dance floor and the R&B chart in the 70s.", "Earth, Wind & Fire in 1977"),
        ("donna-1977", "Artists", "Donna Summer: The 1977 Hit Too Influential for the Charts", "/blog/artists/donna-summer/",
         "The disco queen whose sound changed the decade's dance floors.", "Donna Summer in 1977"),
        ("village-people-1970s", "Artists", "Village People in the 70s: The Disco Act Everyone Missed", "/blog/artists/village-people/",
         "Another disco act, with a story the charts missed.", "Village People in the 1970s"),
    ]

    cards = []
    for img, cat, title, href, blurb, alt in related:
        big = 669 if img == "earth-wind-and-fire-1977" else 800
        bigjpg = f"/images/blog/{img}-{big}w.jpg" if img == "earth-wind-and-fire-1977" else f"/images/blog/srcset/{img}-{big}w.jpg"
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
      {{"@type": "ListItem", "position": 4, "name": "KC and the Sunshine Band Songs", "item": "{URL}"}}
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
        KC and the Sunshine Band Songs
      </nav>

      <article class="section seo-content">
        <h1>{TITLE}</h1>

        <p class="post-byline">By <a href="https://musicofthe70s.net/about/author/">Charlie</a> &middot; Published {PUBLISHED.strftime('%B')} {PUBLISHED.day}, {PUBLISHED.year}</p>
        <p class="jump-to-list"><a class="btn-primary jump-btn" href="#kc-and-the-sunshine-band-songs-list">&#9654; Jump to the playable list</a></p>

        <p class="post-intro">KC and the Sunshine Band songs filled the dance floors of the late 70s.</p>
        <p class="post-intro">Five of them reached number one on the Hot 100, four in the decade itself and one in January 1980.</p>
        <p class="post-intro">This page plays {NUM[n]} of them, from Queen of Clubs to Please Don't Go.</p>
        <p class="post-intro">Six reached the Hot 100's top ten, and almost all were written by Harry Wayne Casey and Richard Finch.</p>
        <p class="post-intro">Some began as B-sides, and one was a cover of a Four Tops hit.</p>
        <p class="post-intro">Press Play on every hit below, then read the story behind each one.</p>

{feat_pic}
        <p class="post-img-caption">KC and the Sunshine Band in concert in Chile in September 1980, during the group's first show there.</p>
        <p class="post-img-caption">Image credit: Artekolor, CC BY 4.0, via Wikimedia Commons.</p>

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
