#!/bin/bash
if [ "$1" == "" ]; then
  >&2 echo "Error: no EGC filename specified"
  >&2 echo "Usage: $0 <egcfile>"
  exit 1
fi

filename=$1
grep -P '^D' $filename | cut -f 2 | cut -c 6- | sort > temp.$filename.D.pmids
grep -P '^[ST]' $filename | cut -f 3 | cut -c 6- | sort -u > temp.$filename.ST.pmids
diff -q temp.$filename.D.pmids temp.$filename.ST.pmids > /dev/null
has_diff=$?
if [ $has_diff ]; then
  diff temp.$filename.D.pmids temp.$filename.ST.pmids > temp.$filename.D_ST.pmids_diff
  grep '^<' temp.$filename.D_ST.pmids_diff | cut -c3- > temp.$filename.inD.notinST.pmids
  n_inD_notinST=`cat temp.$filename.inD.notinST.pmids | wc -l`
  if [ "$n_inD_notinST" -gt 0 ]; then
    echo "Pubmed IDs in D but not in S or T records: (n=${n_inD_notinST})"
    sed -e 's/^/  /' temp.$filename.inD.notinST.pmids
  fi
  grep '^>' temp.$filename.D_ST.pmids_diff | cut -c3- > temp.$filename.inST.notinD.pmids
  n_inST_notinD=`cat temp.$filename.inST.notinD.pmids | wc -l`
  if [ "$n_inST_notinD" -gt 0 ]; then
    echo "Pubmed IDs in S or T but not in D records: (n=${n_inST_notinD})"
    sed -e 's/^/  /' temp.$filename.inST.notinD.pmids
  fi
fi
rm temp.*
