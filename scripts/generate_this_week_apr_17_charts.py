#!/usr/bin/env python3
"""Render the two charts on /blog/trivia/april-17-in-music-history/ from
scripts/generate_this_week_apr_17_page.py (the weekly Hot 100 file is the source of truth).

1. april-17-in-music-history (featured): total weeks at number one, one bar per year.
2. april-17-in-music-history-runs: each song's run as boxes, April 17 week in gold.

Outputs 1200w/800w/400w JPG + WebP. Run: python3 scripts/generate_this_week_apr_17_charts.py
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_this_week_apr_17_page import SONGS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "images/blog"
SRCSET = OUT / "srcset"
STUB = "april-17-in-music-history"
BG, GOLD, TEXT, MUTED, BORDER = "#1a1a2e", "#f5a623", "#f0e6d3", "#9ca3af", "#2d3561"
plt.rcParams["font.family"] = "DejaVu Sans"


def save(fig, stub, w):
    jpg = OUT / f"{stub}-{w}w.jpg" if w == 1200 else SRCSET / f"{stub}-{w}w.jpg"
    fig.savefig(jpg, format="jpg", facecolor=BG)
    fig.savefig(SRCSET / f"{stub}-{w}w.webp", format="webp", facecolor=BG)
    plt.close(fig)


def label(s):
    t = s["title"].split(" / ")[0]
    return f'{s["year"]}  {t}'


def style(ax, w):
    ax.set_facecolor(BG)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(BORDER)
    ax.tick_params(colors=TEXT, labelsize=max(9, w / 48))


def totals(w):
    dpi = 100
    rows = list(reversed(SONGS))
    fig, ax = plt.subplots(figsize=(w / dpi, w * 0.5625 / dpi), dpi=dpi)
    fig.patch.set_facecolor(BG)
    style(ax, w)
    ax.barh([label(s) for s in rows], [s["total"] for s in rows], color=GOLD, zorder=3)
    for i, s in enumerate(rows):
        ax.text(s["total"] + 0.15, i, str(s["total"]), va="center", color=TEXT,
                fontsize=max(9, w / 52), fontweight="bold")
    ax.set_xlim(0, max(s["total"] for s in rows) + 1)
    ax.set_xticks([])
    ax.tick_params(axis="y", labelsize=max(7, w / 62))
    fig.tight_layout(pad=1.4, rect=(0, 0, 1, 0.9))
    fig.text(0.02, 0.94, "Weeks at No. 1, Week of April 17", color=TEXT, fontsize=max(12, w / 38),
             fontweight="bold", ha="left", va="center")
    save(fig, STUB, w)


def runs(w):
    dpi = 100
    rows = list(reversed(SONGS))
    fig, ax = plt.subplots(figsize=(w / dpi, w * 0.5625 / dpi), dpi=dpi)
    fig.patch.set_facecolor(BG)
    style(ax, w)
    for i, s in enumerate(rows):
        for n, k in enumerate(s["offs"]):
            gold = n + 1 == s["pos"]
            ax.add_patch(Rectangle((k + 0.06, i - 0.36), 0.88, 0.72,
                                   facecolor=GOLD if gold else BORDER, edgecolor=BG, zorder=3))
    ax.set_xlim(0, 8.2)
    ax.set_ylim(-0.7, len(rows) - 0.3)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([label(s) for s in rows])
    ax.set_xticks([k + 0.5 for k in range(8)])
    ax.set_xticklabels([str(k + 1) for k in range(8)])
    ax.set_xlabel("Week of the run at No. 1", color=MUTED, fontsize=max(8, w / 60))
    ax.tick_params(axis="y", labelsize=max(7, w / 62))
    fig.tight_layout(pad=1.4, rect=(0, 0, 1, 0.9))
    fig.text(0.02, 0.94, "Where April 17 Fell in Each Run", color=TEXT, fontsize=max(12, w / 38),
             fontweight="bold", ha="left", va="center")
    save(fig, STUB + "-runs", w)


if __name__ == "__main__":
    for width in (1200, 800, 400):
        totals(width)
        runs(width)
    print("charts written")
