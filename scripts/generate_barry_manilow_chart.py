#!/usr/bin/env python3
"""One-off: render the Hot 100 versus Adult Contemporary peaks chart for /blog/artists/barry-manilow-songs/.
Peaks of the 12 songs on the page, from each song's Wikipedia article (checked 2026-10-14).
Outputs 1200w/800w/400w JPG + WebP like the 70s-bands chart.
Run once, by hand: python3 scripts/generate_barry_manilow_chart.py
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
STUB = "barry-manilow-peaks"

# (title, Hot 100 peak, Adult Contemporary peak)
DATA = [("Mandy", 1, 1), ("I Write the Songs", 1, 1), ("Looks Like We Made It", 1, 1), ("Can't Smile Without You", 3, 1),
        ("Could It Be Magic", 6, 4), ("Copacabana", 8, 6), ("Somewhere in the Night", 9, 4), ("Ships", 9, 4),
        ("Tryin' to Get the Feeling Again", 10, 1), ("Weekend in New England", 10, 1), ("It's a Miracle", 12, 1),
        ("Even Now", 19, 1)]
plt.rcParams["font.family"] = "DejaVu Sans"


def render(w):
    dpi = 100
    fig, ax = plt.subplots(figsize=(w / dpi, w * 0.5625 / dpi), dpi=dpi)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    rows = list(reversed(DATA))
    ys = range(len(rows))
    for y, (name, hot, ac) in zip(ys, rows):
        ax.hlines(y, hot, ac, color=BORDER, linewidth=max(2, w / 300), zorder=2)
        ax.plot(hot, y, "o", color=GOLD, markersize=max(6, w / 110), zorder=4, label="Hot 100" if y == 0 else None)
        ax.plot(ac, y, "s", color=WARM, markersize=max(5, w / 130), zorder=3, label="Adult Contemporary" if y == 0 else None)
    ax.set_yticks(list(ys))
    ax.set_yticklabels([r[0] for r in rows], color=TEXT, fontsize=max(8, w / 105))
    ax.set_xlim(21, -1)
    ax.set_xticks([20, 15, 10, 5, 1])
    ax.tick_params(colors=TEXT, labelsize=max(8, w / 110))
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(BORDER)
    ax.grid(axis="x", color=BORDER, linewidth=0.6, zorder=0)
    ax.set_xlabel("Peak position (right is higher)", color=MUTED, fontsize=max(8, w / 115))
    ax.set_title("Barry Manilow Songs: Hot 100 and Adult Contemporary Peaks" if w >= 800 else "Manilow Peaks", color=TEXT,
                 fontsize=max(11, w / 80), fontweight="bold", pad=14, loc="left")
    ax.legend(loc="upper left", bbox_to_anchor=(0.0, 0.97), frameon=False, labelcolor=TEXT, fontsize=max(8, w / 115))
    fig.tight_layout(pad=1.4)
    jpg = OUT / f"{STUB}-{w}w.jpg" if w == 1200 else SRCSET / f"{STUB}-{w}w.jpg"
    fig.savefig(jpg, format="jpg", facecolor=BG)
    fig.savefig(SRCSET / f"{STUB}-{w}w.webp", format="webp", facecolor=BG)
    plt.close(fig)


for w in (1200, 800, 400):
    render(w)
shutil.copy(OUT / f"{STUB}-1200w.jpg", SRCSET / f"{STUB}-1200w.jpg")
