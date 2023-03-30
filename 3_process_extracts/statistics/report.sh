#!/bin/bash

if [ "$1" == "" ]; then
  sets="archaea bacteria hydro"
else
  sets="$1"
fi

had_err=0
filenames=""
for set in $sets; do
  filename=../${set}.egc
  filenames="$filenames $filename"
done
egctools-stats $filenames
