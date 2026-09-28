#!/usr/bin/env python3
"""One-off: render the featured bar chart for /blog/artists/70s-bands/.
Top 10 bands by solo... by GROUP year-end Hot 100 hits, 1970-1979, matching
the site's design tokens. Outputs 1200w/800w/400w JPG + WebP into
images/blog/ and images/blog/srcset/, same naming convention as 70s-singers.
Not part of the standing data-generation pipeline; run once, by hand.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "images/blog"
SRCSET = OUT / "srcset"
SRCSET.mkdir(parents=True, exist_ok=True)

BG = "#1a1a2e"
CARD = "#16213e"
GOLD = "#f5a623"
WARM = "#e8956d"
TEXT = "#f0e6d3"
MUTED = "#9ca3af"
BORDER = "#2d3561"

DATA = [
    ("Bee Gees", 12),
    ("Wings", 11),
    ("The Carpenters", 11),
    ("Chicago", 8),
    ("Electric Light Orchestra", 8),
    ("The Jackson 5", 7),
    ("Three Dog Night", 7),
    ("Gladys Knight & the Pips", 7),
    ("Earth, Wind & Fire", 7),
    ("War", 7),
]

plt.rcParams["font.family"] = "DejaVu Sans"

def render(width_px, out_stub):
    dpi = 100
    fig_w, fig_h = width_px / dpi, (width_px * 0.5625) / dpi
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    names = [d[0] for d in reversed(DATA)]
    vals = [d[1] for d in reversed(DATA)]
    colors = [GOLD if v == max(vals) else WARM for v in vals]

    bars = ax.barh(names, vals, color=colors, height=0.62, zorder=3)
    for bar, v in zip(bars, vals):
        ax.text(v + 0.15, bar.get_y() + bar.get_height() / 2, str(v),
                 va="center", ha="left", color=TEXT, fontsize=max(9, width_px / 90), fontweight="bold")

    ax.set_xlim(0, 13.8)
    ax.tick_params(colors=TEXT, labelsize=max(8, width_px / 105))
    for label in ax.get_yticklabels():
        label.set_color(TEXT)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(BORDER)
    ax.set_xticks(range(0, 14, 2))
    ax.grid(axis="x", color=BORDER, linewidth=0.6, zorder=0)
    ax.set_xlabel("Year-end Hot 100 hits, 1970–1979", color=MUTED, fontsize=max(8, width_px / 115))
    title = "The Biggest 70s Bands, by the Charts" if width_px >= 800 else "The Biggest 70s Bands"
    ax.set_title(title, color=TEXT,
                 fontsize=max(11, width_px / 80), fontweight="bold", pad=14, loc="left")

    fig.tight_layout(pad=1.4)
    jpg = SRCSET / f"{out_stub}-{width_px}w.jpg" if width_px != 1200 else OUT / f"{out_stub}-{width_px}w.jpg"
    webp = SRCSET / f"{out_stub}-{width_px}w.webp"
    fig.savefig(jpg, format="jpg", facecolor=BG)
    fig.savefig(webp, format="webp", facecolor=BG)
    plt.close(fig)
    return jpg, webp

for w in (1200, 800, 400):
    j, wp = render(w, "70s-bands")
    print(j, j.stat().st_size, wp, wp.stat().st_size)

# Also drop a copy of the 1200w jpg into srcset/ (og:image + srcset both reference it,
# matching how 70s-singers-1200w.jpg exists in both images/blog/ and images/blog/srcset/)
import shutil
shutil.copy(OUT / "70s-bands-1200w.jpg", SRCSET / "70s-bands-1200w.jpg")
