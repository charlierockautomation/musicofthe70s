#!/usr/bin/env python3
"""One-off: render two charts for /blog/artists/ac-dc-songs/.
1. acdc-album-peaks: Billboard 200 peaks of the AC/DC albums released in the US in the 1970s.
2. acdc-uk-singles-peaks: UK Singles Chart peaks of the 1970s singles that charted there.
Numbers from Wikipedia's "AC/DC discography" albums and singles tables (checked 2026-11-23).
Outputs 1200w/800w/400w JPG + WebP like the other artist charts.
Run once, by hand: python3 scripts/generate_acdc_chart.py
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

ALBUMS = [("High Voltage\n1976", 146), ("Let There\nBe Rock\n1977", 154), ("Powerage\n1978", 133),
          ("If You Want\nBlood\n1978", 113), ("Highway\nto Hell\n1979", 17)]
UK = [("Rock 'n' Roll Damnation (1978)", 24), ("Whole Lotta Rosie (1977)", 36), ("Dirty Deeds Done Dirt Cheap (1976)", 47),
      ("High Voltage (1976)", 48), ("It's a Long Way to the Top (1976)", 55)]


def save(fig, stub, w):
    jpg = OUT / f"{stub}-{w}w.jpg" if w == 1200 else SRCSET / f"{stub}-{w}w.jpg"
    fig.savefig(jpg, format="jpg", facecolor=BG)
    fig.savefig(SRCSET / f"{stub}-{w}w.webp", format="webp", facecolor=BG)
    plt.close(fig)


def albums(w):
    dpi = 100
    fig, ax = plt.subplots(figsize=(w / dpi, w * 0.5625 / dpi), dpi=dpi)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    xs = range(len(ALBUMS))
    heights = [201 - pk for _, pk in ALBUMS]
    colors = [GOLD if pk <= 20 else WARM for _, pk in ALBUMS]
    ax.bar(xs, heights, color=colors, zorder=3, width=0.62)
    for x, (_, pk), h in zip(xs, ALBUMS, heights):
        ax.text(x, h + 4, f"No. {pk}", ha="center", va="bottom", color=TEXT, fontsize=max(8, w / 95), fontweight="bold")
    ax.set_xticks(list(xs))
    ax.set_xticklabels([a[0] for a in ALBUMS], color=TEXT, fontsize=max(6, w / 120))
    ax.set_ylim(0, 225)
    ax.set_yticks([])
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(BORDER)
    ax.set_ylabel("Taller bar = higher peak", color=MUTED, fontsize=max(8, w / 115))
    ax.set_title("AC/DC Songs of the 70s: US Album Peaks" if w >= 800 else "AC/DC US Album Peaks", color=TEXT,
                 fontsize=max(11, w / 80), fontweight="bold", pad=14, loc="left")
    fig.tight_layout(pad=1.4)
    save(fig, "acdc-album-peaks", w)


def uk(w):
    dpi = 100
    fig, ax = plt.subplots(figsize=(w / dpi, w * 0.5625 / dpi), dpi=dpi)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    rows = list(reversed(UK))
    ys = range(len(rows))
    for y, (name, pk) in zip(ys, rows):
        c = GOLD if pk < 40 else WARM
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
    ax.set_xlabel("UK Singles Chart peak (right is higher)", color=MUTED, fontsize=max(8, w / 115))
    ax.set_title("AC/DC 70s Singles: UK Chart Peaks" if w >= 800 else "AC/DC 70s UK Peaks", color=TEXT,
                 fontsize=max(11, w / 80), fontweight="bold", pad=14, loc="left")
    fig.tight_layout(pad=1.4)
    save(fig, "acdc-uk-singles-peaks", w)


for w in (1200, 800, 400):
    albums(w)
    uk(w)
for stub in ("acdc-album-peaks", "acdc-uk-singles-peaks"):
    shutil.copy(OUT / f"{stub}-1200w.jpg", SRCSET / f"{stub}-1200w.jpg")
