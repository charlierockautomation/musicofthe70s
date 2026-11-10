#!/usr/bin/env python3
"""One-off: render the two charts for /blog/artists/70s-rock-bands/ (build queue step 4.3).
Counts come from the step 4.3 row builder (.base/step-4.3/rows.py), which reads
data/billboard/year_end_hot100.json with credit variants merged.
  70s-rock-bands       featured: every rock band with 4+ year-end Hot 100 hits
  70s-rock-bands-styles  year-end hits by rock style
Outputs 1200w (featured only) / 800w / 400w JPG + WebP, site design tokens. Run by hand.
"""
import shutil
import sys
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / ".base/step-4.3"))
from rows import build, STYLE_NAME  # noqa: E402

OUT = ROOT / "images/blog"
SRCSET = OUT / "srcset"
BG, GOLD, WARM, TEXT, MUTED, BORDER = "#1a1a2e", "#f5a623", "#e8956d", "#f0e6d3", "#9ca3af", "#2d3561"
plt.rcParams["font.family"] = "DejaVu Sans"

rows = build()
TOP = [(x["band"], x["count"]) for x in rows if x["count"] >= 4]
styles = Counter()
for x in rows:
    styles[STYLE_NAME[x["style"]]] += x["count"]
STY = sorted(styles.items(), key=lambda kv: -kv[1])


def render(data, width_px, stub, title_long, title_short, xlabel):
    dpi = 100
    fig, ax = plt.subplots(figsize=(width_px / dpi, width_px * 0.5625 / dpi), dpi=dpi)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    names = [d[0] for d in reversed(data)]
    vals = [d[1] for d in reversed(data)]
    bars = ax.barh(names, vals, color=[GOLD if v == max(vals) else WARM for v in vals], height=0.62, zorder=3)
    for bar, v in zip(bars, vals):
        ax.text(v + max(vals) * 0.012, bar.get_y() + bar.get_height() / 2, str(v), va="center", ha="left",
                color=TEXT, fontsize=max(8, width_px / 95), fontweight="bold")
    ax.set_xlim(0, max(vals) * 1.12)
    ax.tick_params(colors=TEXT, labelsize=max(7, width_px / 110))
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(BORDER)
    ax.grid(axis="x", color=BORDER, linewidth=0.6, zorder=0)
    ax.set_xlabel(xlabel, color=MUTED, fontsize=max(8, width_px / 115))
    ax.set_title(title_long if width_px >= 800 else title_short, color=TEXT,
                 fontsize=max(11, width_px / 80), fontweight="bold", pad=14, loc="left")
    fig.tight_layout(pad=1.4)
    jpg = (OUT if width_px == 1200 else SRCSET) / f"{stub}-{width_px}w.jpg"
    webp = SRCSET / f"{stub}-{width_px}w.webp"
    fig.savefig(jpg, format="jpg", facecolor=BG)
    fig.savefig(webp, format="webp", facecolor=BG)
    plt.close(fig)
    print(jpg, webp)


for w in (1200, 800, 400):
    render(TOP, w, "70s-rock-bands", "70s Rock Bands With the Most Year-End Hits", "Most Year-End Hits",
           "Billboard year-end Hot 100 hits, 1970 to 1979")
shutil.copy(OUT / "70s-rock-bands-1200w.jpg", SRCSET / "70s-rock-bands-1200w.jpg")
for w in (800, 400):
    render(STY, w, "70s-rock-bands-styles", "Year-End Hits by Rock Style", "Hits by Rock Style",
           "Billboard year-end Hot 100 hits by rock bands, 1970 to 1979")
print(TOP)
print(STY)
