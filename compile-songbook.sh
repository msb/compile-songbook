#!/usr/bin/env bash

set -x

songbooks=$HOME/Documents/Songbooks

read -r -d '' indexlist << LIST
something-different.tsv
something-different-2.tsv
old-cambridge-songbooks.tsv
missing-wednesdays.tsv
rob.tsv
karen.tsv
mikes-song-book.tsv
LIST

set -e

docker run -v "$songbooks:/data" --rm -u $(id -u):$(id -g) compile-songbook --title=cambridge-ukulele.title.pdf --supplement=supplement.tsv cambridge-ukulele.pdf $indexlist

cp $songbooks/cambridge-ukulele.pdf "$songbooks/Cambridge Ukulele.pdf"

