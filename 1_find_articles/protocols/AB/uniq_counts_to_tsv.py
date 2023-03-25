#!/usr/bin/env python3
"""
Transform the output of uniq -c to a tabular file

Usage:
  ./uniq_counts_to_tsv.py [options] <uniq_c_out>

Arguments:
  <uniq_c_out>   TSV file

Algorithm:
  the first column containing only spaces AFTER at least one column containing
  not only spaces is assumed to be divisor column between the counts and the
  lines in the output of uniq; the file is splitted on that column, the first
  element is casted to int() and the file is rejoined using tab
"""
from docopt import docopt

def first_non_spaces(longest, lines):
  for col in range(longest):
    for line in lines:
      if len(line)>=col:
        if line[col] != " ":
          return col

def main(args):
  with open(args["<uniq_c_out>"]) as f:
    lines = [l.rstrip() for l in f.readlines()]
  longest = max([len(line) for line in lines])
  col=first_non_spaces(longest, lines)
  while col < longest:
    col += 1
    found=True
    for line in lines:
      if line[col] != " ":
        found=False
        break
    if found:
      break
  for line in lines:
    print("\t".join([str(int(line[0:col])), line[col+1:]]))

if __name__ == "__main__":
  args = docopt(__doc__, version="0.1")
  main(args)
