#!/usr/bin/env python3
"""One-off: render the in-body 'weeks at number one' chart for
/blog/artists/70s-bands/. Not part of the standing pipeline, run once by hand.
Network access to Wikimedia Commons is blocked in this environment, so this
self-made data chart stands in for a sourced photo as the post's required
second in-body image (real data, same chart style as the featured image).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRCSET = ROOT / "images/blog/srcset"
SRCSET.mkdir(parents=True, exist_ok=True)

BG = "#1a1a2e"
GOLD = "#f5a623"
WARM = "#e8956d"
TEXT = "#f0e6d3"
MUTED = "#9ca3af"
BORDER = "#2d3561"

DATA = [
    ("Bee Gees", 27),
    ("Wings", 13),
    ("The Jackson 5", 10),
    ("Three Dog Night", 9),
    ("The Carpenters", 7),
    ("Chic", 7),
]

def render(width_px):
    dpi = 100
    fig_w, fig_h = width_px / dpi, (width_px * 0.5625) / dpi
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    names = [d[0] for d in reversed(DATA)]
    vals = [d[1] for d in reversed(DATA)]
    colors = [GOLD if v == max(vals) else WARM for v in vals]

    bars = ax.barh(names, vals, color=colors, height=0.58, zorder=3)
    for bar, v in zip(bars, vals):
        ax.text(v + 0.4, bar.get_y() + bar.get_height() / 2, str(v),
                 va="center", ha="left", color=TEXT, fontsize=max(9, width_px / 90), fontweight="bold")

    ax.set_xlim(0, 31)
    ax.tick_params(colors=TEXT, labelsize=max(8, width_px / 100))
    for label in ax.get_yticklabels():
        label.set_color(TEXT)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(BORDER)
    ax.grid(axis="x", color=BORDER, linewidth=0.6, zorder=0)
    ax.set_xlabel("Weeks at No. 1 on the Hot 100, 1970–1979", color=MUTED, fontsize=max(8, width_px / 115))
    ax.set_title("70s Bands With the Most Weeks at No. 1", color=TEXT,
                 fontsize=max(10, width_px / 75), fontweight="bold", pad=12, loc="left")

    fig.tight_layout(pad=1.3)
    jpg = SRCSET / f"70s-bands-weeks-{width_px}w.jpg"
    webp = SRCSET / f"70s-bands-weeks-{width_px}w.webp"
    fig.savefig(jpg, format="jpg", facecolor=BG)
    fig.savefig(webp, format="webp", facecolor=BG)
    plt.close(fig)
    return jpg, webp

for w in (800, 400):
    j, wp = render(w)
    print(j, j.stat().st_size, wp, wp.stat().st_size)
