#!/usr/bin/env python3
"""One-off: render the chart-peaks lollipop for /blog/songs/weve-only-just-begun/ and resize its photos.
Peaks from the Wikipedia article on the song (checked 2026-10-20). Japan Oricon (71) is left to the table.
Outputs 1200w/800w/400w JPG + WebP. Run once, by hand: python3 scripts/generate_weve_only_just_begun_chart.py <greek-1975-source.jpg>
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
STUB = "weve-only-just-begun-peaks"
DATA = [("US Adult Contemporary", 1), ("US Cash Box Top 100", 1), ("Canada RPM Top Singles", 1), ("Canada RPM Adult Contemporary", 1),
        ("US Billboard Hot 100", 2), ("US Cash Box Radio Active Airplay", 3), ("Quebec (ADISQ)", 4), ("Australia", 6), ("UK Singles Chart", 28)]
plt.rcParams["font.family"] = "DejaVu Sans"


def render(w):
    dpi = 100
    fig, ax = plt.subplots(figsize=(w / dpi, w * 0.5625 / dpi), dpi=dpi)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    rows = list(reversed(DATA))
    for y, (name, peak) in enumerate(rows):
        ax.hlines(y, 30, peak, color=BORDER, linewidth=max(2, w / 300), zorder=2)
        ax.plot(peak, y, "o", color=GOLD, markersize=max(6, w / 110), zorder=4)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], color=TEXT, fontsize=max(8, w / 105))
    ax.set_xlim(30, -1)
    ax.set_xticks([28, 20, 10, 5, 1])
    ax.tick_params(colors=TEXT, labelsize=max(8, w / 110))
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(BORDER)
    ax.grid(axis="x", color=BORDER, linewidth=0.6, zorder=0)
    ax.set_xlabel("Peak position (right is higher)", color=MUTED, fontsize=max(8, w / 115))
    ax.set_title("We've Only Just Begun: Chart Peaks, 1970 to 1971" if w >= 800 else "Chart Peaks", color=TEXT,
                 fontsize=max(11, w / 80), fontweight="bold", pad=14, loc="left")
    fig.tight_layout(pad=1.4)
    jpg = OUT / f"{STUB}-{w}w.jpg" if w == 1200 else SRCSET / f"{STUB}-{w}w.jpg"
    fig.savefig(jpg, format="jpg", facecolor=BG)
    fig.savefig(SRCSET / f"{STUB}-{w}w.webp", format="webp", facecolor=BG)
    plt.close(fig)


def photo(src, stub):
    im = Image.open(src).convert("L" if Image.open(src).mode == "L" else "RGB")
    for w in (1200, 800, 400):
        h = round(im.height * w / im.width)
        r = im.resize((w, h), Image.LANCZOS)
        jpg = OUT / f"{stub}-{w}w.jpg" if w == 1200 else SRCSET / f"{stub}-{w}w.jpg"
        r.save(jpg, quality=80, optimize=True)
        r.save(SRCSET / f"{stub}-{w}w.webp", quality=78)


for w in (1200, 800, 400):
    render(w)
if len(sys.argv) > 1:
    photo(sys.argv[1], "carpenters-greek-1975")
