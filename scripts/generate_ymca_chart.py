#!/usr/bin/env python3
"""One-off: render two charts for /blog/songs/song-ymca/.
1. ymca-song-chart-peaks: peak positions (US Hot 100 weekly, UK Singles, US year-end 1979).
2. ymca-song-weeks-on-chart: weeks on the US Hot 100 vs the UK chart.
Sources: LOC blog (US No. 2), SPIN oral history (26 weeks US), Official Charts Company (UK No. 1, 16 weeks),
data/billboard/year_end_hot100.json (year-end No. 8). Checked 2026-11-24.
Run once, by hand: python3 scripts/generate_ymca_chart.py
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
plt.rcParams["font.family"] = "DejaVu Sans"

PEAKS = [("UK Singles Chart, weekly peak", 1), ("US Hot 100, weekly peak", 2), ("US Billboard year-end 1979 rank", 8)]
WEEKS = [("US Hot 100", 26), ("UK Singles Chart", 16)]


def save(fig, stub, w):
    jpg = OUT / f"{stub}-{w}w.jpg" if w == 1200 else SRCSET / f"{stub}-{w}w.jpg"
    fig.savefig(jpg, format="jpg", facecolor=BG)
    fig.savefig(SRCSET / f"{stub}-{w}w.webp", format="webp", facecolor=BG)
    plt.close(fig)


def style(ax, w, title_long, title_short, xlabel):
    ax.set_facecolor(BG)
    ax.tick_params(colors=TEXT, labelsize=max(7, w / 100))
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(BORDER)
    ax.grid(axis="x", color=BORDER, linewidth=0.6, zorder=0)
    ax.set_xlabel(xlabel, color=MUTED, fontsize=max(8, w / 115))
    ax.set_title(title_long if w >= 800 else title_short, color=TEXT, fontsize=max(11, w / 80), fontweight="bold", pad=14, loc="left")


def peaks(w):
    fig, ax = plt.subplots(figsize=(w / 100, w * 0.5625 / 100), dpi=100)
    fig.patch.set_facecolor(BG)
    rows = list(reversed(PEAKS))
    for y, (name, pk) in enumerate(rows):
        c = GOLD if pk == 1 else WARM
        ax.hlines(y, 11, pk, color=c, linewidth=max(2, w / 300), zorder=3)
        ax.plot(pk, y, "o", color=c, markersize=max(6, w / 110), zorder=4)
        ax.text(pk - 0.25, y, f"No. {pk}", va="center", ha="left", color=TEXT, fontsize=max(8, w / 100), fontweight="bold")
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], color=TEXT, fontsize=max(7, w / 95))
    ax.set_xlim(11, -1)
    ax.set_xticks([10, 8, 6, 4, 2, 1])
    style(ax, w, "Y.M.C.A. by Village People: Chart Peaks", "YMCA Chart Peaks", "Chart position (right is higher)")
    fig.tight_layout(pad=1.4)
    save(fig, "ymca-song-chart-peaks", w)


def weeks(w):
    fig, ax = plt.subplots(figsize=(w / 100, w * 0.5625 / 100), dpi=100)
    fig.patch.set_facecolor(BG)
    rows = list(reversed(WEEKS))
    for y, (name, n) in enumerate(rows):
        ax.barh(y, n, color=GOLD if n == 26 else WARM, height=0.5, zorder=3)
        ax.text(n + 0.5, y, f"{n} weeks", va="center", ha="left", color=TEXT, fontsize=max(8, w / 100), fontweight="bold")
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], color=TEXT, fontsize=max(8, w / 95))
    ax.set_xlim(0, 31)
    style(ax, w, "Y.M.C.A.: Weeks on the Chart", "YMCA Weeks on Chart", "Weeks on the chart")
    fig.tight_layout(pad=1.4)
    save(fig, "ymca-song-weeks-on-chart", w)


for w in (1200, 800, 400):
    peaks(w)
    weeks(w)
for stub in ("ymca-song-chart-peaks", "ymca-song-weeks-on-chart"):
    shutil.copy(OUT / f"{stub}-1200w.jpg", SRCSET / f"{stub}-1200w.jpg")
