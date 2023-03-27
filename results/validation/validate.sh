#!/bin/bash

# checks:
# - equivalence of D identifiers set (PMID:...) from second column of D
#     with set of D references in S and T records, third column
# - equivalence of U identifiers set (U...) from second column of U
#     with set of U references in A and U records
# - all U references in M third column and SM tags shall be U identifiers
# - G identifiers (G...) in V fifth column and in C fifth and seventh column
#     must be all in G
# - all G identifiers must be either in V/C or in G sixth column
# - A identifiers must be in all in V/C fourth column
# - S references in V/C

if [ "$1" == "" ]; then
  sets="archaea bacteria hydro"
else
  sets="$1"
fi

had_err=0
for set in $sets; do
  echo "Analysing set ${set}..."
  filename=../${set}.egc
  tabrec-validate-refs $filename S:3,T:3 D --colon
  had_err=$[$had_err + $?]
  tabrec-validate-refs $filename A:3-4,U:4 U -R 'U.*'
  had_err=$[$had_err + $?]
  tabrec-validate-refs $filename M:2-SM U -R 'U.*' --nr
  had_err=$[$had_err + $?]
  tabrec-validate-refs $filename V:5,C:5-7,G:5 G -R 'G.*' -r "GO.*"
  had_err=$[$had_err + $?]
  tabrec-validate-refs $filename V:4,C:4 A -R 'A.*'
  had_err=$[$had_err + $?]
  tabrec-validate-refs $filename V:3,C:3 S -R 'S.*'
  had_err=$[$had_err + $?]
done

if [ $had_err -gt 0 ]; then
  echo "ERRORS, validation not passed, $had_err errors"
  exit 1
else
  echo "OK, validation passed"
  exit 0
fi
