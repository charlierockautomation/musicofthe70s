#!/usr/bin/env python3
"""Every playable song list must use the shared continuous player.

Fails (exit 1) if any built page has Play buttons (data-yt) that are not inside
a <table ... data-inline-player>, or that page does not load /js/table-player.js,
or loads an old one-off list player. js/table-player.js is what makes a list
play continuously, song after song, until Stop.

Usage: python3 scripts/check_list_players.py
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP = {'radio'}  # /radio/ has its own station player (js/radio.js)
OLD = ('number-one-player.js', 'one-hit-wonder-player.js')

problems = []
for page in sorted(ROOT.rglob('*.html')):
    rel = page.relative_to(ROOT)
    if rel.parts[0] in SKIP or rel.parts[0].startswith('.'):
        continue
    html = page.read_text(encoding='utf-8', errors='ignore')
    if 'data-yt=' not in html:
        continue
    if '/js/table-player.js' not in html:
        problems.append(f'{rel}: has Play buttons but does not load /js/table-player.js')
    for old in OLD:
        if old in html:
            problems.append(f'{rel}: still loads retired {old}')
    # every data-yt button must sit inside a data-inline-player table
    for m in re.finditer(r'<table\b[^>]*>.*?</table>', html, re.S):
        block = m.group(0)
        if 'data-yt=' in block and 'data-inline-player' not in block[:block.find('>') + 1]:
            problems.append(f'{rel}: a table with Play buttons is missing data-inline-player')
    outside = re.sub(r'<table\b[^>]*>.*?</table>', '', html, flags=re.S)
    if re.search(r'<button[^>]*data-yt=', outside):
        problems.append(f'{rel}: Play buttons outside a table (shared player only handles tables)')

if problems:
    print('FAIL')
    for p in problems:
        print('  ' + p)
    sys.exit(1)
print('PASS')
