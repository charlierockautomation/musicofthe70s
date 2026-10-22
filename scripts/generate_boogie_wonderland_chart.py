#!/usr/bin/env python3
"""One-off: render the chart-peaks lollipop for /blog/songs/mandy-barry-manilow/.
Peaks from the Wikipedia article on the song (checked 2026-10-22). Eleven 1974-75 peaks shown; the Westlife 2003 peaks sit in the page text.
Outputs 1200w/800w/400w JPG + WebP. Run once, by hand: python3 scripts/generate_ill_be_there_jackson_5_chart.py
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "images/blog"
SRCSET = OUT / "srcset"
BG, GOLD, TEXT, MUTED, BORDER = "#1a1a2e", "#f5a623", "#f0e6d3", "#9ca3af", "#2d3561"
STUB = "boogie-wonderland-peaks"
DATA = [("US Hot Soul Singles", 2), ("France (IFOP)", 2), ("Norway (VG-lista)", 2), ("UK Singles", 4), ("Belgium (Flanders)", 4), ("Netherlands (Top 40)", 4), ("Australia (Kent)", 5),
        ("Ireland (IRMA)", 5), ("US Cash Box Top 100", 5), ("US Billboard Hot 100", 6), ("New Zealand", 7), ("Sweden", 7), ("Finland", 10), ("Canada", 11), ("US Disco Top 80", 14)]
DATA.sort(key=lambda r: r[1])
plt.rcParams["font.family"] = "DejaVu Sans"


def render(w, mobile=False):
    """mobile=True: square crop with big type, for the phone <source> (text stays legible at ~335px wide)."""
    dpi = 100
    fs = (lambda base: w * 0.034) if mobile else (lambda base: base)
    fig, ax = plt.subplots(figsize=(w / dpi, (w if mobile else w * 0.5625) / dpi), dpi=dpi)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    rows = list(reversed(DATA))
    for y, (name, peak) in enumerate(rows):
        ax.hlines(y, 16, peak, color=BORDER, linewidth=max(2, w / 300), zorder=2)
        ax.plot(peak, y, "o", color=GOLD, markersize=(w * 0.03 if mobile else max(6, w / 110)), zorder=4)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], color=TEXT, fontsize=fs(max(8, w / 105)))
    ax.set_xlim(16, 0)
    ax.set_xticks([1, 5, 10, 15])
    ax.tick_params(colors=TEXT, labelsize=fs(max(8, w / 110)))
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(BORDER)
    ax.grid(axis="x", color=BORDER, linewidth=0.6, zorder=0)
    ax.set_xlabel("Right is higher" if mobile else "Peak position (right is higher)", color=MUTED, fontsize=fs(max(8, w / 115)) * (0.85 if mobile else 1))
    ax.set_title("Boogie Wonderland: Chart Peaks, 1979" if w >= 800 and not mobile else "Chart Peaks", color=TEXT,
                 fontsize=fs(max(11, w / 80)), fontweight="bold", pad=14, loc="left")
    fig.tight_layout(pad=1.4)
    stub = STUB + "-mobile" if mobile else STUB
    jpg = OUT / f"{stub}-{w}w.jpg" if w == 1200 and not mobile else SRCSET / f"{stub}-{w}w.jpg"
    fig.savefig(jpg, format="jpg", facecolor=BG)
    fig.savefig(SRCSET / f"{stub}-{w}w.webp", format="webp", facecolor=BG)
    plt.close(fig)


for w in (1200, 800, 400):
    render(w)
for w in (800, 400):
    render(w, mobile=True)
