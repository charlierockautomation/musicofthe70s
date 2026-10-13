#!/usr/bin/env python3
"""Build the Olivia Newton-John Songs Artists post (blog/artists/olivia-newton-john-songs/index.html).

Data: data/radio/radio-songs.json (ten Olivia Newton-John rows of the Year-End Hot 100, solo and with John Travolta,
each with a YouTube ID), data/billboard/hot100_weekly.json (her three weekly Hot 100 #1s and the weeks at #1),
data/billboard/beyond_year_end.json (two further singles on the weekly Hot 100 but on no 1970s year-end list: Something
Better to Do and Sam, peaks and YouTube IDs checked). Year-End Rank is the year-end rank, never a peak. Hot 100 and
country peaks, writers, release dates and story facts come from the linked Wikipedia articles, checked 2026-10-13, and
are credited to Wikipedia on the page. The site JSON's fun_fact text for Olivia Newton-John is not used for anything
Wikipedia does not also state.

Run: python3 scripts/generate_olivia_newton_john_page.py
"""
import html
import json
from datetime import date

from genre_page_common import ROOT, read, play_button, write
from generate_country_page import p, tbl, pic

SLUG = "olivia-newton-john-songs"
PAGE = f"blog/artists/{SLUG}/"
URL = f"https://musicofthe70s.net/{PAGE}"
IMG = "olivia-newton-john-1978"
IMG2 = "olivia-newton-john-1978-awards"
PUBLISHED = date(2026, 10, 13)
NUM = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
       10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen"}

# title -> (release year, Hot 100 peak, country peak or None, released text, writers, album, artist credit)
# Every value read from the song's Wikipedia article, checked 2026-10-13.
INFO = {
    "If Not for You": (1971, 25, None, "March 1971", "Bob Dylan", "If Not for You"),
    "Let Me Be There": (1973, 6, 7, "September 1973", "John Rostill", "Let Me Be There"),
    "If You Love Me (Let Me Know)": (1974, 5, 2, "April 1974", "John Rostill", "If You Love Me, Let Me Know"),
    "I Honestly Love You": (1974, 1, 6, "August 1974", "Jeff Barry and Peter Allen", "If You Love Me, Let Me Know (US)"),
    "Have You Never Been Mellow": (1975, 1, 3, "January 1975", "John Farrar", "Have You Never Been Mellow"),
    "Please Mr. Please": (1975, 3, 5, "June 1975", "Bruce Welch and John Rostill", "Have You Never Been Mellow"),
    "Something Better to Do": (1975, 13, 19, "September 1975", "John Farrar", "Clearly Love"),
    "Sam": (1977, 20, None, "January 1977", "Don Black, Hank Marvin and John Farrar", "Don't Stop Believin'"),
    "You're the One That I Want": (1978, 1, None, "March 1978 (US)", "John Farrar", "Grease soundtrack"),
    "Summer Nights": (1978, 5, None, "July 1978 (US)", "Jim Jacobs and Warren Casey", "Grease soundtrack"),
    "Hopelessly Devoted to You": (1978, 3, 20, "June 1978", "John Farrar", "Grease soundtrack"),
    "A Little More Love": (1978, 3, None, "November 1978", "John Farrar", "Totally Hot"),
}
ORDER = list(INFO)
BEYOND = {"Something Better to Do", "Sam"}


def main():
    radio = json.loads(read(ROOT / "data/radio/radio-songs.json"))
    weekly = json.loads(read(ROOT / "data/billboard/hot100_weekly.json"))
    beyond = {s["title"]: s for s in json.loads(read(ROOT / "data/billboard/beyond_year_end.json"))["songs"]
              if s["page"] == PAGE}

    ye = {s["title"]: s for s in radio if "Newton-John" in s["artist"] and s.get("youtube_id")}
    assert len(ye) == 10, len(ye)
    assert set(beyond) == BEYOND, set(beyond)
    assert set(ye) | BEYOND == set(INFO), (set(ye) | BEYOND) ^ set(INFO)
    for t in BEYOND:
        assert beyond[t]["weekly_peak"] == INFO[t][1], t
    for t, s in ye.items():
        assert s["year"] in (INFO[t][0], INFO[t][0] + 1), (t, s["year"])

    # Weekly Hot 100 number ones from the site's own data (1970-1979).
    nones = {}
    for yr in weekly:
        for w in weekly[yr]:
            if "Newton-John" in w["artist"]:
                nones.setdefault(w["title"], []).append(w)
    assert set(nones) == {"I Honestly Love You", "Have You Never Been Mellow", "You're the One That I Want"}, set(nones)
    for t, v in nones.items():
        assert len(v) == v[0]["weeks_at_number_one"], t
        assert INFO[t][1] == 1, t
    assert sum(len(v) for v in nones.values()) == 4
    assert {t for t in INFO if INFO[t][1] == 1} == set(nones)
    n_one = len(nones)
    top_ten = [t for t in INFO if INFO[t][1] <= 10]
    assert len(top_ten) == 9

    yt = {t: (ye[t]["youtube_id"] if t in ye else beyond[t]["youtube_id"]) for t in INFO}
    who = {t: ye[t]["artist"] if t in ye else "Olivia Newton-John" for t in INFO}
    n = len(INFO)
    ytoiw = ye["You're the One That I Want"]["rank"]
    n_cn = sum(1 for t in INFO if INFO[t][2] is not None)
    assert n_cn == 7

    rows = []
    for t in ORDER:
        y, pk, cn, rel, wr, alb = INFO[t]
        ye_year = ye[t]["year"] if t in ye else ""
        ye_rank = ye[t]["rank"] if t in ye else ""
        rows.append(f'              <tr><td class="ohw-listen">{play_button(yt[t], t, who[t])}</td>'
                    f'<td class="ohw-song">{html.escape(t)}</td>'
                    f'<td>{y}</td><td>{ye_year}</td><td>{ye_rank}</td><td>{pk}</td>'
                    f'<td>{"Yes" if t in nones else ""}</td></tr>')

    crossover_rows = [[html.escape(t), INFO[t][1], INFO[t][2], INFO[t][3]] for t in ORDER if INFO[t][2] is not None]
    crossover_rows.sort(key=lambda r: r[2])

    one_rows = []
    for t, v in sorted(nones.items(), key=lambda kv: kv[1][0]["week_start"]):
        a, b = v[0]["week_start"], v[-1]["week_end"]
        wks = len(v)
        one_rows.append([html.escape(t), html.escape(v[0]["artist"]),
                         f"{wks} week{'s' if wks > 1 else ''}", a, b])

    writer_rows = [[html.escape(t), INFO[t][4], INFO[t][3], html.escape(INFO[t][5])] for t in ORDER]

    faq = [
        ("What is Olivia Newton-John's biggest song of the 1970s?",
         ["You're the One That I Want, her duet with John Travolta, is the biggest of her 1970s songs by sales and by year-end rank.",
          "It reached number one on the Hot 100 in 1978 and ranks #13 on that year's Year-End Hot 100.",
          "Wikipedia says it sold more than 4 million copies in the US and UK alone, and estimates over 15 million worldwide."]),
        ("How many number one songs did Olivia Newton-John have in the 1970s?",
         ["Olivia Newton-John had three number one songs on the Billboard Hot 100 in the 1970s, according to this site's weekly chart data.",
          "I Honestly Love You held the top spot for two weeks in October 1974.",
          "Have You Never Been Mellow had one week in March 1975, and You're the One That I Want had one week in June 1978."]),
        ("Who wrote Have You Never Been Mellow?",
         ["John Farrar wrote Have You Never Been Mellow, and he also produced Olivia Newton-John's recording of it.",
          "It was recorded in 1974 at Abbey Road Studios in London and released in January 1975.",
          "It reached number one on the Hot 100 in March 1975, and it also topped the adult contemporary chart, according to Wikipedia."]),
        ("Was Olivia Newton-John a country singer in the 1970s?",
         ["Olivia Newton-John charted on Billboard's country list with seven songs from this page, so she was a country crossover star for part of the decade.",
          "If You Love Me (Let Me Know) reached number two on the country chart in 1974.",
          "Let Me Be There won her a Grammy in the female country vocal category, according to Wikipedia."]),
        ("Who wrote Hopelessly Devoted to You from Grease?",
         ["John Farrar wrote Hopelessly Devoted to You, Olivia Newton-John's solo ballad in the film Grease.",
          "She was owed a solo in the film, and none had been written halfway through shooting, so Farrar wrote and submitted this one.",
          "It reached number three on the Hot 100 in 1978 and earned an Academy Award nomination for Best Original Song, according to Wikipedia."]),
    ]
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": " ".join(a)}} for q, a in faq]},
        indent=2, ensure_ascii=False)
    faq_ld = "\n".join("  " + l for l in faq_ld.split("\n"))
    faq_html = "\n".join(
        f'          <div class="faq-item">\n            <h3>{html.escape(q)}</h3>\n' + "\n".join(f"            <p>{html.escape(l)}</p>" for l in a) + "\n          </div>"
        for q, a in faq).replace("&#x27;", "'")

    TITLE = f"Olivia Newton-John Songs: {n} Hits Played, {n_one} at No. 1"
    desc = (f"Olivia Newton-John songs of the 70s, all {n} playable: I Honestly Love You, Have You Never Been Mellow and Grease. "
            "Read the story behind each.")
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

    toc = [("olivia-newton-john-songs-list", f"Olivia Newton-John Songs: Play All {n} Hits"),
           ("by-the-numbers", "Olivia Newton-John Songs on the Charts: Three Number Ones"),
           ("country-years", "The Country Years: If Not for You, Let Me Be There and If You Love Me"),
           ("number-ones", "The Number Ones: I Honestly Love You and Have You Never Been Mellow"),
           ("jukebox-and-radio", "Please Mr. Please, Something Better to Do and Sam"),
           ("grease", "Grease: Hopelessly Devoted to You, Summer Nights and You're the One That I Want"),
           ("totally-hot", "Totally Hot: A Little More Love"),
           ("who-wrote-what", "Who Wrote Each of the Olivia Newton-John Songs"),
           ("sources", "Sources"), ("faq", "Frequently Asked Questions")]
    toc_html = "\n".join(f'            <li><a href="#{i}">{t}</a></li>' for i, t in toc)

    feat_pic = pic(IMG, "Olivia Newton-John arriving at Schiphol airport in November 1978, holding roses, the year of her Grease hits and Olivia Newton-John songs",
                   "(max-width: 700px) 100vw, 669px", 669, 444, widths=(400, 669), lazy=False).replace(
        'class="post-featured-img"', 'class="post-featured-img" style="aspect-ratio:669/444;max-width:669px;height:auto;margin:1.5rem auto"', 1)
    award_pic = pic(IMG2, "Olivia Newton-John smiling and holding two award trophies at a Schiphol press room in November 1978",
                    "(max-width: 700px) 80vw, 360px", 480, 724, widths=(300, 480)).replace(
        "<img\n", '<img style="display:block;width:100%;max-width:360px;height:auto;margin:1.5rem auto;border-radius:8px"\n', 1)

    body = f'''        <h2 id="olivia-newton-john-songs-list">Olivia Newton-John Songs: Play All {n} Hits</h2>
{p(f"Here are {NUM[n]} Olivia Newton-John songs from 1971 to 1978, including all three of her number ones.",
   "Ten sit on a Billboard Year-End Hot 100, and two more charted weekly without making a year-end list.",
   "Press Play on any row to watch it here, and tap a heading to sort.")}

        <div class="data-table-wrap scroll-list">
          <table class="data-table sortable-table" id="oliviaNewtonJohnSongsTable" data-inline-player>
            <caption>{n} Olivia Newton-John songs of the 70s, with release year, Billboard Year-End Hot 100 rank, Hot 100 peak and number one status</caption>
            <thead>
              <tr>
                <th><span class="visually-hidden">Play</span></th>
                <th><button type="button" data-col="1" data-type="text">Song</button></th>
                <th aria-sort="ascending"><button type="button" data-col="2" data-type="num">Released</button></th>
                <th><button type="button" data-col="3" data-type="num">Year-End List</button></th>
                <th><button type="button" data-col="4" data-type="num">Year-End Rank</button></th>
                <th><button type="button" data-col="5" data-type="num">Hot 100 Peak</button></th>
                <th><button type="button" data-col="6" data-type="text">#1 Hit</button></th>
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
   "The #1 flag comes from this site's weekly chart data.",
   "The two Grease duets are credited to John Travolta and Olivia Newton-John, as the charts credit them.")}

        <h2 id="by-the-numbers">Olivia Newton-John Songs on the Charts: Three Number Ones</h2>
{p("Olivia Newton-John had three number ones in the 70s, and none of them sound alike.",
   "One is a spare ballad, one is a soft country-pop song, and one is a movie duet.",
   "The table lists each one, with the weeks it held the top spot in this site's weekly data.")}

{tbl("Olivia Newton-John's three Hot 100 number ones of the 70s: weeks at number one and week range (this site's weekly chart data)", ["Song", "Credit", "Weeks at #1", "First week starts", "Last week ends"], one_rows)}

        <h3>What the Chart Numbers Say</h3>
{p(f"Nine of the {NUM[n]} Olivia Newton-John songs on this page reached the Hot 100's top ten.")}
        <ul>
          <li>I Honestly Love You, Have You Never Been Mellow and You're the One That I Want reached number one, for four weeks in total.</li>
          <li>Please Mr. Please, A Little More Love and Hopelessly Devoted to You each stopped at number three.</li>
          <li>Let Me Be There and If You Love Me (Let Me Know) reached number six and number five, her first two US top tens.</li>
          <li>Something Better to Do, at number 13, broke a streak of five top tens in a row on both the Hot 100 and the country chart, according to Wikipedia.</li>
        </ul>
{p('Her year-end totals also put her first among women, as the page on the <a href="/blog/artists/70s-female-singers/">70s female singers</a> shows.')}

        <h2 id="country-years">The Country Years: If Not for You, Let Me Be There and If You Love Me</h2>
{p("Olivia Newton-John arrived in the US with a Bob Dylan song and then became a country crossover star.",
   f"{NUM[n_cn].capitalize()} of the Olivia Newton-John songs on this page reached Billboard's country chart.",
   "The table shows how high each one went.")}

{tbl("Olivia Newton-John songs that crossed to Billboard's country chart: Hot 100 and country peaks (Wikipedia)", ["Song", "Hot 100 Peak", "Country Peak", "Released"], crossover_rows)}

        <h3>If Not for You</h3>
{p("Bob Dylan wrote If Not for You, and he released it on his 1970 album New Morning.",
   "Olivia Newton-John's manager suggested it after hearing George Harrison's version.",
   "She had reservations, since it did not feel like her type of song.",
   "Producers Bruce Welch and John Farrar arranged it closer to Harrison's version than to Dylan's, with prominent slide guitar.")}
{p("It came out in March 1971 as her first international single.",
   "It became the title track of her debut album.",
   "It reached number 25 on the Hot 100 and number seven in the UK.",
   "It spent three weeks at number one on the Easy Listening chart.",
   f"It ranks #{ye['If Not for You']['rank']} on the 1971 Year-End Hot 100.")}

        <h3>Let Me Be There</h3>
{p("John Rostill wrote Let Me Be There, and Welch and Farrar produced it.",
   "It was the second single from the album of the same name, released in September 1973.",
   "Mike Sammes sings a bass vocal harmony, and the sound is country-influenced.",
   "It reached number six on the Hot 100 and number seven on the country chart.",
   "It was her first US top ten.",
   "It won her a Grammy in the female country vocal category, according to Wikipedia.")}

        <h3>If You Love Me (Let Me Know)</h3>
{p("Rostill wrote this one too, and Farrar produced it for MCA in April 1974.",
   "Mike Sammes sings the bass harmony again, as he did on Let Me Be There.",
   "It reached number five on the Hot 100 and number two on the country chart.",
   "It also reached number two on the adult contemporary chart.",
   "In Canada it was number one on both the country and adult contemporary charts.",
   "It earned a nomination for the 1974 Country Music Association Single of the Year.")}
{p("In 1978 she sang it with Andy Gibb and ABBA on her ABC-TV special Olivia!.",
   'For a wider look at the style, read the page on <a href="/blog/genres/70s-country-songs/">70s country songs</a>.')}

        <h2 id="number-ones">The Number Ones: I Honestly Love You and Have You Never Been Mellow</h2>
{p("Two number ones came within six months of each other, and they have different writers.",
   "Farrar produced both, and both topped the adult contemporary chart too.")}

        <h3>I Honestly Love You</h3>
{p("Jeff Barry and Peter Allen wrote I Honestly Love You, and Farrar produced it.",
   "It came out in the US in August 1974.",
   "It reached number one on the chart dated October 5.",
   "It stayed there for two weeks and for three weeks at the top of the adult contemporary chart.",
   "The RIAA certified it gold for one million copies.")}
{p("At the 17th Grammy Awards in 1975 it won both Record of the Year and Best Pop Vocal Performance, Female.",
   "It was also nominated for Song of the Year, which went to The Way We Were.")}
{p(f"It ranks #{ye['I Honestly Love You']['rank']} on the 1974 Year-End Hot 100, because it only peaked in the autumn.")}

        <h3>An Australian Title, a Co-Writer's Own Version and a Cameo in Jaws</h3>
        <ul>
          <li>It was first released in Australia as I Love You, I Honestly Love You, named after the chorus.</li>
          <li>Peter Allen recorded it around the same time for his album Continental American.</li>
          <li>Alan Hawkshaw, who also played on the recording, won an arrangement award from the American Academy of Arts and Sciences for it.</li>
          <li>A snippet of Lynn Anderson's cover plays over Chief Brody's radio in the 1975 film Jaws.</li>
        </ul>

        <h3>Have You Never Been Mellow</h3>
{p("Farrar wrote and produced Have You Never Been Mellow, and the sessions were in 1974 at Abbey Road Studios in London.",
   "It was released in January 1975 as the lead single from the album of the same name.",
   "It reached number one on the Hot 100 in March 1975, and Wikipedia calls it her second consecutive number one.",
   "This site's weekly data shows one week at the top.")}
        <h3>Gold Records and a Grammy Nomination</h3>
{p("It also reached number one on the adult contemporary chart, and number three on the country chart.",
   "The RIAA gave it a gold certification, her fourth gold single in a row.",
   "It was nominated for Best Pop Vocal Performance, Female at the 18th Grammy Awards, and it lost to Janis Ian's At Seventeen.",
   'To meet more voices like hers, spin the <a href="/pages/random-artist-picker">Random Artist Picker</a>.')}
{award_pic}
        <p class="post-img-caption">Olivia Newton-John with two trophies at a press conference at Schiphol airport, November 24, 1978.</p>
        <p class="post-img-caption">Image credit: Photo by Bert Verhoeff for Anefo, CC0, via Wikimedia Commons (Nationaal Archief).</p>

        <h2 id="jukebox-and-radio">Please Mr. Please, Something Better to Do and Sam</h2>
{p("Three more Olivia Newton-John songs filled the middle of the decade, and each one shows a different side.",
   "All three reached number one on the adult contemporary chart, and only Please Mr. Please ranks on a year-end list.")}

        <h3>Please Mr. Please</h3>
{p("Bruce Welch and John Rostill wrote Please Mr. Please, and both were members of The Shadows, the backing band of Cliff Richard.",
   "Welch recorded it himself in 1974 with no commercial success.",
   "Olivia Newton-John's version came out in June 1975, as the second single from Have You Never Been Mellow.",
   "It reached number three on the Hot 100 on August 9, 1975, and number five on the country chart.",
   "It spent three weeks at number one on the adult contemporary chart, from July 12.")}
{p("The song opens as a tribute to the jukebox, then turns to how some jukebox songs can trigger painful memories.",
   f"It ranks #{ye['Please Mr. Please']['rank']} on the 1975 Year-End Hot 100.")}

        <h3>Something Better to Do</h3>
{p("Farrar wrote Something Better to Do, and it was the lead single from the album Clearly Love in September 1975.",
   "The narrator is struggling to adjust to life without a departed lover, and the birds that sing to her are not welcome.",
   "Record World wrote that its strong multi-tracked chorus contains the old Olivia charm.",
   "It reached number 13 on the Hot 100, and number one on the adult contemporary chart for three weeks.",
   "On the country chart it reached number 19.")}

        <h3>Sam</h3>
{p("Sam was the third and final single from the album Don't Stop Believin', released in January 1977.",
   "Don Black, Hank Marvin and John Farrar wrote it.",
   "It reached number 20 on the Hot 100, and number one on the adult contemporary chart.",
   'Test what you know about the decade with the <a href="/pages/70s-trivia-quiz">70s Music Trivia Quiz</a>.')}

        <h2 id="grease">Grease: Hopelessly Devoted to You, Summer Nights and You're the One That I Want</h2>
{p("Three Olivia Newton-John songs on this page come from the 1978 film Grease, and all three reached the Hot 100's top five.",
   "Two of them are duets with John Travolta.")}

        <h3>You're the One That I Want</h3>
{p("John Farrar wrote You're the One That I Want for Olivia Newton-John's appearance in the film, since it was not in the original stage musical.",
   "It reached number one on the Hot 100, and this site's weekly data shows one week at the top.",
   f"It ranks #{ytoiw} on the 1978 Year-End Hot 100.",
   "In the UK it spent nine weeks at number one in the summer of 1978.",
   "Director Randal Kleiser disliked the song, according to Wikipedia.")}
{p("Wikipedia says it sold more than 4 million copies in the US and UK alone, and estimates over 15 million worldwide.")}

        <h3>Summer Nights</h3>
{p("Jim Jacobs and Warren Casey wrote Summer Nights for the stage show's move to Broadway.",
   "The original Chicago version of the musical had a different song at that point, Foster Beach.",
   "John Travolta and Olivia Newton-John sing the lead vocals in the film, with other cast members on backing and cameo lines.",
   "The song alternates between Danny telling the T-Birds about the romance and Sandy telling the Pink Ladies.")}
{p("The US single came out in July 1978, and it reached number five on the Hot 100.",
   f"It ranks #{ye['Summer Nights']['rank']} on the 1978 Year-End Hot 100.",
   "In the UK it was number one for seven weeks, and together with You're the One That I Want it spent 16 weeks at number one there in 1978.")}

        <h3>Hopelessly Devoted to You</h3>
{p("Farrar wrote Hopelessly Devoted to You after Olivia Newton-John's contract solo had still not been written halfway through shooting.",
   "The production team was reluctant, but approved it, and it was recorded after the rest of the film was complete.",
   "In a 2004 interview, Farrar said he spent the longest period writing the lyrics of any song he had written.",
   "He used thesauruses and rhyming dictionaries.")}
{p("It was released in June 1978 on RSO Records, and it reached number three on the Hot 100.",
   "It was also number seven on the adult contemporary chart and number 20 on the country chart.",
   "In the UK and Australia it reached number two.",
   "It was nominated for Best Original Song at the 51st Academy Awards, and it lost to Last Dance from Thank God It's Friday.",
   f"It ranks #{ye['Hopelessly Devoted to You']['rank']} on the 1978 Year-End Hot 100.")}

        <h2 id="totally-hot">Totally Hot: A Little More Love</h2>
{p("A Little More Love was the first release after Grease, and it closed the decade for Olivia Newton-John.",
   "John Farrar wrote and produced it, and it was the lead single from the album Totally Hot, in November 1978.",
   "It was recorded in Hollywood at Cherokee Studios, Hollywood Sound and Hollywood Group IV.")}
{p("It reached number three on the Hot 100 in February 1979, number four on the adult contemporary chart and number four in the UK.",
   f"It ranks #{ye['A Little More Love']['rank']} on the 1979 Year-End Hot 100, the only one of her songs here on that year's list.",
   "The Guardian ranked it her third best song and called it pure pop perfection.",
   "The song is pop rock, a step away from the country sound of her early hits.")}

        <h2 id="who-wrote-what">Who Wrote Each of the Olivia Newton-John Songs</h2>
{p(f"John Farrar wrote or co-wrote six of the {NUM[n]} Olivia Newton-John songs on this page, and he produced most of them.",
   "John Rostill wrote two, and co-wrote a third with Bruce Welch.",
   "The table shows who wrote each song, when it was released and which album it came from.")}

{tbl("Olivia Newton-John songs of the 70s: writers, release date and album (Wikipedia)", ["Song", "Written by", "Released", "Album"], writer_rows)}

        <h3>Keep Exploring</h3>
{p("Olivia Newton-John songs were the sound of a decade that let country, pop and movie music share one chart.",
   "Three of them reached number one, and nine reached the top ten.",
   'The page on <a href="/blog/artists/carpenters-songs/">Carpenters songs</a> covers another soft pop act of the decade.')}

        <h2 id="sources">Sources</h2>
{p("Year-end ranks and weeks at number one come from this site's own Billboard data, described on the <a href='/about/methodology/'>methodology page</a>.",
   'Every list on <a href="/">Music of the 70s</a> plays inside the page.',
   "Peaks, dates and stories behind the Olivia Newton-John songs above can be checked against these outside sources:")}
        <ul>
          <li><a href="https://en.wikipedia.org/wiki/Olivia_Newton-John_discography" rel="noopener">Wikipedia: Olivia Newton-John discography</a> for the singles, albums and chart peaks.</li>
          <li><a href="https://en.wikipedia.org/wiki/If_Not_for_You" rel="noopener">Wikipedia: If Not for You</a> and <a href="https://en.wikipedia.org/wiki/Let_Me_Be_There" rel="noopener">Let Me Be There</a> for the early singles.</li>
          <li><a href="https://en.wikipedia.org/wiki/If_You_Love_Me_(Let_Me_Know)" rel="noopener">Wikipedia: If You Love Me (Let Me Know)</a> and <a href="https://en.wikipedia.org/wiki/I_Honestly_Love_You" rel="noopener">I Honestly Love You</a> for 1974.</li>
          <li><a href="https://en.wikipedia.org/wiki/Have_You_Never_Been_Mellow_(song)" rel="noopener">Wikipedia: Have You Never Been Mellow</a> and <a href="https://en.wikipedia.org/wiki/Please_Mr._Please" rel="noopener">Please Mr. Please</a> for 1975.</li>
          <li><a href="https://en.wikipedia.org/wiki/Something_Better_to_Do" rel="noopener">Wikipedia: Something Better to Do</a> and <a href="https://en.wikipedia.org/wiki/Sam_(Olivia_Newton-John_song)" rel="noopener">Sam</a> for the songs outside the year-end lists.</li>
          <li><a href="https://en.wikipedia.org/wiki/Hopelessly_Devoted_to_You" rel="noopener">Wikipedia: Hopelessly Devoted to You</a>, <a href="https://en.wikipedia.org/wiki/You%27re_the_One_That_I_Want" rel="noopener">You're the One That I Want</a> and <a href="https://en.wikipedia.org/wiki/Summer_Nights_(Grease_song)" rel="noopener">Summer Nights</a> for Grease.</li>
          <li><a href="https://en.wikipedia.org/wiki/A_Little_More_Love_(Olivia_Newton-John_song)" rel="noopener">Wikipedia: A Little More Love</a> for the Totally Hot single.</li>
        </ul>

        <section class="faq-block" id="faq">
          <h2>Frequently Asked Questions</h2>
{faq_html}
        </section>'''

    related = [
        ("70s-female-singers", "Artists", "70s Female Singers: The Women Who Ruled the Hot 100", "/blog/artists/70s-female-singers/",
         "Olivia Newton-John leads the year-end count, with every woman ranked and playable.",
         "Bar chart of the top ten 70s female singers by year-end Hot 100 hits"),
        ("dolly-parton-1970s", "Genres", "70s Country Songs: Play 60 Hits, See Who Ruled #1", "/blog/genres/70s-country-songs/",
         "Sixty country hits to play, and the acts that really ruled the country chart.",
         "Dolly Parton in a publicity photo from 1977"),
        ("carpenters-1972", "Artists", "Carpenters Songs: 11 Hits Played, 3 at Number One", "/blog/artists/carpenters-songs/",
         "Another soft pop act of the decade, with every Carpenters hit playable.",
         "The Carpenters in 1972"),
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
      {{"@type": "ListItem", "position": 4, "name": "Olivia Newton-John Songs", "item": "{URL}"}}
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
        Olivia Newton-John Songs
      </nav>

      <article class="section seo-content">
        <h1>{TITLE}</h1>

        <p class="post-byline">By <a href="https://musicofthe70s.net/about/author/">Charlie</a> &middot; Published {PUBLISHED.strftime('%B')} {PUBLISHED.day}, {PUBLISHED.year}</p>
        <p class="jump-to-list"><a class="btn-primary jump-btn" href="#olivia-newton-john-songs-list">&#9654; Jump to the playable list</a></p>

        <p class="post-intro">Olivia Newton-John songs filled the Hot 100, the country chart and the adult contemporary dial in the 1970s.</p>
        <p class="post-intro">This page plays {NUM[n]} of them, and three reached number one.</p>
        <p class="post-intro">I Honestly Love You got there in 1974, and Have You Never Been Mellow followed in 1975.</p>
        <p class="post-intro">You're the One That I Want topped the chart in 1978.</p>
        <p class="post-intro">Nine of the {NUM[n]} reached the top ten, and {NUM[n_cn]} also charted on Billboard's country list.</p>
        <p class="post-intro">Press Play on every hit below, then read the story behind each one.</p>

{feat_pic}
        <p class="post-img-caption">Olivia Newton-John arriving at Schiphol airport, November 24, 1978, with a bouquet of roses.</p>
        <p class="post-img-caption">Image credit: Photo by Bert Verhoeff for Anefo, CC0, via Wikimedia Commons (Nationaal Archief).</p>

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
