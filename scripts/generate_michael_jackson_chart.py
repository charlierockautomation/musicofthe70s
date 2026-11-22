#!/usr/bin/env python3
"""One-off: render two charts for /blog/artists/michael-jackson-songs/.
1. michael-jackson-singles-peaks: weekly Hot 100 peaks of ten 1970s solo singles.
2. michael-jackson-album-peaks: Billboard 200 peaks of the five 1970s solo studio albums.
Numbers from Wikipedia's "Michael Jackson singles discography" and "albums discography" (checked 2026-11-21).
Outputs 1200w/800w/400w JPG + WebP like the other artist charts.
Run once, by hand: python3 scripts/generate_michael_jackson_chart.py
"""
import shutil
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "images/blog"
SRCSET = OUT / "srcset"
BG, GOLD, WARM, TEXT, MUTED, BORDER = "#1a1a2e", "#f5a623", "#e8956d", "#f0e6d3", "#9ca3af", "#2d3561"
plt.rcParams["font.family"] = "DejaVu Sans"

SINGLES = [("Ben (1972)", 1), ("Don't Stop 'Til You Get Enough (1979)", 1), ("Rock with You (1979)", 1),
           ("Rockin' Robin (1972)", 2), ("Got to Be There (1971)", 4), ("Off the Wall (1979)", 10),
           ("I Wanna Be Where You Are (1972)", 16), ("Just a Little Bit of You (1975)", 23),
           ("With a Child's Heart (1973)", 50), ("We're Almost There (1975)", 54)]
ALBUMS = [("Got to Be\nThere\n1972", 14), ("Ben\n1972", 5), ("Music & Me\n1973", 92),
          ("Forever,\nMichael\n1975", 101), ("Off the Wall\n1979", 3)]


def save(fig, stub, w):
    jpg = OUT / f"{stub}-{w}w.jpg" if w == 1200 else SRCSET / f"{stub}-{w}w.jpg"
    fig.savefig(jpg, format="jpg", facecolor=BG)
    fig.savefig(SRCSET / f"{stub}-{w}w.webp", format="webp", facecolor=BG)
    plt.close(fig)


def singles(w):
    dpi = 100
    fig, ax = plt.subplots(figsize=(w / dpi, w * 0.5625 / dpi), dpi=dpi)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    rows = list(reversed(SINGLES))
    ys = range(len(rows))
    for y, (name, pk) in zip(ys, rows):
        c = GOLD if pk <= 10 else WARM
        ax.hlines(y, 101, pk, color=c, linewidth=max(2, w / 300), zorder=3)
        ax.plot(pk, y, "o", color=c, markersize=max(6, w / 110), zorder=4)
        ax.text(pk - 2.5, y, f"No. {pk}", va="center", ha="left", color=TEXT, fontsize=max(8, w / 100), fontweight="bold")
    ax.set_yticks(list(ys))
    ax.set_yticklabels([r[0] for r in rows], color=TEXT, fontsize=max(7, w / 105))
    ax.set_xlim(101, -8)
    ax.set_xticks([100, 75, 50, 40, 25, 10, 1])
    ax.tick_params(colors=TEXT, labelsize=max(7, w / 110))
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(BORDER)
    ax.grid(axis="x", color=BORDER, linewidth=0.6, zorder=0)
    ax.set_xlabel("Weekly Billboard Hot 100 peak (right is higher)", color=MUTED, fontsize=max(8, w / 115))
    ax.set_title("Michael Jackson Songs of the 70s: Hot 100 Peaks" if w >= 800 else "MJ 70s Hot 100 Peaks", color=TEXT,
                 fontsize=max(11, w / 80), fontweight="bold", pad=14, loc="left")
    fig.tight_layout(pad=1.4)
    save(fig, "michael-jackson-singles-peaks", w)


def albums(w):
    dpi = 100
    fig, ax = plt.subplots(figsize=(w / dpi, w * 0.5625 / dpi), dpi=dpi)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    xs = range(len(ALBUMS))
    heights = [201 - pk for _, pk in ALBUMS]
    colors = [GOLD if pk <= 10 else WARM for _, pk in ALBUMS]
    ax.bar(xs, heights, color=colors, zorder=3, width=0.62)
    for x, (_, pk), h in zip(xs, ALBUMS, heights):
        ax.text(x, h + 4, f"No. {pk}", ha="center", va="bottom", color=TEXT, fontsize=max(8, w / 95), fontweight="bold")
    ax.set_xticks(list(xs))
    ax.set_xticklabels([a[0] for a in ALBUMS], color=TEXT, fontsize=max(6, w / 125))
    ax.set_ylim(0, 225)
    ax.set_yticks([])
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(BORDER)
    ax.set_ylabel("Taller bar = higher peak", color=MUTED, fontsize=max(8, w / 115))
    ax.set_title("Michael Jackson Solo Albums: Billboard 200 Peaks, 1972 to 1979" if w >= 800 else "MJ Solo Album Peaks",
                 color=TEXT, fontsize=max(11, w / 80), fontweight="bold", pad=14, loc="left")
    fig.tight_layout(pad=1.4)
    save(fig, "michael-jackson-album-peaks", w)


for w in (1200, 800, 400):
    singles(w)
    albums(w)
for stub in ("michael-jackson-singles-peaks", "michael-jackson-album-peaks"):
    shutil.copy(OUT / f"{stub}-1200w.jpg", SRCSET / f"{stub}-1200w.jpg")
