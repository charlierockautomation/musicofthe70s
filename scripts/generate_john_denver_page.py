#!/usr/bin/env python3
"""Build the John Denver Songs Artists post (blog/artists/john-denver-songs/index.html).

Data: data/radio/radio-songs.json (six John Denver rows of the 1971-1975 Year-End Hot 100, each with a YouTube ID),
data/billboard/hot100_weekly.json (four Hot 100 number ones in the site's 1970-1979 weekly data: Sunshine on My
Shoulders, Annie's Song, Thank God I'm a Country Boy and I'm Sorry), data/billboard/beyond_year_end.json (five further
singles on the weekly Hot 100 but on no 1970s year-end list: Back Home Again, Fly Away, Looking for Space, Like a Sad
Song and My Sweet Lady; peaks and official-channel or Topic YouTube IDs checked).
Year-End Rank is the year-end rank, never a peak. Hot 100 peaks, release dates, writers and story facts come from the
linked Wikipedia articles and the John Denver discography article, checked 2026-10-15, and are credited to Wikipedia.
Sweet Surrender (peak 13, Adult Contemporary number one) is left off the player: no official studio upload was found.
The site JSON's fun_fact and trivia text for the artist is not used.

Run: python3 scripts/generate_john_denver_page.py
"""
import html
import json
from datetime import date

from genre_page_common import ROOT, read, play_button, write
from generate_country_page import p, tbl, pic

SLUG = "john-denver-songs"
PAGE = f"blog/artists/{SLUG}/"
URL = f"https://musicofthe70s.net/{PAGE}"
IMG = "john-denver-1974"
IMG2 = "john-denver-ford-1975"
CHART = "john-denver-peaks"
PUBLISHED = date(2026, 10, 15)
ARTIST = "John Denver"
NUM = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
       10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen"}

ROADS, ROCKY, SUNSHINE, ANNIE = "Take Me Home, Country Roads", "Rocky Mountain High", "Sunshine on My Shoulders", "Annie's Song"
HOME, BOY, SORRY, FLY = "Back Home Again", "Thank God I'm a Country Boy", "I'm Sorry", "Fly Away"
SPACE, SAD, LADY = "Looking for Space", "Like a Sad Song", "My Sweet Lady"
PPP = "Poems, Prayers & Promises"
JD = "John Denver"

# title -> (release year, Hot 100 peak, released text, album it first appeared on, written by)
# Every value read from the song's Wikipedia article or the John Denver discography article, checked 2026-10-15.
INFO = {
    ROADS: (1971, 2, "April 12, 1971", PPP, "Bill Danoff, Taffy Nivert and John Denver"),
    ROCKY: (1972, 9, "October 30, 1972", "Rocky Mountain High", "John Denver and Mike Taylor"),
    SUNSHINE: (1973, 1, "May 1973", PPP, "John Denver, Dick Kniss and Mike Taylor"),
    ANNIE: (1974, 1, "June 1974", "Back Home Again", JD),
    HOME: (1974, 5, "September 1974", "Back Home Again", JD),
    BOY: (1975, 1, "March 1975", "An Evening with John Denver", "John Sommers"),
    SORRY: (1975, 1, "July 1975", "Windsong", JD),
    FLY: (1975, 13, "November 1975", "Windsong", JD),
    SPACE: (1976, 29, "February 1976", "Windsong", JD),
    SAD: (1976, 36, "August 1976", "Spirit", JD),
    LADY: (1977, 32, "1977", PPP, JD),
}
ORDER = list(INFO)
BEYOND = {HOME, FLY, SPACE, SAD, LADY}
YE_SET = {ROADS, ROCKY, SUNSHINE, ANNIE, BOY, SORRY}

# Hot 100 singles from the discography that are not on the playable list (peak 100 or better)
OTHERS = [("Friends with You", 1971, 47), ("Everyday", 1972, 81), ("Goodbye Again", 1972, 88),
          ("I'd Rather Be a Cowboy (Lady's Chains)", 1973, 62), ("Farewell, Andromeda (Welcome to My Morning)", 1973, 89),
          ("Please, Daddy", 1973, 69), ("Sweet Surrender", 1974, 13), ("It Makes Me Giggle", 1976, 60),
          ("Baby, You Look Good to Me Tonight", 1976, 65), ("How Can I Leave You Again", 1977, 44),
          ("I Want to Live", 1977, 55), ("It Amazes Me", 1978, 59)]


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

    # weekly number ones by the artist in the site's own 1970-1979 data
    wk = {}
    for yr in weekly:
        for w in weekly[yr]:
            if w["artist"] == ARTIST:
                wk.setdefault(w["title"], []).append(w)
    assert set(wk) == {SUNSHINE, ANNIE, BOY, SORRY}, set(wk)
    assert [w["week_start"] for w in wk[SUNSHINE]] == ["1974-03-30"]
    assert [w["week_start"] for w in wk[ANNIE]] == ["1974-07-27", "1974-08-03"]
    assert [w["week_start"] for w in wk[BOY]] == ["1975-06-07"]
    assert [w["week_start"] for w in wk[SORRY]] == ["1975-09-27"]
    weeks_total = 1 + 2 + 1 + 1
    assert weeks_total == 5

    rk = {t: ye[t]["rank"] for t in ye}
    yr_of = {t: ye[t]["year"] for t in ye}
    n = len(INFO)
    assert n == 11
    top_ten = [t for t in INFO if INFO[t][1] <= 10]
    assert len(top_ten) == 7, top_ten
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
    other_rows = [[html.escape(t), y, pk] for t, y, pk in sorted(OTHERS, key=lambda r: (r[1], r[2]))]

    faq = [
        ("How many number one songs did John Denver have in the 1970s?",
         ["John Denver had four Billboard Hot 100 number ones in the 1970s, according to Wikipedia's discography.",
          "They were Sunshine on My Shoulders, Annie's Song, Thank God I'm a Country Boy and I'm Sorry.",
          "This site's weekly chart data gives them five weeks at the top between them.",
          "Annie's Song held the spot for two of those weeks."]),
        ("Did Take Me Home, Country Roads reach number one?",
         ["Take Me Home, Country Roads peaked at number two on the Billboard Hot 100 for the week ending August 28, 1971.",
          "The Bee Gees' How Can You Mend a Broken Heart was ahead of it.",
          "It did reach number one on Record World's pop singles chart and on the Cash Box Top 100.",
          "It ranks number eight on the 1971 Billboard Year-End Hot 100."]),
        ("Who wrote Take Me Home, Country Roads?",
         ["Bill Danoff, Taffy Nivert and John Denver wrote Take Me Home, Country Roads, according to Wikipedia.",
          "Danoff and Nivert, a married couple, came up with the title line.",
          "Denver heard the unfinished song at The Cellar Door in Washington, D.C.",
          "They finished it on December 30, 1970, and RCA released it as a single on April 12, 1971."]),
        ("Who was Annie's Song written for?",
         ["John Denver wrote Annie's Song for his wife at the time, Annie Martell Denver, according to Wikipedia.",
          "He wrote it in January 1973 on a ski lift up Aspen Mountain.",
          "It took about ten and a half minutes.",
          "RCA released it in June 1974.",
          "It reached number one on the Billboard Hot 100 and the UK singles chart."]),
        ("When did John Denver die?",
         ["John Denver died on October 12, 1997, at age 53, according to Wikipedia.",
          "His Rutan Long-EZ aircraft crashed into Monterey Bay near Pacific Grove, California.",
          "He was the only person aboard, and the official cause of death was multiple blunt force trauma.",
          "An autopsy found no alcohol or drugs, and he was born Henry John Deutschendorf Jr. in 1943."]),
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

    TITLE = f"John Denver Songs: {n} Hits Played, 4 at No. 1"
    desc = (f"John Denver songs of the 70s, all {n} playable: Country Roads, Annie's Song and more. "
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

    toc = [("john-denver-songs-list", f"John Denver Songs: Play All {n} Hits"),
           ("by-the-numbers", "John Denver Songs on the Charts: Four Number Ones, Seven Top Tens"),
           ("origins", "From Deutschendorf to Denver: Where the John Denver Songs Began"),
           ("year-1971-73", "1971 to 1973: Take Me Home, Country Roads, Rocky Mountain High and Sunshine on My Shoulders"),
           ("year-1974", "1974: Annie's Song and Back Home Again"),
           ("year-1975", "1975: Thank God I'm a Country Boy, I'm Sorry and Fly Away"),
           ("year-1976-77", "1976 and 1977: Looking for Space, Like a Sad Song and My Sweet Lady"),
           ("other-singles", "The Other John Denver Singles on the 70s Hot 100"),
           ("beyond-the-charts", "Beyond the Charts: Awards, State Songs and Later Honors"),
           ("who-wrote-what", "Who Wrote and Released Each of the John Denver Songs"),
           ("sources", "Sources"), ("faq", "Frequently Asked Questions")]
    toc_html = "\n".join(f'            <li><a href="#{i}">{t}</a></li>' for i, t in toc)

    feat_pic = pic(IMG, "John Denver in a 1974 RCA Records publicity portrait, the singer behind the John Denver songs of the 70s",
                   "(max-width: 700px) 100vw, 420px", 800, 1030, widths=(400, 800), lazy=False).replace(
        'class="post-featured-img"', 'class="post-featured-img" style="aspect-ratio:800/1030;max-width:420px;width:100%;height:auto;margin:1.5rem auto"', 1)
    pic2 = pic(IMG2, "President Gerald R. Ford shaking hands with John Denver in the Oval Office on April 14, 1975",
               "(max-width: 700px) 100vw, 800px", 800, 546, widths=(400, 800)).replace(
        "<img\n", '<img style="display:block;width:100%;max-width:800px;height:auto;margin:1.5rem auto;border-radius:8px"\n', 1)
    chart_pic = pic(CHART, "Lollipop chart of eleven John Denver songs by Hot 100 peak, from four number ones to Like a Sad Song at number 36",
                    "(max-width: 700px) 100vw, 800px", 800, 450, widths=(400, 800, 1200)).replace(
        "<img\n", '<img style="display:block;width:100%;max-width:800px;height:auto;margin:1.5rem auto;border-radius:8px"\n', 1)

    body = f'''        <h2 id="john-denver-songs-list">John Denver Songs: Play All {n} Hits</h2>
{p(f"Here are {NUM[n]} hits from 1971 to 1977, from Take Me Home, Country Roads to My Sweet Lady.",
   "Six sit on a Billboard Year-End Hot 100, and five more charted weekly without making a year-end list.",
   "Press Play on any row to watch it here, and tap a heading to sort.")}

        <div class="data-table-wrap scroll-list">
          <table class="data-table sortable-table" id="johnDenverSongsTable" data-inline-player>
            <caption>{n} John Denver songs of the 70s, with release year, Billboard Year-End Hot 100 rank and Hot 100 peak</caption>
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
   "Hot 100 Peak is the weekly peak, from each song's Wikipedia article or the John Denver discography article.",
   "All four number ones are Hot 100 chart toppers in this site's weekly chart data.")}

        <h2 id="by-the-numbers">John Denver Songs on the Charts: Four Number Ones, Seven Top Tens</h2>
{p("The run at the top was short and steep, with all four number ones landing inside two years.",
   "Sunshine on My Shoulders held the top spot for one week, starting March 30, 1974.",
   "Annie's Song held it for two weeks, starting July 27 and August 3, 1974.",
   "Thank God I'm a Country Boy did it in the week starting June 7, 1975.",
   "I'm Sorry followed in the week starting September 27, 1975.")}

{chart_pic}
        <p class="post-img-caption">Hot 100 peaks of the eleven hits on this page, per Wikipedia's song and discography articles.</p>

{tbl("John Denver songs of the 70s ranked by weekly Hot 100 peak, with release date (Wikipedia)", ["Song", "Hot 100 Peak", "Released"], peak_rows)}

        <h3>What the Chart Numbers Say</h3>
{p(f"Seven of the {NUM[n]} hits on this page reached the Hot 100's top ten.")}
        <ul>
          <li>Sunshine on My Shoulders, Annie's Song, Thank God I'm a Country Boy and I'm Sorry all reached number one.</li>
          <li>Take Me Home, Country Roads stopped at number two, and Back Home Again reached number five.</li>
          <li>Take Me Home, Country Roads ranks #{rk[ROADS]} on the 1971 Year-End Hot 100, the highest of his six year-end songs.</li>
          <li>Thank God I'm a Country Boy ranks #{rk[BOY]} on the 1975 list, and Sunshine on My Shoulders ranks #{rk[SUNSHINE]} on the 1974 list.</li>
          <li>Rocky Mountain High ranks #{rk[ROCKY]} on the 1973 list, Annie's Song ranks #{rk[ANNIE]} on the 1974 list, and I'm Sorry ranks #{rk[SORRY]} on the 1975 list.</li>
          <li>Eight of his songs reached number one on the Adult Contemporary chart, per Wikipedia, and three reached number one on the country chart.</li>
        </ul>

        <h2 id="origins">From Deutschendorf to Denver: Where the John Denver Songs Began</h2>
{p("The John Denver songs of the 70s came from a folk singer who had changed his name.",
   "He was born Henry John Deutschendorf Jr. on December 31, 1943, in Roswell, New Mexico.",
   "Randy Sparks, founder of the New Christy Minstrels, suggested that Deutschendorf would not fit comfortably on a marquee.")}

        <h3>The Chad Mitchell Trio and the First RCA Album</h3>
{p("He joined The Chad Mitchell Trio in 1965, replacing its founder Chad Mitchell.",
   "He left in 1969 to go solo.",
   "That year he released his first RCA Records album, Rhymes &amp; Reasons.",
   "Poems, Prayers &amp; Promises followed in 1971, and Wikipedia calls it his breakthrough in the United States.")}

        <h3>How Big the Catalog Got</h3>
{p("Wikipedia puts his estimated sales at more than 33 million copies.",
   "It says 33 of his albums and singles were certified gold or platinum in the U.S.",
   "It also credits him with a string of four number-one songs and three number-one albums in 1974 and 1975.",
   'Spin the dial on more voices from the decade with the <a href="/pages/random-artist-picker">Random Artist Picker</a>.')}

        <h2 id="year-1971-73">1971 to 1973: Take Me Home, Country Roads, Rocky Mountain High and Sunshine on My Shoulders</h2>
{p("The first three John Denver songs on this page came from the album that made him a star and the one that followed.")}

        <h3>Take Me Home, Country Roads</h3>
{p("Take Me Home, Country Roads was written by Bill Danoff, Taffy Nivert and John Denver.",
   "Danoff and Nivert were a married couple.",
   "They came up with the title line while Nivert drove along Clopper Road in Montgomery County, Maryland.",
   "Danoff said the idea drew on his childhood in western New England.",
   "He did not want to write about Massachusetts, because the word was not musical.")}
{p("Denver heard the unfinished song at The Cellar Door in Washington, D.C., and decided he had to record it.",
   "The writers had planned to offer it to Johnny Cash, and they finished it on December 30, 1970.",
   "Denver recorded it in New York in January 1971.",
   "RCA released it on April 12, 1971, with Poems, Prayers and Promises on the flip.")}
        <h3>Chart Peak: Number Two Behind the Bee Gees</h3>
{p("It peaked at number two on the Hot 100 for the week ending August 28, 1971.",
   "The Bee Gees' How Can You Mend a Broken Heart was ahead of it that week.",
   "It reached number one on Record World's pop singles chart and on the Cash Box Top 100.",
   f"It ranks #{rk[ROADS]} on the 1971 Year-End Hot 100, and the RIAA certified it gold on August 18, 1971.",
   'Its year-end company is on the page for <a href="/blog/years/top-songs-of-1971/">top songs of 1971</a>.')}

        <h3>A Song That Kept Being Honored and Covered</h3>
        <ul>
          <li>1973: Olivia Newton-John covered it in January 1973, and it reached number 15 in the UK.</li>
          <li>1998: It received the Grammy Hall of Fame Award.</li>
          <li>2001: The Hermes House Band covered it as Country Roads, and it reached number two in Germany and Ireland.</li>
          <li>2014: West Virginia made it one of its official state songs in March.</li>
          <li>2023: It was selected for the Library of Congress National Recording Registry.</li>
        </ul>

        <h3>Rocky Mountain High</h3>
{p("Rocky Mountain High was written by John Denver and Mike Taylor.",
   "RCA Victor released it on October 30, 1972.",
   "It was the title track of the album, and Spring was on the flip.",
   "Wikipedia says it was inspired by his move to Aspen, Colorado, about three years before he wrote it.",
   "It was also inspired by his love for the state.")}
        <h3>Nine Months to Write</h3>
{p("Denver told mid-1970s audiences that it took him nine months to write.",
   "It peaked at number nine on the Hot 100 in 1973 and number three on the Adult Contemporary chart.",
   f"It ranks #{rk[ROCKY]} on the 1973 Year-End Hot 100, and Cash Box said it sparkles with sincerity.")}
{p("In 1985, Denver testified before Congress during the Parents Music Resource Center hearings about the song's meaning.",
   "On March 12, 2007, Colorado made it one of two official state songs.",
   "The other is Where the Columbines Grow.")}

        <h3>Sunshine on My Shoulders</h3>
{p("Sunshine on My Shoulders was written by John Denver, Dick Kniss and Mike Taylor.",
   "Denver says he wrote it in Minnesota in late winter or early spring.",
   "It first appeared on Poems, Prayers &amp; Promises in 1971.",
   "RCA released it as a single in May 1973, as the B-side of I'd Rather Be a Cowboy.")}
        <h3>A Number One in 1974</h3>
{p("As the Vietnam War ended, the song gained new significance and got airplay on adult contemporary stations.",
   "It entered the Hot 100 at number 90 on January 26, 1974.",
   "It then reached number one for one week.",
   f"It ranks #{rk[SUNSHINE]} on the 1974 Year-End Hot 100, and it topped the Adult Contemporary chart for two weeks in 1974.")}
{p("A 1973 CBS television movie, Sunshine, used it as its theme.",
   "The series that followed ran for three months in the summer of 1974.",
   "Pat Kelly had a 1974 reggae hit with a cover, and Carly Rae Jepsen released a version in 2008.",
   'More gentle hits from the same years are on the page for <a href="/blog/genres/70s-soft-rock/">70s soft rock</a>.')}

        <h2 id="year-1974">1974: Annie's Song and Back Home Again</h2>
{p("1974 was the year the John Denver songs came in a rush, and the CMA and the ACM both took notice.")}

        <h3>Annie's Song</h3>
{p("John Denver wrote Annie's Song in January 1973 on a ski lift up Aspen Mountain.",
   "Wikipedia says it took about ten and a half minutes.",
   "He wrote it for his wife at the time, Annie Martell Denver.")}
{p("RCA released it in June 1974 as the lead single from Back Home Again.",
   "Cool an' Green an' Shady was on the flip.",
   "It reached number one on the Hot 100, his second.",
   "This site's weekly data gives it two weeks at the top.",
   f"It ranks #{rk[ANNIE]} on the 1974 Year-End Hot 100, and it also topped the Adult Contemporary chart.")}
        <h3>Number One in the UK and Beyond</h3>
{p("It reached number one on the UK singles chart, and Wikipedia calls it his only major UK hit single.",
   "It also reached number one in Ireland and Canada, and number five in Australia.",
   "The RIAA certified it gold, and the UK certified it platinum.",
   "James Galway's instrumental version was a major British hit for him four years later.",
   'Test your memory of the decade with the <a href="/pages/70s-trivia-quiz">70s Music Trivia Quiz</a>.')}

        <h3>Back Home Again</h3>
{p("Back Home Again was written by John Denver.",
   "RCA released it in September 1974 from the album of the same name.",
   "It's Up to You was on the flip, and the single runs 4:42.",
   "It peaked at number five on the Hot 100 in November 1974, his fifth top ten pop hit.")}
{p("It topped the Adult Contemporary chart for two weeks.",
   "It also reached number one on the country chart for one week.",
   "Wikipedia calls that the first of three country number ones for him.")}

        <h3>The Awards for Back Home Again</h3>
{p("The RIAA certified the single gold, and it won the 1975 CMA Award for Song of the Year.",
   "The album won the Academy of Country Music's 1974 Album of the Year award.")}
{pic2}
        <p class="post-img-caption">President Gerald R. Ford shaking hands with John Denver in the Oval Office on April 14, 1975.</p>
        <p class="post-img-caption">Image credit: U.S. National Archives and Records Administration, public domain, via Wikimedia Commons.</p>

        <h2 id="year-1975">1975: Thank God I'm a Country Boy, I'm Sorry and Fly Away</h2>
{p("1975 gave him his last two number ones, and a duet with Olivia Newton-John.")}

        <h3>Thank God I'm a Country Boy</h3>
{p("Thank God I'm a Country Boy was written by John Sommers, who played in Denver's backup band.",
   "The single is the live version from An Evening with John Denver.",
   "It was recorded on August 26, 1974, at the Universal Amphitheatre in Los Angeles.",
   "RCA released it in March 1975.")}
{p("It reached number one on the Hot Country Singles chart for one week, on May 31.",
   "It then reached number one on the Hot 100 for one week.",
   "This site's weekly data puts that in the week starting June 7, 1975.",
   f"It ranks #{rk[BOY]} on the 1975 Year-End Hot 100 and #44 on the year-end country chart.")}
{p("Wikipedia lists covers by Billy Dean, Alvin and the Chipmunks, Dolly Parton and Home Free, among others.",
   'For the wider genre, see the page on <a href="/blog/genres/70s-country-songs/">70s country songs</a>.')}

        <h3>I'm Sorry</h3>
{p("I'm Sorry was written and recorded by John Denver.",
   "RCA Victor released it in July 1975 from the album Windsong.",
   "Calypso was on the flip, and Wikipedia says both sides got substantial Top 40 airplay.",
   "Cash Box credited the arrangement to Lee Holdridge.")}
        <h3>Number One on Three Charts</h3>
{p("It reached number one on the Hot 100 on September 27, 1975.",
   "This site's weekly data gives it one week at the top.",
   "It also topped the Adult Contemporary chart.",
   "It reached number one on the country chart six weeks after the pop chart.",
   "Wikipedia calls it his third and final country number one, and the final pop number one of his career.")}
{p(f"It ranks #{rk[SORRY]} on the 1975 Year-End Hot 100.",
   "Wikipedia ranks it number 242 on the Hot 100 all-time chart for 1958 to 2018.",
   "It also reached number one in Canada.")}

        <h3>Fly Away</h3>
{p("Fly Away was written by John Denver, and RCA released it in November 1975 from Windsong.",
   "Olivia Newton-John joins in on the chorus, and Record World praised that added bonus.",
   "Two Shots was on the flip.")}
{p("It peaked at number 13 on the Hot 100 and number 12 on the country chart.",
   "It spent two weeks at number one on the Adult Contemporary chart in early 1976.",
   "That was his sixth number one there.",
   'Her own career is covered on the page for <a href="/blog/artists/olivia-newton-john-songs/">Olivia Newton-John songs</a>.')}

        <h2 id="year-1976-77">1976 and 1977: Looking for Space, Like a Sad Song and My Sweet Lady</h2>
{p("The John Denver songs slowed on the pop chart after 1975, but the Adult Contemporary chart kept calling.")}

        <h3>Looking for Space</h3>
{p("Looking for Space was released in February 1976 as a single from Windsong, with Windsong on the flip.",
   "It peaked at number 29 on the Hot 100 in April 1976.",
   "It also reached number one on the Easy Listening chart.",
   "That was his seventh chart-topper there.")}
{p("Denver told Billboard it is about looking for the definition of who you are.",
   "He credited his Erhard Seminars Training for inspiring the lyrics, and he dedicated it to Werner Erhard.",
   "It became the theme song for the EST organization.")}
{p("Olivia Newton-John recorded it in 1976.",
   "It stayed unreleased until a 2010 Japanese reissue included it as a bonus track.",
   "It also played in full over the last four minutes of the 1987 Magnum, P.I. episode Limbo.")}

        <h3>Like a Sad Song</h3>
{p("Like a Sad Song was released in August 1976 as a single from the album Spirit.",
   "Pegasus was on the flip.",
   "Wikipedia says it only reached number 36 on the Hot 100.",
   "It still reached number one on the Easy Listening chart.",
   "Wikipedia calls it his eighth single to top that chart within three years.")}

        <h3>My Sweet Lady</h3>
{p("My Sweet Lady first appeared on Poems, Prayers &amp; Promises in 1971.",
   "Denver released it as a single in 1977.",
   "The discography lists it at number 32 on the Hot 100.",
   "Cliff DeYoung's 1973 cover reached number 17 and was part of the soundtrack for the film Sunshine.",
   "It is on no 1970s year-end list, so its peak above is a weekly peak only.")}

        <h2 id="other-singles">The Other John Denver Singles on the 70s Hot 100</h2>
{p("Not every one of the John Denver songs fit on the playable list.",
   "Wikipedia's discography shows a dozen more singles on the Hot 100 in the decade.",
   "One of them, Sweet Surrender, reached number 13 and topped the Adult Contemporary chart.",
   "We could not confirm an official studio upload of it on YouTube, so it is not in the player.")}

{tbl("John Denver singles on the 1970s Hot 100 that are not on the playable list (Wikipedia discography)", ["Single", "Released", "Hot 100 Peak"], other_rows)}

        <h2 id="beyond-the-charts">Beyond the Charts: Awards, State Songs and Later Honors</h2>
{p("The John Denver songs above also won trophies.",
   "Wikipedia lists these milestones.")}
        <ul>
          <li>1974: The Academy of Country Music named Back Home Again its Album of the Year.</li>
          <li>1975: The CMA named him Entertainer of the Year, and Back Home Again its Song of the Year.</li>
          <li>1975: An Evening with John Denver won an Emmy for Outstanding Variety, Music or Comedy Special.</li>
          <li>1975: The American Music Awards named him Favorite Pop/Rock Male Artist.</li>
          <li>1976: The American Music Awards named him Favorite Country Male Artist and gave him Favorite Country Album.</li>
          <li>1977: He starred in the film Oh, God! opposite George Burns.</li>
          <li>1996: He was inducted into the Songwriters Hall of Fame.</li>
          <li>2007: Colorado made Rocky Mountain High an official state song.</li>
          <li>2014: West Virginia approved Take Me Home, Country Roads as a state song, and he received a Hollywood Walk of Fame star on October 24.</li>
        </ul>
{p("He died on October 12, 1997, at age 53.",
   "His Rutan Long-EZ aircraft crashed into Monterey Bay near Pacific Grove, California.",
   "Wikipedia says he won one Grammy, in 1997 for Best Musical Album for Children, for All Aboard!")}

        <h2 id="who-wrote-what">Who Wrote and Released Each of the John Denver Songs</h2>
{p(f"The table lists the release date, first album and writers for each of the {NUM[n]} hits.",
   "He wrote or co-wrote ten of these hits, and the exception is Thank God I'm a Country Boy.")}

{tbl("John Denver songs of the 70s: release date, album and writers (Wikipedia)", ["Song", "Released", "First Appeared On", "Written By"], album_rows)}

        <h3>Keep Exploring</h3>
{p("These John Denver songs gave the decade four number ones and a long run of gentle hits.",
   "Seven of the eleven reached the top ten.",
   'Another act that owned the same radio dial is covered on the page for <a href="/blog/artists/carpenters-songs/">Carpenters songs</a>.')}

        <h2 id="sources">Sources</h2>
{p("Year-end ranks come from this site's own Billboard data, described on the <a href='/about/methodology/'>methodology page</a>.",
   'Every list on <a href="/">Music of the 70s</a> plays inside the page.',
   "Peaks, dates and stories behind the John Denver songs above can be checked against these outside sources:")}
        <ul>
          <li><a href="https://en.wikipedia.org/wiki/John_Denver" rel="noopener">Wikipedia: John Denver</a> and <a href="https://en.wikipedia.org/wiki/John_Denver_discography" rel="noopener">his discography</a> for the biography, honors, singles and chart peaks.</li>
          <li><a href="https://en.wikipedia.org/wiki/Take_Me_Home,_Country_Roads" rel="noopener">Wikipedia: Take Me Home, Country Roads</a>, <a href="https://en.wikipedia.org/wiki/Rocky_Mountain_High" rel="noopener">Rocky Mountain High</a> and <a href="https://en.wikipedia.org/wiki/Sunshine_on_My_Shoulders" rel="noopener">Sunshine on My Shoulders</a> for 1971 to 1973.</li>
          <li><a href="https://en.wikipedia.org/wiki/Annie%27s_Song" rel="noopener">Wikipedia: Annie's Song</a> and <a href="https://en.wikipedia.org/wiki/Back_Home_Again_(song)" rel="noopener">Back Home Again</a> for 1974.</li>
          <li><a href="https://en.wikipedia.org/wiki/Thank_God_I%27m_a_Country_Boy" rel="noopener">Wikipedia: Thank God I'm a Country Boy</a>, <a href="https://en.wikipedia.org/wiki/I%27m_Sorry_(John_Denver_song)" rel="noopener">I'm Sorry</a> and <a href="https://en.wikipedia.org/wiki/Fly_Away_(John_Denver_song)" rel="noopener">Fly Away</a> for 1975.</li>
          <li><a href="https://en.wikipedia.org/wiki/Looking_for_Space" rel="noopener">Wikipedia: Looking for Space</a>, <a href="https://en.wikipedia.org/wiki/Like_a_Sad_Song" rel="noopener">Like a Sad Song</a> and <a href="https://en.wikipedia.org/wiki/My_Sweet_Lady" rel="noopener">My Sweet Lady</a> for 1976 and 1977.</li>
        </ul>

        <section class="faq-block" id="faq">
          <h2>Frequently Asked Questions</h2>
{faq_html}
        </section>'''

    related = [
        ("olivia-newton-john-1978", "Artists", "Olivia Newton-John Songs: 12 Hits Played, 3 at No. 1", "/blog/artists/olivia-newton-john-songs/",
         "The singer who joined John Denver on Fly Away.", "Olivia Newton-John in 1978"),
        ("carpenters-1972", "Artists", "Carpenters Songs: 11 Hits Played, 3 at No. 1", "/blog/artists/carpenters-songs/",
         "Another act that owned the soft rock radio dial.", "The Carpenters in 1972"),
        ("helen-reddy-1975", "Artists", "Helen Reddy Songs: 13 Hits Played, 3 at No. 1", "/blog/artists/helen-reddy-songs/",
         "Another 70s star with three Hot 100 number ones.", "Helen Reddy in 1975"),
    ]

    cards = []
    for img, cat, title, href, blurb, alt in related:
        big = 669 if img in ("olivia-newton-john-1978", "helen-reddy-1975") else 800
        bigjpg = f"/images/blog/{img}-{big}w.jpg" if big == 669 else f"/images/blog/srcset/{img}-{big}w.jpg"
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
      {{"@type": "ListItem", "position": 4, "name": "John Denver Songs", "item": "{URL}"}}
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
        John Denver Songs
      </nav>

      <article class="section seo-content">
        <h1>{TITLE}</h1>

        <p class="post-byline">By <a href="https://musicofthe70s.net/about/author/">Charlie</a> &middot; Published {PUBLISHED.strftime('%B')} {PUBLISHED.day}, {PUBLISHED.year}</p>
        <p class="jump-to-list"><a class="btn-primary jump-btn" href="#john-denver-songs-list">&#9654; Jump to the playable list</a></p>

        <p class="post-intro">John Denver songs turned mountain air and small-town warmth into four Billboard Hot 100 number ones in the 1970s.</p>
        <p class="post-intro">Sunshine on My Shoulders, Annie's Song, Thank God I'm a Country Boy and I'm Sorry all got there.</p>
        <p class="post-intro">Take Me Home, Country Roads stopped one spot short, at number two.</p>
        <p class="post-intro">This page plays {NUM[n]} of his hits, from Country Roads in 1971 to My Sweet Lady in 1977.</p>
        <p class="post-intro">Seven reached the Hot 100's top ten, and he wrote or co-wrote ten of the eleven.</p>
        <p class="post-intro">Press Play on every hit below, then read the story behind each one.</p>

{feat_pic}
        <p class="post-img-caption">John Denver in a 1974 RCA Records publicity photo.</p>
        <p class="post-img-caption">Image credit: RCA Records, public domain, via Wikimedia Commons.</p>

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
