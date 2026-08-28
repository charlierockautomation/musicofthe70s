#!/usr/bin/env python3
"""One-time mechanical insert of the 'Listen Now' nav link into every existing
page's shared <nav class="main-nav"> block, between Tools and About.

Every one of these 75 pages currently has this exact block:
    <a href="/index.html#tools">Tools</a>
    <a href="/pages/about.html">About</a>

Skips radio/index.html, which was authored with the link already in place.
Fails loudly (does not touch the file) if a page's block doesn't match the
expected exact text, so nothing gets silently skipped or double-inserted.
"""
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OLD = '        <a href="/index.html#tools">Tools</a>\n        <a href="/pages/about.html">About</a>\n'
NEW = ('        <a href="/index.html#tools">Tools</a>\n'
       '        <a href="/radio/index.html">Listen Now</a>\n'
       '        <a href="/pages/about.html">About</a>\n')


def find_target_files():
    out = subprocess.run(
        ["grep", "-rl", "main-nav", "--include=*.html", "."],
        cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.splitlines()
    return sorted(f for f in out if f != "radio/index.html")


def main():
    files = find_target_files()
    updated = 0
    skipped = []
    for rel_path in files:
        path = os.path.join(ROOT, rel_path)
        with open(path) as f:
            content = f.read()
        if "Listen Now" in content:
            skipped.append((rel_path, "already has Listen Now"))
            continue
        count = content.count(OLD)
        if count != 1:
            skipped.append((rel_path, f"expected block found {count} times, not 1"))
            continue
        content = content.replace(OLD, NEW, 1)
        with open(path, "w") as f:
            f.write(content)
        updated += 1

    print(f"Updated {updated}/{len(files)} files.")
    if skipped:
        print("Skipped:")
        for path, reason in skipped:
            print(f"  {path}: {reason}")


if __name__ == "__main__":
    main()
