#!/usr/bin/env python3
"""
Outputs a list of identifiers in a TSV file which are completely
contained in other identifiers.

Usage:
    identify_contained.py <filename> <column>

Arguments:
    <filename>  Path to the input TSV file
    <column>    The 1-based column number in which the identifiers are found

Options:
    -h, --help  Show this help message and exit
"""

from docopt import docopt
import csv


def find_contained_identifiers(filename, column):
    identifiers = set()
    with open(filename, 'r') as tsv_file:
        reader = csv.reader(tsv_file, delimiter='\t')
        for row in reader:
            if len(row) >= column:
                identifier = row[column - 1]
                identifiers.add(identifier)
    with open(filename, 'r') as tsv_file:
        reader = csv.reader(tsv_file, delimiter='\t')
        for row in reader:
            if len(row) >= column:
                identifier = row[column - 1]
                for other_identifier in identifiers:
                    if identifier != other_identifier and \
                        identifier in other_identifier:
                        print(identifier)
                        break

if __name__ == '__main__':
    args = docopt(__doc__)
    filename = args['<filename>']
    column = int(args['<column>'])
    find_contained_identifiers(filename, column)
