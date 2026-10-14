#!/usr/bin/env python3
"""Build the Earth, Wind & Fire Songs Artists post (blog/artists/earth-wind-and-fire-songs/index.html).

Data: data/radio/radio-songs.json (eight Earth, Wind & Fire rows of the 1975, 1976, 1978 and 1979 Year-End Hot 100,
each with a YouTube ID), data/billboard/hot100_weekly.json (Shining Star, the one Hot 100 number one in the site's
1970-1979 weekly data), data/billboard/beyond_year_end.json (four further singles on the weekly Hot 100 but on no 1970s
year-end list: Saturday Nite, Can't Hide Love, Fantasy and Got to Get You into My Life, peaks and YouTube IDs checked).
Year-End Rank is the year-end rank, never a peak. Hot 100, soul and UK peaks, release dates, writers, certifications and
story facts come from the linked Wikipedia articles, checked 2026-10-14, and are credited to Wikipedia on the page.
The site JSON's fun_fact and trivia text for Earth, Wind & Fire is not used.

Run: python3 scripts/generate_earth_wind_fire_page.py
"""
import html
import json
from datetime import date

from genre_page_common import ROOT, read, play_button, write
from generate_country_page import p, tbl, pic

SLUG = "earth-wind-and-fire-songs"
PAGE = f"blog/artists/{SLUG}/"
URL = f"https://musicofthe70s.net/{PAGE}"
IMG = "earth-wind-and-fire-1977"
CHART = "earth-wind-and-fire-peaks"
PUBLISHED = date(2026, 10, 14)
E = "Earth, Wind &amp; Fire"
NUM = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
       10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen"}

# title -> (release year, Hot 100 peak, soul chart peak, UK peak or None, released text, album, written by)
# Every value read from the song's Wikipedia article or the Earth, Wind & Fire discography, checked 2026-10-14.
INFO = {
    "Shining Star": (1975, 1, 1, None, "January 21, 1975", "That's the Way of the World",
                     "Maurice White, Larry Dunn and Philip Bailey"),
    "That's the Way of the World": (1975, 12, 5, None, "June 17, 1975", "That's the Way of the World",
                                    "Maurice White, Charles Stepney and Verdine White"),
    "Sing a Song": (1975, 5, 1, None, "November 1975", "Gratitude", "Maurice White and Al McKay"),
    "Can't Hide Love": (1976, 39, 11, None, "1976", "Gratitude", "Skip Scarborough"),
    "Getaway": (1976, 12, 1, None, "July 7, 1976", "Spirit", "Bernard Taylor and Peter Cor Belenky"),
    "Saturday Nite": (1976, 21, 4, 17, "1976", "Spirit", "Maurice White, Al McKay and Philip Bailey"),
    "Serpentine Fire": (1977, 13, 1, None, "October 15, 1977", "All 'n All",
                        "Maurice White, Verdine White and Reginald Burke"),
    "Fantasy": (1978, 32, 12, 14, "January 1978", "All 'n All", "Maurice White, Verdine White and Eddie del Barrio"),
    "Got to Get You into My Life": (1978, 9, 1, 33, "July 14, 1978", "Sgt. Pepper's Lonely Hearts Club Band soundtrack",
                                    "John Lennon and Paul McCartney (Beatles cover)"),
    "September": (1978, 8, 1, 3, "November 18, 1978", "The Best of Earth, Wind & Fire, Vol. 1",
                  "Allee Willis and Maurice White"),
    "Boogie Wonderland": (1979, 6, 2, 4, "April 24, 1979", "I Am", "Allee Willis and Jon Lind"),
    "After the Love Has Gone": (1979, 2, 2, 4, "July 1979", "I Am", "David Foster, Jay Graydon and Bill Champlin"),
}
ORDER = list(INFO)
BEYOND = {"Saturday Nite", "Can't Hide Love", "Fantasy", "Got to Get You into My Life"}
BILLED = {"Boogie Wonderland": "Earth, Wind & Fire with The Emotions"}


def main():
    radio = json.loads(read(ROOT / "data/radio/radio-songs.json"))
    weekly = json.loads(read(ROOT / "data/billboard/hot100_weekly.json"))
    beyond = {s["title"]: s for s in json.loads(read(ROOT / "data/billboard/beyond_year_end.json"))["songs"]
              if s["page"] == PAGE}

    ye = {s["title"]: s for s in radio
          if s["artist"].startswith("Earth, Wind & Fire") and s.get("youtube_id")}
    assert len(ye) == 8, len(ye)
    assert set(beyond) == BEYOND, set(beyond)
    assert set(ye) | BEYOND == set(INFO), (set(ye) | BEYOND) ^ set(INFO)
    for t in BEYOND:
        assert beyond[t]["weekly_peak"] == INFO[t][1], t
        assert beyond[t]["released"] == INFO[t][0], t
    for t, s in ye.items():
        assert s["year"] in (INFO[t][0], INFO[t][0] + 1), (t, s["year"])

    # weekly number ones by Earth, Wind & Fire in the site's own 1970-1979 data
    wk = {}
    for yr in weekly:
        for w in weekly[yr]:
            if w["artist"] == "Earth, Wind & Fire":
                wk.setdefault(w["title"], []).append(w)
    assert set(wk) == {"Shining Star"} and len(wk["Shining Star"]) == 1, set(wk)
    ss_week = wk["Shining Star"][0]["week_start"]
    assert ss_week == "1975-05-24", ss_week

    rk = {t: ye[t]["rank"] for t in ye}
    r_way = rk["That's the Way of the World"]
    n = len(INFO)
    assert n == 12
    top_ten = [t for t in INFO if INFO[t][1] <= 10]
    assert len(top_ten) == 6, top_ten
    soul_ones = [t for t in INFO if INFO[t][2] == 1]
    assert len(soul_ones) == 6, soul_ones
    yt = {t: (ye[t]["youtube_id"] if t in ye else beyond[t]["youtube_id"]) for t in INFO}

    rows = []
    for t in ORDER:
        y, pk, soul, uk, rel, alb, wr = INFO[t]
        ye_year = ye[t]["year"] if t in ye else ""
        ye_rank = ye[t]["rank"] if t in ye else ""
        rows.append(f'              <tr><td class="ohw-listen">{play_button(yt[t], t, BILLED.get(t, "Earth, Wind & Fire"))}</td>'
                    f'<td class="ohw-song">{html.escape(t)}</td>'
                    f'<td>{y}</td><td>{ye_year}</td><td>{ye_rank}</td><td>{pk}</td></tr>')

    peak_rows = sorted(([html.escape(t), INFO[t][1], INFO[t][2], INFO[t][4]] for t in ORDER), key=lambda r: (r[1], r[0]))
    uk_rows = sorted(([html.escape(t), INFO[t][1], INFO[t][3], INFO[t][4]] for t in ORDER if INFO[t][3] is not None),
                     key=lambda r: r[2])
    assert len(uk_rows) == 6
    album_rows = [[html.escape(t), INFO[t][4], html.escape(INFO[t][5]), html.escape(INFO[t][6])] for t in ORDER]

    faq = [
        ("What is Earth, Wind and Fire's biggest hit?",
         ["Shining Star is Earth, Wind and Fire's biggest hit of the 70s, the only one to reach number one on the Billboard Hot 100 in this site's weekly chart data.",
          "It spent one week at the top, starting May 24, 1975, and it ranks #7 on the 1975 Year-End Hot 100.",
          "Wikipedia says it also topped the soul chart and won a Grammy."]),
        ("How many number one songs did Earth, Wind and Fire have in the 1970s?",
         ["Earth, Wind and Fire had one Hot 100 number one in the 1970s, Shining Star in 1975.",
          "Six of their songs reached number one on the soul chart, according to Wikipedia: Shining Star, Sing a Song, Getaway, Serpentine Fire, Got to Get You into My Life and September.",
          "After the Love Has Gone came closest on the Hot 100, stopping at number two."]),
        ("Who wrote September by Earth, Wind and Fire?",
         ["Allee Willis and Maurice White wrote September, based on a music sequence by Al McKay, according to Wikipedia.",
          "It was released on November 18, 1978, and it reached number eight on the Hot 100, number one on the soul chart and number three in the UK.",
          "It entered the Library of Congress National Recording Registry in 2018."]),
        ("Which Earth, Wind and Fire albums reached number one in the 1970s?",
         ["Two Earth, Wind and Fire albums reached number one on the Billboard 200 in the 1970s: That's the Way of the World and Gratitude.",
          "Both also topped the soul albums chart, per Wikipedia.",
          "All 'n All reached number three on the Billboard 200, and number one on the soul albums chart."]),
        ("Who sang with Earth, Wind and Fire on Boogie Wonderland?",
         ["The Emotions sang with Earth, Wind and Fire on Boogie Wonderland, and the single is credited to both acts.",
          "Wanda, Jeanette and Sheila Hutchinson provide the backing vocals, according to Wikipedia.",
          "It was released on April 24, 1979, from the album I Am, and it reached number six on the Hot 100 and number four in the UK."]),
    ]
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": " ".join(a)}} for q, a in faq]},
        indent=2, ensure_ascii=False)
    faq_ld = "\n".join("  " + l for l in faq_ld.split("\n"))
    faq_html = "\n".join(
        f'          <div class="faq-item">\n            <h3>{html.escape(q)}</h3>\n' + "\n".join(f"            <p>{html.escape(l)}</p>" for l in a) + "\n          </div>"
        for q, a in faq).replace("&#x27;", "'")

    TITLE = f"Earth Wind and Fire Songs: {n} Hits Played, 1 at No. 1"
    desc = (f"Earth Wind and Fire songs of the 70s, all {n} playable: Shining Star, September, Boogie Wonderland and more. "
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

    toc = [("earth-wind-and-fire-songs-list", f"Earth Wind and Fire Songs: Play All {n} Hits"),
           ("by-the-numbers", "Earth Wind and Fire Songs on the Charts: One Number One, Six Top Tens"),
           ("origins", "From Chicago to Caribou Ranch: How Earth, Wind &amp; Fire Began"),
           ("mid-70s", "1975 and 1976: Shining Star, That's the Way of the World, Sing a Song and Getaway"),
           ("spirit-years", "Can't Hide Love and Saturday Nite: The Spirit Era"),
           ("all-n-all", "All 'n All: Serpentine Fire and Fantasy"),
           ("september-years", "1978: Got to Get You into My Life and September"),
           ("i-am", "1979: Boogie Wonderland and After the Love Has Gone"),
           ("who-wrote-what", "Who Wrote and Released Each of the Earth Wind and Fire Songs"),
           ("sources", "Sources"), ("faq", "Frequently Asked Questions")]
    toc_html = "\n".join(f'            <li><a href="#{i}">{t}</a></li>' for i, t in toc)

    feat_pic = pic(IMG, "Earth, Wind and Fire in a black and white 1977 Columbia Records press photo, nine members standing close together, the Earth Wind and Fire songs lineup",
                   "(max-width: 700px) 100vw, 669px", 669, 440, widths=(400, 669), lazy=False).replace(
        'class="post-featured-img"', 'class="post-featured-img" style="aspect-ratio:669/440;max-width:669px;height:auto;margin:1.5rem auto"', 1)
    chart_pic = pic(CHART, "Lollipop chart of twelve Earth, Wind and Fire songs by weekly Billboard Hot 100 peak, from Shining Star at number one to Can't Hide Love at number 39",
                    "(max-width: 700px) 100vw, 800px", 800, 450, widths=(400, 800, 1200)).replace(
        "<img\n", '<img style="display:block;width:100%;max-width:800px;height:auto;margin:1.5rem auto;border-radius:8px"\n', 1)

    body = f'''        <h2 id="earth-wind-and-fire-songs-list">Earth Wind and Fire Songs: Play All {n} Hits</h2>
{p(f"Here are {NUM[n]} Earth Wind and Fire songs from 1975 to 1979, from Shining Star to After the Love Has Gone.",
   "Eight sit on a Billboard Year-End Hot 100, and four more charted weekly without making a year-end list.",
   "Press Play on any row to watch it here, and tap a heading to sort.")}

        <div class="data-table-wrap scroll-list">
          <table class="data-table sortable-table" id="earthWindFireSongsTable" data-inline-player>
            <caption>{n} Earth, Wind &amp; Fire songs of the 70s, with release year, Billboard Year-End Hot 100 rank and Hot 100 peak</caption>
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
   "The one number one is the Hot 100 chart topper in this site's weekly chart data.")}

        <h2 id="by-the-numbers">Earth Wind and Fire Songs on the Charts: One Number One, Six Top Tens</h2>
{p("The Earth Wind and Fire songs of the 70s were bigger on the soul chart than on the Hot 100.",
   "Only Shining Star reached number one on the Hot 100, and this site's weekly chart data gives it one week at the top, starting May 24, 1975.",
   "Six of the songs on this page reached number one on the soul chart, according to Wikipedia.",
   "That list is Shining Star, Sing a Song, Getaway, Serpentine Fire, Got to Get You into My Life and September.")}

{chart_pic}
        <p class="post-img-caption">Weekly Hot 100 peaks of the twelve Earth, Wind &amp; Fire songs on this page, from each song's Wikipedia article.</p>

{tbl("Earth, Wind &amp; Fire songs of the 70s ranked by weekly Hot 100 peak, with the soul chart peak and release date (Wikipedia)", ["Song", "Hot 100 Peak", "Soul Chart Peak", "Released"], peak_rows)}

        <h3>What the Chart Numbers Say</h3>
{p(f"Six of the {NUM[n]} Earth Wind and Fire songs on this page reached the Hot 100's top ten.")}
        <ul>
          <li>Shining Star reached number one on the Hot 100, in 1975.</li>
          <li>After the Love Has Gone stalled at number two in 1979, behind My Sharona by The Knack.</li>
          <li>Sing a Song, Boogie Wonderland, September and Got to Get You into My Life all reached the top ten.</li>
          <li>Shining Star ranks #{rk['Shining Star']} on the 1975 Year-End Hot 100, the best year-end rank of any song here, ahead of After the Love Has Gone at #{rk['After the Love Has Gone']}.</li>
          <li>Of the seven songs released before 1978, only Shining Star and Sing a Song reached the top ten.</li>
        </ul>
{p('To see which groups charted the most, read the page on <a href="/blog/artists/70s-bands/">70s bands</a>, ranked by year-end hits.')}

        <h3>The UK Chart Told a Similar Story</h3>
{p(f"{NUM[len(uk_rows)].capitalize()} of these songs have a UK peak in the Wikipedia articles used for this page.",
   "September did best, reaching number three.",
   "Boogie Wonderland and After the Love Has Gone both reached number four.")}

{tbl("Earth Wind and Fire songs of the 70s with a UK Singles Chart peak next to the Hot 100 peak (Wikipedia)", ["Song", "Hot 100 Peak", "UK Peak", "Released"], uk_rows)}

        <h2 id="origins">From Chicago to Caribou Ranch: How Earth, Wind &amp; Fire Began</h2>
{p("The story behind the Earth Wind and Fire songs starts in Chicago, Illinois.",
   "Wikipedia says Maurice White formed the band there in 1969, and that the group began as the Salty Peppers.",
   "His younger brother Verdine White moved from Chicago to Los Angeles on June 6, 1970, to become the bassist.",
   "Philip Bailey joined as a vocalist in 1972, when Maurice re-formed the group after the first lineup split.",
   'To meet more voices from the decade, spin the <a href="/pages/random-artist-picker">Random Artist Picker</a>.')}

        <h3>The Lineup and the Phenix Horns</h3>
{p("The 1970s lineup grew over the years.",
   "Larry Dunn played keyboards, Ralph Johnson played percussion, and Andrew Woolfolk played saxophone.",
   "Al McKay and Johnny Graham played guitar, and Fred White played drums after the album Open Our Eyes.",
   "Around 1975, the Phenix Horns formed, with Don Myrick, Louis Satterfield, Rahmlee Davis and Michael Harris.")}
{p("Wikipedia says the band is known for its kalimba sound, and the production credits on its records read Kalimba Productions.")}

        <h3>Two Number One Albums</h3>
{p("The albums made the hits.",
   "That's the Way of the World reached number one on the Billboard 200 and the soul albums chart.",
   "Gratitude, a double live album, did the same.",
   "Open Our Eyes reached number one on the soul albums chart, and so did All 'n All, which stopped at number three on the Billboard 200.",
   'For more of the sound they helped define, read the page on <a href="/blog/genres/70s-soul-music/">70s soul music</a>.')}

        <h2 id="mid-70s">1975 and 1976: Shining Star, That's the Way of the World, Sing a Song and Getaway</h2>
{p("The mid-70s were the first big run of Earth Wind and Fire songs on the radio.",
   "Four singles from three albums ranked on the 1975 and 1976 year-end lists.")}

        <h3>Shining Star</h3>
{p("Shining Star was released on January 21, 1975, from That's the Way of the World, and Maurice White, Larry Dunn and Philip Bailey wrote it.",
   "Maurice White and Charles Stepney produced it, and it was recorded in the autumn of 1974.",
   "Wikipedia says Maurice conceived the song while strolling at night at Caribou Ranch, inspired by the starry sky.")}
{p(f"It was the band's first single to top the Hot 100 and the soul chart, and it ranks #{rk['Shining Star']} on the 1975 Year-End Hot 100.",
   "It won the Grammy for Best R&amp;B Performance by a Duo or Group with Vocals, and the RIAA certified it Gold.",
   "The Grammy Hall of Fame inducted it in 2008, and MC Lyte, Snoop Dogg and Salt-N-Pepa are among the acts that sampled it.",
   'Spin a different decade favorite with the <a href="/pages/random-70s-song">Random 70s Song Generator</a>.')}

        <h3>That's the Way of the World</h3>
{p("That's the Way of the World was released on June 17, 1975, as the title track of the album, with Africano on the B-side.",
   "Maurice White, Charles Stepney and Verdine White wrote it, and Maurice produced it.",
   f"It reached number 12 on the Hot 100 and number five on the soul chart, and it ranks #{r_way} on the 1975 Year-End Hot 100.")}
{p("Rolling Stone placed it at number 329 on its 2004 list of the 500 greatest songs, per Wikipedia.",
   "Dwele covered it on the 2007 tribute compilation Interpretations: Celebrating the Music of Earth, Wind &amp; Fire, and earned a Grammy nomination for it.")}

        <h3>Sing a Song</h3>
{p("Sing a Song was released in November 1975, from Gratitude, and Maurice White and Al McKay wrote it.",
   "Maurice White and Charles Stepney produced it.",
   f"It reached number five on the Hot 100 and number one on the soul chart for two weeks, and it ranks #{rk['Sing a Song']} on the 1976 Year-End Hot 100.",
   "The RIAA certified it Gold.")}
{p("Beyonc&eacute; sampled it on Hey Goldmember, from Austin Powers in Goldmember, in 2002.",
   "Take 6 and Point of Grace both covered it in 1996.")}

        <h3>Getaway</h3>
{p("Getaway was released on July 7, 1976, as the first single from the album Spirit.",
   "Bernard Taylor and Peter Cor Belenky wrote it, and Maurice White and Charles Stepney produced it.",
   f"It reached number 12 on the Hot 100 and number one on the soul chart, and it ranks #{rk['Getaway']} on the 1976 Year-End Hot 100.",
   "The RIAA certified it Gold.")}
{p("Music Week credited Philip Bailey's falsetto with sweetening the song's funky rhythms in 1976.",
   "A remix appears in the video game Gran Turismo 4, and Boards of Canada sampled it on Sixtyten.",
   'For more of the same groove, read the page on <a href="/blog/genres/70s-funk/">70s funk</a>.')}

        <h2 id="spirit-years">Can't Hide Love and Saturday Nite: The Spirit Era</h2>
{p("Two more singles from 1976 never made a year-end list, but both charted weekly.",
   "Can't Hide Love came from the Gratitude sessions, and Saturday Nite came from Spirit.")}

        <h3>Can't Hide Love</h3>
{p("Skip Scarborough wrote Can't Hide Love, and Maurice White and Charles Stepney produced the single, released in 1976.",
   "Wikipedia says it was recorded in 1975, with Gratitude as the album.",
   "It reached number 39 on the Hot 100 and number 11 on the soul chart, and it earned a Grammy nomination for Best Instrumental Arrangement Accompanying Vocalist(s).",
   "It is on no 1970s year-end list, so its peak above is a weekly peak only.")}
{p("Drake sampled it on Beautiful Life in 2009, and Rick Ross sampled it on Capone Suite.",
   "Prince performed it live at the Hotel Gansevoort in Manhattan in 2008, per Wikipedia.")}

        <h3>Saturday Nite</h3>
{p("Maurice White, Al McKay and Philip Bailey wrote Saturday Nite, and Maurice produced it.",
   "It was released in 1976, with Departure on the B-side.",
   "It reached number 21 on the Hot 100 and number four on the soul chart.",
   "It also reached number 17 in the UK, which was the band's first UK hit.")}
{p("The Spice Girls sampled it on Say You'll Be There in 1996.")}

        <h2 id="all-n-all">All 'n All: Serpentine Fire and Fantasy</h2>
{p("All 'n All was the band's 1977 album, and it brought two more of the Earth Wind and Fire songs to the radio.",
   "It reached number one on the soul albums chart and number three on the Billboard 200.")}

        <h3>Serpentine Fire</h3>
{p("Serpentine Fire was released on October 15, 1977, and Maurice White, Verdine White and Reginald Burke wrote it.",
   "Maurice produced it for Kalimba Productions, and Tom Tom 84 arranged it.",
   f"It reached number 13 on the Hot 100, and it ranks #{rk['Serpentine Fire']} on the 1978 Year-End Hot 100.")}
{p("It spent seven weeks at number one on the soul chart, and Wikipedia says Billboard named it the R&amp;B single of the year.",
   "Dave Marsh ranked it number 307 in his 1989 book The 1001 Greatest Singles Ever Made.")}

        <h3>Fantasy</h3>
{p("Fantasy was released in January 1978, and Maurice White, Verdine White and Eddie del Barrio wrote it.",
   "It reached number 32 on the Hot 100, number 12 on the soul chart and number 14 in the UK.",
   "It earned a Grammy nomination for Best R&amp;B Song.",
   "It is on no 1970s year-end list, so its peak above is a weekly peak only.")}
{p("Wikipedia says the song took three months to compose, and that Maurice finished it after he was inspired by Close Encounters of the Third Kind.",
   "The album version runs 4:38, and the single version runs 3:46.",
   "Black Box covered it in 1990, and that version reached number five in the UK.",
   'Test your memory of the decade with the <a href="/pages/70s-trivia-quiz">70s Music Trivia Quiz</a>.')}

        <h2 id="september-years">1978: Got to Get You into My Life and September</h2>
{p("Two singles in 1978 came out around a film and a greatest hits album.",
   "Both reached number one on the soul chart.")}

        <h3>Got to Get You into My Life</h3>
{p("Got to Get You into My Life was released on July 14, 1978, a cover of the Beatles song.",
   "The band recorded it for the film Sgt. Pepper's Lonely Hearts Club Band, and it also appears on the compilation The Best of Earth, Wind &amp; Fire, Vol. 1.",
   "Maurice White produced it.",
   "It reached number nine on the Hot 100 and number one on the soul chart, and it reached number 33 in the UK.")}
{p("It won the Grammy for Best Instrumental Arrangement Accompanying Vocalist(s), and it was nominated for Best Pop Performance by a Duo or Group with Vocals.",
   "It is on no 1970s year-end list, so its peak above is a weekly peak only.")}

        <h3>September</h3>
{p("September was released on November 18, 1978, from The Best of Earth, Wind &amp; Fire, Vol. 1, where it was one of two new tracks.",
   "Allee Willis and Maurice White wrote it, based on a music sequence by Al McKay, and Maurice produced it.",
   "It was recorded in September 1978.")}
{p(f"It reached number eight on the Hot 100, and it ranks #{rk['September']} on the 1979 Year-End Hot 100.",
   "It reached number one on the soul chart and number three in the UK.")}
        <h3>The Lyric Story Behind September</h3>
{p("Wikipedia says Allee Willis disliked the nonsense syllables in the lyric and asked Maurice to rewrite it.",
   "His answer was that the lyric did not matter much, and Willis later called it a lesson in letting the groove lead.",
   "The lyrics refer to the 21st of September.")}
{p("Kirk Franklin released a gospel cover in 2007, and Phats &amp; Small released a remix, September '99, in 1999.",
   "The Library of Congress added the song to the National Recording Registry in 2018.",
   'Dance to more of this era with the page on <a href="/blog/genres/disco-music-of-the-70s/">70s disco music</a>.')}

        <h2 id="i-am">1979: Boogie Wonderland and After the Love Has Gone</h2>
{p("The album I Am gave the band its last two songs of the decade.",
   f"Both reached the top ten, and both are on the 1979 Year-End Hot 100, at #{rk['After the Love Has Gone']} and #{rk['Boogie Wonderland']}.")}

        <h3>Boogie Wonderland</h3>
{p("Boogie Wonderland was released on April 24, 1979, as the first single from I Am.",
   "Allee Willis and Jon Lind wrote it, and Maurice White and Al McKay produced it.",
   "The single is credited to Earth, Wind &amp; Fire with The Emotions, and Wanda, Jeanette and Sheila Hutchinson provide backing vocals.")}
{p(f"It reached number six on the Hot 100, number two on the soul chart and number 14 on the US Disco Top 80, and it ranks #{rk['Boogie Wonderland']} on the 1979 Year-End Hot 100.",
   "It reached number four in the UK, where it was certified Platinum, and the RIAA certified it Gold.",
   "Stretch &amp; Vern built the 1996 single I'm Alive on it, and that reached number six in the UK.")}

        <h3>After the Love Has Gone</h3>
{p("After the Love Has Gone was released in July 1979, as the second single from I Am.",
   "David Foster and Jay Graydon wrote the music, Bill Champlin wrote the lyrics, and Maurice White produced it.",
   "Wikipedia says Champlin planned it for his 1978 solo album Single before it moved to the Earth, Wind &amp; Fire album.")}
{p(f"It reached number two on the Hot 100, behind My Sharona by The Knack, and it ranks #{rk['After the Love Has Gone']} on the 1979 Year-End Hot 100.",
   "It reached number two on the soul chart, number three on the adult contemporary chart and number four in the UK.",
   "It earned Grammy nominations for Record of the Year and Song of the Year.")}
{p("It won two Grammys, Best R&amp;B Vocal Performance by a Duo or Group, and Best R&amp;B Song for Champlin, Foster and Graydon.",
   "The RIAA certified it Gold, and the BPI certified it Silver.",
   "It also played in an episode of WKRP in Cincinnati.")}

        <h3>The Grammys That Followed</h3>
{p("Wikipedia lists five Earth Wind and Fire songs and albums that won Grammys in the 70s.",
   "Shining Star, Got to Get You into My Life and After the Love Has Gone are on this page.",
   "The other two were the album All 'n All and the instrumental Runnin'.",
   'The page on <a href="/blog/artists/jackson-5-songs/">Jackson 5 songs</a> tells the story of another act that ruled the soul chart.')}

        <h2 id="who-wrote-what">Who Wrote and Released Each of the Earth Wind and Fire Songs</h2>
{p(f"The table lists when each of the {NUM[n]} songs was released, on which album, and who wrote it.",
   "Maurice White shared a writing credit on seven of them.")}

{tbl("Earth Wind and Fire songs of the 70s: release date, album and writers (Wikipedia)", ["Song", "Released", "Album", "Written By"], album_rows)}

        <h3>Keep Exploring</h3>
{p("Earth Wind and Fire songs turned a Chicago band into one of the defining acts of the 70s.",
   "One reached number one on the Hot 100, and six reached the top ten.",
   'The page on <a href="/blog/genres/70s-soul-music/">70s soul music</a> sets them beside the other voices of the decade.')}

        <h2 id="sources">Sources</h2>
{p("Year-end ranks come from this site's own Billboard data, described on the <a href='/about/methodology/'>methodology page</a>.",
   'Every list on <a href="/">Music of the 70s</a> plays inside the page.',
   "Peaks, dates and stories behind the Earth Wind and Fire songs above can be checked against these outside sources:")}
        <ul>
          <li><a href="https://en.wikipedia.org/wiki/Earth,_Wind_%26_Fire" rel="noopener">Wikipedia: Earth, Wind &amp; Fire</a> and <a href="https://en.wikipedia.org/wiki/Earth,_Wind_%26_Fire_discography" rel="noopener">its discography</a> for the band history, albums, singles and chart peaks.</li>
          <li><a href="https://en.wikipedia.org/wiki/Shining_Star_(Earth,_Wind_%26_Fire_song)" rel="noopener">Wikipedia: Shining Star</a> and <a href="https://en.wikipedia.org/wiki/That%27s_the_Way_of_the_World_(Earth,_Wind_%26_Fire_song)" rel="noopener">That's the Way of the World</a> for 1975.</li>
          <li><a href="https://en.wikipedia.org/wiki/Sing_a_Song_(Earth,_Wind_%26_Fire_song)" rel="noopener">Wikipedia: Sing a Song</a>, <a href="https://en.wikipedia.org/wiki/Getaway_(Earth,_Wind_%26_Fire_song)" rel="noopener">Getaway</a>, <a href="https://en.wikipedia.org/wiki/Can%27t_Hide_Love" rel="noopener">Can't Hide Love</a> and <a href="https://en.wikipedia.org/wiki/Saturday_Nite" rel="noopener">Saturday Nite</a> for 1975 and 1976.</li>
          <li><a href="https://en.wikipedia.org/wiki/Serpentine_Fire" rel="noopener">Wikipedia: Serpentine Fire</a> and <a href="https://en.wikipedia.org/wiki/Fantasy_(Earth,_Wind_%26_Fire_song)" rel="noopener">Fantasy</a> for All 'n All.</li>
          <li><a href="https://en.wikipedia.org/wiki/Got_to_Get_You_into_My_Life" rel="noopener">Wikipedia: Got to Get You into My Life</a> and <a href="https://en.wikipedia.org/wiki/September_(Earth,_Wind_%26_Fire_song)" rel="noopener">September</a> for 1978.</li>
          <li><a href="https://en.wikipedia.org/wiki/Boogie_Wonderland" rel="noopener">Wikipedia: Boogie Wonderland</a> and <a href="https://en.wikipedia.org/wiki/After_the_Love_Has_Gone" rel="noopener">After the Love Has Gone</a> for I Am.</li>
        </ul>

        <section class="faq-block" id="faq">
          <h2>Frequently Asked Questions</h2>
{faq_html}
        </section>'''

    related = [
        ("war-1971", "Genres", "70s Funk: Why War Out-Charted Every Other Act", "/blog/genres/70s-funk/",
         "The funk side of the decade, with every song playable.", "War in 1971"),
        ("70s-soul-music-infographic", "Genres", "70s Soul Music: The Artists Who Redefined a Genre", "/blog/genres/70s-soul-music/",
         "Where Earth, Wind &amp; Fire sits among the soul voices of the decade.", "Infographic of 70s soul music"),
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
      {{"@type": "ListItem", "position": 4, "name": "Earth Wind and Fire Songs", "item": "{URL}"}}
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
        Earth Wind and Fire Songs
      </nav>

      <article class="section seo-content">
        <h1>{TITLE}</h1>

        <p class="post-byline">By <a href="https://musicofthe70s.net/about/author/">Charlie</a> &middot; Published {PUBLISHED.strftime('%B')} {PUBLISHED.day}, {PUBLISHED.year}</p>
        <p class="jump-to-list"><a class="btn-primary jump-btn" href="#earth-wind-and-fire-songs-list">&#9654; Jump to the playable list</a></p>

        <p class="post-intro">Earth Wind and Fire songs filled the soul chart in the 70s, and one of them, Shining Star, reached number one on the Hot 100.</p>
        <p class="post-intro">This page plays {NUM[n]} of them, from Shining Star to After the Love Has Gone.</p>
        <p class="post-intro">Six reached number one on the soul chart, and September got to number three in the UK.</p>
        <p class="post-intro">Maurice White led the band from Chicago, and Philip Bailey joined in 1972.</p>
        <p class="post-intro">Press Play on every hit below, then read the story behind each one.</p>

{feat_pic}
        <p class="post-img-caption">Earth, Wind &amp; Fire in a Columbia Records press photo, circa 1977.</p>
        <p class="post-img-caption">Image credit: Photo distributed by Columbia Records, public domain in the United States, via Wikimedia Commons.</p>

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
