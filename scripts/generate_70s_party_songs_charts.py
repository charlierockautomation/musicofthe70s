#!/usr/bin/env python3
"""One-off: render the two charts on /blog/songs/70s-party-songs/ from the list in
scripts/generate_70s_party_songs_page.py (the data on disk is the source of truth).

1. 70s-party-songs-by-year: how many of the 30 songs sit on each year-end Hot 100.
2. 70s-party-songs-weeks: the longest runs at number one among the songs on the list
   (weeks from data/billboard/hot100_weekly.json, only runs the file states unambiguously).

Outputs 1200w/800w/400w JPG + WebP. Run: python3 scripts/generate_70s_love_songs_charts.py
"""
import sys
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_70s_party_songs_page import SONGS, LONG_RUNS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "images/blog"
SRCSET = OUT / "srcset"
BG, GOLD, TEXT, MUTED, BORDER = "#1a1a2e", "#f5a623", "#f0e6d3", "#9ca3af", "#2d3561"
plt.rcParams["font.family"] = "DejaVu Sans"


def save(fig, stub, w):
    jpg = OUT / f"{stub}-{w}w.jpg" if w == 1200 else SRCSET / f"{stub}-{w}w.jpg"
    fig.savefig(jpg, format="jpg", facecolor=BG)
    fig.savefig(SRCSET / f"{stub}-{w}w.webp", format="webp", facecolor=BG)
    plt.close(fig)


def style(ax, w):
    ax.set_facecolor(BG)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(BORDER)
    ax.tick_params(colors=TEXT, labelsize=max(9, w / 48))


def by_year(w):
    dpi = 100
    counts = Counter(s["year"] for s in SONGS)
    years = list(range(1970, 1980))
    fig, ax = plt.subplots(figsize=(w / dpi, w * 0.5625 / dpi), dpi=dpi)
    fig.patch.set_facecolor(BG)
    style(ax, w)
    vals = [counts.get(y, 0) for y in years]
    ax.bar([str(y) for y in years], vals, color=GOLD, zorder=3)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.08, str(v), ha="center", color=TEXT, fontsize=max(10, w / 40), fontweight="bold")
    ax.set_ylim(0, max(vals) + 1)
    ax.set_yticks([])
    ax.tick_params(axis="x", labelsize=max(8, w / 62))
    ax.set_title("30 70s Party Songs by Year-End Hot 100 Year", color=TEXT, fontsize=max(12, w / 36),
                 fontweight="bold", pad=14, loc="left")
    fig.tight_layout(pad=1.4)
    save(fig, "70s-party-songs", w)


def weeks(w):
    dpi = 100
    rows = sorted(LONG_RUNS, key=lambda r: (r[1], r[0]))
    fig, ax = plt.subplots(figsize=(w / dpi, w * 0.5625 / dpi), dpi=dpi)
    fig.patch.set_facecolor(BG)
    style(ax, w)
    ax.barh([r[0] for r in rows], [r[1] for r in rows], color=GOLD, zorder=3)
    for i, r in enumerate(rows):
        ax.text(r[1] + 0.15, i, str(r[1]), va="center", color=TEXT, fontsize=max(9, w / 52), fontweight="bold")
    ax.set_xlim(0, max(r[1] for r in rows) + 1.2)
    ax.set_xticks([])
    ax.tick_params(axis="y", labelsize=max(8, w / 58))
    ax.set_title("Party Songs: 3+ Weeks at #1", color=TEXT, fontsize=max(12, w / 38),
                 fontweight="bold", pad=14, loc="left")
    fig.tight_layout(pad=1.4)
    save(fig, "70s-party-songs-weeks", w)


if __name__ == "__main__":
    for w in (1200, 800, 400):
        by_year(w)
        weeks(w)
    print("charts written")
