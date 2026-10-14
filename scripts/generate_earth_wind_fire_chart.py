#!/usr/bin/env python3
"""One-off: render the Hot 100 peaks chart for /blog/artists/earth-wind-and-fire-songs/.
Weekly Hot 100 peaks of the 12 songs on the page, from each song's Wikipedia article
(checked 2026-10-14). Outputs 1200w/800w/400w JPG + WebP like the 70s-bands chart.
Run once, by hand: python3 scripts/generate_earth_wind_fire_chart.py
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
STUB = "earth-wind-and-fire-peaks"

DATA = [("Shining Star", 1), ("After the Love Has Gone", 2), ("Sing a Song", 5), ("Boogie Wonderland", 6),
        ("September", 8), ("Got to Get You into My Life", 9), ("Getaway", 12), ("That's the Way of the World", 12),
        ("Serpentine Fire", 13), ("Saturday Nite", 21), ("Fantasy", 32), ("Can't Hide Love", 39)]
plt.rcParams["font.family"] = "DejaVu Sans"


def render(w):
    dpi = 100
    fig, ax = plt.subplots(figsize=(w / dpi, w * 0.5625 / dpi), dpi=dpi)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    rows = list(reversed(DATA))
    ys = range(len(rows))
    for y, (name, pk) in zip(ys, rows):
        c = GOLD if pk == 1 else WARM
        ax.hlines(y, 42, pk, color=c, linewidth=max(2, w / 300), zorder=3)
        ax.plot(pk, y, "o", color=c, markersize=max(6, w / 110), zorder=4)
        ax.text(pk - 1.2, y, f"#{pk}", va="center", ha="left", color=TEXT, fontsize=max(8, w / 100), fontweight="bold")
    ax.set_yticks(list(ys))
    ax.set_yticklabels([r[0] for r in rows], color=TEXT, fontsize=max(8, w / 105))
    ax.set_xlim(42, -4)
    ax.set_xticks([40, 30, 20, 10, 1])
    ax.tick_params(colors=TEXT, labelsize=max(8, w / 110))
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(BORDER)
    ax.grid(axis="x", color=BORDER, linewidth=0.6, zorder=0)
    ax.set_xlabel("Weekly Billboard Hot 100 peak (right is higher)", color=MUTED, fontsize=max(8, w / 115))
    ax.set_title("Earth, Wind & Fire Songs: Hot 100 Peaks" if w >= 800 else "EWF Hot 100 Peaks", color=TEXT,
                 fontsize=max(11, w / 80), fontweight="bold", pad=14, loc="left")
    fig.tight_layout(pad=1.4)
    jpg = OUT / f"{STUB}-{w}w.jpg" if w == 1200 else SRCSET / f"{STUB}-{w}w.jpg"
    fig.savefig(jpg, format="jpg", facecolor=BG)
    fig.savefig(SRCSET / f"{STUB}-{w}w.webp", format="webp", facecolor=BG)
    plt.close(fig)


for w in (1200, 800, 400):
    render(w)
shutil.copy(OUT / f"{STUB}-1200w.jpg", SRCSET / f"{STUB}-1200w.jpg")
