# Internal Linking & Tools-as-Pillars — Full Detail

Pulled out of content-build.md 2026-09-02. Only needed during the internal-linking
step of a build. Open it then, not at session start.

Related: post-template.md holds the Internal Tool Linking Map (which tool matches
which post type) and the Anchor Text & Position Rule itself. This file holds the
strategy context and the running log.

---

## Tools as Pillars (real data, confirmed via repo audit 2026-08-09)

The site's two permanent pillar types are the homepage and the interactive tools.
Every new post links to whichever pillar its content actually supports, not the
homepage by default, and not a mismatched tool for the sake of a tool link.

| Tool | Real Data Source | Confirmed Facts |
|---|---|---|
| Random 70s Song Generator | data/songs/hot_100_songs_1970-1979.json | 1,000 records but filtered to billboard_peak <= 40 for display, real live pool is 400 songs. Own genre/mood/vibe schema per song, separate from the artist-level genre field. |
| Birthday #1 Song Finder | data/billboard/hot100_weekly.json | 522 weekly #1 records, full 1970-1979 coverage. Same file already used for Years-post research. |
| Mood Song Matcher | data/artists/*.json (same as Artist Picker) | Matches ARTISTS by mood/vibe/era tags, not genre. Tags: mood (happy 331, nostalgic 296, pumped-up 233, romantic 231, rebellious 207, melancholy 202), vibe (reflect 298, chill 272, party 250, drive 234, dance 221, rock-out 188), era (late-70s 541, mid-70s 517, early-70s 415). Does NOT map to Genres content, use the genre field instead. |
| Random Artist Picker | data/artists/*.json (10 files) | 619 total records, 601 unique artists (18 IDs appear in two genre files). Buckets: country 100, soft-rock 69, hard-rock 68, classic-rock 66, soul 66, disco 65, funk 50, pop-crossover 50, prog-rock 50, punk 35 (contaminated with 12 new-wave artists). No dedicated Glam bucket (17 glam artists scattered in hard-rock and pop-crossover). "country 100" is the whole genre:"country" field, not country-rock (real country-rock roster is 14 artists across 3 files). Don't trust a bucket count for a subgenre post without checking the subgenre field. |
| 70s Music Trivia Quiz | js/quiz-questions.js | 50 questions. Powers the built-but-not-live "70s Music Quiz" post (all 50, scored) and this tool page's own 10-question random rounds. |
| 70s Decade Wheel | data/billboard/year_end_hot100.json | Same file as the Years blog posts. No distinct dataset. |
| Rock Trivia Game (built 2026-08-23, NOT pushed) | data/artists/ classic_rock, hard_rock, prog_rock, punk_new_wave (219 artists) | 7th tool, at /pages/rock-trivia-game.html, keyword `rock trivia game`. `scripts/generate_rock_trivia_data.py` builds `js/rock-trivia-data.js` (1,384 questions) from structured fields only, no free-text parsing. Category select + date-seeded Daily Challenge with localStorage streak. Rerun the generator after editing any of the 4 source JSON files. Awaiting Charlie's go-ahead per the Publish Gate. |

Known data-quality gap (non-blocking): only 243 of 570 distinct artistIds in the
song data resolve to a real artist record. Would block any future feature that
joins songs and artists programmatically.

---

## Internal Linking Strategy

Every post links up to its category page and to at least one relevant Tool.
Cross-category links matter as much as same-category "Related Posts" links.

Each post gets one **primary destination** (the single most topically relevant
pillar, hub, or tool, not the homepage by default) and up to two **secondary
destinations**, only where genuinely useful. Never link to hit a quota.

**Link owed** (cross-category links that should exist once their target is built):

*(Table empty as of 2026-08-16 — the last open row, Bohemian Rhapsody -> Glam or
Prog Rock, was closed by the 70s Progressive Rock post; link added both
directions.)*

---

## Anchor Text & Position Log

Rule (also in post-template.md): before placing any internal link, check the last
3-5 rows for the same category. Anchor text AND position must not repeat within
that window. Anchor text = brand phrase "Music of the 70s" OR the target's own
focus keyword, never generic. Log new entries here after placing links. Log
starts 2026-08-28; prior posts not backfilled.

When this file nears 195 lines, prune the oldest rows to CONTENT-INDEX-ARCHIVE.md.

| Post | Category | Anchor Text | Target | Position |
|---|---|---|---|---|
| Donna Summer | Artists | Random Artist Picker | /pages/random-artist-picker.html | Body, "1974-1976: A Session Singer in Munich Becomes a Star" H2, mid-section |
| Donna Summer | Artists | Disco Music of the 70s | /blog/genres/disco-music-of-the-70s/index.html | Body, "1977: The Hit Too Influential for the Charts" H2, mid-sentence before the video embed |
| Donna Summer | Artists | 70s Music Trivia Quiz | /pages/70s-trivia-quiz.html | Body, "1978: An Oscar for a Song from a B-Movie" H2, mid-section |
| Donna Summer | Artists | Village People | /blog/artists/village-people/index.html | Body, opening sentence of the "1979: Three Number Ones, One Calendar Year" H2 |
| Al Green | Artists | Marvin Gaye | /blog/artists/marvin-gaye/index.html | Body, "1971-1972: Three Songs, One Year-End Chart" H2, mid-sentence contrast, not at an H2's end |
| Al Green | Artists | 70s Soul Music | /blog/genres/70s-soul-music/index.html | Body, end of "1972: The Album That Wouldn't Leave Number One" H2 |
| Al Green | Artists | Random Artist Picker | /pages/random-artist-picker.html | Body, inside the "1976-1977: Ministry" H2, mid-section |
| Al Green | Artists | 70s Music Trivia Quiz | /pages/70s-trivia-quiz.html | Body, inside the "Al Green's Real 1970s Chart Record" recap H2 |
| ABBA Waterloo | Songs | ABBA (artist) | /blog/artists/abba/index.html | Body, "Waterloo Wasn't the Real American Breakthrough" H3, opening sentence |
| ABBA Waterloo | Songs | ABBA vs Queen | /blog/trivia/abba-vs-queen/index.html | Body, same H3 as above, mid-section |
| ABBA Waterloo | Songs | Waterloo (Listen Now deep link) | /radio/index.html?play=1974-49-waterloo | Body, "The Swedish Tax Law Behind the Costumes" H2, sentence directly before the video embed |
| ABBA Waterloo | Songs | Music of the 70s | /index.html | Body, end of "Waterloo Wasn't the Real American Breakthrough" H3, closing sentence before FAQ |
| How Can You Mend a Broken Heart | Songs | Bee Gees (artist) | /blog/artists/bee-gees/index.html | Body, "A Songwriting Credit That Took 38 Years to Arrive" H3, closing sentence |
| How Can You Mend a Broken Heart | Songs | Al Green (artist) | /blog/artists/al-green/index.html | Body, "The Cover That Finished What the Original Couldn't" H2, closing sentence |
| How Can You Mend a Broken Heart | Songs | Mood Song Matcher | /pages/mood-song-matcher.html | Body, "What Maurice Actually Played" H3, mid-section before the radio deep link |
| How Can You Mend a Broken Heart | Songs | How Can You Mend a Broken Heart (Listen Now) | /radio/index.html?play=1971-5-how-can-you-mend-a-broken-heart | Body, same H3, sentence directly before the video embed |
| How Can You Mend a Broken Heart | Songs | Random 70s Song Generator | /pages/random-70s-song.html | Body, "The Chart That Ignored It Completely" H3, closing sentence, mid-post |
| How Can You Mend a Broken Heart | Songs | Music of the 70s | /index.html | Body, end of "A Second Life in Movie Theaters" H3, closing sentence after the film list |
| Killer Queen | Songs | Music of the 70s | /index.html | Body, end of the "Killer Queen Was a Deliberate Bet on a Pop Hit" H2 main paragraph, before the H3 quote subhead |
| Killer Queen | Songs | Random 70s Song Generator | /pages/random-70s-song.html | Body, "Four Real Production Choices That Built the Sound" H3, mid-paragraph after the bullet list |
| Killer Queen | Songs | Mood Song Matcher | /pages/mood-song-matcher.html | Body, "Why This Site's Own Database Shows '78,' Not '12'" H3, mid-section question lead-in |
| Killer Queen | Songs | Brian May and Queen (artist) | /blog/artists/brian-may-and-queen/index.html | Body, "Why Killer Queen Still Marks Queen's Turning Point" H2, mid-section sentence |
| Killer Queen | Songs | Bohemian Rhapsody (song) | /blog/songs/bohemian-rhapsody/index.html | Body, same H2, song-to-song cross-link |
| Killer Queen | Songs | Killer Queen (Listen Now) | /radio/index.html?play=1975-78-killer-queen | Body, same H2, closing section before FAQ, deliberately not adjacent to the video embed |
| One of These Nights | Songs | Random 70s Song Generator | /pages/random-70s-song.html | Body, closing sentence of the "One of These Nights Was a Country Band Chasing an R&B Groove" H2 main text |
| One of These Nights | Songs | Mood Song Matcher | /pages/mood-song-matcher.html | Body, closing sentence of the "The Disco Beat Henley Admitted To" H3 |
| One of These Nights | Songs | Eagles the Band (artist) | /blog/artists/eagles-the-band/index.html | Body, second sentence of the "The Lineup That Made It Did Not Last" H2 |
| One of These Nights | Songs | Hotel California (song) | /blog/songs/hotel-california/index.html | Body, "Joe Walsh and the Road to Hotel California" H3, song-to-song cross-link |
| One of These Nights | Songs | One of These Nights (Listen Now) | /radio/index.html?play=1975-10-one-of-these-nights | Body, end of the "A Second Number One in the Same Year" H2, sentence directly before the video embed |
| One of These Nights | Songs | Music of the 70s | /index.html | Body, final sentence of the "Joe Walsh and the Road to Hotel California" H3, last content section before FAQ |
| Let's Stay Together | Songs | Mood Song Matcher | /pages/mood-song-matcher.html | Body, "The Winos on the Studio Floor" H3, closing sentence |
| Let's Stay Together | Songs | Al Green (artist) | /blog/artists/al-green/index.html | Body, "A Template for Everything After" H3, closing sentence |
| Let's Stay Together | Songs | Let's Stay Together (Listen Now) | /radio/index.html?play=1972-11-lets-stay-together | Body, "Why 'Nine Weeks at Number One' Gets Misquoted" H3, the sentence right after the data table, not adjacent to the video embed |
| Let's Stay Together | Songs | Music of the 70s | /index.html | Body, opening sentence of the "The Song's Second Life" H2 |
| Let's Stay Together | Songs | Random 70s Song Generator | /pages/random-70s-song.html | Body, "From the Apollo to the Charts Again" H3, closing sentence, last content line before the video embed |
| Al Green (artist) | Artists | Let's Stay Together (song) | /blog/songs/al-green-lets-stay-together/index.html | Body, "Three Songs in One Chart" H3, closing sentence, forward link added the session the song post published |
| Bee Gees (artist) | Artists | How Can You Mend a Broken Heart (song) | /blog/songs/how-can-you-mend-a-broken-heart/index.html | Body, "The Slump and Reinvention in Miami" H2, opening section |
| ABBA (artist) | Artists | Waterloo (song) | /blog/songs/abba-waterloo/index.html | Body, "The Contest That Actually Launched ABBA" H2, mid-section |
| Rick James | Artists | George Clinton | /blog/artists/george-clinton/index.html | Body, "Rick James's Real 1970s Chart Record" H2, mid-section sentence |
| Rick James | Artists | 70s Funk | /blog/genres/70s-funk/index.html | Body, "Rick James's Real 1970s Chart Record" H2, sentence after the George Clinton link |
| Marvin Gaye | Artists | James Brown in the 70s | /blog/artists/james-brown/index.html | Body, end of the "1971: The Album Berry Gordy Tried to Bury" H2 |
| Marvin Gaye | Artists | 70s Music Trivia Quiz | /pages/70s-trivia-quiz.html | Body, end of the "1973: Let's Get It On" H2 |
| Marvin Gaye | Artists | Random Artist Picker | /pages/random-artist-picker.html | Body, end of the "Diana & Marvin" H2 |
| Marvin Gaye | Artists | 70s Soul Music | /blog/genres/70s-soul-music/index.html | Body, after the video embed in the "Got to Give It Up" H2 |
| What's Going On Marvin Gaye | Songs | Marvin Gaye (artist) | /blog/artists/marvin-gaye/index.html | Body, "Why Marvin Gaye Took It On" H3, closing sentence |
| What's Going On Marvin Gaye | Songs | Random 70s Song Generator | /pages/random-70s-song.html | Body, "A Saxophone Line That Was Just a Warm-Up" H3, closing sentence |
| What's Going On Marvin Gaye | Songs | What's Going On (Listen Now) | /radio/index.html?play=1971-21-whats-going-on | Body, end of the "How the Record Got Made by Accident" H2, not adjacent to the video embed |
| What's Going On Marvin Gaye | Songs | Music of the 70s | /index.html | Body, "Where the Song Landed on the Charts" H2, third sentence |
| What's Going On Marvin Gaye | Songs | Mood Song Matcher | /pages/mood-song-matcher.html | Body, "Why the Song Still Gets Played" H2, mid-section |
| What's Going On Marvin Gaye | Songs | 70s Soul Music | /blog/genres/70s-soul-music/index.html | Body, "Why the Song Still Gets Played" H2, closing sentence |
| Marvin Gaye (artist) | Artists | What's Going On (song) | /blog/songs/whats-going-on-marvin-gaye/index.html | Body, "A Refusal, Then a Strike" H3, closing sentence, forward link added and pushed the session the song post went live (012d3af) |
| Donna Summer Hot Stuff | Songs | Donna Summer (artist) | /blog/artists/donna-summer/index.html | Body, opening sentence of the "Donna Summer Wanted a Rock Record, Not Another Disco Single" H2 |
| Donna Summer Hot Stuff | Songs | Hot Stuff (Listen Now) | /radio/index.html?play=1979-7-hot-stuff | Body, "One Take on a Clearance-Bin Guitar" H3, mid-section, several sentences before the video embed |
| Donna Summer Hot Stuff | Songs | Mood Song Matcher | /pages/mood-song-matcher.html | Body, opening of the "The Grammy a Disco Record Was Not Supposed to Win" H2 |
| Donna Summer Hot Stuff | Songs | Music of the 70s | /index.html | Body, mid-sentence in the "What Donna Summer Brought to It" H3 |
| Donna Summer Hot Stuff | Songs | Random 70s Song Generator | /pages/random-70s-song.html | Body, end of the "The Year-End Picture" H3 |
| Donna Summer Hot Stuff | Songs | I Will Survive (song) | /blog/songs/i-will-survive/index.html | Body, "The Year-End Picture" H3, song-to-song cross-link |
| Superstition Stevie Wonder | Songs | Superstition (Listen Now) | /radio/index.html?play=1973-26-superstition | Intro, sentence before the "Motown had other plans" line, not adjacent to the video embed |
| Superstition Stevie Wonder | Songs | What's Going On (song) | /blog/songs/whats-going-on-marvin-gaye/index.html | Body, "The Trade That Never Paid Off for Beck" H3, mid-section, song-to-song cross-link |
| Superstition Stevie Wonder | Songs | Stevie Wonder (artist) | /blog/artists/stevie-wonder/index.html | Body, mid-paragraph in the "How Stevie Wonder Built Superstition Almost Entirely Alone" H2, not opening or closing sentence |
| Superstition Stevie Wonder | Songs | Mood Song Matcher | /pages/mood-song-matcher.html | Body, same H2, mid-section after the personnel list |
| Superstition Stevie Wonder | Songs | Random 70s Song Generator | /pages/random-70s-song.html | Body, end of the "The Year-End Picture" H3 |
| Superstition Stevie Wonder | Songs | Music of the 70s | /index.html | Body, "Why Superstition Still Reunites Its Original Creators" H2, mid-section |
| Stevie Wonder (artist) | Artists | Superstition (song) | /blog/songs/superstition-stevie-wonder/index.html | Body, "The Classic Period Hits, Charted Year by Year" H3, list item anchor, forward link added the session the song post published |
| Jolene | Songs | Dolly Parton (artist) | /blog/artists/dolly-parton/index.html | Body, "The Fan Who Gave It a Name" H3, mid-paragraph, not opening or closing sentence |
| Jolene | Songs | Random 70s Song Generator | /pages/random-70s-song.html | Body, "Why the Country Hit Barely Touched Pop" H3, closing sentence, before the year-end table section |
| Jolene | Songs | Mood Song Matcher | /pages/mood-song-matcher.html | Body, "The Chart Record Jolene Just Broke in 2026" H2, mid-section, opening of the third sentence |
| Jolene | Songs | 70s Music Trivia Quiz | /pages/70s-trivia-quiz.html | Body, "Three Covers, Three Very Different Outcomes" H3, closing sentence |
| Jolene | Songs | Music of the 70s | /index.html | Body, "A Chart Table That Took Five Decades to Fill In" H3, closing sentence, mid-post |
| Bad Bad Leroy Brown | Songs | Jim Croce (artist) | /blog/artists/jim-croce/index.html | Intro, opening sentence of the "The Real Leroy Brown Jim Croce Met in the Army" H2 |
| Bad Bad Leroy Brown | Songs | Random 70s Song Generator | /pages/random-70s-song.html | Body, mid-section of the "A Strong Year-End Finish" H3, not a closing sentence |
| Bad Bad Leroy Brown | Songs | Mood Song Matcher | /pages/mood-song-matcher.html | Body, closing sentence of "The Song He Never Got to Hear at the Top" H3 |
| Bad Bad Leroy Brown | Songs | Bad Bad Leroy Brown (Listen Now) | /radio/index.html?play=bad-bad-leroy-brown | Body, "A Folk-Rock Storyteller's Biggest Hit" H3, sentence directly before close, adjacent style not used in the last 4 Songs posts |
| Bad Bad Leroy Brown | Songs | 70s Music Trivia Quiz | /pages/70s-trivia-quiz.html | Body, closing sentence of the "Grammy Recognition and What Came After" H2 |
| Bad Bad Leroy Brown | Songs | 70s Soft Rock (genre) | /blog/genres/70s-soft-rock/index.html | Body, "A Folk-Rock Storyteller's Biggest Hit" H3, mid-section, secondary destination |
| Jim Croce (artist) | Artists | Bad Bad Leroy Brown (song) | /blog/songs/bad-bad-leroy-brown/index.html | Body, "A Character Sketch Becomes His Biggest Hit Yet" H3, closing sentence, forward link added the session the song post published |
| Carole King It's Too Late | Songs | Carole King (artist) | /blog/artists/carole-king/index.html | Body, "Carole King It's Too Late Started as Two Separate Songs" H2, 2nd paragraph, mid-sentence |
| Carole King It's Too Late | Songs | It's Too Late / I Feel the Earth Move (Listen Now) | /radio/index.html?play=1971-3-its-too-late-i-feel-the-earth-move | Body, closing sentence of "The Musicians Behind Both Sides of the Single" H2, not adjacent to the video embed |
| Carole King It's Too Late | Songs | Random 70s Song Generator | /pages/random-70s-song.html | Body, "A Platinum Single From a Diamond Album" H3, closing sentence |
| Carole King It's Too Late | Songs | Mood Song Matcher | /pages/mood-song-matcher.html | Body, closing sentence of "One Grammy Award for Two Songs" H2 |
| Carole King It's Too Late | Songs | Music of the 70s | /index.html | Body, closing sentence of "The Cover Version an Earthquake Ended" H2, last content line before FAQ |
| Carole King It's Too Late | Songs | 70s Soft Rock (genre) | /blog/genres/70s-soft-rock/index.html | Body, "The Cover Version an Earthquake Ended" H2, mid-section, secondary destination |
| Carole King (artist) | Artists | Carole King It's Too Late (song) | /blog/songs/carole-king-its-too-late/index.html | Body, "Five Weeks at Number One on the Hot 100" H3, mid-sentence, forward link added the session the song post published |
| Song YMCA | Songs | Music of the 70s | /index.html | Body, closing sentence of "Song YMCA Started With a Question About What YMCA Even Meant" H2, mid-post, not adjacent to FAQ |
| Song YMCA | Songs | Village People (artist) | /blog/artists/village-people/index.html | Body, "Recorded at Sigma Sound, Released on Cruisin'" H3, mid-sentence |
| Song YMCA | Songs | Mood Song Matcher | /pages/mood-song-matcher.html | Body, closing of "Randy Jones's Misunderstanding Theory" H3, directly before the video embed |
| Song YMCA | Songs | Y.M.C.A. (Listen Now) | /radio/index.html?play=1979-8-ymca | Body, sentence immediately after the video embed, not adjacent-before style used in the last 4 Songs posts |
| Song YMCA | Songs | Random 70s Song Generator | /pages/random-70s-song.html | Body, closing sentence of "Sales That Outran Its Own Chart Peak" H3 |
| Song YMCA | Songs | Disco Music of the 70s (genre) | /blog/genres/disco-music-of-the-70s/index.html | Body, closing sentence of "The Library of Congress Called It Historically Significant" H2, secondary destination |
| Village People (artist) | Artists | Song YMCA (song) | /blog/songs/song-ymca/index.html | Body, "Village People in the 70s: Y.M.C.A. Got Bigger Than Anyone Expected" H2, closing sentence, forward link added the session the song post was built |
