#!/usr/bin/env python3
"""Build the Chicago Band Songs Artists post (blog/artists/chicago-band-songs/index.html).

Data: data/radio/radio-songs.json (Chicago rows of the Year-End Hot 100, each with a YouTube ID),
data/billboard/hot100_weekly.json (weekly Hot 100 #1s), data/billboard/beyond_year_end.json (four
Chicago singles on the weekly Hot 100 but on no 1970s year-end list, peaks from Wikipedia).
Year-End Rank is the year-end rank, never a peak. Weekly Hot 100 peaks for non-#1 songs, writers,
dates and story facts come from the linked Wikipedia articles, checked 2026-10-12, and are credited
to Wikipedia on the page. The site JSON's fun_fact text for Chicago is not used (it carries an
unsourced Hendrix claim and a "both sides charting" claim that Wikipedia does not support).

Run: python3 scripts/generate_chicago_page.py
"""
import collections
import html
import json
from datetime import date

from genre_page_common import ROOT, norm, read, play_button, write
from generate_country_page import p, tbl, pic, fmt_date

SLUG = "chicago-band-songs"
PAGE = f"blog/artists/{SLUG}/"
URL = f"https://musicofthe70s.net/{PAGE}"
KW = "Chicago band songs"
PUBLISHED = date(2026, 10, 12)
IMG = "chicago-1973"
NUM = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
       10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen"}

# Weekly Hot 100 peak, writer, single release and album, read from each song's Wikipedia article (checked 2026-10-12).
PEAK = {"Make Me Smile": 9, "25 or 6 to 4": 4, "Does Anybody Really Know What Time It Is?": 7,
        "Beginnings / Colour My World": 7, "Saturday in the Park": 3, "Feelin' Stronger Every Day": 10,
        "Just You 'n' Me": 4, "(I've Been) Searchin' So Long": 9, "Call on Me": 6, "Old Days": 5,
        "If You Leave Me Now": 1, "Baby, What a Big Surprise": 4}
WRITER = {"Make Me Smile": "James Pankow", "25 or 6 to 4": "Robert Lamm",
          "Does Anybody Really Know What Time It Is?": "Robert Lamm", "Beginnings / Colour My World": "Robert Lamm (Beginnings)",
          "Saturday in the Park": "Robert Lamm", "Feelin' Stronger Every Day": "Peter Cetera and James Pankow",
          "Just You 'n' Me": "James Pankow", "(I've Been) Searchin' So Long": "James Pankow", "Call on Me": "Lee Loughnane",
          "Old Days": "James Pankow", "If You Leave Me Now": "Peter Cetera", "Baby, What a Big Surprise": "Peter Cetera"}
RELEASED = {"Make Me Smile": "March 17, 1970", "25 or 6 to 4": "June 12, 1970",
            "Does Anybody Really Know What Time It Is?": "November 4, 1970",
            "Beginnings / Colour My World": "June 11, 1971 (re-release)", "Saturday in the Park": "July 13, 1972",
            "Feelin' Stronger Every Day": "June 5, 1973", "Just You 'n' Me": "September 7, 1973",
            "(I've Been) Searchin' So Long": "February 21, 1974", "Call on Me": "May 31, 1974", "Old Days": "April 1975",
            "If You Leave Me Now": "July 30, 1976", "Baby, What a Big Surprise": "September 1977"}
ALBUM = {"Make Me Smile": "Chicago (1970)", "25 or 6 to 4": "Chicago (1970)",
         "Does Anybody Really Know What Time It Is?": "Chicago Transit Authority", "Beginnings / Colour My World": "Chicago Transit Authority",
         "Saturday in the Park": "Chicago V", "Feelin' Stronger Every Day": "Chicago VI", "Just You 'n' Me": "Chicago VI",
         "(I've Been) Searchin' So Long": "Chicago VII", "Call on Me": "Chicago VII", "Old Days": "Chicago VIII",
         "If You Leave Me Now": "Chicago X", "Baby, What a Big Surprise": "Chicago XI"}


def main():
    radio = json.loads(read(ROOT / "data/radio/radio-songs.json"))
    weekly = json.loads(read(ROOT / "data/billboard/hot100_weekly.json"))
    beyond = json.loads(read(ROOT / "data/billboard/beyond_year_end.json"))["songs"]

    ye = [s for s in radio if s["artist"] == "Chicago" and s.get("youtube_id")]
    assert len(ye) == 8, len(ye)
    extra = [b for b in beyond if b["page"] == PAGE]
    assert len(extra) == 4, len(extra)
    yt_check = {s["title"] for s in ye} | {b["title"] for b in extra}
    assert yt_check == set(PEAK), yt_check ^ set(PEAK)
    for b in extra:
        assert b["weekly_peak"] == PEAK[b["title"]], b["title"]

    runs = collections.OrderedDict()
    for yr in sorted(weekly):
        for w in weekly[yr]:
            if w["artist"] == "Chicago":
                d = runs.setdefault(w["title"], {"first": w["week_start"], "weeks": 0})
                d["weeks"] += 1
    assert list(runs) == ["If You Leave Me Now"], list(runs)
    leave = runs["If You Leave Me Now"]
    assert leave["weeks"] == 2 and leave["first"] == "1976-10-23"
    n1, wk1 = len(runs), sum(d["weeks"] for d in runs.values())

    entries = []  # (title, chart year, year-end rank or None, youtube id)
    for s in ye:
        entries.append((s["title"], s["year"], s["rank"], s["youtube_id"]))
    for b in extra:
        entries.append((b["title"], b["released"], None, b["youtube_id"]))
    entries.sort(key=lambda e: (e[1], e[2] if e[2] else 999, e[0]))
    n = len(entries)
    ye_by_title = {t: r for t, _, r, _ in entries if r}
    ye_years = sorted({s["year"] for s in ye})
    missing = [y for y in range(1970, 1980) if y not in ye_years]

    rows = []
    for t, y, r, yt in entries:
        rows.append(f'              <tr><td class="ohw-listen">{play_button(yt, t, "Chicago")}</td>'
                    f'<td class="ohw-song">{html.escape(t)}</td>'
                    f'<td>{y}</td><td>{r if r else ""}</td><td>{PEAK[t]}</td><td>{"Yes" if t in runs else ""}</td></tr>')

    year_rows = []
    for y in ye_years:
        ys = [s for s in ye if s["year"] == y]
        best = min(ys, key=lambda s: s["rank"])
        year_rows.append([y, len(ys), f'{html.escape(best["title"])} (#{best["rank"]})',
                          "If You Leave Me Now" if leave["first"].startswith(str(y)) else "None"])

    writer_rows = [[html.escape(t), WRITER[t], RELEASED[t], ALBUM[t], PEAK[t]]
                   for t in sorted(PEAK, key=lambda k: list(RELEASED).index(k))]

    album_rows = [
        ["Chicago Transit Authority", "April 1969", "Debut album, as Chicago Transit Authority",
         "Beginnings (7, 1971 re-release), Does Anybody Really Know What Time It Is? (7)"],
        ["Chicago (also called Chicago II)", "January 1970", "Second album",
         "Make Me Smile (9), 25 or 6 to 4 (4)"],
        ["Chicago V", "1972", "The album Saturday in the Park helped reach number one", "Saturday in the Park (3)"],
        ["Chicago VI", "1973", "Two singles on this page", "Feelin' Stronger Every Day (10), Just You 'n' Me (4)"],
        ["Chicago VII", "1974", "Two singles on this page", "(I've Been) Searchin' So Long (9), Call on Me (6)"],
        ["Chicago VIII", "1975", "One single on this page", "Old Days (5)"],
        ["Chicago X", "1976", "Recorded March and April 1976", "If You Leave Me Now (1)"],
        ["Chicago XI", "1977", "Last album released before Terry Kath died", "Baby, What a Big Surprise (4)"],
    ]

    top_row = min((s for s in ye), key=lambda s: s["rank"])

    faq = [
        ("Which Chicago song reached number one in the 1970s?",
         ["If You Leave Me Now was the only Chicago song to reach number one on the Hot 100 in this site's 1970s weekly data.",
          f"It spent {NUM[leave['weeks']]} weeks at the top, starting {fmt_date(leave['first'])}.",
          "Peter Cetera wrote it and sang lead, and it came from the album Chicago X."]),
        ("Who sings Make Me Smile by Chicago?",
         ["Terry Kath, the band's guitarist, sang lead on Make Me Smile.",
          "James Pankow wrote it as the first part of a seven-part suite called Ballet for a Girl in Buchannon.",
          "The single came out on March 17, 1970, and reached number nine on the Hot 100, the band's first top 10 record, according to Wikipedia."]),
        ("What are the biggest Chicago band songs of the 70s?",
         [f"If You Leave Me Now was the only number one, and Saturday in the Park reached number three.",
          "25 or 6 to 4, Just You 'n' Me and Baby, What a Big Surprise each reached number four.",
          f"Chicago had {NUM[len(ye)]} songs on a 1970s Year-End Hot 100, and the best-ranked was If You Leave Me Now at #{ye_by_title['If You Leave Me Now']} for 1976."]),
        ("What does 25 or 6 to 4 mean?",
         ["The title of 25 or 6 to 4 refers to the time of night when Robert Lamm wrote it.",
          "Lamm said he was trying to write a song in the middle of the night and looked at his watch, which read 25 or 26 minutes to four in the morning.",
          "It reached number four on the Hot 100 after its June 12, 1970 release, according to Wikipedia."]),
        ("Did Chicago win a Grammy for If You Leave Me Now?",
         ["Chicago won its first Grammy for If You Leave Me Now, in the category Best Pop Vocal Performance by a Duo, Group or Chorus.",
          "The song also won Best Arrangement Accompanying Vocalist(s) for arranger Jimmie Haskell and producer James William Guercio.",
          "It was nominated for Record of the Year as well, according to Wikipedia."]),
    ]
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": " ".join(a)}} for q, a in faq]},
        indent=2, ensure_ascii=False)
    faq_ld = "\n".join("  " + l for l in faq_ld.split("\n"))
    faq_html = "\n".join(
        f'          <div class="faq-item">\n            <h3>{html.escape(q)}</h3>\n' + "\n".join(f"            <p>{html.escape(l)}</p>" for l in a) + "\n          </div>"
        for q, a in faq).replace("&#x27;", "'")

    TITLE = f"Chicago Band Songs: {n} Hits Played, 1 at Number One"
    desc = (f"Chicago band songs: play all {n} hits of the 70s, from Make Me Smile to If You Leave Me Now. "
            "Read how 25 or 6 to 4 and Saturday in the Park came to be.")
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
    "image": "https://musicofthe70s.net/images/blog/{IMG}-960w.jpg",
    "mainEntityOfPage": "{URL}"
  }}'''

    toc = [("chicago-band-songs-list", f"Chicago Band Songs: Play All {n} Hits"),
           ("by-the-numbers", "The Numbers Behind the Hits"),
           ("chicago-transit-authority", "From Chicago Transit Authority to Chicago"),
           ("chicago-ii", "Chicago II: Make Me Smile and 25 or 6 to 4"),
           ("beginnings", "Beginnings: The 1969 Song That Needed a Second Try"),
           ("three-albums", "Chicago V, VI and VII: Five Hits in Three Years"),
           ("if-you-leave-me-now", "If You Leave Me Now: The One Number One"),
           ("after-kath", "Baby, What a Big Surprise and the End of an Era"),
           ("who-wrote-what", "Who Wrote What: Lamm, Pankow and Cetera"),
           ("sources", "Sources"), ("faq", "Frequently Asked Questions")]
    toc_html = "\n".join(f'            <li><a href="#{i}">{t}</a></li>' for i, t in toc)

    early_pic = pic("chicago-1969", "The seven members of Chicago Transit Authority in a grayscale photo from Hit Parader magazine, January 1970, before Chicago band songs reached the Hot 100",
                    "(max-width: 700px) 100vw, 800px", 800, 579, widths=(400, 600, 800)).replace(
        "<img\n", '<img style="display:block;width:100%;max-width:800px;height:auto;margin:1.5rem auto;border-radius:8px"\n', 1)
    feat_pic = pic(IMG, "Chicago, the band behind Chicago band songs like If You Leave Me Now and Saturday in the Park, in a Columbia Records photo from about 1973",
                   "(max-width: 700px) 100vw, 800px", 960, 656, widths=(400, 800, 960), lazy=False).replace(
        'class="post-featured-img"', 'class="post-featured-img" style="aspect-ratio:960/656;max-width:800px;height:auto;margin:1.5rem auto"', 1)

    body = f'''        <h2 id="chicago-band-songs-list">Chicago Band Songs: Play All {n} Hits</h2>
{p(f"Here are {NUM[n]} Chicago singles from the 1970s.",
   f"{NUM[len(ye)].capitalize()} come from this site's Year-End Hot 100 data, and four charted on the weekly Hot 100 only.",
   "Press Play on any row to watch it here, and tap a heading to sort.")}

        <div class="data-table-wrap scroll-list">
          <table class="data-table sortable-table" id="chicagoBandSongsTable" data-inline-player>
            <caption>{n} Chicago band songs of the 70s, with Billboard Year-End Hot 100 rank, weekly Hot 100 peak and number one status</caption>
            <thead>
              <tr>
                <th><span class="visually-hidden">Play</span></th>
                <th><button type="button" data-col="1" data-type="text">Song</button></th>
                <th aria-sort="ascending"><button type="button" data-col="2" data-type="num">Year</button></th>
                <th><button type="button" data-col="3" data-type="num">Year-End Rank</button></th>
                <th><button type="button" data-col="4" data-type="num">Weekly Hot 100 Peak</button></th>
                <th><button type="button" data-col="5" data-type="text">#1 Hit</button></th>
              </tr>
            </thead>
            <tbody>
{chr(10).join(rows)}
            </tbody>
          </table>
        </div>
{p("Year is the year-end list year for the eight ranked songs.",
   "For the other four, it is the single's release year.",
   "Year-End Rank is the song's spot on that year's Billboard Year-End Hot 100.",
   "It is blank for songs that list left out.",
   "Weekly Hot 100 Peak comes from each song's Wikipedia article.",
   "The #1 Hit flag comes from this site's own weekly data.")}

        <h2 id="by-the-numbers">The Numbers Behind the Hits</h2>
{p(f"Chicago band songs made a 1970s Year-End Hot 100 in six different years, with {NUM[len(ye)]} entries in all.",
   f"The band had no entry in {', '.join(str(y) for y in missing[:-1])} or {missing[-1]}.",
   "That is a steady run, and the weekly chart adds four more hits the year-end lists left out.")}

{tbl("Chicago on the Year-End Hot 100 and the weekly number ones, 1970 to 1976", ["Year", "Songs on the year-end list", "Best year-end rank", "Number ones that began that year"], year_rows)}

        <h3>Three Ways to Read Chicago Band Songs</h3>
{p("The year-end list and the weekly chart tell different stories here.")}
        <ul>
          <li>If You Leave Me Now ranks #{ye_by_title["If You Leave Me Now"]} for 1976, the best year-end rank of any Chicago song.</li>
          <li>It was also their only number one in the decade.</li>
          <li>Saturday in the Park ranks only #{ye_by_title["Saturday in the Park"]} for 1972, even though it reached number three on the weekly chart.</li>
          <li>25 or 6 to 4 reached number four on the weekly chart and ranks #{ye_by_title["25 or 6 to 4"]} for 1970.</li>
          <li>Old Days, Just You 'n' Me and Baby, What a Big Surprise all reached the top five and are on no year-end list in this site's data.</li>
        </ul>
{p('For every chart-topper of the decade, see the full list of <a href="/blog/songs/70s-number-one-hits/">70s number one hits</a>.')}

        <h2 id="chicago-transit-authority">From Chicago Transit Authority to Chicago</h2>

        <h3>Seven Players From Chicago</h3>
{p("Chicago formed in the city of Chicago on February 15, 1967.",
   "Its first name was the Big Thing.",
   "It became the Chicago Transit Authority in 1968 and was shortened to Chicago in 1969.",
   "Wikipedia lists the seven original members as Peter Cetera, Terry Kath, Robert Lamm, Lee Loughnane, James Pankow, Walter Parazaider and Danny Seraphine.")}
{early_pic}
        <p class="post-img-caption">Chicago Transit Authority, from a feature in the January 1970 issue of Hit Parader magazine.</p>
        <p class="post-img-caption">Image credit: Hit Parader magazine, public domain, via Wikimedia Commons.</p>

        <h3>Horns in a Rock Band</h3>
{p("What set the band apart was a horn section built into a rock lineup.",
   "Terry Kath played guitar, and Peter Cetera played bass and sang.",
   "Lee Loughnane, James Pankow and Walter Parazaider supplied the horns and woodwinds.")}

        <h3>The Albums Behind the Chicago Band Songs</h3>
{p("Each hit below comes from one of eight albums.",
   "The table shows the order they arrived in.")}

{tbl("The albums behind the Chicago band songs of the 70s", ["Album", "Released", "Note", "Singles from this page (weekly Hot 100 peak)"], album_rows)}

        <h2 id="chicago-ii">Chicago II: Make Me Smile and 25 or 6 to 4</h2>
{p("The second album was simply called Chicago, and fans call it Chicago II.",
   "It came out in January 1970.",
   "It gave the band its first two top 10 singles in a few months, and both of these Chicago band songs are in the playable list.")}

        <h3>Make Me Smile</h3>
{p("James Pankow wrote Make Me Smile.",
   "It is the first part of a seven-part suite called Ballet for a Girl in Buchannon.",
   "Terry Kath sang the lead.",
   "The single came out on March 17, 1970, and reached number nine.",
   "It was the band's first top 10 record.",
   "The radio edit shortens the intro and the guitar solo, and borrows a few lines from the suite's closing piece, Now More Than Ever.",
   "It ranks #59 on the 1970 year-end list.")}
{p("Wikipedia says its success renewed interest in the earlier singles Questions 67 and 68 and Beginnings.",
   "Billboard called it a solid beat rocker.")}

        <h3>25 or 6 to 4</h3>
{p("Robert Lamm wrote 25 or 6 to 4, and Peter Cetera sang it.",
   "Lamm has said the title is a clock time.",
   "He was trying to write a song in the middle of the night, looked at his watch, and it read 25 or 26 minutes to four.",
   "The band recorded it on July 24, 1969.",
   "The single came out on June 12, 1970, and reached number four.",
   "Terry Kath plays a wah-wah guitar solo on the album version, and the single edit drops the second verse and most of that solo.")}
{p("Wikipedia notes one odd detail about the vocal.",
   "Guercio and Loughnane both said Cetera sang it while his jaw was still wired shut, after an attack at a Dodger Stadium game on May 20, 1969.",
   "The song was banned in Singapore in 1970 over alleged allusions to drugs, and the ban was lifted in 1993.")}

        <h3>Does Anybody Really Know What Time It Is?</h3>
{p("Lamm also wrote Does Anybody Really Know What Time It Is?, and he sang it.",
   "It was recorded January 27 to 30, 1969, and it was the first song cut for the debut album.",
   "The album version opens with a 1:15 free-form piano solo.",
   "The single came out on November 4, 1970, and reached number seven.",
   "It was the band's third straight top 10 single.")}
{p("It is on no Billboard year-end list, because it straddled two chart years.",
   "That is why it sits among the four songs the year-end data leaves out.")}

        <h2 id="beginnings">Beginnings: The 1969 Song That Needed a Second Try</h2>
{p("Robert Lamm wrote Beginnings for the debut album, and it was the band's second single after Questions 67 and 68.",
   "The first release, on October 28, 1969, did not reach the Billboard or Cash Box charts.",
   "Then on June 11, 1971, Columbia reissued it as a double-sided single with Colour My World on the flip.",
   "That version reached number seven on the Hot 100 and number one on the Billboard Easy Listening chart.",
   "It ranks #56 on the 1971 year-end list under the name Beginnings / Colour My World.")}
{p("Lamm said an Ash Grove performance by Richie Havens in Los Angeles inspired the song.",
   "He also said he wrote it on a twelve-string guitar missing its two low E strings.",
   'To meet another act from the decade, spin the <a href="/pages/random-artist-picker">Random Artist Picker</a>.')}

        <h2 id="three-albums">Chicago V, VI and VII: Five Hits in Three Years</h2>
{p("From 1972 to 1974 the band put five singles in the playable list.",
   'Some of the later ones are tagged soft rock in the site data, and that genre has its own page: <a href="/blog/genres/70s-soft-rock/">70s soft rock</a>.')}

        <h3>Saturday in the Park</h3>
{p("Robert Lamm wrote Saturday in the Park for Chicago V.",
   "It came out on July 13, 1972, and reached number three, which was the band's highest chart spot at the time.",
   "It also reached number two in Canada and went gold.",
   "Wikipedia says the sources conflict on where it came from.",
   "Walter Parazaider recalled the band recording Chicago III in New York City on July 4, 1970, and Lamm coming back from Central Park very excited.",
   "Lamm has said he wrote it while watching footage he shot in Central Park over a few years in the early 1970s.")}
{p("The song helped Chicago V reach number one on the album chart.",
   "Billboard ranked it #76 for 1972.")}

        <h3>Feelin' Stronger Every Day and Just You 'n' Me</h3>
{p("Chicago VI arrived in 1973 with two songs in the playable list.",
   "Peter Cetera and James Pankow wrote Feelin' Stronger Every Day, and it came out on June 5, 1973, as the first single.",
   "It reached number 10.",
   "Drummer Danny Seraphine said Cetera wrote it about his marriage falling apart.",
   "Cetera recalled that it began with a riff Pankow was playing before a delayed outdoor gig at the Akron Rubber Bowl.")}
{p("Pankow wrote Just You 'n' Me alone, and it came out on September 7, 1973.",
   "He wrote it after a fight with his future wife Karen, and said it poured out of him in its entirety.",
   "It reached number four on the Hot 100 and number one on Cash Box.",
   "It later went gold, and Chicago station WLS played it as its final song before switching to talk radio in 1989.")}

        <h3>Searchin' So Long and Call on Me</h3>
{p("Chicago VII brought two more Chicago band songs.",
   "James Pankow wrote (I've Been) Searchin' So Long, and Cetera sang it.",
   "It came out on February 21, 1974, reached number nine, and ranks #73 for 1974.",
   "Cash Box called it a dreamy, progressive ballad.")}
{p("Lee Loughnane wrote Call on Me, the first of his compositions the band released.",
   "Cetera sang it, and Wikipedia says he helped rewrite the lyrics and melody without credit.",
   "It came out on May 31, 1974, reached number six and went to number one on the Adult Contemporary chart.",
   "Conga drums played by Guille Garcia run through the arrangement.",
   "It ranks #98 on the 1974 year-end list.")}

        <h3>Old Days</h3>
{p("James Pankow wrote Old Days in 1975 as a nostalgic song about his childhood.",
   "He cited The Howdy Doody Show and collecting baseball cards and comic books.",
   "It came out in April 1975 on Chicago VIII, with Cetera singing, and reached number five.",
   "It peaked at number three on the Adult Contemporary chart.",
   "The band later stopped playing it live because Cetera refused to sing it, calling the lyrics corny.")}
{p("Old Days is one of the four Chicago band songs that no year-end list in this site's data includes.",
   'To test what you know about the decade, take the <a href="/pages/70s-trivia-quiz">70s Music Trivia Quiz</a>.')}

        <h2 id="if-you-leave-me-now">If You Leave Me Now: The One Number One</h2>
{p("Peter Cetera wrote If You Leave Me Now and sang the lead.",
   "The band cut it in March and April 1976 for Chicago X, and Columbia released it as a single on July 30, 1976.",
   f"On October 23, 1976, it became the band's first number one, and it held the top spot for {NUM[leave['weeks']]} weeks.",
   f"It ranks #{ye_by_title['If You Leave Me Now']} on the 1976 year-end list.")}

        <h3>An Acoustic Guitar and a McCartney Mix-Up</h3>
{p("Guercio played acoustic guitar on the demo, and the band kept his part on the final record.",
   "Cetera recalled that the track was recorded live with the band, then his vocal was redone and Terry Kath added electric guitar.",
   "Parazaider heard it on the radio and at first thought it sounded like Paul McCartney.",
   "Wikipedia says it sold 1.4 million copies in the US by August 1978.")}

        <h3>Grammys and the UK Chart</h3>
        <ul>
          <li>It won Best Pop Vocal Performance by a Duo, Group or Chorus, the band's first Grammy.</li>
          <li>It won Best Arrangement Accompanying Vocalist(s), for arranger Jimmie Haskell and producer Guercio.</li>
          <li>It was nominated for Record of the Year.</li>
          <li>It reached number one in the UK and stayed there for three weeks.</li>
        </ul>
{p('For another band whose biggest years came in the mid-70s, read the story of <a href="/blog/artists/fleetwood-mac-songs/">Fleetwood Mac songs</a>.')}

        <h2 id="after-kath">Baby, What a Big Surprise and the End of an Era</h2>
{p("Peter Cetera wrote Baby, What a Big Surprise for Chicago XI, and it came out in September 1977.",
   "It reached number four.",
   "Wikipedia calls it the band's last top 10 single before the accidental death of guitarist Terry Kath, and the last top 10 single Guercio produced.",
   "Carl Wilson of the Beach Boys and Tim Cetera sang extra backing vocals.",
   "Parazaider plays flute on the introduction, and Loughnane plays piccolo trumpet.")}
{p("Terry Kath died on January 23, 1978, from an accidental, self-inflicted gunshot wound.",
   "He believed the gun was unloaded.",
   "Cetera left the band in the summer of 1985.",
   "Baby, What a Big Surprise closes the run of Chicago band songs in the playable list.")}

        <h2 id="who-wrote-what">Who Wrote What: Lamm, Pankow and Cetera</h2>
{p(f"Four writers share all {NUM[n]} Chicago band songs in the playable list.",
   "James Pankow wrote four, Robert Lamm wrote four, and Peter Cetera wrote two.",
   "Lee Loughnane wrote one, and Cetera and Pankow shared one.",
   "The table shows who wrote each song and when it came out.",
   "It also shows how high each climbed on the weekly Hot 100.")}

{tbl("Chicago band songs of the 70s: writer, release, album and weekly Hot 100 peak (Wikipedia)", ["Song", "Written by", "Released", "Album", "Weekly Hot 100 Peak"], writer_rows)}

        <h3>Keep Exploring</h3>
{p("Chicago band songs of the 70s are the sound of a rock band that learned to write ballads without losing its horns.",
   "The year-end list keeps only eight of them, and the weekly chart tells the rest of the story.")}

        <h2 id="sources">Sources</h2>
{p("Year-end ranks and Hot 100 number ones come from this site's own Billboard data, described on the <a href='/about/methodology/'>methodology page</a>.",
   'Every list on <a href="/">Music of the 70s</a> plays inside the page.',
   "Peaks, dates and stories behind the Chicago band songs above can be checked against these outside sources:")}
        <ul>
          <li><a href="https://en.wikipedia.org/wiki/Chicago_(band)" rel="noopener">Wikipedia: Chicago (band)</a> for the formation, the members, the albums, Terry Kath's death and Peter Cetera's departure.</li>
          <li><a href="https://en.wikipedia.org/wiki/If_You_Leave_Me_Now" rel="noopener">Wikipedia: If You Leave Me Now</a> for the number one, the Grammys and the recording.</li>
          <li><a href="https://en.wikipedia.org/wiki/Make_Me_Smile" rel="noopener">Wikipedia: Make Me Smile</a> and <a href="https://en.wikipedia.org/wiki/25_or_6_to_4" rel="noopener">25 or 6 to 4</a> for the Chicago II singles.</li>
          <li><a href="https://en.wikipedia.org/wiki/Beginnings_(Chicago_song)" rel="noopener">Wikipedia: Beginnings</a> and <a href="https://en.wikipedia.org/wiki/Does_Anybody_Really_Know_What_Time_It_Is%3F" rel="noopener">Does Anybody Really Know What Time It Is?</a> for the debut album songs.</li>
          <li><a href="https://en.wikipedia.org/wiki/Saturday_in_the_Park" rel="noopener">Wikipedia: Saturday in the Park</a> and <a href="https://en.wikipedia.org/wiki/Feelin%27_Stronger_Every_Day" rel="noopener">Feelin' Stronger Every Day</a> for the 1972 and 1973 hits.</li>
          <li><a href="https://en.wikipedia.org/wiki/Just_You_%27n%27_Me" rel="noopener">Wikipedia: Just You 'n' Me</a>, <a href="https://en.wikipedia.org/wiki/(I%27ve_Been)_Searchin%27_So_Long" rel="noopener">Searchin' So Long</a> and <a href="https://en.wikipedia.org/wiki/Call_on_Me_(Chicago_song)" rel="noopener">Call on Me</a> for the 1973 and 1974 singles.</li>
          <li><a href="https://en.wikipedia.org/wiki/Old_Days" rel="noopener">Wikipedia: Old Days</a> and <a href="https://en.wikipedia.org/wiki/Baby,_What_a_Big_Surprise" rel="noopener">Baby, What a Big Surprise</a> for the 1975 and 1977 singles.</li>
        </ul>

        <section class="faq-block" id="faq">
          <h2>Frequently Asked Questions</h2>
{faq_html}
        </section>'''

    related = [
        ("fleetwood-mac-1977", "Artists", "Fleetwood Mac Songs: 9 Hits Played, 1 at Number One", "/blog/artists/fleetwood-mac-songs/",
         "Rumours, Dreams and every Fleetwood Mac hit playable.", "Fleetwood Mac members in a 1977 Rumours advertisement"),
        ("70s-bands", "Artists", "70s Bands: The Groups That Ruled the Hot 100", "/blog/artists/70s-bands/",
         "Every band ranked by year-end Hot 100 hits, sortable and playable.", "Bar chart of the top ten 70s bands by year-end Hot 100 hits"),
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
  <meta property="og:image" content="https://musicofthe70s.net/images/blog/{IMG}-960w.jpg">
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
      {{"@type": "ListItem", "position": 4, "name": "Chicago Band Songs", "item": "{URL}"}}
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
        Chicago Band Songs
      </nav>

      <article class="section seo-content">
        <h1>{TITLE}</h1>

        <p class="post-byline">By <a href="https://musicofthe70s.net/about/author/">Charlie</a> &middot; Published {PUBLISHED.strftime('%B')} {PUBLISHED.day}, {PUBLISHED.year}</p>
        <p class="jump-to-list"><a class="btn-primary jump-btn" href="#chicago-band-songs-list">&#9654; Jump to the playable list</a></p>

        <p class="post-intro">Chicago band songs of the 1970s run from horn-driven rock to number one ballads, and this page plays {NUM[n]} of them.</p>
        <p class="post-intro">Eight made a Year-End Hot 100, and If You Leave Me Now reached number one for two weeks in October 1976.</p>
        <p class="post-intro">The band went by Chicago Transit Authority until 1969, and its first hits came from that debut album.</p>
        <p class="post-intro">Press Play on every hit below, then read the story behind each one.</p>

{feat_pic}
        <p class="post-img-caption">Chicago, in a Columbia Records photo from about 1973.</p>
        <p class="post-img-caption">Image credit: Columbia Records, public domain, via Wikimedia Commons (Billboard, July 7, 1973).</p>

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
    print(f"wrote {out}: {n} rows, {n1} number one, {wk1} week, ye years {ye_years}, missing {missing}")


if __name__ == "__main__":
    main()
