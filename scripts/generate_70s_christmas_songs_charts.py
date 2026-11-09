#!/usr/bin/env python3
"""Render the two charts on /blog/songs/70s-christmas-songs/ from SONGS in
scripts/generate_70s_christmas_songs_page.py.

1. 70s-christmas-songs (featured): timeline of the 14 songs by release year.
2. 70s-christmas-songs-years: songs per year, 1970 to 1979.

Outputs 1200w/800w/400w JPG + WebP. Run: python3 scripts/generate_70s_christmas_songs_charts.py
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_70s_christmas_songs_page import SONGS, YEARS  # noqa: E402

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


def timeline(w):
    dpi = 100
    rows = list(reversed(SONGS))
    fig, ax = plt.subplots(figsize=(w / dpi, w * 0.5625 / dpi), dpi=dpi)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(BORDER)
    labels = [r[0] if len(r[0]) <= 30 else r[0][:28] + "..." for r in rows]
    ys = range(len(rows))
    ax.hlines(ys, 1969.6, [r[2] for r in rows], color=BORDER, lw=1, zorder=1)
    ax.scatter([r[2] for r in rows], ys, color=GOLD, s=w / 18, zorder=3)
    ax.set_yticks(list(ys))
    ax.set_yticklabels(labels)
    ax.set_xticks(range(1970, 1980))
    ax.set_xlim(1969.6, 1979.5)
    ax.tick_params(colors=TEXT, labelsize=max(6, w / 85))
    ax.tick_params(axis="y", length=0)
    fig.suptitle("14 Christmas Songs by Release Year, 1970 to 1979", color=TEXT,
                 fontsize=max(10, w / 44), fontweight="bold", x=0.02, ha="left")
    fig.tight_layout(pad=1.2, rect=(0, 0, 1, 0.95))
    save(fig, "70s-christmas-songs", w)


def per_year(w):
    dpi = 100
    yrs = list(range(1970, 1980))
    vals = [len(YEARS.get(y, [])) for y in yrs]
    fig, ax = plt.subplots(figsize=(w / dpi, w * 0.5625 / dpi), dpi=dpi)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(BORDER)
    ax.bar([str(y) for y in yrs], vals, color=GOLD, zorder=3)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.08, str(v), ha="center", color=TEXT, fontsize=max(9, w / 52), fontweight="bold")
    ax.set_yticks([])
    ax.tick_params(colors=TEXT, labelsize=max(8, w / 60))
    ax.set_ylim(0, max(vals) + 1)
    ax.set_title("Songs on This List per Year", color=TEXT, fontsize=max(12, w / 38),
                 fontweight="bold", pad=14, loc="left")
    fig.tight_layout(pad=1.4)
    save(fig, "70s-christmas-songs-years", w)


if __name__ == "__main__":
    for w in (1200, 800, 400):
        timeline(w)
        per_year(w)
    print("charts written")
