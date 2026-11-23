#!/usr/bin/env python3
"""Record the slot 5.4 AC/DC IDs in data/official-videos.json (verified 2026-11-23 with yt-dlp, channel AC/DC)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "data/official-videos.json"
raw = P.read_text()
data = json.loads(raw)
indent = 2 if raw.startswith('{\n  "') else 4
assert json.dumps(data, indent=indent, ensure_ascii=False) + ("\n" if raw.endswith("\n") else "") == raw, "round trip differs"
V = data["videos"]
D = "2026-11-23"
NEW = {
    "Nnjh-zp6pP4": "High Voltage - AC/DC",
    "GChhRrU6BJU": "It's a Long Way to the Top (If You Wanna Rock 'N' Roll) - AC/DC",
    "CiJeSSzu9Bo": "T.N.T. - AC/DC",
    "x7qQmpK9b1M": "Jailbreak - AC/DC",
    "jsjdjWGDvFk": "Dirty Deeds Done Dirt Cheap - AC/DC",
    "S4uwi5cUyco": "Problem Child - AC/DC",
    "3f2g4RMfhS0": "Let There Be Rock - AC/DC",
    "BL58K-3XGKs": "Whole Lotta Rosie - AC/DC",
    "-0Oa5wvARSc": "Rock 'N' Roll Damnation - AC/DC",
    "pdnFm6uZSc8": "Sin City - AC/DC",
    "7S69xWkV4uM": "Riff Raff - AC/DC",
    "l482T0yNkeo": "Highway to Hell - AC/DC",
    "YFMF4ZFmtnU": "Girls Got Rhythm - AC/DC",
    "JGftIcp2SC0": "Touch Too Much - AC/DC",
    "UKwVvSleM6w": "Shot Down in Flames - AC/DC",
    "_bP6aVG6L1w": "Walk All Over You - AC/DC",
}
added = 0
for vid, song in NEW.items():
    if vid in V:
        print("already recorded:", vid, V[vid].get("channel"))
        continue
    V[vid] = {"official": True, "channel": "AC/DC", "verified": D, "song": song}
    added += 1
P.write_text(json.dumps(data, indent=indent, ensure_ascii=False) + ("\n" if raw.endswith("\n") else ""))
print("added", added)
