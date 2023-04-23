#!/usr/bin/env python3
"""
Read an output description file (in YAML format), containing a list of output
sections and the YAML files they are contained in (as dict entries or
list items), and output the selected values or items in the specified order.

Usage:
  combine_sections.py [options] <output_desc_file>

Options:
  --no-newlines, -N    Don't output newlines after each section and item.

Example of an output description file:
- dict1.yaml: key
- dict2.yaml: [key1, key2]
- list1.yaml#: [2, 3] # 1-based indexing; # means numbered output
- list2.yaml!!!: "*" # select all items; each ! means indent by 2 spaces
"""

import os
import sys
import yaml
import re
from docopt import docopt
from jsonschema import validate, ValidationError

# Define the JSON schema to validate the output description file
SCHEMA = yaml.safe_load("""
type: array
items:
  anyOf:
    - type: string
    - type: object
      additionalProperties: false
      patternProperties:
        "^[^:]+$":
          anyOf:
            - type: string
            - type: integer
              minimum: 1
            - type: integer
              maximum: -1
            - type: array
              items:
                anyOf:
                  - type: integer
                    minimum: 1
                  - type: integer
                    maximum: -1
            - type: array
              items:
                type: string
                not:
                  pattern: "^[0-9]+$"
                  const: "*"
      minProperties: 1
      maxProperties: 1
""")

def validate_output_desc_file(output_desc_file):
  """Validate the input file against the JSON schema"""
  with open(output_desc_file) as f:
    data = yaml.safe_load(f)
  try:
    validate(instance=data, schema=SCHEMA)
  except ValidationError as e:
    raise RuntimeError(f"Invalid output description file: {e}")
  return data

def parse_slice_selector(start_str, end_str):
  start = int(start_str)
  end = int(end_str)
  if start == 0 or end == 0 or (start < 0 and end > 0) or \
      (start > end and end > 0) or (start > end and start < 0):
    raise RuntimeError(f"Invalid range selector: {start_str}:{end_str}")
  if start > 0:
    start -= 1
  if end == -1:
    end = None
  elif end < -1:
    end += 1
  return slice(start, end)

def parse_filename(filename):
  indent = 0
  with_num = False
  no_section_sep = False
  while filename[-1] in ["!", "#", "-"]:
    if filename[-1] == "#":
      with_num = True
    elif filename[-1] == "-":
      no_section_sep = True
    else:
      indent += 2
    filename = filename[:-1]
  return filename, with_num, indent, no_section_sep

def collect_file_contents(data):
  files = {}
  for item in data:
    if isinstance(item, dict):
      filename = parse_filename(list(item.keys())[0])[0]
      if filename not in files:
        if not os.path.isfile(filename):
          raise RuntimeError(f"File not found: {filename}")
        with open(filename) as f:
          files[filename] = yaml.safe_load(f)
  return files

def handle_star_selector(selector, files, filename):
  if isinstance(files[filename], dict):
    return files[filename].values()
  elif isinstance(files[filename], list):
    return files[filename][:]

def handle_slice_selector(selector, files, filename):
  if isinstance(files[filename], dict):
    raise RuntimeError("Invalid selector for file"+\
        f" '{filename}': {selector}.\n"+\
        "Cannot use range selector with a dict.")
  elif isinstance(files[filename], list):
    return files[filename][selector]

def handle_list_selector(selector, files, filename):
  selection = []
  for key in selector:
    err = False
    if isinstance(files[filename], dict):
      k = key
      if key not in files[filename]:
        err="Key"
    elif isinstance(files[filename], list):
      try:
        k = int(key)
      except ValueError:
        raise RuntimeError("Invalid selector for file"+\
            f" '{filename}': {selector}.\n"+\
            "Expected: int when selecting from list.")
        sys.exit(1)
      if k > 0:
        k = k - 1
      if k > len(files[filename]):
        err="Index"
    else:
      raise RuntimeError("Invalid data type for root level "+\
          f"of '{filename}': {type(files[filename])}.\n"+\
          "Must be a dict or a list.")
    if err:
      raise RuntimeError(f"{err} '{key}' not found in file"+\
          f" '{filename}'.")
    item = files[filename][k]
    selection.append(item)
  return selection

def get_selection(selector, files, filename):
  if isinstance(selector, str):
    if selector == "*":
      return handle_star_selector(selector, files, filename)
    m = re.match(r"(\-?\d+)\.\.(\-?\d+)$", selector)
    if m:
      return handle_slice_selector(\
          parse_slice_selector(*m.groups()), files, filename)
    elif selector != "*":
      selector = [selector]
  elif isinstance(selector, int):
    selector = [selector]
  if not isinstance(selector, list):
    raise RuntimeError("Invalid selector for file"+\
        f" '{filename}': {selector}.\n"+\
        "Expected: string or list of strings or ints.")
  return handle_list_selector(selector, files, filename)

def output_selection(selection, with_num, output_newlines,
                     indent, no_section_sep):
  selection_flattened = []
  for item in selection:
    if isinstance(item, list):
      selection_flattened.extend(item)
    else:
      selection_flattened.append(item)
  for i, part in enumerate(selection_flattened):
    if with_num:
      part = ["  "+ln for ln in part.splitlines(True)]
      part = f"({i+1})\n{''.join(part)}"
    if indent > 0:
      part = [" "*indent+ln for ln in part.splitlines(True)]
      part = ''.join(part)
    print(part, end="")
    if output_newlines and part[-1] != "\n":
      print()
  if output_newlines and not no_section_sep:
    print()

def main():
  # Parse command-line arguments
  args = docopt(__doc__)
  output_desc_file = args["<output_desc_file>"]
  output_newlines = not args["--no-newlines"]

  try:
    output_desc = validate_output_desc_file(output_desc_file)
    files = collect_file_contents(output_desc)
    for entry in output_desc:
      with_num = False
      no_section_sep = False
      indent = 0
      if isinstance(entry, str):
        selection = [entry]
      else:
        filename = list(entry.keys())[0]
        selector = entry[filename]
        filename, with_num, indent, no_section_sep = parse_filename(filename)
        selection = get_selection(selector, files, filename)
      output_selection(selection, with_num, output_newlines,
                       indent, no_section_sep)
  except RuntimeError as e:
    print(e, file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
  main()
