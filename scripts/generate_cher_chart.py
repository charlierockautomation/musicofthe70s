#!/usr/bin/env python3
"""One-off: render two charts for /blog/artists/cher-songs/.
1. cher-singles-peaks: US Billboard Hot 100 peaks of 12 Cher singles of the 1970s.
2. cher-adult-contemporary-peaks: US Adult Contemporary peaks of the 9 that charted there.
Numbers from Wikipedia's "Cher singles discography" (checked 2026-11-23).
Outputs 1200w/800w/400w JPG + WebP like the other artist charts.
Run once, by hand: python3 scripts/generate_cher_chart.py
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

HOT = [("Gypsys, Tramps & Thieves (1971)", 1), ("Half-Breed (1973)", 1), ("Dark Lady (1974)", 1),
       ("Take Me Home (1979)", 8), ("The Way of Love (1972)", 7), ("Train of Thought (1974)", 27),
       ("Living in a House Divided (1972)", 22), ("I Saw a Man... (1974)", 42), ("Don't Hide Your Love (1972)", 46),
       ("Wasn't It Good (1979)", 49), ("Hell on Wheels (1979)", 59), ("Pirate (1977)", 93)]
AC = [("The Way of Love (1972)", 2), ("Living in a House Divided (1972)", 2), ("Half-Breed (1973)", 3),
      ("Dark Lady (1974)", 3), ("I Saw a Man... (1974)", 3), ("Gypsys, Tramps & Thieves (1971)", 6),
      ("Train of Thought (1974)", 9), ("Don't Hide Your Love (1972)", 19), ("Take Me Home (1979)", 19)]


def save(fig, stub, w):
    jpg = OUT / f"{stub}-{w}w.jpg" if w == 1200 else SRCSET / f"{stub}-{w}w.jpg"
    fig.savefig(jpg, format="jpg", facecolor=BG)
    fig.savefig(SRCSET / f"{stub}-{w}w.webp", format="webp", facecolor=BG)
    plt.close(fig)


def lollipop(w, data, stub, title_long, title_short, xlabel, xmax, ticks, gold_cut):
    dpi = 100
    fig, ax = plt.subplots(figsize=(w / dpi, w * 0.5625 / dpi), dpi=dpi)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    rows = list(reversed(data))
    ys = range(len(rows))
    for y, (name, pk) in zip(ys, rows):
        c = GOLD if pk <= gold_cut else WARM
        ax.hlines(y, xmax + 1, pk, color=c, linewidth=max(2, w / 300), zorder=3)
        ax.plot(pk, y, "o", color=c, markersize=max(6, w / 110), zorder=4)
        ax.text(pk - xmax * 0.02, y, f"No. {pk}", va="center", ha="left", color=TEXT, fontsize=max(8, w / 100), fontweight="bold")
    ax.set_yticks(list(ys))
    ax.set_yticklabels([r[0] for r in rows], color=TEXT, fontsize=max(6, w / 105))
    ax.set_xlim(xmax + 1, -xmax * 0.09)
    ax.set_xticks(ticks)
    ax.tick_params(colors=TEXT, labelsize=max(7, w / 110))
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(BORDER)
    ax.grid(axis="x", color=BORDER, linewidth=0.6, zorder=0)
    ax.set_xlabel(xlabel, color=MUTED, fontsize=max(8, w / 115))
    ax.set_title(title_long if w >= 800 else title_short, color=TEXT, fontsize=max(11, w / 80), fontweight="bold", pad=14, loc="left")
    fig.tight_layout(pad=1.4)
    save(fig, stub, w)


for w in (1200, 800, 400):
    lollipop(w, HOT, "cher-singles-peaks", "Cher Songs of the 70s: Hot 100 Peaks", "Cher 70s Hot 100 Peaks",
             "Billboard Hot 100 peak (right is higher)", 100, [100, 75, 50, 25, 10, 1], 1)
    lollipop(w, AC, "cher-adult-contemporary-peaks", "Cher 70s Singles: Adult Contemporary Peaks", "Cher 70s AC Peaks",
             "US Adult Contemporary peak (right is higher)", 20, [20, 15, 10, 5, 1], 3)
for stub in ("cher-singles-peaks", "cher-adult-contemporary-peaks"):
    shutil.copy(OUT / f"{stub}-1200w.jpg", SRCSET / f"{stub}-1200w.jpg")
