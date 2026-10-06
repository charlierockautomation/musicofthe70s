#!/usr/bin/env python3
"""Reword year-end positions on the Top Songs of 1970-1979 pages.

On those pages "#N" almost always means the Year-End Hot 100 rank, but phrases
like "reached #9" or "hit #41" read as weekly chart peaks. This rewrites
"reached/hit/landed at/came in at/charted at #N" to "ranked #N" and, where the
sentence has no year-end qualifier, adds "on the YYYY year-end chart" after the
last number. Sentences about weekly #1s ("at #1 on the weekly Hot 100", "all
reached #1") are left alone. Applied identically to the body and FAQ schema.

Run: python3 scripts/reword_year_end_ranks.py [--apply]   (default: dry run)
"""
import glob
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NUM = re.compile(r"#\d+")


VERB = re.compile(r"\b(reached|hit|landed at|came in at|charted at|peaked at|climbed to|rose to|debuted at|entered at|finished at)(\s+)(#\d+)")
YE = re.compile(r"year-end|for the year|that year", re.I)


LANDED_AT = re.compile(r"\b([Ll])anded at (#\d+)")
LANDED_TITLE = re.compile(r'\blanded (\\?"[^"]+?\\?") at (#\d+)')
CHARTED = re.compile(r"\b(?:charted|followed)\b[^.#]*?(?:\bat|with [^#]*? at) #\d+")


def fix_sentence(s, year, in_run):
    """Returns (new_sentence, cites_rank, has_year_end_wording)."""
    if "weekly" in s or "first three singles" in s:
        return s, False, False
    out = LANDED_AT.sub(lambda m: ("R" if m.group(1) == "L" else "r") + "anked " + m.group(2), s)
    out = LANDED_TITLE.sub(lambda m: f"placed {m.group(1)} at {m.group(2)}", out)
    out = VERB.sub(lambda m: "ranked " + m.group(3), out)
    if out == s and not CHARTED.search(s):
        return s, False, False
    if not YE.search(out) and not in_run:
        last = list(NUM.finditer(out))[-1]
        out = out[:last.end()] + f" on the {year} year-end chart" + out[last.end():]
    return out, True, True


def fix_line(line, year, prev_run):
    """prev_run: the previous sentence cited a year-end rank with the qualifier in its run."""
    parts = re.split(r"(?<=[.!?])(\s+)", line)
    out, run = [], prev_run
    for i, p in enumerate(parts):
        if i % 2:
            out.append(p)
            continue
        new, cites, _ = fix_sentence(p, year, run)
        # a sentence that already said year-end (or got the qualifier) keeps the run alive
        # a rank sentence keeps the run alive; so does a context sentence that already says "year-end"
        run = (bool(YE.search(new)) or run) if cites else "year-end" in p.lower()
        out.append(new)
    return "".join(out), run


def main():
    apply = "--apply" in sys.argv
    changed = 0
    for f in sorted(glob.glob(str(ROOT / "blog/years/top-songs-of-*/index.html"))):
        year = f.split("top-songs-of-")[1][:4]
        lines = Path(f).read_text(encoding="utf-8").split("\n")
        new, run = [], False
        for l in lines:
            is_p = l.lstrip().startswith("<p>") or '"text"' in l
            nl, run_after = fix_line(l, year, run if is_p else False)
            new.append(nl)
            run = run_after if is_p else False
        for i, (a, b) in enumerate(zip(lines, new), 1):
            if a != b:
                changed += 1
                if not apply or "--show" in sys.argv:
                    print(f"{year}:{i}\n  - {a.strip()[:230]}\n  + {b.strip()[:260]}")
        if apply:
            Path(f).write_text("\n".join(new), encoding="utf-8")
    print(f"{changed} lines {'changed' if apply else 'would change'}")


if __name__ == "__main__":
    main()
