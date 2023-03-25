#!/usr/bin/env python3
"""
Usage:
    get_journal_names.py <filename>

Options:
    -h --help     Show this screen.
    <filename>    Name of file containing PubMed IDs, one per line.
"""

import requests
from xml.etree import ElementTree
from docopt import docopt

def get_journal_names(pmid_list):
    pmid_str = ','.join(pmid_list)
    url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid_str}&retmode=xml'
    response = requests.get(url)
    root = ElementTree.fromstring(response.content)
    journal_names = []
    for article in root.findall('.//PubmedArticle'):
        journal_info = article.find('.//MedlineJournalInfo')
        if journal_info is not None:
            journal_name = journal_info.findtext('MedlineTA')
            journal_names.append(journal_name)
    return journal_names

def get_pmid_list(filename):
    pmid_list = []
    with open(filename, 'r') as f:
        for line in f:
            pmid = line.strip()
            if pmid:
                pmid_list.append(pmid)
    return pmid_list

if __name__ == '__main__':
    arguments = docopt(__doc__)
    filename = arguments['<filename>']
    pmid_list = get_pmid_list(filename)
    journal_names = get_journal_names(pmid_list)
    for name in journal_names:
        print(name)
