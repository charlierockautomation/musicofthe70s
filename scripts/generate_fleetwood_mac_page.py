#!/usr/bin/env python3
"""Build the Fleetwood Mac Songs Artists post (blog/artists/fleetwood-mac-songs/index.html).

Data: data/radio/radio-songs.json (Fleetwood Mac rows of the Year-End Hot 100, each with a YouTube ID),
data/billboard/hot100_weekly.json (weekly Hot 100 #1s), data/billboard/beyond_year_end.json (four
Fleetwood Mac singles on the weekly Hot 100 but on no 1970s year-end list, peaks from Wikipedia).
Year-End Rank is the year-end rank, never a peak. Weekly Hot 100 peaks for non-#1 songs, writers,
dates and story facts come from the linked Wikipedia articles, checked 2026-10-12, and are credited
to Wikipedia on the page.

Run: python3 scripts/generate_fleetwood_mac_page.py
"""
import collections
import html
import json
from datetime import date

from genre_page_common import ROOT, norm, read, play_button, write
from generate_country_page import p, tbl, pic, fmt_date

SLUG = "fleetwood-mac-songs"
PAGE = f"blog/artists/{SLUG}/"
URL = f"https://musicofthe70s.net/{PAGE}"
KW = "Fleetwood Mac songs"
PUBLISHED = date(2026, 10, 12)
IMG = "fleetwood-mac-1977"
NUM = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
       10: "ten", 11: "eleven", 12: "twelve"}

# Weekly Hot 100 peak, writer and release month, read from each song's Wikipedia article (checked 2026-10-12).
PEAK = {"Over My Head": 20, "Rhiannon": 11, "Say You Love Me": 11, "Go Your Own Way": 10, "Dreams": 1,
        "Don't Stop": 3, "You Make Loving Fun": 9, "Tusk": 8, "Sara": 7}
WRITER = {"Over My Head": "Christine McVie", "Rhiannon": "Stevie Nicks", "Say You Love Me": "Christine McVie",
          "Go Your Own Way": "Lindsey Buckingham", "Dreams": "Stevie Nicks", "Don't Stop": "Christine McVie",
          "You Make Loving Fun": "Christine McVie", "Tusk": "Lindsey Buckingham", "Sara": "Stevie Nicks"}
RELEASED = {"Over My Head": "September 1975", "Rhiannon": "February 1976", "Say You Love Me": "June 1976",
            "Go Your Own Way": "December 20, 1976", "Dreams": "March 24, 1977", "Don't Stop": "June 1977",
            "You Make Loving Fun": "September 1977", "Tusk": "September 21, 1979", "Sara": "December 5, 1979"}
ALBUM = {"Over My Head": "Fleetwood Mac (1975)", "Rhiannon": "Fleetwood Mac (1975)", "Say You Love Me": "Fleetwood Mac (1975)",
         "Go Your Own Way": "Rumours", "Dreams": "Rumours", "Don't Stop": "Rumours", "You Make Loving Fun": "Rumours",
         "Tusk": "Tusk", "Sara": "Tusk"}


def main():
    radio = json.loads(read(ROOT / "data/radio/radio-songs.json"))
    weekly = json.loads(read(ROOT / "data/billboard/hot100_weekly.json"))
    beyond = json.loads(read(ROOT / "data/billboard/beyond_year_end.json"))["songs"]

    ye = [s for s in radio if s["artist"] == "Fleetwood Mac" and s.get("youtube_id")]
    assert len(ye) == 5, len(ye)
    extra = [b for b in beyond if b["page"] == PAGE]
    assert len(extra) == 4, len(extra)
    yt_check = {s["title"] for s in ye} | {b["title"] for b in extra}
    assert yt_check == set(PEAK), yt_check ^ set(PEAK)

    runs = collections.OrderedDict()
    for yr in sorted(weekly):
        for w in weekly[yr]:
            if w["artist"] == "Fleetwood Mac":
                d = runs.setdefault(w["title"], {"first": w["week_start"], "weeks": 0})
                d["weeks"] += 1
    assert list(runs) == ["Dreams"], list(runs)
    dreams = runs["Dreams"]
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
        rows.append(f'              <tr><td class="ohw-listen">{play_button(yt, t, "Fleetwood Mac")}</td>'
                    f'<td class="ohw-song">{html.escape(t)}</td>'
                    f'<td>{y}</td><td>{r if r else ""}</td><td>{PEAK[t]}</td><td>{"Yes" if t in runs else ""}</td></tr>')

    year_rows = []
    for y in ye_years:
        ys = [s for s in ye if s["year"] == y]
        best = min(ys, key=lambda s: s["rank"])
        year_rows.append([y, len(ys), f'{html.escape(best["title"])} (#{best["rank"]})',
                          "Dreams" if dreams["first"].startswith(str(y)) else "None"])

    writer_rows = [[html.escape(t), WRITER[t], RELEASED[t], ALBUM[t], PEAK[t]]
                   for t in sorted(PEAK, key=lambda k: list(RELEASED).index(k))]
    wcount = collections.Counter(WRITER.values())

    album_rows = [
        ["Fleetwood Mac", "July 11, 1975", "Number one on the chart dated Sept. 4, 1976, after first peaking at number nine",
         "Over My Head (20), Rhiannon (11), Say You Love Me (11)"],
        ["Rumours", "February 4, 1977", "31 non-consecutive weeks at number one",
         "Go Your Own Way (10), Dreams (1), Don't Stop (3), You Make Loving Fun (9)"],
        ["Tusk", "1979", "20-track double album",
         "Tusk (8), Sara (7)"],
    ]

    top_row = min((s for s in ye), key=lambda s: s["rank"])
    top_ranks = ", ".join(f'{s["title"]} (#{s["rank"]})' for s in sorted(ye, key=lambda s: s["rank"]))

    faq = [
        ("Which Fleetwood Mac song reached number one in the 1970s?",
         [f"Dreams was the only Fleetwood Mac song to reach number one on the Hot 100 in this site's 1970s weekly data.",
          f"It spent {NUM[dreams['weeks']]} week at the top, starting {fmt_date(dreams['first'])}.",
          "Stevie Nicks wrote it, and it came from the album Rumours."]),
        ("Who wrote Dreams by Fleetwood Mac?",
         ["Stevie Nicks wrote Dreams for the 1977 album Rumours.",
          "According to Wikipedia, she wrote it in about 10 minutes at the Record Plant studio in Sausalito, California.",
          "The single came out on March 24, 1977, and reached number one on June 18, 1977."]),
        ("What are the biggest Fleetwood Mac songs of the 70s?",
         [f"Dreams was the highest-ranked Fleetwood Mac song on a 1970s Year-End Hot 100, at #{top_row['rank']} for {top_row['year']}.",
          "Don't Stop, Rhiannon, Say You Love Me, Go Your Own Way, You Make Loving Fun, Tusk and Sara also charted.",
          "Peaks run from number one for Dreams down to number 20 for Over My Head."]),
        ("Which Fleetwood Mac songs are on the album Rumours?",
         ["Go Your Own Way, Dreams, Don't Stop and You Make Loving Fun are the four Rumours singles here.",
          "All four reached the top 10 of the Hot 100, according to Wikipedia.",
          "Rumours came out on February 4, 1977, and spent 31 non-consecutive weeks at number one on the Billboard 200."]),
        ("Why did Bill Clinton use Don't Stop?",
         ["Bill Clinton used Fleetwood Mac's Don't Stop as the theme of his 1992 presidential campaign.",
          "Christine McVie wrote it about her separation from John McVie.",
          "Clinton chose it because he approved of its message.",
          "Clinton then asked the band to play it at his 1993 inaugural ball, according to Wikipedia."]),
    ]
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": " ".join(a)}} for q, a in faq]},
        indent=2, ensure_ascii=False)
    faq_ld = "\n".join("  " + l for l in faq_ld.split("\n"))
    faq_html = "\n".join(
        f'          <div class="faq-item">\n            <h3>{html.escape(q)}</h3>\n' + "\n".join(f"            <p>{html.escape(l)}</p>" for l in a) + "\n          </div>"
        for q, a in faq).replace("&#x27;", "'")

    TITLE = f"Fleetwood Mac Songs: {n} Hits Played, 1 at Number One"
    desc = (f"Fleetwood Mac songs: play all {n} hits of the 70s, from Over My Head to Sara. "
            "Read how Dreams, Rhiannon and Go Your Own Way came to be.")
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

    toc = [("fleetwood-mac-song-list", f"Fleetwood Mac Songs: Play All {n} Hits"),
           ("by-the-numbers", "The Numbers Behind the Hits"),
           ("two-fleetwood-macs", "Two Fleetwood Macs: Blues Band to Pop Giants"),
           ("self-titled-album", "The 1975 Album That Took More Than a Year to Reach Number One"),
           ("rumours", "Rumours: Four Top 10 Singles From a Breakup Record"),
           ("dreams", "Dreams: One Week at Number One, Then 2020"),
           ("tusk-and-sara", "Tusk and Sara: The 1979 Double Album"),
           ("who-wrote-what", "Who Wrote What: McVie, Nicks and Buckingham"),
           ("sources", "Sources"), ("faq", "Frequently Asked Questions")]
    toc_html = "\n".join(f'            <li><a href="#{i}">{t}</a></li>' for i, t in toc)

    early_pic = pic("fleetwood-mac-1970", "Peter Green and Mick Fleetwood of Fleetwood Mac on stage in Hannover, Germany, in March 1970, the blues-band era before Fleetwood Mac songs hit the Hot 100",
                    "(max-width: 700px) 100vw, 800px", 800, 534, widths=(400, 600, 800)).replace(
        "<img\n", '<img style="display:block;width:100%;max-width:800px;height:auto;margin:1.5rem auto;border-radius:8px"\n', 1)
    feat_pic = pic(IMG, "Fleetwood Mac members Mick Fleetwood, Christine McVie, John McVie, Stevie Nicks and Lindsey Buckingham in a 1977 Rumours advertisement, the lineup behind Fleetwood Mac songs of the 70s",
                   "(max-width: 700px) 100vw, 560px", 960, 960, widths=(400, 800, 960), lazy=False).replace(
        'class="post-featured-img"', 'class="post-featured-img" style="aspect-ratio:1/1;max-width:560px;margin:1.5rem auto"', 1)

    body = f'''        <h2 id="fleetwood-mac-song-list">Fleetwood Mac Songs: Play All {n} Hits</h2>
{p(f"Here are {NUM[n]} Fleetwood Mac singles from the 1970s.",
   "Five come from this site's Year-End Hot 100 data, and four charted on the weekly Hot 100 only.",
   "Press Play on any row to watch it here, and tap a heading to sort.")}

        <div class="data-table-wrap scroll-list">
          <table class="data-table sortable-table" id="fleetwoodMacSongsTable" data-inline-player>
            <caption>{n} Fleetwood Mac songs of the 70s, with Billboard Year-End Hot 100 rank, weekly Hot 100 peak and number one status</caption>
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
{p("Year is the year-end list year for the five ranked songs.",
   "For the other four, it is the single's release year.",
   "Year-End Rank is the song's spot on that year's Billboard Year-End Hot 100.",
   "It is blank for songs that list left out.",
   "Weekly Hot 100 Peak comes from each song's Wikipedia article.",
   "The #1 Hit flag comes from this site's own weekly data.")}

        <h2 id="by-the-numbers">The Numbers Behind the Hits</h2>
{p(f"Only {NUM[len(ye)]} Fleetwood Mac songs made a 1970s Year-End Hot 100, and they all landed in {ye_years[0]} and {ye_years[1]}.",
   f"The band had no entry in {', '.join(str(y) for y in missing[:-1])} or {missing[-1]}.",
   "That is a tight window, because the lineup behind them had only come together at the end of 1974.")}

{tbl("Fleetwood Mac on the Year-End Hot 100 and the weekly number ones, 1976 and 1977", ["Year", "Songs on the year-end list", "Best year-end rank", "Number ones that began that year"], year_rows)}

        <h3>Three Ways to Read Fleetwood Mac Songs</h3>
{p("The year-end list and the weekly chart tell different stories here.")}
        <ul>
          <li>Dreams ranks #{ye_by_title["Dreams"]} for 1977, the best year-end rank of any Fleetwood Mac song.</li>
          <li>It was also their only number one in the decade.</li>
          <li>Go Your Own Way ranks only #{ye_by_title["Go Your Own Way"]} for 1977, even though it reached number 10 on the weekly chart.</li>
          <li>Tusk and Sara reached number 8 and number 7 on the weekly chart.</li>
          <li>Neither is on a year-end list in this site's data.</li>
        </ul>
{p('For every chart-topper of the decade, see the full list of <a href="/blog/songs/70s-number-one-hits/">70s number one hits</a>.')}

        <h2 id="two-fleetwood-macs">Two Fleetwood Macs: Blues Band to Pop Giants</h2>

        <h3>Peter Green and a London Blues Band</h3>
{p("Peter Green formed Fleetwood Mac in London in July 1967, after he left John Mayall's Bluesbreakers.",
   "Mick Fleetwood was his rhythm-section partner in that first band.",
   "It grew out of John Mayall's blues group, a long way from the radio sound the name carries today.")}
{early_pic}
        <p class="post-img-caption">Peter Green and Mick Fleetwood on stage in Hannover, Germany, March 18, 1970.</p>
        <p class="post-img-caption">Image credit: Photo by Herbert Weber, CC BY-SA 4.0, via Wikimedia Commons.</p>

        <h3>The Bob Welch Years</h3>
{p("Bob Welch, an American singer and guitarist, joined in 1971 after the band heard a tape of his songs.",
   "Wikipedia says they hired him without ever playing with him first.",
   "He stayed until 1974, then left to go solo, just before the lineup everyone remembers arrived.")}

        <h3>New Year's Eve, 1974</h3>
{p("Lindsey Buckingham and Stevie Nicks joined on New Year's Eve 1974.",
   "Mick Fleetwood had met Buckingham at Sound City Studios.",
   "Nicks came on the condition that she be included too.",
   "Mick Fleetwood on drums and John McVie on bass stayed on.",
   "Christine McVie played keyboards and sang, according to Wikipedia.",
   "Every song in the playable list above comes from that five-person band.")}
{p('If you want another act from the same decade, the <a href="/pages/random-artist-picker">Random Artist Picker</a> will pull one for you.')}

        <h2 id="self-titled-album">The 1975 Album That Took More Than a Year to Reach Number One</h2>
{p(f"The first album with the new lineup was simply called Fleetwood Mac.",
   "It came out on July 11, 1975.",
   "It was recorded at Sound City Studios in Van Nuys, California.",
   "It debuted at number 183 on the chart dated August 2, 1975, and first peaked at number nine.",
   "Then it climbed again.",
   "It reached number one on the chart dated September 4, 1976, more than a year after it entered.",
   "The RIAA certified it 9 times platinum for US sales.")}
{p("Three songs from it are in the playable list, and the first single is the least remembered.")}

        <h3>Over My Head</h3>
{p("Christine McVie wrote Over My Head and sang the lead.",
   "Reprise chose it as the lead single, and it came out in September 1975.",
   "It reached number 20 on the Hot 100, according to Wikipedia.",
   "It was the warm-up for the two singles that followed.")}

        <h3>Rhiannon</h3>
{p("Stevie Nicks wrote Rhiannon after reading a novel called Triad by Mary Bartlet Leader, which mentions a Welsh legend.",
   "She said she had to write something about the character.",
   "She only learned in early 1978 that Rhiannon was a Welsh goddess.",
   "The single followed in February 1976 and reached number 11.")}
{p("Nicks often introduced it live as a song about an old Welsh witch.",
   "Mick Fleetwood later recalled her performance of it as being like an exorcism.",
   "The song was played on every Fleetwood Mac tour from 1975 to 1982, according to Wikipedia.")}

        <h3>Say You Love Me</h3>
{p("Christine McVie wrote Say You Love Me too.",
   "It was the first song the band rehearsed for the album.",
   "The single came out in June 1976 and also reached number 11, holding there for three weeks.",
   "The single version adds overdubbed guitar and a faster fade-out than the album cut.",
   'It is a good example of the gentler <a href="/blog/genres/70s-soft-rock/">70s soft rock</a> side of the band.')}

        <h2 id="rumours">Rumours: Four Top 10 Singles From a Breakup Record</h2>
{p("Rumours came out on February 4, 1977.",
   "Most of it was recorded in 1976 at the Record Plant in Sausalito, California.",
   "Wikipedia says the sessions took place while Christine and John McVie divorced.",
   "Lindsey Buckingham and Stevie Nicks also ended their relationship for good.",
   "Mick Fleetwood's wife also left him for his best friend.",
   "Two of the singles below were written about those splits, and the band recorded them together anyway.")}

{tbl("The three albums behind the Fleetwood Mac songs of the 70s", ["Album", "Released", "Chart run or format", "Singles from this page (weekly Hot 100 peak)"], album_rows)}

{p("Rumours spent 31 non-consecutive weeks at number one on the Billboard 200.",
   "It won Album of the Year at the 1978 Grammy Awards, according to Wikipedia's article on the album.",
   "Wikipedia also says it had sold over 40 million copies worldwide as of February 2023.",
   'The top of the chart was crowded, as the story of <a href="/blog/artists/carpenters-songs/">Carpenters songs</a> from a few years earlier shows.')}

        <h3>Go Your Own Way</h3>
{p("Lindsey Buckingham wrote Go Your Own Way as a reply to his breakup with Stevie Nicks.",
   "It was the lead single, released on December 20, 1976, and it reached number 10 on March 12, 1977.",
   "Buckingham was inspired by the drum feel of the Rolling Stones' Street Fighting Man.",
   "Mick Fleetwood built his own pattern across the tom-toms, with the bass drum on the middle beat.",
   "He described his playing as capitalizing on his own ineptness.")}

        <h3>Don't Stop</h3>
{p("Christine McVie wrote Don't Stop, and it came out in the US in June 1977.",
   "It reached number three on the Hot 100 in September 1977.",
   "She wrote it about her separation from John McVie after eight years of marriage.",
   "Wikipedia says he did not know what it was about until the record came out.",
   "The basic track was cut on March 16, 1976, under the working title Yesterday's Gone.",
   "Buckingham sang the first verse and McVie the second, with Nicks on backing vocals.")}
{p("In 1992 Bill Clinton used it as the theme of his presidential campaign.",
   "It played during the balloon drop on the final night of the Democratic National Convention.",
   "After he won, Clinton asked the band to play it at his 1993 inaugural ball.")}

        <h3>You Make Loving Fun</h3>
{p("Christine McVie wrote You Make Loving Fun as the fourth and final single from Rumours.",
   "It came out in September 1977 and reached number nine.",
   "Wikipedia says it was inspired by her affair with the band's lighting director, Curry Grant.",
   "To avoid trouble with her husband, she said the song was about her dog.",
   "The record leans on a Rhodes piano, a Hohner Clavinet through a wah-wah pedal, and a Hammond organ.")}

        <h2 id="dreams">Dreams: One Week at Number One, Then 2020</h2>
{p(f"Stevie Nicks wrote Dreams, and Wikipedia quotes her saying she wrote it in about 10 minutes.",
   "She wrote it at the Record Plant in Sausalito, during the Rumours sessions.",
   f"It was released on March 24, 1977.",
   "On June 18, 1977, it became the band's first number one in this site's weekly data.",
   f"It held the top spot for {NUM[dreams['weeks']]} week, and ranks #{ye_by_title['Dreams']} on the 1977 year-end list.")}

        <h3>A Skateboard and a Cran-Raspberry Juice</h3>
{p("In 2020 a man named Nathan Apodaca posted a video of himself skateboarding to work.",
   "He drank Ocean Spray cran-raspberry juice and lip-synced to Dreams.",
   "Wikipedia says the video drew over 50 million views.",
   "The song reached number one on the Billboard Rock Digital Song Sales chart in October 2020.",
   "It also re-entered the Hot 100 at number 21 on October 17, 2020.",
   "The next week it rose to number 12.",
   "Wikipedia adds that Rolling Stone ranked it number nine on its 2021 list of the 500 Greatest Songs.")}
{p('To test what you know about the decade, take the <a href="/pages/70s-trivia-quiz">70s Music Trivia Quiz</a>.')}

        <h2 id="tusk-and-sara">Tusk and Sara: The 1979 Double Album</h2>
{p("Tusk arrived in 1979 as a 20-track double album.",
   "Two singles from it are in the playable list.",
   "Neither made a 1970s year-end list in this site's data.")}

        <h3>Tusk and a Marching Band</h3>
{p("Lindsey Buckingham wrote Tusk and sang it, and it came out on September 21, 1979.",
   "It reached number eight on the Hot 100 and held there for three weeks.",
   "It grew out of a rehearsal riff Buckingham played at sound checks, with the working title Stage Riff.",
   "Mick Fleetwood asked for the USC Trojan Marching Band.",
   "The band recorded with 112 members at Dodger Stadium.",
   "The venue was secured for free through Dodgers player Ron Cey.")}

        <h3>Sara and Its Many Subjects</h3>
{p("Stevie Nicks wrote Sara, and it came out on December 5, 1979, as the second single from Tusk.",
   "It reached number seven on the Hot 100, according to Wikipedia.",
   "The album version runs 6 minutes and 22 seconds, and the single edit runs 4 minutes and 37 seconds.",
   "Nicks said in the early 1990s that it was partly about her friend Sara Recor.",
   "Don Henley claimed it was about their unborn child.",
   "In a 2014 Billboard interview, Nicks said that account was accurate but not the entirety of it.")}

        <h2 id="who-wrote-what">Who Wrote What: McVie, Nicks and Buckingham</h2>
{p(f"Three writers share all {NUM[n]} Fleetwood Mac songs in the playable list.",
   f"Christine McVie wrote {NUM[wcount['Christine McVie']]}, Stevie Nicks wrote {NUM[wcount['Stevie Nicks']]}, and Lindsey Buckingham wrote {NUM[wcount['Lindsey Buckingham']]}.",
   "The table shows who wrote each song and when it came out.",
   "It also shows how high each climbed on the weekly Hot 100.")}

{tbl("Fleetwood Mac songs of the 70s: writer, release, album and weekly Hot 100 peak (Wikipedia)", ["Song", "Written by", "Released", "Album", "Weekly Hot 100 Peak"], writer_rows)}

        <h3>Keep Exploring</h3>
{p(f"Fleetwood Mac songs of the 70s are the sound of five people turning private trouble into public hits.",
   "The year-end list keeps only five of them, and the weekly chart tells the rest of the story.")}

        <h2 id="sources">Sources</h2>
{p("Year-end ranks and Hot 100 number ones come from this site's own Billboard data, described on the <a href='/about/methodology/'>methodology page</a>.",
   'Every list on <a href="/">Music of the 70s</a> plays inside the page.',
   "Peaks, dates and stories behind the Fleetwood Mac songs above can be checked against these outside sources:")}
        <ul>
          <li><a href="https://en.wikipedia.org/wiki/Fleetwood_Mac" rel="noopener">Wikipedia: Fleetwood Mac</a> for the formation, the Bob Welch years, and the 1974 lineup.</li>
          <li><a href="https://en.wikipedia.org/wiki/Fleetwood_Mac_(1975_album)" rel="noopener">Wikipedia: Fleetwood Mac (1975 album)</a> and <a href="https://en.wikipedia.org/wiki/Rumours_(album)" rel="noopener">Rumours</a> for release dates, chart runs and the recording sessions.</li>
          <li><a href="https://en.wikipedia.org/wiki/Dreams_(Fleetwood_Mac_song)" rel="noopener">Wikipedia: Dreams</a> for the writing, the number one and the 2020 revival.</li>
          <li><a href="https://en.wikipedia.org/wiki/Go_Your_Own_Way" rel="noopener">Wikipedia: Go Your Own Way</a> and <a href="https://en.wikipedia.org/wiki/Don%27t_Stop_(Fleetwood_Mac_song)" rel="noopener">Don't Stop</a> for the writing stories and the Clinton campaign.</li>
          <li><a href="https://en.wikipedia.org/wiki/Rhiannon_(song)" rel="noopener">Wikipedia: Rhiannon</a>, <a href="https://en.wikipedia.org/wiki/Say_You_Love_Me_(Fleetwood_Mac_song)" rel="noopener">Say You Love Me</a>, <a href="https://en.wikipedia.org/wiki/Over_My_Head_(Fleetwood_Mac_song)" rel="noopener">Over My Head</a> and <a href="https://en.wikipedia.org/wiki/You_Make_Loving_Fun" rel="noopener">You Make Loving Fun</a> for peaks and recording notes.</li>
          <li><a href="https://en.wikipedia.org/wiki/Tusk_(song)" rel="noopener">Wikipedia: Tusk</a> and <a href="https://en.wikipedia.org/wiki/Sara_(Fleetwood_Mac_song)" rel="noopener">Sara</a> for the 1979 singles.</li>
        </ul>

        <section class="faq-block" id="faq">
          <h2>Frequently Asked Questions</h2>
{faq_html}
        </section>'''

    related = [
        ("carpenters-1972", "Artists", "Carpenters Songs: 11 Hits Played, 3 at Number One", "/blog/artists/carpenters-songs/",
         "Karen and Richard Carpenter, with every Year-End hit playable.", "Karen Carpenter at the drums beside Richard Carpenter on stage in 1972"),
        ("carole-1971", "Genres", "70s Soft Rock: The Sound Built to Calm the Decade Down", "/blog/genres/70s-soft-rock/",
         "The quieter side of the decade, with a full playable list.", "Carole King at a piano in 1971, representing 70s soft rock"),
        ("70s-number-one-hits", "Songs", "70s Number One Hits: Every Billboard #1", "/blog/songs/70s-number-one-hits/",
         "All 253 Hot 100 number ones of the decade, sortable and playable.", "A collage for the 70s number one hits list"),
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
      {{"@type": "ListItem", "position": 4, "name": "Fleetwood Mac Songs", "item": "{URL}"}}
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
        Fleetwood Mac Songs
      </nav>

      <article class="section seo-content">
        <h1>{TITLE}</h1>

        <p class="post-byline">By <a href="https://musicofthe70s.net/about/author/">Charlie</a> &middot; Published {PUBLISHED.strftime('%B')} {PUBLISHED.day}, {PUBLISHED.year}</p>
        <p class="jump-to-list"><a class="btn-primary jump-btn" href="#fleetwood-mac-song-list">&#9654; Jump to the playable list</a></p>

        <p class="post-intro">Fleetwood Mac songs of the 1970s split into two eras, and this page plays {NUM[n]} from the second one.</p>
        <p class="post-intro">Only {NUM[len(ye)]} made a Year-End Hot 100, and Dreams reached number one for a week in June 1977.</p>
        <p class="post-intro">Rumours, the album behind four of them, was recorded while two couples in the band were splitting up.</p>
        <p class="post-intro">Press Play on every hit below, then read the story behind each one.</p>

{feat_pic}
        <p class="post-img-caption">Fleetwood Mac, from left: Mick Fleetwood, Christine McVie, John McVie, Stevie Nicks and Lindsey Buckingham, in a 1977 Rumours advertisement.</p>
        <p class="post-img-caption">Image credit: Warner Bros. Records, public domain, via Wikimedia Commons (Billboard, June 25, 1977).</p>

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
