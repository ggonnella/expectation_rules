#!/usr/bin/env bash
#
# Given a list of assembly accessions, query the NCBI assembly database
# for related pubmed entries
#
# Usage:
#   ./run_query.sh <accessions> <fieldnum>
#
# Arguments:
#   <accessions>   Tabular file, tab-separated, with accessions in a column
#                  or file with one accession per line
#   <column>       1-based column number if tab-separated file;
#                  Use "1" if file with one accession per line
#

ACCESSIONS=$1
COLUMN=$2
N_AT_A_TIME=200

# (1) sed adds the search field suffix to each line
# (2) xargs splits the IDs in bunches
# (3) sed separates the IDs using |
# (4) xargs runs esearch using the IDs as query
# (5) elink searches for links from assembly to pubmed
# (6) efetch retrieves the records (as IDs)

#set -e -x

i=0
(cut -d$'\t' -f $COLUMN ${ACCESSIONS} | \
  sed 's/$/[ASAC]/' | \
  xargs -n ${N_AT_A_TIME} echo | \
  sed 's/ /|/g') | while read -r query; do
  i=$[i+1]
  >&2 echo -n "[$(date)] Running query number ${i}... "
  #>&2 echo "Query: $query"
  (esearch -db assembly -query "$query" < /dev/null | \
        elink -db assembly -target pubmed | \
            efetch -format uid)
  >&2 echo "exit code: $?"
done

