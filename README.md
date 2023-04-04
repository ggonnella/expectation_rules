This is a database of expectation rules
about the contents of prokaryotic genomes,
manually extracted from scientific literature.

# Format

The rules are expressed in EGC format,
described in the manuscript
"EGC: a format for expressing prokaryotic genomes content expectations",
available at
https://doi.org/10.48550/arXiv.2303.08758

An implementation in TextFormats of the EGC format
is available at
https://github.com/ggonnella/egc-spec

# Organization

```
1_find_articles          creation of articles lists for searching expectations
|
|- protocols             protocols / pipelines for the creation
|  |
|  |- H                  related to genomes of prokaryotes in hydrothermal
|  |                     vents; done using Pubmed queries
|  |
|  |- AB                 related to the bacterial (B) and archaeal (A);
|                        from entries in the NCBI assembly database
|
|- statistics            analysis of the results, e.g. basic statistics

2_process_articles       extraction of expectations from articles
|
|- protocols             protocols (scratchpad) for the H, A and B lists
|
|- results               list of processed documents;
|                        extracted sentences/tables/paragraphs
|
|- validation            scripts/pipeline for results validation
|
|- statistics            basic statisics about the processed articles
|                        and the results

scripts                  scripts are contained here and linked in the
                         protocols and statistics directories

3_process_extracts       final EGC files with the rules collections
|
|-validation             validation of the EGC files
|
|-statistics             statistics about the contents of the EGC files
```

## Acknowledgements

This rule collection has been created in context of the DFG project GO 3192/1-1
“Automated characterization of microbial genomes and metagenomes by collection
and verification of association rules”. The funders had no role in study
design, data collection and analysis.

