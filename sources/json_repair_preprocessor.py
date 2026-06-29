#!/usr/bin/env python3
"""Repair JSON files with unescaped inner quotes and raw control characters.

Heuristic: walk the text. While inside a string, a `"` closes the string only
if the next non-whitespace char is a structural delimiter (: , } ]) or EOF.
Otherwise it's a stray inner quote and gets escaped. Raw control characters
inside strings (newlines, tabs) are escaped too.
"""
import json, sys

STRUCTURAL = set(':,}]')

def repair(text):
    out = []
    in_str = False
    escaped = False
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if not in_str:
            if c == '"':
                in_str = True
                out.append(c)
            else:
                out.append(c)
            i += 1
            continue
        # inside a string
        if escaped:
            out.append(c)
            escaped = False
            i += 1
            continue
        if c == '\\':
            out.append(c)
            escaped = True
            i += 1
            continue
        if c == '"':
            # look ahead for next non-whitespace
            j = i + 1
            while j < n and text[j] in ' \t\r\n':
                j += 1
            if j >= n or text[j] in STRUCTURAL:
                # genuine closing quote
                out.append(c)
                in_str = False
            else:
                # stray inner quote -> escape
                out.append('\\"')
            i += 1
            continue
        # raw control characters inside string
        if c == '\n':
            out.append('\\n'); i += 1; continue
        if c == '\r':
            out.append('\\r'); i += 1; continue
        if c == '\t':
            out.append('\\t'); i += 1; continue
        if ord(c) < 0x20:
            out.append('\\u%04x' % ord(c)); i += 1; continue
        out.append(c)
        i += 1
    return ''.join(out)

for path in sys.argv[1:]:
    with open(path, 'r', encoding='utf-8') as f:
        raw = f.read()
    try:
        json.loads(raw)
        print(f"OK (no fix needed): {path}")
        continue
    except Exception as e:
        pass
    fixed = repair(raw)
    obj = json.loads(fixed)  # raises if still broken
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print(f"FIXED: {path}")
