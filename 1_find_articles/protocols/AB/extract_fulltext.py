#!/usr/bin/env python3
"""
Extract fulltext of articles from Pubmed Central XML

Usage:
  ./extract_fulltext.py <xmlfile>
"""
from docopt import docopt
from pathlib import Path
import xml.etree.ElementTree as ET

def main(args):
  tree=ET.parse(args["<xmlfile>"])
  root = tree.getroot()
  articlen = 0
  for pubmed_article in root.findall('article'):
    front = pubmed_article.find('front')
    articleid = front.find('article-meta').find('article-id')
    articleid = "".join(articleid.itertext())
    assert(articleid != None)
    journal = front.find('journal-meta').find('journal-title')
    if journal == None:
      journal = front.find('journal-meta').find('journal-title-group').\
          find('journal-title')
    journal = "".join(journal.itertext())
    title = front.find('article-meta').find('title-group').\
        find('article-title')
    title = "".join(title.itertext())
    authors = []
    for contribgrp in front.find('article-meta').findall('contrib-group'):
      for author in contribgrp.findall('contrib'):
        if len(authors) == 5:
          authors[4] = authors[4] + " et al."
          break
        if author.find('name'):
          surname = "".join(author.find('name').find('surname').itertext())
          given_name = \
            "".join(author.find('name').find('given-names').itertext())
          authors.append(f"{given_name} {surname}")
    authors = ", ".join(authors)
    abstract_node = front.find('article-meta').find('abstract')
    if abstract_node != None:
      abstract = []
      abstract_lines = "".join(abstract_node.itertext())
      for l in abstract_lines.split("\n"):
        l = l.strip()
        if l:
          abstract.append(l)
      abstract = "\n\n".join(abstract)
    else:
      abstract = ""
    body = pubmed_article.findall('body')
    if not body:
      continue
    text = []
    for section in body:
      for paragraph in section:
        ptext = "".join(paragraph.itertext())
        for l in ptext.split("\n"):
          l = l.strip()
          if l:
            text.append(l)
    text = "\n\n".join(text)
    articlen += 1
    if articlen > 0:
      print("#"*50+"\n\n")
    print(f"[PMID]\n\n{articleid}\n\n")
    print(f"[Authors]\n\n{authors}\n\n")
    print(f"[Title]\n\n{title}\n\n")
    print(f"[Journal]\n\n{journal}\n\n")
    print(f"[Abstract]\n\n{abstract}\n\n")
    print(f"[Fulltext]\n\n{text}\n\n")

if __name__ == "__main__":
  args = docopt(__doc__, version="0.1")
  main(args)
