#!/bin/bash

# checks:
# (1) equivalence of U identifiers set (U...) from second column of U
#     with set of U references in A and U records
# (2) all U references in M third column and SM tags shall be U identifiers

had_err=0
for set in archaea bacteria hydro; do
  echo "Analysing set ${set}..."
  filename=../${set}.contents.egc
  tabrec-validate-refs $filename A:3-4,U:4 U -R 'U.*'
  had_err=$[$had_err + $?]
  tabrec-validate-refs $filename M:3-SM U -R 'U.*' --nr
  had_err=$[$had_err + $?]
done

if [ $had_err -gt 0 ]; then
  echo "ERRORS, validation not passed"
  exit 1
else
  echo "OK, validation passed"
  exit 0
fi
