#!/usr/bin/env python3
"""One-off: render the Hot 100 peaks chart for /blog/artists/gladys-knight-songs/.
Peaks of the 12 songs on the page, from each song's Wikipedia article (checked 2026-10-15).
Outputs 1200w/800w/400w JPG + WebP like the Barry Manilow chart.
Run once, by hand: python3 scripts/generate_helen_reddy_chart.py
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
STUB = "gladys-knight-peaks"

# (title, release year, Hot 100 peak)
DATA = [("Midnight Train to Georgia", 1973, 1), ("Neither One of Us", 1972, 2), ("Best Thing That Ever Happened to Me", 1974, 3),
        ("I've Got to Use My Imagination", 1973, 4), ("On and On", 1974, 5), ("If I Were Your Woman", 1970, 9),
        ("The Way We Were/Try to Remember", 1975, 11), ("I Don't Want to Do Wrong", 1971, 17),
        ("Daddy Could Swear, I Declare", 1973, 19), ("I Feel a Song (In My Heart)", 1974, 21), ("Part Time Love", 1975, 22),
        ("Where Peaceful Waters Flow", 1973, 28)]
plt.rcParams["font.family"] = "DejaVu Sans"


def render(w):
    dpi = 100
    fig, ax = plt.subplots(figsize=(w / dpi, w * 0.5625 / dpi), dpi=dpi)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    rows = list(reversed(DATA))
    for y, (name, yr, pk) in enumerate(rows):
        c = GOLD if pk == 1 else WARM
        ax.hlines(y, 30, pk, color=BORDER, linewidth=max(2, w / 300), zorder=2)
        ax.plot(pk, y, "o", color=c, markersize=max(6, w / 110), zorder=4)
        ax.text(pk - 0.9, y, f"#{pk}", color=c, va="center", ha="left", fontsize=max(7, w / 120), zorder=5)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([f"{r[0]} ({r[1]})" if w >= 800 else r[0] for r in rows], color=TEXT, fontsize=max(8, w / 105))
    ax.set_xlim(31, -3)
    ax.set_xticks([30, 25, 20, 15, 10, 5, 1])
    ax.tick_params(colors=TEXT, labelsize=max(8, w / 110))
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(BORDER)
    ax.grid(axis="x", color=BORDER, linewidth=0.6, zorder=0)
    ax.set_xlabel("Weekly Hot 100 peak (right is higher)", color=MUTED, fontsize=max(8, w / 115))
    ax.set_title("Gladys Knight Songs: Hot 100 Peaks" if w >= 800 else "Gladys Knight Peaks", color=TEXT,
                 fontsize=max(11, w / 80), fontweight="bold", pad=14, loc="left")
    fig.tight_layout(pad=1.4)
    jpg = OUT / f"{STUB}-{w}w.jpg" if w == 1200 else SRCSET / f"{STUB}-{w}w.jpg"
    fig.savefig(jpg, format="jpg", facecolor=BG)
    fig.savefig(SRCSET / f"{STUB}-{w}w.webp", format="webp", facecolor=BG)
    plt.close(fig)


for w in (1200, 800, 400):
    render(w)
shutil.copy(OUT / f"{STUB}-1200w.jpg", SRCSET / f"{STUB}-1200w.jpg")
