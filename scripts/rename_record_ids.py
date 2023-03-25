#!/usr/bin/env python3
"""
Usage:
  rename_record_ids.py <filename> <record_type> [<prefix>]

Arguments:
  <filename>     TSV file containing records
  <record_type>  type of record in the first column
  <prefix>       prefix to use (default == record_type)

Options:
  -h --help     Show this screen.
"""

import csv
from docopt import docopt

def rename_record_ids(filename, record_type, prefix):
    with open(filename, 'r') as input_file, \
         open(f"{filename}.out", 'w', newline="") as output_file:

        reader = csv.reader(input_file, delimiter='\t',
                            quoting=csv.QUOTE_NONE)
        writer = csv.writer(output_file, delimiter='\t',
                            lineterminator="\n", quoting=csv.QUOTE_NONE)

        count = 1
        for row in reader:
            if row[0] == record_type:
                row[1] = f"{prefix}{count}"
                count += 1
            writer.writerow(row)

if __name__ == '__main__':
    arguments = docopt(__doc__)
    filename = arguments['<filename>']
    record_type = arguments['<record_type>']
    prefix = arguments['<prefix>'] or record_type
    rename_record_ids(filename, record_type, prefix)

