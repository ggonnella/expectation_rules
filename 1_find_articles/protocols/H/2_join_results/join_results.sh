#!/bin/bash

DIR="../step1"
PFX="pubmed-query-hydrothermal-vent"
LIST="archaea-genome archaea-sequence bacteria-genome bacteria-sequence"

# (1) extract all lines except the header from all files
rm -f temp1.*.tsv
for x in ${LIST}; do
  tail -n+2 $DIR/${PFX}-${x}.tsv > temp1.${x}.tsv
done
# (2) join the records and remove duplicates
cat temp1.*.tsv | sort -u > temp2.joined.tsv
rm temp1.*.tsv
# (3) extract the header from one of the files
head -n 1 $DIR/pubmed-query-hydrothermal-vent-archaea-genome.tsv > temp2.header.tsv
# (4) create the final file
cat temp2.header.tsv temp2.joined.tsv > pubmed-queries-joined.tsv
rm temp2.*.tsv
