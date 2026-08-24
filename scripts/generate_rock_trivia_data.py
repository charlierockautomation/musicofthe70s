#!/usr/bin/env python3
"""
Generates js/rock-trivia-data.js from the site's own validated artist JSON
(data/artists/artists_classic_rock.json, _hard_rock, _prog_rock, _punk_new_wave).

Every question is built directly from structured fields (album title/year,
song title, formed year, origin) — never from free-text parsing — so every
fact traces back to ground-truth data. Re-run after any edit to those four
source files.
"""
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "artists"
OUT_FILE = ROOT / "js" / "rock-trivia-data.js"

GENRE_FILES = {
    "classic-rock": "artists_classic_rock.json",
    "hard-rock": "artists_hard_rock.json",
    "prog-rock": "artists_prog_rock.json",
    "punk-new-wave": "artists_punk_new_wave.json",
}

GENRE_LABELS = {
    "classic-rock": "Classic Rock",
    "hard-rock": "Hard Rock",
    "prog-rock": "Prog Rock",
    "punk-new-wave": "Punk & New Wave",
}

random.seed(70197019)  # deterministic output across regenerations

MAX_ALBUM_Q_PER_ARTIST = 2


def load_genre(genre):
    with open(DATA_DIR / GENRE_FILES[genre]) as f:
        return json.load(f)


def pick_distractors(pool, exclude, n, key):
    candidates = [key(a) for a in pool if key(a) != exclude and key(a)]
    candidates = list(dict.fromkeys(candidates))  # dedupe, keep order
    random.shuffle(candidates)
    return candidates[:n]


def build_options(correct, distractors):
    opts = [correct] + distractors
    random.shuffle(opts)
    return opts, opts.index(correct)


def explain_for(artist):
    if artist.get("trivia"):
        return artist["trivia"][0]
    return f"{artist['name']} formed in {artist.get('formed', 'the 70s')} out of {artist.get('origin', 'the scene')}."


def gen_questions(genre, artists):
    qs = []
    for artist in artists:
        name = artist["name"]
        albums = artist.get("key_albums_70s", [])
        songs = artist.get("key_songs_70s", [])
        formed = artist.get("formed")
        origin = artist.get("origin")
        explain = explain_for(artist)

        # album -> artist
        for album in albums[:MAX_ALBUM_Q_PER_ARTIST]:
            distractors = pick_distractors(artists, name, 3, lambda a: a["name"])
            if len(distractors) < 3:
                continue
            opts, idx = build_options(name, distractors)
            qs.append({
                "genre": genre,
                "q": f"Which artist released the album \"{album['title']}\" in {album['year']}?",
                "options": opts,
                "answer": idx,
                "explain": explain,
            })

        # album -> year
        for album in albums[:MAX_ALBUM_Q_PER_ARTIST]:
            correct_year = album["year"]
            near_years = [correct_year + d for d in (-2, -1, 1, 2) if 1970 <= correct_year + d <= 1979]
            distractors = list(dict.fromkeys(near_years))[:3]
            if len(distractors) < 3:
                continue
            opts, idx = build_options(correct_year, distractors)
            qs.append({
                "genre": genre,
                "q": f"In what year did {name} release \"{album['title']}\"?",
                "options": [str(o) for o in opts],
                "answer": idx,
                "explain": explain,
            })

        # song -> artist
        if songs:
            song = songs[0]
            distractor_pool = [a for a in artists if a["name"] != name and a.get("key_songs_70s")]
            random.shuffle(distractor_pool)
            distractor_songs = []
            for a in distractor_pool:
                if a["key_songs_70s"][0] != song:
                    distractor_songs.append(a["key_songs_70s"][0])
                if len(distractor_songs) == 3:
                    break
            if len(distractor_songs) == 3:
                opts, idx = build_options(song, distractor_songs)
                qs.append({
                    "genre": genre,
                    "q": f"Which of these songs is a 70s track by {name}?",
                    "options": opts,
                    "answer": idx,
                    "explain": explain,
                })

        # formed year
        if formed:
            distractors = pick_distractors(artists, name, 8, lambda a: a.get("formed"))
            distractors = [d for d in distractors if d != formed][:3]
            if len(distractors) == 3:
                opts, idx = build_options(formed, distractors)
                qs.append({
                    "genre": genre,
                    "q": f"In what year was {name} formed?",
                    "options": [str(o) for o in opts],
                    "answer": idx,
                    "explain": explain,
                })

        # origin
        if origin:
            distractors = pick_distractors(artists, name, 8, lambda a: a.get("origin"))
            distractors = [d for d in distractors if d != origin][:3]
            if len(distractors) == 3:
                opts, idx = build_options(origin, distractors)
                qs.append({
                    "genre": genre,
                    "q": f"Where did {name} originate?",
                    "options": opts,
                    "answer": idx,
                    "explain": explain,
                })
    return qs


def main():
    all_questions = []
    counts = {}
    for genre in GENRE_FILES:
        artists = load_genre(genre)
        qs = gen_questions(genre, artists)
        all_questions.extend(qs)
        counts[genre] = len(qs)

    random.shuffle(all_questions)

    lines = []
    lines.append("/* Rock Trivia Game — question pool, generated from data/artists/*.json.")
    lines.append("   Every fact traces to structured fields (album/year/song/formed/origin) in")
    lines.append("   the site's own validated artist data, never free text. Regenerate with")
    lines.append("   scripts/generate_rock_trivia_data.py after editing any source file.")
    lines.append("   Genres: " + ", ".join(f"{g} ({counts[g]})" for g in GENRE_FILES) + f". Total: {len(all_questions)}. */")
    lines.append("const ROCK_TRIVIA_GENRE_LABELS = " + json.dumps(GENRE_LABELS) + ";")
    lines.append("const ROCK_TRIVIA_POOL = " + json.dumps(all_questions, separators=(",", ":")) + ";")

    OUT_FILE.write_text("\n".join(lines) + "\n")
    print(f"Wrote {len(all_questions)} questions to {OUT_FILE}")
    for g, c in counts.items():
        print(f"  {g}: {c}")


if __name__ == "__main__":
    main()
