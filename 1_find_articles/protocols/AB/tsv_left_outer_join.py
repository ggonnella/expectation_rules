#!/usr/bin/env python3
"""
Left outer join of two TSV

Usage:
  ./tsv_left_outer_join.py [options] <ltable> <lkey> <rtable> <rkey>

Arguments:
  <ltable>/<rtable>: left and right table, TSV files
  <lkey>/<rkey>:     join key in the left and right tables, 1-based

Example:

  <ltable>        <rtable>         <join with lkey 2 and rkey 2>
  A 1 a           x 1 X            A 1 a x X
  B 1 b           y 2 Y            B 1 b x X
  C 2 c           z 3 Z            C 2 c y Y
  D 4 d                            D 4 d

Note:
  the rkey column is skipped when appending the right columns
  since it would be a duplicate of the lkey column
"""

from docopt import docopt

def main(args):
  kL = int(args["<lkey>"])-1
  kR = int(args["<rkey>"])-1
  right = {}
  with open(args["<rtable>"]) as f:
    for line in f:
      elems = line.rstrip().split("\t")
      right[elems[kR]] = [elems[i] for i in range(len(elems)) if i != kR]
  with open(args["<ltable>"]) as f:
    for line in f:
      elems = line.rstrip().split("\t")
      print("\t".join(elems + right.get(elems[kL], [])))

if __name__ == "__main__":
  args = docopt(__doc__, version="0.1")
  main(args)
