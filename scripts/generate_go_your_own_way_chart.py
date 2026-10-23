#!/usr/bin/env python3
"""One-off: render the chart-peaks lollipop for /blog/songs/go-your-own-way/.
Peaks from the Wikipedia article on the song (checked 2026-10-23). Fourteen 1977 peaks shown.
Outputs 1200w/800w/400w JPG + WebP. Run once, by hand: python3 scripts/generate_go_your_own_way_chart.py
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
STUB = "go-your-own-way-peaks"
DATA = [("Netherlands Dutch Top 40", 1), ("Netherlands Single Top 100", 1), ("Belgium (Flanders)", 1), ("South Africa (Springbok)", 4), ("US Radio & Records Top 40", 8),
        ("US Billboard Hot 100", 10), ("US Cash Box Top 100", 10), ("US Record World", 10), ("Canada Top Singles (RPM)", 11), ("West Germany (GfK)", 11),
        ("Australia (Kent)", 20), ("New Zealand", 23), ("UK Singles", 38), ("US Adult Contemporary", 45)]
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
        ax.hlines(y, 48, peak, color=BORDER, linewidth=max(2, w / 300), zorder=2)
        ax.plot(peak, y, "o", color=GOLD, markersize=(w * 0.03 if mobile else max(6, w / 110)), zorder=4)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], color=TEXT, fontsize=fs(max(8, w / 105)))
    ax.set_xlim(48, -1)
    ax.set_xticks([1, 10, 20, 30, 40])
    ax.tick_params(colors=TEXT, labelsize=fs(max(8, w / 110)))
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(BORDER)
    ax.grid(axis="x", color=BORDER, linewidth=0.6, zorder=0)
    ax.set_xlabel("Right is higher" if mobile else "Peak position (right is higher)", color=MUTED, fontsize=fs(max(8, w / 115)) * (0.85 if mobile else 1))
    ax.set_title("Go Your Own Way: Chart Peaks, 1977" if w >= 800 and not mobile else "Chart Peaks", color=TEXT,
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
