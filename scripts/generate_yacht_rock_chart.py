#!/usr/bin/env python3
"""One-off: render two charts for /blog/genres/yacht-rock-songs/.
1. yacht-rock-songs-peaks: weekly Hot 100 peaks of the 16 songs (Wikipedia song and discography pages, checked 2026-11-21;
   Baby Come Back and What a Fool Believes No. 1 weeks match data/billboard/hot100_weekly.json).
2. yacht-rock-songs-year-end: Billboard year-end ranks of the 11 songs that made the site's year-end lists (data/billboard/year_end_hot100.json).
Outputs 1200w/800w/400w JPG + WebP like the other charts. Run once, by hand: python3 scripts/generate_yacht_rock_chart.py
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

PEAKS = [("Baby Come Back, Player (1977)", 1), ("What a Fool Believes, Doobie Brothers (1978)", 1),
         ("After the Love Has Gone, Earth, Wind & Fire (1979)", 2), ("Lowdown, Boz Scaggs (1976)", 3),
         ("Hold the Line, Toto (1978)", 5), ("Whenever I Call You Friend, Loggins (1978)", 5),
         ("Love Will Find a Way, Pablo Cruise (1978)", 6), ("What You Won't Do for Love, Caldwell (1978)", 9),
         ("Smoke from a Distant Fire, Sanford-Townsend (1977)", 9), ("Peg, Steely Dan (1977)", 11),
         ("This Is It, Kenny Loggins (1979)", 11), ("Takin' It to the Streets, Doobie Brothers (1976)", 13),
         ("Minute by Minute, Doobie Brothers (1978)", 14), ("Deacon Blues, Steely Dan (1977)", 19),
         ("FM (No Static at All), Steely Dan (1978)", 22), ("Kid Charlemagne, Steely Dan (1976)", 82)]
YEAR_END = [("Baby Come Back, Player (1978)", 7), ("What a Fool Believes, Doobie Brothers (1979)", 19),
            ("After the Love Has Gone, Earth, Wind & Fire (1979)", 38), ("Hold the Line, Toto (1979)", 44),
            ("Love Will Find a Way, Pablo Cruise (1978)", 44), ("Lowdown, Boz Scaggs (1976)", 49),
            ("What You Won't Do for Love, Caldwell (1979)", 59), ("Peg, Steely Dan (1978)", 62),
            ("Smoke from a Distant Fire, Sanford-Townsend (1977)", 67),
            ("Whenever I Call You Friend, Loggins (1978)", 83), ("Deacon Blues, Steely Dan (1978)", 100)]


def save(fig, stub, w):
    jpg = OUT / f"{stub}-{w}w.jpg" if w == 1200 else SRCSET / f"{stub}-{w}w.jpg"
    fig.savefig(jpg, format="jpg", facecolor=BG)
    fig.savefig(SRCSET / f"{stub}-{w}w.webp", format="webp", facecolor=BG)
    plt.close(fig)


def lollipop(w, data, stub, title_long, title_short, xlabel, xmax, ticks, gold_cut):
    dpi = 100
    fig, ax = plt.subplots(figsize=(w / dpi, w * 0.5625 / dpi), dpi=dpi)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    rows = list(reversed(data))
    ys = range(len(rows))
    for y, (name, v) in zip(ys, rows):
        c = GOLD if v <= gold_cut else WARM
        ax.hlines(y, xmax, v, color=c, linewidth=max(2, w / 300), zorder=3)
        ax.plot(v, y, "o", color=c, markersize=max(6, w / 110), zorder=4)
        ax.text(v - xmax * 0.025, y, f"{'No.' if stub.endswith('peaks') else 'Rank'} {v}", va="center", ha="left", color=TEXT, fontsize=max(7, w / 105), fontweight="bold")
    ax.set_yticks(list(ys))
    ax.set_yticklabels([r[0] for r in rows], color=TEXT, fontsize=max(6, w / 120))
    ax.set_xlim(xmax, -xmax * 0.1)
    ax.set_xticks(ticks)
    ax.tick_params(colors=TEXT, labelsize=max(7, w / 110))
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(BORDER)
    ax.grid(axis="x", color=BORDER, linewidth=0.6, zorder=0)
    ax.set_xlabel(xlabel, color=MUTED, fontsize=max(8, w / 115))
    ax.set_title(title_long if w >= 800 else title_short, color=TEXT, fontsize=max(11, w / 80), fontweight="bold", pad=14, loc="left")
    fig.tight_layout(pad=1.4)
    save(fig, stub, w)


for w in (1200, 800, 400):
    lollipop(w, PEAKS, "yacht-rock-songs-peaks", "Yacht Rock Songs of the 70s: Hot 100 Peaks", "Yacht Rock Hot 100 Peaks",
             "Weekly Billboard Hot 100 peak (right is higher)", 101, [100, 75, 50, 25, 10, 1], 10)
    lollipop(w, YEAR_END, "yacht-rock-songs-year-end", "Yacht Rock Songs on the Year-End Hot 100", "Yacht Rock Year-End Ranks",
             "Billboard year-end rank (right is higher)", 105, [100, 75, 50, 25, 10, 1], 25)
for stub in ("yacht-rock-songs-peaks", "yacht-rock-songs-year-end"):
    shutil.copy(OUT / f"{stub}-1200w.jpg", SRCSET / f"{stub}-1200w.jpg")
