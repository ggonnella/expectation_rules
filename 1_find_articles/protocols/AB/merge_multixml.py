#!/usr/bin/env python3
"""
Merge containing muliple concatenated XML files into single files
in that subsequent lines after the beginning of the file
containing <?xml ... or <!DOCTYPE are deleted
and the root tag is joined.

All the documents must have the same given root tag.

Usage:
  ./merge_multixml.py <multixml> <roottag>
"""

from docopt import docopt

def main(args):
  roottag = args["<roottag>"]
  with open(args["<multixml>"]) as f:
    found_xmlheader = False
    found_doctype = False
    for line in f:
      sline = line.strip()
      if sline.startswith("<?xml"):
        if not found_xmlheader:
          found_xmlheader = True
          print(line)
        continue
      elif sline.startswith("<!DOCTYPE"):
        if not found_doctype:
          print(line)
          print(f"<{roottag}>")
          found_doctype = True
          continue
      else:
        if sline.startswith(f"<{roottag}>"):
          sline = sline[len(roottag)+2:]
        if sline.endswith(f"</{roottag}>"):
          sline = sline[:-(len(roottag)+3)]
        print(sline)
    print(f"</{roottag}>")

if __name__ == "__main__":
  args = docopt(__doc__, version="0.1")
  main(args)
