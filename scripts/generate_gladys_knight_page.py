#!/usr/bin/env python3
"""Build the Gladys Knight Songs Artists post (blog/artists/gladys-knight-songs/index.html).

Data: data/radio/radio-songs.json (seven Gladys Knight & the Pips rows of the 1971-1975 Year-End Hot 100, each with a
YouTube ID), data/billboard/hot100_weekly.json (Midnight Train to Georgia, the one Hot 100 number one in the site's
1970-1979 weekly data), data/billboard/beyond_year_end.json (five further singles on the weekly Hot 100 but on no
1970s year-end list: I Don't Want to Do Wrong, Daddy Could Swear, I Declare, Where Peaceful Waters Flow, I Feel a Song
(In My Heart) and Part Time Love; peaks and Topic/VEVO YouTube IDs checked).
Year-End Rank is the year-end rank, never a peak. Hot 100 peaks, release dates, writers and story facts come from the
linked Wikipedia articles and the group's discography article, checked 2026-10-15, and are credited to Wikipedia.
The site JSON's fun_fact and trivia text for the group is not used.

Run: python3 scripts/generate_gladys_knight_page.py
"""
import html
import json
from datetime import date

from genre_page_common import ROOT, read, play_button, write
from generate_country_page import p, tbl, pic

SLUG = "gladys-knight-songs"
PAGE = f"blog/artists/{SLUG}/"
URL = f"https://musicofthe70s.net/{PAGE}"
IMG = "gladys-knight-1974"
IMG2 = "gladys-knight-soul-train"
CHART = "gladys-knight-peaks"
PUBLISHED = date(2026, 10, 15)
ARTIST = "Gladys Knight & the Pips"
NUM = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
       10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen"}

IFI, IDW, NEITHER, MIDNIGHT = "If I Were Your Woman", "I Don't Want to Do Wrong", "Neither One of Us (Wants to Be the First to Say Goodbye)", "Midnight Train to Georgia"
IGU, BEST, ONON = "I've Got to Use My Imagination", "Best Thing That Ever Happened to Me", "On and On"
DADDY, WATERS, IFEEL = "Daddy Could Swear, I Declare", "Where Peaceful Waters Flow", "I Feel a Song (In My Heart)"
WAY, PART = "The Way We Were/Try to Remember", "Part Time Love"

# title -> (release year, Hot 100 peak, released text, album, written by)
# Every value read from the song's Wikipedia article or the group's discography article, checked 2026-10-15.
# Album and writers are "" where neither article states them.
INFO = {
    IFI: (1970, 9, "November 1970", "If I Were Your Woman", "Pam Sawyer, Clay McMurray and Gloria Jones"),
    IDW: (1971, 17, "1971", "If I Were Your Woman", "Johnny Bristol, Gladys Knight, Merald Knight, William Guest and Katherine Anderson-Schaffner"),
    NEITHER: (1972, 2, "December 1972", "Neither One of Us", "Jim Weatherly"),
    MIDNIGHT: (1973, 1, "August 1973", "Imagination", "Jim Weatherly"),
    DADDY: (1973, 19, "1973", "Neither One of Us", ""),
    WATERS: (1973, 28, "1973", "Imagination", ""),
    IGU: (1973, 4, "November 1973", "Imagination", "Gerry Goffin and Barry Goldberg"),
    BEST: (1974, 3, "February 1974", "Imagination", "Jim Weatherly"),
    ONON: (1974, 5, "April 1974", "Claudine (soundtrack)", "Curtis Mayfield"),
    IFEEL: (1974, 21, "October 1974", "I Feel a Song", "Tony Camillo and Mary Sawyer"),
    WAY: (1975, 11, "1975", "", ""),
    PART: (1975, 22, "1975", "", ""),
}
ORDER = list(INFO)
BEYOND = {IDW, DADDY, WATERS, IFEEL, PART}
YE_SET = {IFI, NEITHER, MIDNIGHT, IGU, BEST, ONON, WAY}


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

    # weekly number ones by the group in the site's own 1970-1979 data
    wk = {}
    for yr in weekly:
        for w in weekly[yr]:
            if w["artist"] == ARTIST:
                wk.setdefault(w["title"], []).append(w)
    assert set(wk) == {MIDNIGHT}, set(wk)
    assert len(wk[MIDNIGHT]) == 2 and all(w["weeks_at_number_one"] == 2 for w in wk[MIDNIGHT])
    assert wk[MIDNIGHT][0]["week_start"] == "1973-10-27", wk[MIDNIGHT][0]["week_start"]

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
    assert len(album_rows) == 8, len(album_rows)
    first_rows = [
        [MIDNIGHT, "Jim Weatherly, as Midnight Plane to Houston; Cissy Houston then recorded it as Midnite Train to Georgia in 1973"],
        [NEITHER, "Jim Weatherly, before the group recorded it"],
        [BEST, "Ray Price, whose 1973 country single reached number one on Hot Country Singles and number 82 on the Hot 100"],
        [ONON, "The Impressions, in 1972, as Our Love Goes On and On"],
        [IFEEL, "Sandra Richardson, in 1971; the group's version was the song's fourth recording"],
    ]

    faq = [
        ("What is Gladys Knight's most famous song?",
         ["Gladys Knight's most famous song is Midnight Train to Georgia, which she recorded with the Pips in 1973.",
          "It reached number one on the Billboard Hot 100 on October 27, 1973, and stayed there for two weeks.",
          "It won the 1974 Grammy for Best R&B Vocal Performance by a Duo, Group or Chorus.",
          "It entered the Grammy Hall of Fame in 1999."]),
        ("How many number one songs did Gladys Knight and the Pips have in the 70s?",
         ["Gladys Knight & the Pips had one Hot 100 number one in the 70s, Midnight Train to Georgia, with two weeks at the top in 1973.",
          "They also topped the R&B chart with six songs on this page.",
          "Those include If I Were Your Woman, Neither One of Us and Best Thing That Ever Happened to Me."]),
        ("Who wrote Midnight Train to Georgia?",
         ["Jim Weatherly wrote Midnight Train to Georgia, according to Wikipedia.",
          "He first recorded it himself as Midnight Plane to Houston.",
          "Cissy Houston recorded it as Midnite Train to Georgia in 1973, and Gladys Knight & the Pips kept that title.",
          "Knight wrote that she and Bubba Knight worked with Weatherly to rewrite the lyrics so she would be more comfortable singing them."]),
        ("Did Gladys Knight and the Pips win a Grammy for Neither One of Us?",
         ["Neither One of Us won the Grammy for Best Pop Vocal Performance by a Duo or Group, at the March 2, 1974 ceremony, according to Wikipedia.",
          "It reached number two on the Hot 100, held from number one by Vicki Lawrence's The Night the Lights Went Out in Georgia.",
          "It was number one on the R&B chart for four weeks from March 17, 1973."]),
        ("Who were the Pips in Gladys Knight and the Pips?",
         ["The Pips were Merald Bubba Knight, William Guest and Edward Patten, who sang with Gladys Knight throughout the 1970s, according to Wikipedia.",
          "Patten had joined in 1959.",
          "The group left Motown in February 1973 after contract talks failed and signed with Buddah Records, where they made Midnight Train to Georgia."]),
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

    TITLE = f"Gladys Knight Songs: {n} Hits Played, 1 at Number One"
    desc = (f"Gladys Knight songs of the 70s, all {n} playable: Midnight Train to Georgia, Neither One of Us and more. "
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
    "image": "https://musicofthe70s.net/images/blog/{IMG}-668w.jpg",
    "mainEntityOfPage": "{URL}"
  }}'''

    toc = [("gladys-knight-songs-list", f"Gladys Knight Songs: Play All {n} Hits"),
           ("by-the-numbers", "Gladys Knight Songs on the Charts: One Number One, Six Top Tens"),
           ("origins", "The Pips and Motown: Who Sang on Every Gladys Knight Song"),
           ("year-1970-72", "1970 to 1972: If I Were Your Woman, I Don't Want to Do Wrong and Neither One of Us"),
           ("year-1973", "1973: Midnight Train to Georgia, I've Got to Use My Imagination and More"),
           ("year-1974", "1974: Best Thing That Ever Happened to Me, On and On and I Feel a Song"),
           ("year-1975", "1975: The Way We Were/Try to Remember and Part Time Love"),
           ("beyond-the-charts", "Beyond the Charts: Awards, Television and Contract Fights"),
           ("earlier-versions", "Songs with Earlier Versions: Who Sang Each Gladys Knight Song First"),
           ("who-wrote-what", "Who Wrote and Released Each of the Gladys Knight Songs"),
           ("sources", "Sources"), ("faq", "Frequently Asked Questions")]
    toc_html = "\n".join(f'            <li><a href="#{i}">{t}</a></li>' for i, t in toc)

    feat_pic = pic(IMG, "Black and white 1974 CBS Television publicity photo of Gladys Knight, the voice behind the Gladys Knight songs of the 70s, smiling in a dark top",
                   "(max-width: 700px) 100vw, 668px", 668, 892, widths=(400, 668), lazy=False).replace(
        'class="post-featured-img"', 'class="post-featured-img" style="aspect-ratio:668/892;max-width:668px;height:auto;margin:1.5rem auto"', 1)
    pic2 = pic(IMG2, "Gladys Knight and the Pips performing on the television program Soul Train, in a 1974 Billboard section about the show",
               "(max-width: 700px) 100vw, 800px", 800, 352, widths=(400, 800)).replace(
        "<img\n", '<img style="display:block;width:100%;max-width:800px;height:auto;margin:1.5rem auto;border-radius:8px"\n', 1)
    chart_pic = pic(CHART, "Lollipop chart of twelve Gladys Knight songs by Hot 100 peak, from Midnight Train to Georgia at number one to Where Peaceful Waters Flow at number 28",
                    "(max-width: 700px) 100vw, 800px", 800, 450, widths=(400, 800, 1200)).replace(
        "<img\n", '<img style="display:block;width:100%;max-width:800px;height:auto;margin:1.5rem auto;border-radius:8px"\n', 1)

    body = f'''        <h2 id="gladys-knight-songs-list">Gladys Knight Songs: Play All {n} Hits</h2>
{p(f"Here are {NUM[n]} hits from 1970 to 1975, from If I Were Your Woman to Part Time Love.",
   "Seven sit on a Billboard Year-End Hot 100, and five more charted weekly without making a year-end list.",
   "Press Play on any row to watch it here, and tap a heading to sort.")}

        <div class="data-table-wrap scroll-list">
          <table class="data-table sortable-table" id="gladysKnightSongsTable" data-inline-player>
            <caption>{n} Gladys Knight & the Pips songs of the 70s, with release year, Billboard Year-End Hot 100 rank and Hot 100 peak</caption>
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
   "Hot 100 Peak is the weekly peak, from each song's Wikipedia article or the group's discography article.",
   "The one number one is the Hot 100 chart topper in this site's weekly chart data.")}

        <h2 id="by-the-numbers">Gladys Knight Songs on the Charts: One Number One, Six Top Tens</h2>
{p("The group's 70s hits were bigger on the soul chart than on the pop chart.",
   "One reached number one on the Hot 100, and this site's weekly data gives it two weeks at the top.",
   "Midnight Train to Georgia held the top spot in the weeks starting October 27 and November 3, 1973.",
   "Wikipedia says it replaced Angie by the Rolling Stones.")}

{chart_pic}
        <p class="post-img-caption">Hot 100 peaks of the twelve hits on this page, from each song's Wikipedia article and the group's discography article.</p>

{tbl("Gladys Knight & the Pips songs of the 70s ranked by weekly Hot 100 peak, with release date (Wikipedia)", ["Song", "Hot 100 Peak", "Released"], peak_rows)}

        <h3>What the Chart Numbers Say</h3>
{p(f"Six of the {NUM[n]} hits on this page reached the Hot 100's top ten.")}
        <ul>
          <li>Midnight Train to Georgia was the only number one, in 1973.</li>
          <li>Neither One of Us stopped at number two, and Best Thing That Ever Happened to Me at number three.</li>
          <li>I've Got to Use My Imagination reached number four, and On and On reached number five.</li>
          <li>If I Were Your Woman rounded out the top ten at number nine.</li>
          <li>Best Thing That Ever Happened to Me ranks #{rk[BEST]} on the 1974 Year-End Hot 100, ahead of I've Got to Use My Imagination at #{rk[IGU]} and On and On at #{rk[ONON]}.</li>
          <li>Six songs on this page reached number one on the R&B chart, per Wikipedia.</li>
        </ul>

        <h2 id="origins">The Pips and Motown: Who Sang on Every Gladys Knight Song</h2>
{p("The Gladys Knight songs of the 70s were group records.",
   "Wikipedia says the lineup all through the decade was Gladys Knight, her brother Merald Bubba Knight, William Guest and Edward Patten.",
   "Patten joined in 1959, and the three men sang the call-and-response parts behind her lead.")}

        <h3>Leaving Motown for Buddah</h3>
{p("The group started the decade on Motown, where Neither One of Us became their biggest seller.",
   "Wikipedia says contract talks failed, and they left Motown in February 1973 for Buddah Records.",
   "Neither One of Us came out in December 1972, during the dispute.",
   "Midnight Train to Georgia followed on Buddah in August 1973.")}

        <h3>The Group on Television</h3>
{p("The group also reached viewers through television.",
   "Their Soul Train appearance is in a Billboard section about the show, dated September 28, 1974.")}
{pic2}
        <p class="post-img-caption">Gladys Knight and the Pips on Soul Train, from a September 28, 1974 Billboard special section.</p>
        <p class="post-img-caption">Image credit: Soul Train, Billboard page ST-10, public domain (US), via Wikimedia Commons.</p>

        <h2 id="year-1970-72">1970 to 1972: If I Were Your Woman, I Don't Want to Do Wrong and Neither One of Us</h2>
{p("The first three Gladys Knight songs here were all Motown hits.",
   "Two reached the top two of the soul chart, and one reached number one.")}

        <h3>If I Were Your Woman</h3>
{p("If I Were Your Woman was recorded on March 13, 1970 at Hitsville USA in Detroit.",
   "Pam Sawyer, Clay McMurray and Gloria Jones wrote it, and McMurray produced it, with Paul Riser as arranger.",
   "Motown released it on its Soul Records label in November 1970.",
   f"It reached number nine on the Hot 100 and number one on the soul chart for one week in January 1971, and it ranks #{rk[IFI]} on the 1971 Year-End Hot 100.")}
{p("George Michael performed it at the Nelson Mandela 70th Birthday Tribute at Wembley Stadium on June 11, 1988, and Stephanie Mills charted with it in 1988.",
   "Alicia Keys recorded it in 2003, and her full version on Unplugged earned a 2006 Grammy nomination for Best Traditional R&B Vocal Performance.",
   'To meet another voice from the decade, spin the <a href="/pages/random-artist-picker">Random Artist Picker</a>.')}

        <h3>I Don't Want to Do Wrong</h3>
{p("I Don't Want to Do Wrong came out in 1971, from the album If I Were Your Woman.",
   "Johnny Bristol produced it, and Bristol, the four members of the group and Katherine Anderson-Schaffner wrote it.",
   "It reached number 17 on the Hot 100 and number two on the soul chart.",
   "It is on no 1970s year-end list, so its peak above is a weekly peak only.")}

        <h3>Neither One of Us (Wants to Be the First to Say Goodbye)</h3>
{p("Jim Weatherly wrote Neither One of Us and recorded it before the group did.",
   "Joe Porter picked it from Weatherly's publishing catalog, and Knight recorded her lead vocal in one take at MoWest in Los Angeles.",
   "The group later returned to add background vocals and to redo her lead.")}
{p("It reached number two on the Hot 100, held from number one by Vicki Lawrence's The Night the Lights Went Out in Georgia.",
   "It was number one on the soul chart on March 17, 1973 and stayed there for four weeks.",
   f"It ranks #{rk[NEITHER]} on the 1973 Year-End Hot 100, and it won the Grammy for Best Pop Vocal Performance by a Duo or Group on March 2, 1974.",
   'See where it landed among 1973 hits on the page for <a href="/blog/years/top-songs-of-1973/">top songs of 1973</a>.')}

        <h3>More Motown Hits</h3>
{p("Three more Motown singles reached the Hot 100 in these years.")}
        <ul>
          <li>You Need Love Like I Do (Don't You) reached number 25 on the Hot 100 and number three on the R&B chart in 1970.</li>
          <li>Make Me the Woman That You Go Home To reached number 27 and number three on the R&B chart in 1971.</li>
          <li>Help Me Make It Through the Night reached number 33 and number 13 on the R&B chart in 1972.</li>
        </ul>

        <h2 id="year-1973">1973: Midnight Train to Georgia, I've Got to Use My Imagination and More</h2>
{p("1973 gave Gladys Knight songs their one Hot 100 number one.",
   "The year also gave the album Imagination, the group's first on Buddah Records.",
   "Wikipedia says it sold a million copies and produced two top ten singles.")}

        <h3>Midnight Train to Georgia</h3>
{p("Jim Weatherly wrote Midnight Train to Georgia, and first recorded it as Midnight Plane to Houston.",
   "Sonny Limbo wanted to record it with Cissy Houston, and asked Weatherly if he minded changing the title.",
   "Weatherly agreed, saying: &quot;Just don't change the rest of the song.&quot;",
   "Houston recorded it as Midnite Train to Georgia in 1973, and the group kept her title.")}
{p("Knight wrote that she and Bubba Knight worked with Weatherly to rewrite the lyrics so she would be more comfortable with them.",
   "Tony Camillo and the group produced their version, and Buddah released it in August 1973 from Imagination.")}
        <h3>Number One on the Hot 100</h3>
{p("It entered the Hot 100 at number 71, and reached number one on October 27, 1973.",
   "This site's weekly data gives it two weeks at the top.",
   "It also topped the soul chart.")}
        <ul>
          <li>The RIAA certified it gold on October 18, 1973, for one million copies.</li>
          <li>It won the 1974 Grammy for Best R&B Vocal Performance by a Duo, Group or Chorus.</li>
          <li>It entered the Grammy Hall of Fame in 1999.</li>
          <li>It also won Favorite Soul/R&B Single at the 1975 American Music Awards.</li>
          <li>It ranks #{rk[MIDNIGHT]} on the 1973 Year-End Hot 100.</li>
        </ul>
{p('Its week at the top is one of the stories on the page about <a href="/blog/songs/70s-number-one-hits/">70s number one hits</a>.')}

        <h3>I've Got to Use My Imagination</h3>
{p("Gerry Goffin and Barry Goldberg wrote I've Got to Use My Imagination, and Kenny Kerner produced it.",
   "Buddah released it in November 1973 from Imagination.",
   "It reached number four on the Hot 100 and number one on the soul chart for one week in early 1974.",
   f"It ranks #{rk[IGU]} on the 1974 Year-End Hot 100, and Wikipedia says it eventually sold more than one million copies.")}
{p("Joan Osborne, Bobby Bland and Joe Cocker are among the singers who covered it.",
   "It was also sung by characters on the television series A Different World.",
   'Find the right mood for it with the <a href="/pages/mood-song-matcher">Mood Song Matcher</a>.')}

        <h3>Daddy Could Swear, I Declare and Where Peaceful Waters Flow</h3>
{p("Two more Gladys Knight songs from 1973 reached the Hot 100 without making a year-end list.",
   "The discography article gives the details.")}
        <ul>
          <li>Daddy Could Swear, I Declare reached number 19 on the Hot 100 and number two on the R&B chart, from the album Neither One of Us.</li>
          <li>Where Peaceful Waters Flow reached number 28 on the Hot 100 and number six on the R&B chart, from the album Imagination.</li>
        </ul>

        <h2 id="year-1974">1974: Best Thing That Ever Happened to Me, On and On and I Feel a Song</h2>
{p("Gladys Knight songs in 1974 included three on the Year-End Hot 100.",
   f"Best Thing That Ever Happened to Me ranks #{rk[BEST]} on that list, I've Got to Use My Imagination #{rk[IGU]} and On and On #{rk[ONON]}.")}

        <h3>Best Thing That Ever Happened to Me</h3>
{p("Jim Weatherly wrote Best Thing That Ever Happened to Me.",
   "He told Tom Roland he wrote it in 1971, in about 30 minutes to an hour.",
   "Ray Price's country version reached number one on Hot Country Singles on October 6, 1973.")}
{p("The group's version came out in February 1974 on Buddah, from Imagination.",
   "It reached number three on the Hot 100 and number one on the soul chart for two weeks.",
   "It also reached number seven in the UK, and the RIAA certified it gold.",
   'The Carpenters sat on the same charts, and their hits are on the page for <a href="/blog/artists/carpenters-songs/">Carpenters songs</a>.')}

        <h3>On and On</h3>
{p("Curtis Mayfield wrote On and On and produced it for the film Claudine.",
   "The Impressions had first recorded it in 1972 as Our Love Goes On and On.",
   "Mayfield changed some lyrics and recut it with the group in 1974.")}
{p("Buddah released it in April 1974, with The Makings of You on the flip.",
   "It reached number five on the Hot 100, number two on the R&B chart and number 13 in Canada.",
   f"It ranks #{rk[ONON]} on the 1974 Year-End Hot 100, and it was nominated for a Golden Globe for Best Original Song.",
   'Test your memory of the decade with the <a href="/pages/70s-trivia-quiz">70s Music Trivia Quiz</a>.')}

        <h3>I Feel a Song (In My Heart)</h3>
{p("Tony Camillo and Mary Sawyer wrote I Feel a Song (In My Heart).",
   "Sandra Richardson made the original recording in 1971, and the group's version was the song's fourth.",
   "Linda Carr and the Stairsteps recorded it in 1972, and the Stairsteps used more spiritual lyrics.")}
{p("Buddah released it in October 1974, from the album I Feel a Song.",
   "It reached number 21 on the Hot 100 and number 13 in Canada.",
   "It was number one on the soul chart for two weeks in late 1974.",
   "It is on no 1970s year-end list, so its peak above is a weekly peak only.")}
        <h3>A Song That Kept Being Sampled</h3>
{p("Cassius sampled it in I &lt;3 U So in 2010.",
   "Jay-Z and Kanye West later sampled that record in Why I Love You, in 2011.",
   "Darkchild sampled it earlier, in Megan Rochell's Heartbreak, in 2006.")}

        <h2 id="year-1975">1975: The Way We Were/Try to Remember and Part Time Love</h2>
{p("The Gladys Knight songs of 1975 were smaller hits than the Buddah years.",
   "Two of them were still on the Hot 100, and one was on the 1975 Year-End Hot 100.")}

        <h3>The Way We Were/Try to Remember</h3>
{p("The group joined The Way We Were with Try to Remember in a medley.",
   "Wikipedia credits Tom Jones and Harvey Schmidt with writing Try to Remember.",
   "It reached number 11 on the Hot 100, and it ranks #{} on the 1975 Year-End Hot 100.".format(rk[WAY]),
   "Wikipedia lists a 1975 Grammy nomination for it, for Best Pop Vocal Performance.")}

        <h3>Part Time Love</h3>
{p("Part Time Love, one of the last Gladys Knight songs on this page, reached number 22 on the Hot 100 and number four on the R&B chart in 1975.",
   "It is on no 1970s year-end list, so its peak above is a weekly peak only.",
   'The decade&#39;s soul sound has its own page, <a href="/blog/genres/70s-soul-music/">70s soul music</a>.')}

        <h3>More Hot 100 Entries</h3>
{p("The discography lists three more Gladys Knight songs on the Hot 100 from 1975 to 1977.")}
        <ul>
          <li>So Sad the Song reached number 47 in 1976, from the soundtrack of Pipe Dreams.</li>
          <li>Baby, Don't Change Your Mind reached number 52 and number 10 on the R&B chart in 1977, and earned a Grammy nomination.</li>
          <li>Money reached number 50 in 1975, from the album 2nd Anniversary.</li>
        </ul>

        <h2 id="beyond-the-charts">Beyond the Charts: Awards, Television and Contract Fights</h2>
{p("The group's work did not stop at the singles chart.",
   "Wikipedia lists these milestones from the decade, alongside the Gladys Knight songs above.")}
        <ul>
          <li>1973: The group left Motown in February and signed with Buddah Records.</li>
          <li>1974: Neither One of Us and Midnight Train to Georgia won Grammys.</li>
          <li>1974: The Claudine soundtrack, produced by Curtis Mayfield, included On and On.</li>
          <li>1975: They won two American Music Awards, Favorite Pop/Rock Band/Duo/Group and Favorite Soul/R&B Band/Duo/Group.</li>
          <li>1975: Imagination won Favorite Soul/R&B Album at the American Music Awards.</li>
          <li>1975: Their variety series, The Gladys Knight & the Pips Show, aired four episodes on NBC.</li>
          <li>1976: They won Favorite Soul/R&B Band/Duo/Group again.</li>
          <li>1977: They were in contract disputes with both Motown and Buddah.</li>
        </ul>
{p("From 1978 to 1980, Knight released two solo albums and the Pips released two side albums.",
   "The group signed with Columbia Records in 1980.",
   "Wikipedia says the Rock and Roll Hall of Fame inducted them in 1996.")}

        <h2 id="earlier-versions">Songs with Earlier Versions: Who Sang Each Gladys Knight Song First</h2>
{p("Many Gladys Knight songs began as records by other singers, as the table shows.",
   "Writers like Jim Weatherly handed the group three of its biggest hits.",
   'For more voices from the decade, read the page on <a href="/blog/artists/70s-female-singers/">70s female singers</a>.')}

{tbl("Gladys Knight & the Pips songs of the 70s that had an earlier version, and who recorded it (Wikipedia)", ["Song", "Earlier Version"], first_rows)}

        <h3>Writers Behind the Hits</h3>
{p("Several Gladys Knight songs came from writers with songs of their own.")}
        <ul>
          <li>Jim Weatherly: Neither One of Us, Midnight Train to Georgia and Best Thing That Ever Happened to Me.</li>
          <li>Gerry Goffin and Barry Goldberg: I've Got to Use My Imagination.</li>
          <li>Curtis Mayfield: On and On.</li>
          <li>Tony Camillo and Mary Sawyer: I Feel a Song (In My Heart).</li>
          <li>Pam Sawyer, Clay McMurray and Gloria Jones: If I Were Your Woman.</li>
        </ul>

        <h2 id="who-wrote-what">Who Wrote and Released Each of the Gladys Knight Songs</h2>
{p(f"The table lists when eight of the {NUM[n]} hits were released, on which album, and who wrote them.",
   "The other four have no writers or albums stated in the sources used.")}

{tbl("Gladys Knight & the Pips songs of the 70s: release date, album and writers (Wikipedia)", ["Song", "Released", "Album", "Written By"], album_rows)}

        <h3>Keep Exploring</h3>
{p("These Gladys Knight songs gave the decade one number one and a long run of soul chart hits.",
   "Six of the twelve reached the top ten.",
   'Helen Reddy had a hit with a song the group also recorded, You and Me Against the World, and her story is on the page for <a href="/blog/artists/helen-reddy-songs/">Helen Reddy songs</a>.')}

        <h2 id="sources">Sources</h2>
{p("Year-end ranks come from this site's own Billboard data, described on the <a href='/about/methodology/'>methodology page</a>.",
   'Every list on <a href="/">Music of the 70s</a> plays inside the page.',
   "Peaks, dates and stories behind the Gladys Knight songs above can be checked against these outside sources:")}
        <ul>
          <li><a href="https://en.wikipedia.org/wiki/Gladys_Knight_%26_the_Pips" rel="noopener">Wikipedia: Gladys Knight &amp; the Pips</a> and <a href="https://en.wikipedia.org/wiki/Gladys_Knight_%26_the_Pips_discography" rel="noopener">their discography</a> for the lineup, awards, singles and chart peaks.</li>
          <li><a href="https://en.wikipedia.org/wiki/If_I_Were_Your_Woman_(song)" rel="noopener">Wikipedia: If I Were Your Woman</a> and <a href="https://en.wikipedia.org/wiki/I_Don%27t_Want_to_Do_Wrong" rel="noopener">I Don't Want to Do Wrong</a> for 1970 and 1971.</li>
          <li><a href="https://en.wikipedia.org/wiki/Neither_One_of_Us_(Wants_to_Be_the_First_to_Say_Goodbye)" rel="noopener">Wikipedia: Neither One of Us</a> for 1972.</li>
          <li><a href="https://en.wikipedia.org/wiki/Midnight_Train_to_Georgia" rel="noopener">Wikipedia: Midnight Train to Georgia</a> and <a href="https://en.wikipedia.org/wiki/I%27ve_Got_to_Use_My_Imagination" rel="noopener">I've Got to Use My Imagination</a> for 1973.</li>
          <li><a href="https://en.wikipedia.org/wiki/Best_Thing_That_Ever_Happened_to_Me" rel="noopener">Wikipedia: Best Thing That Ever Happened to Me</a>, <a href="https://en.wikipedia.org/wiki/On_and_On_(Gladys_Knight_%26_the_Pips_song)" rel="noopener">On and On</a> and <a href="https://en.wikipedia.org/wiki/I_Feel_a_Song_(In_My_Heart)" rel="noopener">I Feel a Song (In My Heart)</a> for 1974.</li>
        </ul>

        <section class="faq-block" id="faq">
          <h2>Frequently Asked Questions</h2>
{faq_html}
        </section>'''

    related = [
        ("marvin-gaye-1973-publicity", "Artists", "Marvin Gaye: The Party Tape That Ended Up in Federal Court", "/blog/artists/marvin-gaye/",
         "Another Motown voice, and the 1970s story behind a number one.", "Marvin Gaye in 1973"),
        ("stevie-wonder-1975", "Artists", "Stevie Wonder: The Deal That Built His Classic Period", "/blog/artists/stevie-wonder/",
         "Another act that left Motown's contract system behind in the 70s.", "Stevie Wonder in 1975"),
        ("al-green-hi-records-1973", "Artists", "Al Green: The Hit He Gave Away Before It Was a Hit", "/blog/artists/al-green/",
         "Another soul voice with three songs on one year-end chart.", "Al Green in 1973"),
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
  <meta property="og:image" content="https://musicofthe70s.net/images/blog/{IMG}-668w.jpg">
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
      {{"@type": "ListItem", "position": 4, "name": "Gladys Knight Songs", "item": "{URL}"}}
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
        Gladys Knight Songs
      </nav>

      <article class="section seo-content">
        <h1>{TITLE}</h1>

        <p class="post-byline">By <a href="https://musicofthe70s.net/about/author/">Charlie</a> &middot; Published {PUBLISHED.strftime('%B')} {PUBLISHED.day}, {PUBLISHED.year}</p>
        <p class="jump-to-list"><a class="btn-primary jump-btn" href="#gladys-knight-songs-list">&#9654; Jump to the playable list</a></p>

        <p class="post-intro">Gladys Knight songs ruled the soul charts through the first half of the 70s.</p>
        <p class="post-intro">One of them, Midnight Train to Georgia, reached number one on the Hot 100, and six topped the R&amp;B chart.</p>
        <p class="post-intro">This page plays {NUM[n]} of them, from If I Were Your Woman to Part Time Love.</p>
        <p class="post-intro">Six reached the Hot 100's top ten, and the group left Motown for Buddah Records in the middle of it all.</p>
        <p class="post-intro">Many began as songs by other writers, including Jim Weatherly and Curtis Mayfield.</p>
        <p class="post-intro">Press Play on every hit below, then read the story behind each one.</p>

{feat_pic}
        <p class="post-img-caption">Gladys Knight in a CBS Television publicity photo dated November 22, 1974.</p>
        <p class="post-img-caption">Image credit: CBS Television, public domain (US, published without notice), via Wikimedia Commons.</p>

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
