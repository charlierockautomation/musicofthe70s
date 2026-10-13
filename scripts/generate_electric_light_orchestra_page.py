#!/usr/bin/env python3
"""Build the Electric Light Orchestra Songs Artists post (blog/artists/electric-light-orchestra-songs/index.html).

Data: data/radio/radio-songs.json (eight Electric Light Orchestra rows of the 1975-1979 Year-End Hot 100, each with a
YouTube ID), data/billboard/hot100_weekly.json (confirms ELO has no weekly Hot 100 number one in 1970-1979),
data/billboard/beyond_year_end.json (three further singles on the weekly Hot 100 but on no 1970s year-end list: Strange
Magic, Do Ya and Mr. Blue Sky, peaks and YouTube IDs checked). Year-End Rank is the year-end rank, never a peak. Hot 100
and UK peaks, release dates, certifications, writers and story facts come from the linked Wikipedia articles, checked
2026-10-13, and are credited to Wikipedia on the page. The site JSON's fun_fact text for ELO is not used.

Run: python3 scripts/generate_electric_light_orchestra_page.py
"""
import html
import json
from datetime import date

from genre_page_common import ROOT, read, play_button, write
from generate_country_page import p, tbl, pic

SLUG = "electric-light-orchestra-songs"
PAGE = f"blog/artists/{SLUG}/"
URL = f"https://musicofthe70s.net/{PAGE}"
IMG = "electric-light-orchestra-1978"
IMG2 = "electric-light-orchestra-1977"
PUBLISHED = date(2026, 10, 13)
NUM = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
       10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen"}

# title -> (release year, Hot 100 peak, UK peak or None, released text, album, RIAA certification or None)
# Every value read from the song's Wikipedia article, checked 2026-10-13. All eleven were written by Jeff Lynne.
INFO = {
    "Can't Get It Out of My Head": (1974, 9, None, "November 1974 (US)", "Eldorado", None),
    "Evil Woman": (1975, 10, 10, "October 31, 1975 (US)", "Face the Music", "Platinum"),
    "Strange Magic": (1976, 14, 38, "February 1976 (US)", "Face the Music", "Gold"),
    "Livin' Thing": (1976, 13, 4, "October 29, 1976", "A New World Record", "Gold"),
    "Do Ya": (1977, 24, None, "January 1977 (US)", "A New World Record", None),
    "Telephone Line": (1977, 7, 8, "May 1977", "A New World Record", "Platinum"),
    "Turn to Stone": (1977, 13, 18, "October 14, 1977", "Out of the Blue", "Gold"),
    "Sweet Talkin' Woman": (1978, 17, 6, "February 1978 (US)", "Out of the Blue", "Gold"),
    "Mr. Blue Sky": (1978, 35, 6, "January 20, 1978 (UK)", "Out of the Blue", None),
    "Shine a Little Love": (1979, 8, 6, "May 11, 1979", "Discovery", None),
    "Don't Bring Me Down": (1979, 4, 3, "July 1979 (US)", "Discovery", "2x Platinum"),
}
ORDER = list(INFO)
BEYOND = {"Strange Magic", "Do Ya", "Mr. Blue Sky"}


def main():
    radio = json.loads(read(ROOT / "data/radio/radio-songs.json"))
    weekly = json.loads(read(ROOT / "data/billboard/hot100_weekly.json"))
    beyond = {s["title"]: s for s in json.loads(read(ROOT / "data/billboard/beyond_year_end.json"))["songs"]
              if s["page"] == PAGE}

    ye = {s["title"]: s for s in radio if s["artist"] == "Electric Light Orchestra" and s.get("youtube_id")}
    assert len(ye) == 8, len(ye)
    assert set(beyond) == BEYOND, set(beyond)
    assert set(ye) | BEYOND == set(INFO), (set(ye) | BEYOND) ^ set(INFO)
    for t in BEYOND:
        assert beyond[t]["weekly_peak"] == INFO[t][1], t
        assert beyond[t]["released"] == INFO[t][0], t
    for t, s in ye.items():
        assert s["year"] in (INFO[t][0], INFO[t][0] + 1), (t, s["year"])

    # ELO has no weekly Hot 100 number one in the site's own 1970-1979 data.
    assert not [w for yr in weekly for w in weekly[yr] if "Electric Light" in w["artist"]]

    rk = {t: ye[t]["rank"] for t in ye}
    r_cgi, r_lt = rk["Can't Get It Out of My Head"], rk["Livin' Thing"]
    r_stw, r_dbmd = rk["Sweet Talkin' Woman"], rk["Don't Bring Me Down"]
    top_ten = [t for t in INFO if INFO[t][1] <= 10]
    assert len(top_ten) == 5
    n = len(INFO)
    yt = {t: (ye[t]["youtube_id"] if t in ye else beyond[t]["youtube_id"]) for t in INFO}
    n_uk = sum(1 for t in INFO if INFO[t][2] is not None)
    assert n_uk == 9
    n_cert = sum(1 for t in INFO if INFO[t][5])
    assert n_cert == 7

    rows = []
    for t in ORDER:
        y, pk, uk, rel, alb, cert = INFO[t]
        ye_year = ye[t]["year"] if t in ye else ""
        ye_rank = ye[t]["rank"] if t in ye else ""
        rows.append(f'              <tr><td class="ohw-listen">{play_button(yt[t], t, "Electric Light Orchestra")}</td>'
                    f'<td class="ohw-song">{html.escape(t)}</td>'
                    f'<td>{y}</td><td>{ye_year}</td><td>{ye_rank}</td><td>{pk}</td></tr>')

    # keep the UK column honest: only songs with a Wikipedia UK peak appear in the UK table
    uk_rows = sorted(([html.escape(t), INFO[t][1], INFO[t][2], INFO[t][3]] for t in ORDER if INFO[t][2] is not None),
                     key=lambda r: r[2])
    cert_rows = [[html.escape(t), INFO[t][5], INFO[t][1], INFO[t][3]] for t in ORDER if INFO[t][5]]
    album_rows = [[html.escape(t), INFO[t][3], html.escape(INFO[t][4])] for t in ORDER]
    us_rows = sorted(([html.escape(t), INFO[t][1], INFO[t][3]] for t in ORDER), key=lambda r: (r[1], r[0]))

    faq = [
        ("What is Electric Light Orchestra's biggest song of the 1970s?",
         ["Don't Bring Me Down is Electric Light Orchestra's biggest song of the 1970s on the Billboard Hot 100, where it reached number four in 1979.",
          "Wikipedia calls it the band's biggest US hit and says the RIAA certified it 2x Platinum.",
          "Telephone Line ranks higher on a year-end list, at #15 on the 1977 Year-End Hot 100."]),
        ("Did Electric Light Orchestra ever have a number one song on the Billboard Hot 100?",
         ["Electric Light Orchestra never had a number one song on the Billboard Hot 100, and this site's weekly chart data for 1970 to 1979 shows none either.",
          "Don't Bring Me Down, at number four in 1979, was the closest.",
          "Wikipedia says the band holds the record for the most Hot 100 top 40 hits, 20, without reaching number one."]),
        ("Who wrote Electric Light Orchestra's songs?",
         ["Jeff Lynne wrote all eleven Electric Light Orchestra songs on this page, including Evil Woman, Telephone Line and Mr. Blue Sky.",
          "He produced most of them too.",
          "Do Ya is the one that began elsewhere, because Lynne first wrote it for his earlier band The Move, whose 1972 version reached number 93 in the US, according to Wikipedia."]),
        ("How did Electric Light Orchestra make the phone ring in Telephone Line?",
         ["Electric Light Orchestra recorded a real US phone ringing for Telephone Line, according to Wikipedia.",
          "Jeff Lynne wanted the American ringtone sound, so the band called a US number they knew would go unanswered and taped it.",
          "They then tuned oscillators on a Moog synthesizer to the same notes to recreate the sound.",
          "The song reached number seven on the Hot 100 in 1977."]),
        ("Does Don't Bring Me Down use a string section?",
         ["Don't Bring Me Down has no string section, and Wikipedia calls it Electric Light Orchestra's first single without one.",
          "Engineer Reinhold Mack says the idea was his.",
          "The drum track is a tape loop of the band's song On the Run, slowed down and then sped up.",
          "It reached number four on the Hot 100 in 1979."]),
    ]
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": " ".join(a)}} for q, a in faq]},
        indent=2, ensure_ascii=False)
    faq_ld = "\n".join("  " + l for l in faq_ld.split("\n"))
    faq_html = "\n".join(
        f'          <div class="faq-item">\n            <h3>{html.escape(q)}</h3>\n' + "\n".join(f"            <p>{html.escape(l)}</p>" for l in a) + "\n          </div>"
        for q, a in faq).replace("&#x27;", "'")

    TITLE = f"Electric Light Orchestra Songs: {n} Hits Played, 5 Top Tens"
    desc = (f"Electric Light Orchestra songs of the 70s, all {n} playable: Evil Woman, Telephone Line, Mr. Blue Sky and more. "
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

    toc = [("electric-light-orchestra-songs-list", f"Electric Light Orchestra Songs: Play All {n} Hits"),
           ("by-the-numbers", "Electric Light Orchestra Songs on the Charts: Five Top Tens, No Number Ones"),
           ("origins", "Roy Wood, Jeff Lynne and the Strings: How ELO Began"),
           ("face-the-music", "Eldorado and Face the Music: Can't Get It Out of My Head, Evil Woman and Strange Magic"),
           ("new-world-record", "A New World Record: Livin' Thing, Do Ya and Telephone Line"),
           ("out-of-the-blue", "Out of the Blue: Turn to Stone, Sweet Talkin' Woman and Mr. Blue Sky"),
           ("discovery", "Discovery: Shine a Little Love and Don't Bring Me Down"),
           ("who-wrote-what", "Who Wrote and Released Each of the Electric Light Orchestra Songs"),
           ("sources", "Sources"), ("faq", "Frequently Asked Questions")]
    toc_html = "\n".join(f'            <li><a href="#{i}">{t}</a></li>' for i, t in toc)

    feat_pic = pic(IMG, "Electric Light Orchestra on stage in Oslo in April 1978, with Jeff Lynne on guitar and cellists beside him, the Electric Light Orchestra songs live",
                   "(max-width: 700px) 100vw, 669px", 669, 414, widths=(400, 669), lazy=False).replace(
        'class="post-featured-img"', 'class="post-featured-img" style="aspect-ratio:669/414;max-width:669px;height:auto;margin:1.5rem auto"', 1)
    band_pic = pic(IMG2, "Black and white portraits of the seven members of Electric Light Orchestra in a 1977 Billboard trade advertisement from Jet Records",
                   "(max-width: 700px) 100vw, 669px", 669, 460, widths=(400, 669)).replace(
        "<img\n", '<img style="display:block;width:100%;max-width:669px;height:auto;margin:1.5rem auto;border-radius:8px"\n', 1)

    body = f'''        <h2 id="electric-light-orchestra-songs-list">Electric Light Orchestra Songs: Play All {n} Hits</h2>
{p(f"Here are {NUM[n]} Electric Light Orchestra songs from 1974 to 1979, from Can't Get It Out of My Head to Don't Bring Me Down.",
   "Eight sit on a Billboard Year-End Hot 100, and three more charted weekly without making a year-end list.",
   "Press Play on any row to watch it here, and tap a heading to sort.")}

        <div class="data-table-wrap scroll-list">
          <table class="data-table sortable-table" id="electricLightOrchestraSongsTable" data-inline-player>
            <caption>{n} Electric Light Orchestra songs of the 70s, with release year, Billboard Year-End Hot 100 rank and Hot 100 peak</caption>
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
   "None of these songs reached number one in this site's weekly chart data.")}

        <h2 id="by-the-numbers">Electric Light Orchestra Songs on the Charts: Five Top Tens, No Number Ones</h2>
{p("Electric Light Orchestra never had a number one on the Hot 100, but it kept returning to the top forty.",
   "Wikipedia says the band had 15 top 20 songs on the Billboard Hot 100 from 1972 to 1986.",
   "It also says the band holds the record for the most Hot 100 top 40 hits, 20, without reaching number one.",
   "The table lists the songs on this page by their Hot 100 peak.")}

{tbl("Electric Light Orchestra songs of the 70s ranked by Hot 100 peak, with release date (Wikipedia)", ["Song", "Hot 100 Peak", "Released"], us_rows)}

        <h3>What the Chart Numbers Say</h3>
{p(f"Five of the {NUM[n]} Electric Light Orchestra songs on this page reached the Hot 100's top ten.")}
        <ul>
          <li>Don't Bring Me Down reached number four, the band's biggest US hit, according to Wikipedia.</li>
          <li>Telephone Line reached number seven, and it ranks #{ye['Telephone Line']['rank']} on the 1977 Year-End Hot 100.</li>
          <li>Shine a Little Love reached number eight, and Can't Get It Out of My Head reached number nine, the band's first US top ten.</li>
          <li>Evil Woman reached number ten, and it was certified Platinum by the RIAA.</li>
          <li>Mr. Blue Sky, now the band's signature song, only reached number 35 on the Hot 100.</li>
        </ul>
{p('To see which groups charted the most, read the page on <a href="/blog/artists/70s-bands/">70s bands</a>, ranked by year-end hits.')}

        <h3>The UK Chart Told a Different Story</h3>
{p(f"{NUM[n_uk].capitalize()} of these songs charted in the UK, and several did better there than in the US.",
   "Livin' Thing reached number four in the UK but number 13 in the US.",
   "Mr. Blue Sky reached number six in the UK but number 35 in the US.")}

{tbl("Electric Light Orchestra songs of the 70s: UK Singles Chart peak next to the Hot 100 peak (Wikipedia)", ["Song", "Hot 100 Peak", "UK Peak", "Released"], uk_rows)}

{p("Can't Get It Out of My Head did not chart in the UK as a single, according to Wikipedia.",
   "It reached number 34 there after it appeared on the 1978 release The ELO EP.")}

        <h2 id="origins">Roy Wood, Jeff Lynne and the Strings: How ELO Began</h2>
{p("Electric Light Orchestra began as a bold idea about rock and orchestras.",
   "Wikipedia says Roy Wood conceived it in 1968, to add strings and woodwinds to rock and pick up where The Beatles left off.",
   "Jeff Lynne joined in January 1970, and Bev Bevan played drums.",
   'To meet more voices from the decade, spin the <a href="/pages/random-artist-picker">Random Artist Picker</a>.')}

        <h3>The Debut and Roy Wood's Exit</h3>
{p("The first song, 10538 Overture, came out on July 12, 1970, and became a UK top ten hit.",
   "The debut album, The Electric Light Orchestra, followed in December 1971, and in the US it came out in March 1972 as No Answer.",
   "Wood left during the sessions for the second album, ELO 2, and took two bandmates with him to form Wizzard.",
   "Lynne took over the leadership, and the band carried on.")}

        <h3>Roll Over Beethoven and the Strings on Stage</h3>
{p("ELO 2 produced the band's first US chart single, a version of Chuck Berry's Roll Over Beethoven.",
   "It opens with a quote from Beethoven's Fifth Symphony, and it reached number six in the UK in 1973.",
   "Barcus Berry pickups, first used at the 1972 Reading Festival, let the string players be properly amplified on stage.")}

        <h3>Eldorado Changed the Sound</h3>
{p("With Eldorado in 1974, Lynne stopped multi-tracking the strings.",
   "He hired Louis Clark as string arranger, with an orchestra and a choir.",
   "That album gave the band its first US top ten, Can't Get It Out of My Head.",
   'Fans of long-form sound can also read about <a href="/blog/genres/70s-progressive-rock/">70s progressive rock</a>, where the album was king.')}
{band_pic}
        <p class="post-img-caption">Electric Light Orchestra in a Jet Records trade advertisement, Billboard, November 19, 1977.</p>
        <p class="post-img-caption">Image credit: Jet Records, public domain, via Wikimedia Commons.</p>

        <h2 id="face-the-music">Eldorado and Face the Music: Can't Get It Out of My Head, Evil Woman and Strange Magic</h2>
{p("Three Electric Light Orchestra songs made the band a real presence on US radio between 1974 and 1976.",
   "Each one was written by Jeff Lynne.")}

        <h3>Can't Get It Out of My Head</h3>
{p("Lynne wrote Can't Get It Out of My Head partly after his father said his earlier songs had no tune.",
   "He wanted to show he could write a song with a beautiful melody.",
   "He has said the lyrics are about a man who dreams of a vision of loveliness, then wakes up to find he is a clerk working in a bank.",
   "It was recorded in 1974 at De Lane Lea Studios in London.")}
{p("It was released in the US in November 1974 from the album Eldorado, and it reached number nine on the Hot 100.",
   f"It ranks #{r_cgi} on the 1975 Year-End Hot 100.",
   "It was the band's first US top ten.")}

        <h3>Evil Woman</h3>
{p("Lynne wrote Evil Woman in a matter of minutes, because the album Face the Music felt like it lacked a strong lead single.",
   "He has said he wrote it while the band was out playing football, and that the first three chords came to him right away.",
   "It was recorded in 1975 at Musicland Studios in Munich.")}
{p("It was released in the US on October 31, 1975, and it reached number ten on the Hot 100 and number ten in the UK.",
   f"It ranks #{ye['Evil Woman']['rank']} on the 1976 Year-End Hot 100.",
   "The RIAA certified it Platinum.",
   "Wikipedia notes that one lyric is a tribute to The Beatles' Fixing a Hole.")}

        <h3>Strange Magic</h3>
{p("Strange Magic was the second Face the Music single to reach the Hot 100, released in the US in February 1976.",
   "Keyboardist Richard Tandy played the weeping guitar lick, and Lynne played a 12-string acoustic guitar through a phase shifter.",
   "Wikipedia describes the song as psychedelic.",
   "It reached number 14 on the Hot 100 and number 38 in the UK, and the RIAA certified it Gold.")}

        <h2 id="new-world-record">A New World Record: Livin' Thing, Do Ya and Telephone Line</h2>
{p("A New World Record in 1976 gave the band three more Hot 100 hits within eight months.",
   "Livin' Thing and Do Ya were recorded at Musicland Studios in Munich, according to Wikipedia.")}

        <h3>Livin' Thing</h3>
{p("Lynne wrote and produced Livin' Thing, and it came out on October 29, 1976.",
   "It reached number 13 on the Hot 100 and number four in the UK.",
   f"It ranks #{r_lt} on the 1977 Year-End Hot 100.",
   "The RIAA certified it Gold, and the BPI certified it Platinum in the UK.")}
        <h3>A Guilty Pleasure, a Cameo and an Uncredited Voice</h3>
        <ul>
          <li>Wikipedia says Patti Quatro sang uncredited vocals, especially the higher and higher parts, according to Suzi Quatro's 2008 memoir.</li>
          <li>Q magazine named it the number one guilty pleasure single of all time in 2006.</li>
          <li>It plays over the final scene and end credits of the 1997 film Boogie Nights.</li>
          <li>The song uses augmented chords, and Lynne said a G augmented chord adds tension and uplift.</li>
        </ul>

        <h3>Do Ya</h3>
{p("Lynne first wrote Do Ya for his earlier band The Move, when he was about 22.",
   "The Move's version came out in June 1972 in the US and reached number 93.",
   "Electric Light Orchestra's version came out in January 1977 on A New World Record.",
   "It reached number 24 on the Hot 100.",
   "In 2000, Lynne found an unedited 1976 alternative mix that he preferred, and it appears on the Flashback box set.")}

        <h3>Telephone Line</h3>
{p("Telephone Line was released in May 1977, and it reached number seven on the Hot 100 and number eight in the UK.",
   f"It ranks #{ye['Telephone Line']['rank']} on the 1977 Year-End Hot 100, the best rank of any Electric Light Orchestra song.",
   "It was the band's first single to earn Gold sales in the US, and the RIAA later certified it Platinum.")}
{p("Lynne wanted the American ringtone sound.",
   "The band called a US number they knew would go unanswered and recorded the ringing.",
   "Then they tuned Moog oscillators to the same notes to recreate it.",
   "Wikipedia adds that the US single was a shortened 3:56 edit, and the only green single the band ever issued.")}

        <h2 id="out-of-the-blue">Out of the Blue: Turn to Stone, Sweet Talkin' Woman and Mr. Blue Sky</h2>
{p("Out of the Blue in 1977 was a double album, and it was the band's most commercially successful release, according to Wikipedia.",
   "Lynne wrote it in a two-week burst in a Swiss chalet.",
   "Three songs from it reached the US Hot 100's top forty, and a fourth, Wild West Hero, did not chart.")}

        <h3>Turn to Stone</h3>
{p("Turn to Stone opens the album, and it was the first single, released on October 14, 1977.",
   "Lynne wrote it in Switzerland, and he played the Moog bassline himself.",
   "The orchestral arrangement at the end was inspired by the strings in The Beatles' A Day in the Life.",
   "It reached number 13 on the Hot 100 and number 18 in the UK.",
   f"It ranks #{ye['Turn to Stone']['rank']} on the 1978 Year-End Hot 100, and the RIAA certified it Gold.")}

        <h3>Sweet Talkin' Woman</h3>
{p("Sweet Talkin' Woman was first titled Dead End Street, and it was renamed during recording.",
   "A few words from the original version remain in the opening of the third verse.",
   "It was released in the US in February 1978, and it reached number 17 on the Hot 100 and number six in the UK.",
   f"It ranks #{r_stw} on the 1978 Year-End Hot 100.",
   "AllMusic's Donald A. Guarisco called it the band's first real step into the disco sound.")}

        <h3>Mr. Blue Sky</h3>
{p("Mr. Blue Sky is the band's signature song, though it only reached number 35 on the Hot 100.",
   "Lynne has said he shut himself in a Swiss chalet to write the follow-up to A New World Record.",
   "After two weeks of misty weather with no ideas, the sun came out, and he wrote this song and 13 others in the next two weeks.",
   "It reached number six in the UK, and it closes the Concerto for a Rainy Day suite on side three of the album.")}
{p("The piano and drum intro is borrowed from The Kinks' song Do You Remember Walter, according to Wikipedia.",
   "Bassist Kelly Groucutt sued Lynne in 1983, claiming he wrote the middle section without credit.",
   'Quiz yourself on the era with the <a href="/pages/70s-trivia-quiz">70s Music Trivia Quiz</a>.')}

        <h3>The Big Night Tour</h3>
{p("The tour for Out of the Blue was called The Big Night.",
   "Wikipedia says it drew 62,000 people to Cleveland Stadium, and that it became the highest-grossing live tour in music history up to 1978.")}

        <h2 id="discovery">Discovery: Shine a Little Love and Don't Bring Me Down</h2>
{p("Discovery in 1979 reached number one on the UK Albums Chart, and it leaned heavily on disco.",
   "Two of its singles ended the decade as the band's biggest US hits.")}

        <h3>Shine a Little Love</h3>
{p("Shine a Little Love opens Discovery, and it was released on May 11, 1979.",
   "It was recorded at Musicland Studios in Munich.",
   "Lynne described it as having a bit of a disco beat.",
   "It reached number eight on the Hot 100 and number six in the UK.",
   f"It ranks #{ye['Shine a Little Love']['rank']} on the 1979 Year-End Hot 100.",
   "It reached number one on the Radio and Records chart in 1979, which Wikipedia calls the band's only number one on a US singles chart.")}

        <h3>Don't Bring Me Down</h3>
{p("Don't Bring Me Down closes Discovery, and it was released in July 1979.",
   "It was the band's first single without a string section, and engineer Reinhold Mack says the idea was his.",
   "The drum track is a tape loop of On the Run, slowed down and then sped up.",
   "The closing door slam came from a metal fire door at Musicland Studios.")}
{p("It reached number four on the Hot 100, number three in the UK and number one in Canada.",
   f"It ranks #{r_dbmd} on the 1979 Year-End Hot 100.",
   "The RIAA certified it 2x Platinum, the highest US certification of any song on this page.")}

        <h3>The Bruce Ad-Lib and Skylab</h3>
        <ul>
          <li>Many listeners hear Lynne's made-up ad-lib as Bruce, and Lynne says it was a placeholder that resembles the German greeting Gruss.</li>
          <li>Mack says it began as a joke about Australians named Bruce.</li>
          <li>The song is dedicated to NASA's Skylab, which burned up on re-entry on July 11, 1979.</li>
          <li>The Hives' 2012 song Go Right Ahead has a nearly identical main riff, and Lynne is credited as a co-writer.</li>
        </ul>

        <h3>After the Decade: Xanadu</h3>
{p("The band's next big project was the 1980 film Xanadu.",
   "Lynne wrote half the songs for the soundtrack, and John Farrar wrote the other half, performed by Olivia Newton-John.",
   "The title track, with Newton-John, is the band's only UK number one single, according to Wikipedia.",
   'Read more about her in the page on <a href="/blog/artists/olivia-newton-john-songs/">Olivia Newton-John songs</a>.')}

        <h2 id="who-wrote-what">Who Wrote and Released Each of the Electric Light Orchestra Songs</h2>
{p(f"Jeff Lynne wrote all {NUM[n]} Electric Light Orchestra songs on this page, and he produced most of them.",
   f"{NUM[n_cert].capitalize()} of them earned a US certification from the RIAA, and the first table shows which.",
   "The second shows when each was released and which album it came from.")}

{tbl("Electric Light Orchestra songs of the 70s certified in the US by the RIAA, with Hot 100 peak (Wikipedia)", ["Song", "RIAA Certification", "Hot 100 Peak", "Released"], cert_rows)}

{tbl("Electric Light Orchestra songs of the 70s: release date and album (Wikipedia)", ["Song", "Released", "Album"], album_rows)}

        <h3>Keep Exploring</h3>
{p("Electric Light Orchestra songs showed how far a rock band could stretch a pop single.",
   "None reached number one, but five reached the top ten.",
   'The page on <a href="/blog/artists/fleetwood-mac-songs/">Fleetwood Mac songs</a> covers another band at the top of the album era.')}

        <h2 id="sources">Sources</h2>
{p("Year-end ranks come from this site's own Billboard data, described on the <a href='/about/methodology/'>methodology page</a>.",
   'Every list on <a href="/">Music of the 70s</a> plays inside the page.',
   "Peaks, dates and stories behind the Electric Light Orchestra songs above can be checked against these outside sources:")}
        <ul>
          <li><a href="https://en.wikipedia.org/wiki/Electric_Light_Orchestra" rel="noopener">Wikipedia: Electric Light Orchestra</a> and <a href="https://en.wikipedia.org/wiki/Electric_Light_Orchestra_discography" rel="noopener">its discography</a> for the band history, singles and chart peaks.</li>
          <li><a href="https://en.wikipedia.org/wiki/Roll_Over_Beethoven_(Electric_Light_Orchestra_song)" rel="noopener">Wikipedia: Roll Over Beethoven</a> for the early single.</li>
          <li><a href="https://en.wikipedia.org/wiki/Can%27t_Get_It_Out_of_My_Head" rel="noopener">Wikipedia: Can't Get It Out of My Head</a>, <a href="https://en.wikipedia.org/wiki/Evil_Woman_(Electric_Light_Orchestra_song)" rel="noopener">Evil Woman</a> and <a href="https://en.wikipedia.org/wiki/Strange_Magic_(song)" rel="noopener">Strange Magic</a> for 1974 to 1976.</li>
          <li><a href="https://en.wikipedia.org/wiki/Livin%27_Thing" rel="noopener">Wikipedia: Livin' Thing</a>, <a href="https://en.wikipedia.org/wiki/Do_Ya_(The_Move_song)" rel="noopener">Do Ya</a> and <a href="https://en.wikipedia.org/wiki/Telephone_Line_(Electric_Light_Orchestra_song)" rel="noopener">Telephone Line</a> for A New World Record.</li>
          <li><a href="https://en.wikipedia.org/wiki/Turn_to_Stone_(Electric_Light_Orchestra_song)" rel="noopener">Wikipedia: Turn to Stone</a>, <a href="https://en.wikipedia.org/wiki/Sweet_Talkin%27_Woman" rel="noopener">Sweet Talkin' Woman</a> and <a href="https://en.wikipedia.org/wiki/Mr._Blue_Sky" rel="noopener">Mr. Blue Sky</a> for Out of the Blue.</li>
          <li><a href="https://en.wikipedia.org/wiki/Shine_a_Little_Love" rel="noopener">Wikipedia: Shine a Little Love</a> and <a href="https://en.wikipedia.org/wiki/Don%27t_Bring_Me_Down" rel="noopener">Don't Bring Me Down</a> for Discovery.</li>
        </ul>

        <section class="faq-block" id="faq">
          <h2>Frequently Asked Questions</h2>
{faq_html}
        </section>'''

    related = [
        ("fleetwood-mac-1977", "Artists", "Fleetwood Mac Songs: 9 Hits Played, 1 at Number One", "/blog/artists/fleetwood-mac-songs/",
         "Rumours, Dreams and every Fleetwood Mac hit playable.", "Fleetwood Mac members in a 1977 Rumours advertisement"),
        ("chicago-1973", "Artists", "Chicago Band Songs: 12 Hits Played, 1 at Number One", "/blog/artists/chicago-band-songs/",
         "Another album-era band, with every Chicago hit playable.", "Chicago on stage in 1973"),
        ("70s-bands", "Artists", "70s Bands: The Groups That Ruled the Hot 100", "/blog/artists/70s-bands/",
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
      {{"@type": "ListItem", "position": 4, "name": "Electric Light Orchestra Songs", "item": "{URL}"}}
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
        Electric Light Orchestra Songs
      </nav>

      <article class="section seo-content">
        <h1>{TITLE}</h1>

        <p class="post-byline">By <a href="https://musicofthe70s.net/about/author/">Charlie</a> &middot; Published {PUBLISHED.strftime('%B')} {PUBLISHED.day}, {PUBLISHED.year}</p>
        <p class="jump-to-list"><a class="btn-primary jump-btn" href="#electric-light-orchestra-songs-list">&#9654; Jump to the playable list</a></p>

        <p class="post-intro">Electric Light Orchestra songs put strings, synthesizers and big pop hooks on the Hot 100 all through the late 1970s.</p>
        <p class="post-intro">This page plays {NUM[n]} of them, and five reached the top ten.</p>
        <p class="post-intro">Don't Bring Me Down got to number four in 1979, and Telephone Line got to number seven in 1977.</p>
        <p class="post-intro">Jeff Lynne wrote every one, from Evil Woman to Mr. Blue Sky.</p>
        <p class="post-intro">Press Play on every hit below, then read the story behind each one.</p>

{feat_pic}
        <p class="post-img-caption">Electric Light Orchestra live at Ekeberghallen, Oslo, April 27, 1978.</p>
        <p class="post-img-caption">Image credit: Photo by Helge Øverås, CC BY-SA 4.0, via Wikimedia Commons.</p>

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
