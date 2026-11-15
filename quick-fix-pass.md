---
type: plan
status: active
tags: [quick-fix-pass, article-standard, keyword-placement, ai-citation]
relatedTo: [article-standard, content-build, upgrades-queue]
---

# Quick-Fix Pass (live pages, started 2026-11-15)

Live blog pages that fail only the quick-fix checks of `scripts/check_standard.py` (P1-P8 keyword placement, C1 pronoun-led fact sentences, T1 Updated date = schema dateModified).
Regenerate this list any time with `python3 scripts/check_standard.py --placement` (read-only).
Rules: never change a live slug, no redirects, no new research or sections (those pages wait for upgrades-queue.md).
Batches of 10 to 15 pages per session in the order below (highest search volume first: Years, Genres, Artists, Songs, Trivia).
Every fixed page must pass `--placement`. PUBLISH GATE applies to every batch: build, preview, Charlie's go-ahead, then commit and push.
Delete a row once its batch is LIVE. When the table is empty, remove the Quick-fix pass item from content-build.md and delete this file.
Most pages need T1 only: add `&middot; Updated Month D, YYYY` to the byline and set the schema dateModified to the same date.

Batch 1 (the 13 registered pages): LIVE 2026-11-15 (5c44ebd, regen e383552), 13/13 live URLs verified.
Batch 2 (rows 1 to 12, Years + Genres): built 2026-11-15, all PASS --placement, awaiting Charlie's review. Delete rows 1 to 12 once LIVE.
Dates (Charlie, 2026-11-15): today only on a real content change; a T1-only page gets its real last content-change date from git history (Hard Rock 2026-10-09, Punk Rock 2026-10-06, 70s Rock 2026-10-09).
Found in batch 2: all 12 legacy pages already fail the K2 stuffing ceilings (worst 300-word window 5 to 8, several with the keyword in 3+ H2s). Edits in this pass never raise K2; de-stuffing is not in the quick-fix scope yet (open question for Charlie).

Batch 3 adds first: Journey meta description 158 chars, trim to 155 or less (O5), then upgrades-queue C5.

| # | Page | Keyword | Fails |
|---|---|---|---|
| 1 | blog/years/top-songs-of-1970/ | top songs of 1970 | P7 P8 |
| 2 | blog/years/top-songs-of-1974/ | top songs of 1974 | C1 |
| 3 | blog/years/top-songs-of-1975/ | top songs of 1975 | C1 |
| 4 | blog/years/top-songs-of-1977/ | top songs of 1977 | P6 |
| 5 | blog/years/top-songs-of-1979/ | top songs of 1979 | C1 |
| 6 | blog/genres/70s-country-rock/ | 70s country rock | T1 P6 P7 |
| 7 | blog/genres/70s-country-songs/ | 70s country songs | T1 P6 P7 |
| 8 | blog/genres/70s-hard-rock/ | 70s hard rock | T1 P7 |
| 9 | blog/genres/70s-progressive-rock/ | 70s progressive rock | T1 P4 |
| 10 | blog/genres/70s-punk-rock/ | 70s punk rock | T1 |
| 11 | blog/genres/70s-rock/ | 70s rock | T1 |
| 12 | blog/genres/glam-rock-in-the-70s/ | glam rock in the 70s | P7 |
| 13 | blog/artists/70s-female-singers/ | 70s female singers | P7 C1 |
| 14 | blog/artists/70s-singers/ | 70s singers | P7 C1 |
| 15 | blog/artists/abba/ | abba | T1 C1 |
| 16 | blog/artists/barry-manilow-songs/ | barry manilow songs | T1 C1 |
| 17 | blog/artists/bee-gees/ | bee gees | T1 |
| 18 | blog/artists/benny-andersson/ | benny andersson | T1 P7 |
| 19 | blog/artists/bjorn-ulvaeus/ | bjorn ulvaeus | T1 |
| 20 | blog/artists/brian-may-and-queen/ | brian may and queen | T1 P6 |
| 21 | blog/artists/carole-king/ | carole king | T1 |
| 22 | blog/artists/carpenters-songs/ | carpenters songs | T1 P6 |
| 23 | blog/artists/diana-ross-songs/ | diana ross songs | T1 |
| 24 | blog/artists/donna-summer/ | donna summer | T1 C1 |
| 25 | blog/artists/eagles-the-band/ | eagles the band | T1 |
| 26 | blog/artists/earth-wind-and-fire-songs/ | earth wind and fire songs | T1 |
| 27 | blog/artists/elton-john/ | elton john | T1 C1 |
| 28 | blog/artists/fleetwood-mac-songs/ | fleetwood mac songs | T1 P8 |
| 29 | blog/artists/george-clinton/ | george clinton | T1 |
| 30 | blog/artists/gladys-knight-songs/ | gladys knight songs | T1 C1 |
| 31 | blog/artists/grateful-dead/ | grateful dead in the 70s | T1 P6 C1 |
| 32 | blog/artists/helen-reddy-songs/ | helen reddy songs | T1 C1 |
| 33 | blog/artists/iggy-pop/ | iggy pop | T1 |
| 34 | blog/artists/jackson-5-songs/ | jackson 5 songs | T1 |
| 35 | blog/artists/james-brown/ | james brown in the 70s | T1 P6 |
| 36 | blog/artists/jim-croce/ | jim croce | T1 C1 |
| 37 | blog/artists/john-denver-songs/ | john denver songs | T1 |
| 38 | blog/artists/kc-and-the-sunshine-band-songs/ | kc and the sunshine band songs | T1 C1 |
| 39 | blog/artists/led-zeppelin-songs/ | led zeppelin songs | T1 P6 P7 C1 |
| 40 | blog/artists/marvin-gaye/ | marvin gaye | T1 C1 |
| 41 | blog/artists/pink-floyd-songs/ | pink floyd songs | T1 |
| 42 | blog/artists/queen-freddie-mercury/ | queen freddie mercury | T1 |
| 43 | blog/artists/rick-james/ | rick james | T1 |
| 44 | blog/artists/stevie-wonder/ | stevie wonder | T1 C1 |
| 45 | blog/artists/talking-heads/ | talking heads | T1 |
| 46 | blog/artists/three-dog-night-songs/ | three dog night songs | T1 |
| 47 | blog/artists/village-people/ | village people in the 70s | T1 P6 |
| 48 | blog/artists/willie-nelson/ | willie nelson | T1 C1 |
| 49 | blog/songs/25-or-6-to-4/ | 25 or 6 to 4 | T1 C1 |
| 50 | blog/songs/70s-dance-songs/ | 70s dance songs | T1 P7 |
| 51 | blog/songs/70s-love-songs/ | 70s love songs | T1 |
| 52 | blog/songs/70s-one-hit-wonders/ | 70s one hit wonders | T1 P7 |
| 53 | blog/songs/70s-party-songs/ | 70s party songs | T1 |
| 54 | blog/songs/70s-road-trip-songs/ | 70s road trip songs | T1 P7 |
| 55 | blog/songs/70s-slow-songs/ | 70s slow songs | T1 P7 |
| 56 | blog/songs/abba-knowing-me-knowing-you/ | abba knowing me knowing you | P6 P7 C1 |
| 57 | blog/songs/abba-waterloo/ | abba waterloo | T1 P6 |
| 58 | blog/songs/al-green-lets-stay-together/ | al green let's stay together | T1 P6 C1 |
| 59 | blog/songs/al-green-tired-of-being-alone/ | al green tired of being alone | T1 P6 P7 C1 |
| 60 | blog/songs/bad-bad-leroy-brown/ | bad bad leroy brown | T1 C1 |
| 61 | blog/songs/best-of-my-love/ | best of my love | T1 C1 |
| 62 | blog/songs/blue-eyes-crying-in-the-rain/ | blue eyes crying in the rain | T1 C1 |
| 63 | blog/songs/bohemian-rhapsody/ | bohemian rhapsody | T1 |
| 64 | blog/songs/boogie-wonderland/ | boogie wonderland | T1 C1 |
| 65 | blog/songs/bridge-over-troubled-water/ | bridge over troubled water | T1 |
| 66 | blog/songs/carole-king-its-too-late/ | carole king it's too late | T1 P6 P7 |
| 67 | blog/songs/close-to-you/ | close to you | T1 |
| 68 | blog/songs/comfortably-numb-pink-floyd/ | comfortably numb | T1 |
| 69 | blog/songs/copacabana-barry-manilow/ | copacabana barry manilow | T1 P6 C1 |
| 70 | blog/songs/dancing-queen/ | dancing queen | T1 |
| 71 | blog/songs/don-mclean-american-pie/ | don mclean american pie | T1 P6 |
| 72 | blog/songs/donna-summer-hot-stuff/ | donna summer hot stuff | T1 P6 C1 |
| 73 | blog/songs/dreams-fleetwood-mac/ | dreams fleetwood mac | T1 P6 P7 C1 |
| 74 | blog/songs/flash-light-parliament/ | flash light parliament | P7 |
| 75 | blog/songs/georgia-on-my-mind/ | georgia on my mind | T1 P6 C1 |
| 76 | blog/songs/gimme-gimme-gimme/ | gimme gimme gimme | T1 P7 |
| 77 | blog/songs/give-up-the-funk-parliament/ | give up the funk parliament | T1 C1 |
| 78 | blog/songs/go-your-own-way/ | go your own way | T1 P7 C1 |
| 79 | blog/songs/heartache-tonight/ | heartache tonight | T1 |
| 80 | blog/songs/hopelessly-devoted-to-you/ | hopelessly devoted to you | T1 C1 |
| 81 | blog/songs/hotel-california/ | hotel california | T1 |
| 82 | blog/songs/how-can-you-mend-a-broken-heart/ | how can you mend a broken heart | T1 P4 C1 |
| 83 | blog/songs/how-deep-is-your-love/ | how deep is your love | T1 |
| 84 | blog/songs/i-am-woman/ | i am woman | T1 |
| 85 | blog/songs/i-want-you-back/ | i want you back | T1 C1 |
| 86 | blog/songs/i-will-always-love-you-dolly-parton/ | i will always love you dolly parton | T1 P4 P6 C1 |
| 87 | blog/songs/if-you-leave-me-now/ | if you leave me now | T1 P7 C1 |
| 88 | blog/songs/ill-be-there-jackson-5/ | i'll be there jackson 5 | T1 P6 C1 |
| 89 | blog/songs/in-the-navy-village-people/ | in the navy village people | T1 P6 |
| 90 | blog/songs/james-brown-get-on-the-good-foot/ | james brown get on the good foot | T1 C1 |
| 91 | blog/songs/jive-talkin/ | jive talkin | T1 C1 |
| 92 | blog/songs/jolene/ | jolene | T1 C1 |
| 93 | blog/songs/joy-to-the-world-three-dog-night/ | joy to the world three dog night | T1 C1 |
| 94 | blog/songs/kashmir-led-zeppelin/ | kashmir led zeppelin | T1 P4 P6 |
| 95 | blog/songs/killer-queen/ | killer queen | T1 |
| 96 | blog/songs/last-dance/ | last dance | T1 C1 |
| 97 | blog/songs/living-for-the-city/ | living for the city | T1 C1 |
| 98 | blog/songs/macarthur-park-donna-summer/ | macarthur park donna summer | T1 P6 C1 |
| 99 | blog/songs/mamma-mia-song/ | mamma mia song | T1 C1 |
| 100 | blog/songs/mandy-barry-manilow/ | mandy barry manilow | T1 P6 C1 |
| 101 | blog/songs/marvin-gaye-lets-get-it-on/ | marvin gaye let's get it on | P6 P7 |
| 102 | blog/songs/midnight-train-to-georgia/ | midnight train to georgia | T1 |
| 103 | blog/songs/mr-blue-sky/ | mr. blue sky | T1 C1 |
| 104 | blog/songs/new-kid-in-town/ | new kid in town | T1 |
| 105 | blog/songs/night-fever/ | night fever | T1 C1 |
| 106 | blog/songs/one-of-these-nights/ | one of these nights | T1 P7 C1 |
| 107 | blog/songs/rhiannon-fleetwood-mac/ | rhiannon fleetwood mac | T1 P4 P6 P7 P8 C1 |
| 108 | blog/songs/rocket-man-elton-john/ | rocket man elton john | T1 P6 P7 C1 |
| 109 | blog/songs/seasons-in-the-sun/ | seasons in the sun | T1 |
| 110 | blog/songs/september-earth-wind-and-fire/ | september earth wind and fire | T1 P6 |
| 111 | blog/songs/sir-duke-stevie-wonder/ | sir duke stevie wonder | T1 P6 P7 |
| 112 | blog/songs/somebody-to-love/ | somebody to love | T1 |
| 113 | blog/songs/song-ymca/ | song ymca | T1 |
| 114 | blog/songs/stairway-to-heaven/ | stairway to heaven | T1 P6 C1 |
| 115 | blog/songs/stayin-alive/ | stayin alive | T1 C1 |
| 116 | blog/songs/superstition-stevie-wonder/ | superstition stevie wonder | T1 P6 |
| 117 | blog/songs/take-a-chance-on-me/ | take a chance on me | T1 P7 C1 |
| 118 | blog/songs/take-it-easy/ | take it easy | T1 |
| 119 | blog/songs/take-me-home-country-roads/ | take me home country roads | T1 P6 P7 |
| 120 | blog/songs/telephone-line-elo/ | telephone line elo | T1 P6 C1 |
| 121 | blog/songs/the-name-of-the-game-abba/ | the name of the game abba | T1 P6 P7 P8 C1 |
| 122 | blog/songs/time-in-a-bottle-jim-croce/ | time in a bottle jim croce | T1 P6 C1 |
| 123 | blog/songs/tiny-dancer/ | tiny dancer | T1 C1 |
| 124 | blog/songs/too-much-heaven/ | too much heaven | T1 C1 |
| 125 | blog/songs/tragedy-bee-gees/ | tragedy bee gees | T1 P6 P7 |
| 126 | blog/songs/we-will-rock-you/ | we will rock you | T1 |
| 127 | blog/songs/whats-going-on-marvin-gaye/ | what's going on marvin gaye | T1 P6 C1 |
| 128 | blog/songs/wish-you-were-here-pink-floyd/ | wish you were here pink floyd | T1 P6 C1 |
| 129 | blog/songs/you-and-i-rick-james/ | you and i rick james | T1 C1 |
| 130 | blog/songs/you-are-the-sunshine-of-my-life/ | you are the sunshine of my life | T1 P7 C1 |
| 131 | blog/songs/you-should-be-dancing/ | you should be dancing | T1 |
| 132 | blog/trivia/70s-music-quiz/ | 70s music quiz | T1 P7 |
| 133 | blog/trivia/april-17-in-music-history/ | april 17 in music history | T1 P6 |
| 134 | blog/trivia/august-19-in-music-history/ | august 19 in music history | T1 P6 |
| 135 | blog/trivia/banned-songs-of-the-70s/ | banned songs of the 70s | T1 |
| 136 | blog/trivia/december-12-in-music-history/ | december 12 in music history | T1 P6 |
| 137 | blog/trivia/december-3-in-music-history/ | december 3 in music history | T1 P6 |
| 138 | blog/trivia/february-1-in-music-history/ | february 1 in music history | T1 P6 |
| 139 | blog/trivia/february-13-in-music-history/ | february 13 in music history | T1 P6 |
| 140 | blog/trivia/january-9-in-music-history/ | january 9 in music history | T1 P6 |
| 141 | blog/trivia/july-15-in-music-history/ | july 15 in music history | T1 P6 |
| 142 | blog/trivia/june-12-in-music-history/ | june 12 in music history | T1 P6 |
| 143 | blog/trivia/march-20-in-music-history/ | march 20 in music history | T1 P6 |
| 144 | blog/trivia/may-1-in-music-history/ | may 1 in music history | T1 P6 |
| 145 | blog/trivia/may-29-in-music-history/ | may 29 in music history | T1 P6 |
| 146 | blog/trivia/november-12-in-music-history/ | november 12 in music history | T1 P6 |
| 147 | blog/trivia/november-19-in-music-history/ | november 19 in music history | T1 P6 |
| 148 | blog/trivia/november-28-in-music-history/ | november 28 in music history | T1 P6 |
| 149 | blog/trivia/november-7-in-music-history/ | november 7 in music history | T1 P6 |
| 150 | blog/trivia/october-8-in-music-history/ | october 8 in music history | T1 P6 |
| 151 | blog/trivia/september-16-in-music-history/ | september 16 in music history | T1 P6 |

## NOT QUICK (queued in upgrades-queue.md, not dropped)

B14: the 10 pages with no recorded focus keyword (keyword rule first, full standard, floor decision recorded). Chicago and ELO run as B13.
B15: 70s Music Trivia full rewrite.

## FAQ-format lines from verify_post (5 batch-1 pages)

MISMATCH and "missing visible question" were a verify_post bug (it compared &#x27; with '), fixed 2026-11-15: schema and visible FAQ text match on all 5.
The remaining "len FAIL" lines are the legacy 40-70-word rule. Article Standard T3 (answers 1 to 3 sentences, each adding a fact) overrides it and all 5 pages pass T3, so no page edit is queued. Open question for Charlie: should verify_post judge registered pages by T3 instead (as it already does for K2)?
