#!/bin/bash

# checks:
# (1) equivalence of D identifiers set (PMID:...) from second column of D
#     with set of D references in S and T records, third column

had_err=0
for set in archaea bacteria hydro; do
  echo "Analysing set ${set}..."
  filename=../${set}.text_extracts.egc
  tabrec-validate-refs $filename S:3,T:3 D --colon
  had_err=$[$had_err + $?]
done

if [ $had_err -gt 0 ]; then
  echo "ERRORS, validation not passed"
  exit 1
else
  echo "OK, validation passed"
  exit 0
fi
