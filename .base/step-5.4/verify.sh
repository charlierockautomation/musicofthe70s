#!/bin/bash
cd "$(dirname "$0")"
: > verify.log
for id in Nnjh-zp6pP4 GChhRrU6BJU CiJeSSzu9Bo x7qQmpK9b1M jsjdjWGDvFk S4uwi5cUyco 3f2g4RMfhS0 BL58K-3XGKs -0Oa5wvARSc pdnFm6uZSc8 7S69xWkV4uM l482T0yNkeo YFMF4ZFmtnU JGftIcp2SC0 UKwVvSleM6w _bP6aVG6L1w; do
  timeout 60 yt-dlp --skip-download --print "%(id)s | %(channel)s | %(channel_id)s | %(title)s | dur=%(duration)s | avail=%(availability)s | emb=%(playable_in_embed)s | age=%(age_limit)s | %(upload_date)s | %(artist)s | %(album)s" "https://www.youtube.com/watch?v=$id" 2>&1 | tail -1 >> verify.log
done
echo DONE >> verify.log
