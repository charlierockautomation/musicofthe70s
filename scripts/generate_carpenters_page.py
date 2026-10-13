#!/usr/bin/env python3
"""Build the Carpenters Songs Artists post (blog/artists/carpenters-songs/index.html).

Data: data/radio/radio-songs.json (Carpenters rows of the Year-End Hot 100, each with a YouTube ID),
data/billboard/hot100_weekly.json (weekly Hot 100 #1s, weeks at #1). Every count and rank in the
prose and tables is computed here. Year-End Rank is the year-end rank, never a peak. Weekly Hot 100
peaks for non-#1 songs, story facts, dates and the Grammy/Oscar notes come from the linked Wikipedia
articles, checked 2026-10-12, and are credited to Wikipedia on the page.

Run: python3 scripts/generate_carpenters_page.py
"""
import collections
import html
import json
from datetime import date

from genre_page_common import ROOT, norm, read, play_button, write
from generate_country_page import p, tbl, pic, fmt_date

SLUG = "carpenters-songs"
URL = f"https://musicofthe70s.net/blog/artists/{SLUG}/"
TITLE = "Carpenters Songs: 11 Hits Played, 3 at Number One"
PUBLISHED = date(2026, 10, 12)
IMG = "carpenters-1972"
NUM = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
       10: "ten", 11: "eleven"}

# Weekly Hot 100 peak and origin, read from each song's Wikipedia article (checked 2026-10-12).
PEAK = {"(They Long to Be) Close to You": 1, "We've Only Just Begun": 2, "Superstar": 2, "For All We Know": 3,
        "Rainy Days and Mondays": 2, "Hurting Each Other": 2, "Sing": 3, "Yesterday Once More": 2,
        "Top of the World": 1, "Please Mr. Postman": 1, "Only Yesterday": 4}
ORIGIN = {
    "(They Long to Be) Close to You": "Burt Bacharach and Hal David, recorded by Richard Chamberlain in 1963",
    "We've Only Just Begun": "Paul Williams and Roger Nichols, from a 1970 bank commercial",
    "Superstar": "Bonnie Bramlett and Leon Russell",
    "For All We Know": "Fred Karlin, Robb Royer and James Griffin, from the film Lovers and Other Strangers",
    "Rainy Days and Mondays": "Paul Williams and Roger Nichols",
    "Hurting Each Other": "Gary Geld and Peter Udell, first recorded by Jimmy Clanton in 1965",
    "Sing": "Joe Raposo, written for Sesame Street in 1971",
    "Yesterday Once More": "Richard Carpenter and John Bettis",
    "Top of the World": "Richard Carpenter and John Bettis",
    "Please Mr. Postman": "A 1961 Motown hit for the Marvelettes, covered by the Beatles in 1963",
    "Only Yesterday": "Richard Carpenter and John Bettis",
}


def main():
    radio = json.loads(read(ROOT / "data/radio/radio-songs.json"))
    weekly = json.loads(read(ROOT / "data/billboard/hot100_weekly.json"))

    songs = sorted((s for s in radio if "carpenters" in s["artist"].lower() and s.get("youtube_id")),
                   key=lambda s: (s["year"], s["rank"]))
    n = len(songs)
    assert n == 11, n
    runs = collections.OrderedDict()
    for yr in sorted(weekly):
        for w in weekly[yr]:
            if "carpenters" in w["artist"].lower():
                d = runs.setdefault(w["title"], {"first": w["week_start"], "weeks": 0, "credit": w["artist"]})
                d["weeks"] += 1
    run_by_title = {norm(t): d for t, d in runs.items()}
    n1, wk1 = len(runs), sum(d["weeks"] for d in runs.values())
    by_title = {s["title"]: s for s in songs}
    years = sorted({s["year"] for s in songs})
    missing = [y for y in range(1970, 1980) if y not in years]
    assert set(PEAK) == set(by_title), set(PEAK) ^ set(by_title)

    rows = []
    for s in songs:
        r = run_by_title.get(norm(s["title"]))
        t, a = html.escape(s["title"]), html.escape(s["artist"])
        rows.append(f'              <tr><td class="ohw-listen">{play_button(s["youtube_id"], s["title"], s["artist"])}</td>'
                    f'<td class="ohw-song">{t}</td>'
                    f'<td>{s["year"]}</td><td>{s["rank"]}</td><td>{"Yes" if r else ""}</td><td>{r["weeks"] if r else ""}</td></tr>')

    year_rows = []
    for y in years:
        ys = [s for s in songs if s["year"] == y]
        best = min(ys, key=lambda s: s["rank"])
        ones = [t for t, d in runs.items() if d["first"].startswith(str(y))]
        year_rows.append([y, len(ys), f'{html.escape(best["title"])} (#{best["rank"]})', html.escape(", ".join(ones)) or "None"])

    run_rows = []
    for t, d in sorted(runs.items(), key=lambda kv: kv[1]["first"]):
        s = by_title[t]
        run_rows.append([html.escape(t), fmt_date(d["first"]), d["weeks"], f'{s["rank"]} ({s["year"]})'])

    origin_rows = [[html.escape(s["title"]), s["year"], PEAK[s["title"]], html.escape(ORIGIN[s["title"]])] for s in songs]

    ctty = runs["(They Long to Be) Close to You"]
    tow = runs["Top of the World"]
    mrp = runs["Please Mr. Postman"]
    top_row = min(songs, key=lambda s: s["rank"])
    stuck2 = [t for t, k in PEAK.items() if k == 2]
    n2 = len(stuck2)

    faq = [
        ("How many number one hits did the Carpenters have?",
         [f"The Carpenters reached number one on the Billboard Hot 100 {NUM[n1]} times, based on this site's weekly chart data.",
          f"Those songs spent {wk1} weeks at the top between July 1970 and January 1975.",
          "They were (They Long to Be) Close to You, Top of the World, and Please Mr. Postman."]),
        ("What are the biggest Carpenters songs of the 1970s on the year-end chart?",
         [f"The highest Carpenters rank on any Year-End Hot 100 of the 1970s was #{top_row['rank']} for {top_row['year']}, held by {top_row['title']}.",
          "That song also spent four weeks at number one in the summer of 1970.",
          "Year-end rank measures a full year of chart performance, not a weekly peak."]),
        ("What is the story behind We've Only Just Begun?",
         ["We've Only Just Begun began as music for a 1970 television commercial for a California bank, Crocker-Citizens National Bank.",
          "Paul Williams and Roger Nichols wrote it, and Richard Carpenter recognized Williams' voice when he saw the ad.",
          "The Carpenters released it on August 21, 1970, according to Wikipedia."]),
        ("Did Karen Carpenter play the drums?",
         ["Karen Carpenter played drums as well as singing lead, and she began on a Ludwig kit around late 1964, according to Wikipedia.",
          "Through 1971 she drummed on stage, then moved out front to sing and kept the sticks for up-tempo numbers.",
          "She is credited on drums for Please Mr. Postman."]),
        ("Is Top of the World a Lynn Anderson song?",
         ["Top of the World was written by Richard Carpenter and John Bettis, and the Carpenters first put it on the 1972 album A Song for You.",
          "Lynn Anderson's country version came out in June 1973 and reached number two on the country chart.",
          "The Carpenters then released their own single on September 17, 1973, and it hit number one in December."]),
    ]
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": " ".join(a)}} for q, a in faq]},
        indent=2, ensure_ascii=False)
    faq_ld = "\n".join("  " + l for l in faq_ld.split("\n"))
    faq_html = "\n".join(
        f'          <div class="faq-item">\n            <h3>{html.escape(q)}</h3>\n' + "\n".join(f"            <p>{html.escape(l)}</p>" for l in a) + "\n          </div>"
        for q, a in faq).replace("&#x27;", "'")

    desc = (f"Carpenters songs: play all {n} hits from the 70s Year-End Hot 100, {NUM[n1]} at number one. "
            "Read how Karen and Richard turned a bank jingle into a classic.")
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

    toc = [("carpenters-song-list", f"Carpenters Songs: Play All {n} Year-End Hits"),
           ("by-the-numbers", "The Numbers Behind the Hits"),
           ("two-siblings", "Two Siblings and a Signing"),
           ("close-to-you", "Close to You: Four Weeks at the Top"),
           ("bank-jingle", "A Bank Jingle Becomes a Wedding Song"),
           ("stuck-at-two", "Five Songs Stuck at Number Two"),
           ("last-number-ones", "Top of the World and Please Mr. Postman"),
           ("stage-and-road", "The White House, Japan and the Drum Kit"),
           ("after-1975", "After 1975"),
           ("sources", "Sources"), ("faq", "Frequently Asked Questions")]
    toc_html = "\n".join(f'            <li><a href="#{i}">{t}</a></li>' for i, t in toc)

    nixon_pic = pic("carpenters-nixon-1972", "President Richard Nixon standing with Karen and Richard Carpenter in the Oval Office at the White House in August 1972",
                    "(max-width: 700px) 100vw, 800px", 800, 527, widths=(400, 600, 800)).replace(
        "<img\n", '<img style="display:block;width:100%;max-width:800px;height:auto;margin:1.5rem auto;border-radius:8px"\n', 1)

    body = f'''        <h2 id="carpenters-song-list">Carpenters Songs: Play All {n} Year-End Hits</h2>
{p(f"Here are all {n} Carpenters songs on this site's Year-End Hot 100 data for the 1970s, from {years[0]} to {years[-1]}.",
   "Press Play on any row to watch it here, and tap a heading to sort.")}

        <div class="data-table-wrap scroll-list">
          <table class="data-table sortable-table" id="carpentersSongsTable" data-inline-player>
            <caption>{n} Carpenters songs of the 70s, by year and Billboard Year-End Hot 100 rank, with weeks at number one</caption>
            <thead>
              <tr>
                <th><span class="visually-hidden">Play</span></th>
                <th><button type="button" data-col="1" data-type="text">Song</button></th>
                <th aria-sort="ascending"><button type="button" data-col="2" data-type="num">Year</button></th>
                <th><button type="button" data-col="3" data-type="num">Year-End Rank</button></th>
                <th><button type="button" data-col="4" data-type="text">#1 Hit</button></th>
                <th><button type="button" data-col="5" data-type="num">Weeks at #1</button></th>
              </tr>
            </thead>
            <tbody>
{chr(10).join(rows)}
            </tbody>
          </table>
        </div>
{p("Year-End Rank is the song's spot on that year's Billboard Year-End Hot 100.",
   "That list keeps only the top 100 songs of each year.",
   "The #1 Hit and Weeks at #1 columns come from this site's own weekly Hot 100 data, not from the year-end list.")}

        <h2 id="by-the-numbers">The Numbers Behind the Hits</h2>
{p(f"Carpenters songs landed on the Year-End Hot 100 in {len(years)} different years of the decade.",
   f"They had no entry in {', '.join(str(y) for y in missing[:-1])} or {missing[-1]}.",
   "The table shows their best-ranked song each year, and any number one that began that year.")}

{tbl("Year-End Hot 100 entries and weekly number ones, 1970 to 1975", ["Year", "Songs on the year-end list", "Best year-end rank", "Number ones that began that year"], year_rows)}

        <h3>Three Ways to Read Carpenters Songs</h3>
{p("Year-end rank and weekly number ones measure different things, and the Carpenters show the gap clearly.")}
        <ul>
          <li>{html.escape(top_row["title"])} ranked #{top_row["rank"]} for {top_row["year"]}, their best year-end rank, after four weeks at number one.</li>
          <li>Top of the World began its run in December 1973, yet it ranks #{by_title["Top of the World"]["rank"]} on the {by_title["Top of the World"]["year"]} year-end list.</li>
          <li>We've Only Just Begun ranks #{by_title["We've Only Just Begun"]["rank"]} for 1970 and never appears in this site's weekly number one data.</li>
        </ul>
{p("The last point is the odd one, because Wikipedia says that song reached number two on the Hot 100.")}

        <h2 id="two-siblings">Two Siblings and a Signing</h2>

        <h3>From a Pit Band to a Trio</h3>
{p("Richard and Karen Carpenter first played together in 1965, in the pit band of a local production of Guys and Dolls.",
   "That same year Richard formed a jazz trio with Wesley Jacobs, with Karen on drums.",
   "Karen had started drumming around late 1964, on a Ludwig kit her parents bought her.",
   "By 1968 the group had shrunk to the two siblings, and they called themselves Carpenters.")}

        <h3>April 22, 1969</h3>
{p("They signed with A&amp;M Records on April 22, 1969.",
   "Karen was 19, so her parents co-signed the contract.",
   "Their first album, Offering, came out on October 9, 1969, and sold only 18,000 copies at first.",
   "The title single, a cover of the Beatles' Ticket to Ride, reached number 54 on the Hot 100, according to Wikipedia.")}

        <h2 id="close-to-you">Close to You: Four Weeks at the Top</h2>
{p(f"The song that changed everything was (They Long to Be) Close to You, released on May 14, 1970.",
   f"It began {NUM[ctty['weeks']]} weeks at number one on {fmt_date(ctty['first'])}, according to this site's weekly data.",
   f"It also ranked #{by_title['(They Long to Be) Close to You']['rank']} on the 1970 year-end list.",
   "The Carpenters had picked up a song other singers had already tried.")}

        <h3>A Song Passed Around Since 1963</h3>
{p("Burt Bacharach and Hal David wrote it.",
   "Richard Chamberlain released it in 1963, and Dionne Warwick and Dusty Springfield both recorded versions in the 1960s.",
   "Herb Alpert had been given the song after his own number one in 1968, but he did not release it.",
   "After Ticket to Ride, he suggested the Carpenters try it.")}

        <h3>The Flugelhorn Solo</h3>
{p("Richard wrote a flugelhorn solo with Alpert in mind.",
   "Alpert was not available, so session player Chuck Findley recorded it.",
   "Richard later said Findley did not play it that way at first, but that they worked on it until he nailed it.",
   "The record won the 1971 Grammy for Best Contemporary Performance by a Duo, Group or Chorus.",
   "At the same ceremony, on March 16, 1971, the Carpenters also won Best New Artist.")}

        <h2 id="bank-jingle">A Bank Jingle Becomes a Wedding Song</h2>
{p("We've Only Just Begun started life as music for a 1970 television commercial for Crocker-Citizens National Bank in California.",
   "Songwriters Paul Williams and Roger Nichols wrote it in a single afternoon, according to Wikipedia.",
   "Richard saw the ad on television and recognized Williams' voice.",
   "He then asked whether a longer version existed.")}
{p("A&amp;M released the full song on August 21, 1970.",
   "Wikipedia says it spent seven weeks at number one on the Adult Contemporary chart.",
   "The Grammy Hall of Fame inducted it in 1998.",
   "The same two writers gave the duo Rainy Days and Mondays the next spring.")}

        <h3>Where Carpenters Songs Came From</h3>
{p("Most Carpenters songs on this site's list were written by someone else.",
   "Richard shaped them with his arrangements, and Karen carried them with her voice.",
   "The table shows who wrote each song, plus its weekly Hot 100 peak from Wikipedia.")}

{tbl("Carpenters songs on the 70s Year-End Hot 100: who wrote them and how high they climbed on the weekly Hot 100", ["Song", "Year-End list", "Hot 100 Peak (Wikipedia)", "Written by or first heard as"], origin_rows)}

        <h2 id="stuck-at-two">{NUM[n2].capitalize()} Songs Stuck at Number Two</h2>
{p(f"Wikipedia lists {NUM[n2]} Carpenters songs on this list as number two on the weekly Hot 100.",
   "Four of them were kept from the top by one specific rival:")}
        <ul>
          <li>Superstar was held out by Rod Stewart's Maggie May.</li>
          <li>Rainy Days and Mondays was kept down by Carole King's <a href="/blog/songs/carole-king-its-too-late/">It's Too Late</a>.</li>
          <li>Hurting Each Other was stopped by Harry Nilsson's Without You.</li>
          <li>Yesterday Once More was blocked by Jim Croce's <a href="/blog/songs/bad-bad-leroy-brown/">Bad, Bad Leroy Brown</a>.</li>
        </ul>
{p("None of those four rivals was a weak song, which is the whole story of the decade's pop chart.")}

        <h3>Superstar and the Changed Lyric</h3>
{p("Richard heard Bette Midler sing Superstar on The Tonight Show on February 15, 1971.",
   "He changed one line in the second verse, because the original lyric was more suggestive than the duo's usual material.",
   "The recording used the Wrecking Crew session musicians, and Wikipedia says it was finished in one take.",
   "The single followed on August 12, 1971.")}

        <h3>Rainy Days and a Voice at Twenty</h3>
{p("Rainy Days and Mondays came out on April 23, 1971, on the album Carpenters.",
   "Richard kept the arrangement sparse to showcase Karen's vocal.",
   "She recorded it a few weeks before her 21st birthday.")}

        <h3>Three More From the Early Years</h3>
{p("For All We Know came from the 1970 film Lovers and Other Strangers.",
   "Its music was by Fred Karlin, and Robb Royer and James Griffin, both of Bread, wrote the words.",
   "Wikipedia says the song won the Academy Award for Best Original Song, and that the Carpenters' version reached number three.",
   "Sing came from Sesame Street, where Joe Raposo wrote it in 1971.",
   "The Carpenters released it on January 13, 1973, with the Jimmy Joyce Children's Choir behind Karen, and it reached number three.")}

        <h3>Yesterday Once More: A Song About Old Radio</h3>
{p("Richard Carpenter and John Bettis wrote Yesterday Once More, released May 16, 1973.",
   "It opened a whole side of the album Now &amp; Then.",
   "Side two was a medley of eight covers of 1960s songs, staged as an oldies radio show.",
   "It is a record about loving records, and it ranks #70 on the 1973 year-end list.")}

        <h2 id="last-number-ones">Top of the World and Please Mr. Postman</h2>
{p(f"The second number one came late in 1973, and the third came at the start of 1975.",
   f"All three Carpenters number ones spent {wk1} weeks at the top between them.")}

{tbl("Every Carpenters number one on the weekly Hot 100, 1970 to 1979", ["Song", "First week at #1", "Weeks at #1", "Year-End Rank (year)"], run_rows)}

        <h3>Top of the World, Written Before Lynn Anderson</h3>
{p("Richard Carpenter and John Bettis wrote Top of the World in 1972.",
   "The duo first put it on the album A Song for You, which came out on June 13, 1972, and meant it as an album track.",
   "Then Lynn Anderson released her country version in June 1973.",
   "It reached number two on the country chart and number 74 on the Hot 100, according to Wikipedia.",
   "Wikipedia says the Carpenters regretted not issuing their own single first, so they did.")}
{p(f"They released it on September 17, 1973, with Karen re-recording her lead vocal because she was not satisfied with the first.",
   f"It began {NUM[tow['weeks']]} weeks at number one on {fmt_date(tow['first'])}, their second chart-topper.",
   f"By year-end it ranks #{by_title['Top of the World']['rank']} on the 1974 list.")}

        <h3>The Last Number One</h3>
{p("Please Mr. Postman was a 1961 Motown hit, the Marvelettes' debut single and the first Motown song to reach number one.",
   "The Beatles covered it in 1963.",
   "The Carpenters released their version on November 8, 1974, from the album Horizon.",
   f"It held number one for {NUM[mrp['weeks']]} week, starting {fmt_date(mrp['first'])}, in this site's weekly data.",
   "Wikipedia calls it their last million-selling single and their final Hot 100 chart-topper.",
   'It joins the full list of <a href="/blog/songs/70s-number-one-hits/">70s number one hits</a>.')}

        <h2 id="stage-and-road">The White House, Japan and the Drum Kit</h2>

        <h3>Meeting the President</h3>
{p("On August 1, 1972, the siblings met President Richard Nixon in the Oval Office.",
   "On April 30, 1973, they returned to the White House for a special concert.")}
{nixon_pic}
        <p class="post-img-caption">President Richard Nixon with Karen and Richard Carpenter in the Oval Office, August 1, 1972.</p>
        <p class="post-img-caption">Image credit: White House Photo Office, public domain, via the U.S. National Archives and Wikimedia Commons.</p>

        <h3>Japan and the Drum Kit</h3>
{p("In May 1974 the duo made their first tour of Japan, which Wikipedia says drew about 85,000 fans.",
   "Karen drummed on stage through 1971, then moved to the front to sing.",
   "After that she played drums mostly on up-tempo numbers, while a touring drummer filled in.",
   "On record, Please Mr. Postman credits her with drums as well as lead vocal.")}

        <h2 id="after-1975">After 1975</h2>
{p(f"The year-end list shows no Carpenters songs for {', '.join(str(y) for y in missing[:-1])} or {missing[-1]}.",
   "Their albums kept coming, though, and A Kind of Hush arrived on June 11, 1976.",
   "Passage followed in 1977.")}

        <h3>The Break in 1978</h3>
{p("Wikipedia says Richard became addicted to Quaaludes.",
   "On September 4, 1978, during an engagement at the MGM Grand in Las Vegas, he decided to stop touring.",
   "The last concert the siblings played together was on December 3, 1978, in Long Beach.",
   "In January 1979 he began six weeks of treatment in Topeka, Kansas, and took the rest of the year off.")}

        <h3>February 4, 1983</h3>
{p("Karen Carpenter died on February 4, 1983, at age 32.",
   "Wikipedia gives the autopsy cause as emetine cardiotoxicity due to anorexia nervosa.",
   "Wikipedia also says the Carpenters have sold more than 100 million records worldwide, a figure it presents as a claim, not an audited total.")}

        <h3>Keep Exploring</h3>
{p('For another act to explore from this decade, try the <a href="/pages/random-artist-picker">Random Artist Picker</a>.',
   'To test what you know about the decade, take the <a href="/pages/70s-trivia-quiz">70s Music Trivia Quiz</a>.',
   'Carpenters songs belong to the gentler side of the decade, and the full story of <a href="/blog/genres/70s-soft-rock/">70s soft rock</a> puts them in context.')}

        <h2 id="sources">Sources</h2>
{p("Year-end ranks and Hot 100 number ones come from this site's own Billboard data, described on the <a href='/about/methodology/'>methodology page</a>.",
   'Every list on <a href="/">Music of the 70s</a> plays inside the page.',
   "Peaks, dates and stories behind the Carpenters songs above can be checked against these outside sources:")}
        <ul>
          <li><a href="https://en.wikipedia.org/wiki/The_Carpenters" rel="noopener">Wikipedia: The Carpenters</a> for the signing, the Grammys, the White House visits, Japan, the 1978 break, and Karen's death.</li>
          <li><a href="https://en.wikipedia.org/wiki/(They_Long_to_Be)_Close_to_You" rel="noopener">Wikipedia: (They Long to Be) Close to You</a> for the earlier versions and the flugelhorn story.</li>
          <li><a href="https://en.wikipedia.org/wiki/We%27ve_Only_Just_Begun" rel="noopener">Wikipedia: We've Only Just Begun</a> for the bank commercial.</li>
          <li><a href="https://en.wikipedia.org/wiki/Top_of_the_World_(Carpenters_song)" rel="noopener">Wikipedia: Top of the World</a> for the Lynn Anderson story.</li>
          <li><a href="https://en.wikipedia.org/wiki/Please_Mr._Postman" rel="noopener">Wikipedia: Please Mr. Postman</a> for the Marvelettes original and the final number one.</li>
          <li><a href="https://en.wikipedia.org/wiki/Rainy_Days_and_Mondays" rel="noopener">Wikipedia: Rainy Days and Mondays</a>, <a href="https://en.wikipedia.org/wiki/Yesterday_Once_More_(song)" rel="noopener">Yesterday Once More</a>, <a href="https://en.wikipedia.org/wiki/Hurting_Each_Other" rel="noopener">Hurting Each Other</a>, <a href="https://en.wikipedia.org/wiki/Sing_(Joe_Raposo_song)" rel="noopener">Sing</a>, and <a href="https://en.wikipedia.org/wiki/For_All_We_Know_(1970_song)" rel="noopener">For All We Know</a> for the peaks and recording notes.</li>
        </ul>

        <section class="faq-block" id="faq">
          <h2>Frequently Asked Questions</h2>
{faq_html}
        </section>'''

    related = [
        ("70s-number-one-hits", "Songs", "70s Number One Hits: Every Billboard #1", "/blog/songs/70s-number-one-hits/",
         "All 253 Hot 100 number ones of the decade, sortable and playable.", "A collage for the 70s number one hits list"),
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
      {{"@type": "ListItem", "position": 4, "name": "Carpenters Songs", "item": "{URL}"}}
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
        Carpenters Songs
      </nav>

      <article class="section seo-content">
        <h1>{TITLE}</h1>

        <p class="post-byline">By <a href="https://musicofthe70s.net/about/author/">Charlie</a> &middot; Published {PUBLISHED.strftime('%B')} {PUBLISHED.day}, {PUBLISHED.year}</p>
        <p class="jump-to-list"><a class="btn-primary jump-btn" href="#carpenters-song-list">&#9654; Jump to the playable list</a></p>

        <p class="post-intro">Carpenters songs filled the Year-End Hot 100 in the early 1970s, with {n} entries across {len(years)} different years.</p>
        <p class="post-intro">{NUM[n1].capitalize()} of them reached number one, and together those songs held the top spot for {wk1} weeks.</p>
        <p class="post-intro">Most were written by other people, then turned into something unmistakable by Karen's voice and Richard's arrangements.</p>
        <p class="post-intro">This page plays all {n} songs, then follows the stories behind the biggest ones.</p>

{pic(IMG, "Karen Carpenter singing behind a drum kit beside Richard Carpenter and bandmates on stage at the Greek Theatre in Los Angeles in 1972", "(max-width: 700px) 100vw, 1100px", 1200, 739, lazy=False)}
        <p class="post-img-caption">The Carpenters on stage at the Greek Theatre, Los Angeles, August 1972.</p>
        <p class="post-img-caption">Image credit: Photo by Kathleen Ballard, Los Angeles Times, CC BY 4.0, via Wikimedia Commons (UCLA Library).</p>

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
    print(f"wrote {out}: {n} rows, {n1} number ones, {wk1} weeks, years {years}, missing {missing}")


if __name__ == "__main__":
    main()
