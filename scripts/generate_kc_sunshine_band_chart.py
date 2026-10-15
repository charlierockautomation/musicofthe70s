#!/usr/bin/env python3
"""One-off: render the Hot 100 peaks chart for /blog/artists/kc-and-the-sunshine-band-songs/.
Peaks of the 12 songs on the page, from each song's Wikipedia article or the band's discography article (checked 2026-10-15).
Outputs 1200w/800w/400w JPG + WebP like the Barry Manilow chart.
Run once, by hand: python3 scripts/generate_kc_sunshine_band_chart.py
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
STUB = "kc-sunshine-band-peaks"

# (title, release year, Hot 100 peak)
DATA = [("Get Down Tonight", 1975, 1), ("That's the Way (I Like It)", 1975, 1), ("(Shake, Shake, Shake) Shake Your Booty", 1976, 1),
        ("I'm Your Boogie Man", 1977, 1), ("Please Don't Go", 1979, 1), ("Keep It Comin' Love", 1977, 2),
        ("Boogie Shoes", 1978, 35), ("It's the Same Old Song", 1978, 35), ("I Like to Do It", 1976, 37),
        ("Wrap Your Arms Around Me", 1977, 48), ("Do You Wanna Go Party", 1979, 50), ("Queen of Clubs", 1974, 66)]
plt.rcParams["font.family"] = "DejaVu Sans"


def render(w):
    dpi = 100
    fig, ax = plt.subplots(figsize=(w / dpi, w * 0.5625 / dpi), dpi=dpi)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    rows = list(reversed(DATA))
    for y, (name, yr, pk) in enumerate(rows):
        c = GOLD if pk == 1 else WARM
        ax.hlines(y, 72, pk, color=BORDER, linewidth=max(2, w / 300), zorder=2)
        ax.plot(pk, y, "o", color=c, markersize=max(6, w / 110), zorder=4)
        ax.text(pk - 1.5, y, f"#{pk}", color=c, va="center", ha="left", fontsize=max(7, w / 120), zorder=5)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([f"{r[0]} ({r[1]})" if w >= 800 else r[0] for r in rows], color=TEXT, fontsize=max(8, w / 105))
    ax.set_xlim(73, -6)
    ax.set_xticks([70, 60, 50, 40, 30, 20, 10, 1])
    ax.tick_params(colors=TEXT, labelsize=max(8, w / 110))
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(BORDER)
    ax.grid(axis="x", color=BORDER, linewidth=0.6, zorder=0)
    ax.set_xlabel("Weekly Hot 100 peak (right is higher)", color=MUTED, fontsize=max(8, w / 115))
    ax.set_title("KC and the Sunshine Band Songs: Hot 100 Peaks" if w >= 800 else "KC Sunshine Band Peaks", color=TEXT,
                 fontsize=max(11, w / 80), fontweight="bold", pad=14, loc="left")
    fig.tight_layout(pad=1.4)
    jpg = OUT / f"{STUB}-{w}w.jpg" if w == 1200 else SRCSET / f"{STUB}-{w}w.jpg"
    fig.savefig(jpg, format="jpg", facecolor=BG)
    fig.savefig(SRCSET / f"{STUB}-{w}w.webp", format="webp", facecolor=BG)
    plt.close(fig)


for w in (1200, 800, 400):
    render(w)
shutil.copy(OUT / f"{STUB}-1200w.jpg", SRCSET / f"{STUB}-1200w.jpg")
