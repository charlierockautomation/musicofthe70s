#!/bin/bash
# Slot 5.4 AC/DC Songs: candidate YouTube uploads per song (flat search, id | channel | title | duration)
cd "$(dirname "$0")"
: > search.log
while IFS= read -r q; do
  echo "### $q" >> search.log
  timeout 60 yt-dlp --flat-playlist --print "%(id)s | %(channel)s | %(title)s | %(duration)s" "ytsearch8:$q" >> search.log 2>/dev/null
done <<'Q'
AC/DC High Voltage official audio
AC/DC It's a Long Way to the Top official
AC/DC T.N.T. official audio
AC/DC Jailbreak official
AC/DC Dirty Deeds Done Dirt Cheap official audio
AC/DC Problem Child official audio
AC/DC Let There Be Rock official audio
AC/DC Whole Lotta Rosie official audio
AC/DC Dog Eat Dog official audio
AC/DC Rock 'n' Roll Damnation official audio
AC/DC Sin City official audio
AC/DC Riff Raff official audio
AC/DC Highway to Hell official video
AC/DC Girls Got Rhythm official audio
AC/DC Touch Too Much official video
AC/DC Shot Down in Flames official audio
AC/DC Walk All Over You official audio
AC/DC Baby, Please Don't Go official audio
Q
echo DONE >> search.log
