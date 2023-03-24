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
1_find_articles          scripts, protocols and results of
|                        the creation of lists of articles from which to
|                        search for expectation rules
|
|- protocols             scripts and protocols for the
|  |                     creation of the list of scientific articles
|  |
|  |- H                  related to genomes of prokaryotes in hydrothermal
|  |                     vents; done using Pubmed queries
|  |
|  |- AB                 related to the bacterial (B) and archaeal (A);
|                        from entries in the NCBI assembly database
|
|- results               resulting H, A and B lists of scientific articles
|
|- statistics            analysis of the results, e.g. basic statistics

2_process_articles       protocols and results of the sentences
|                        extraction
|
|- protocols             protocols for the H, A and B lists
|
|- results               partial EGC files, containing only D, S and T records
|
|- statistics            basic statisics about the processed articles
|                        and the results

3_process_extracts       EGC files containing the complete analysis
|                        of the expectation rules extracted in step2
|
|- results               EGC files
|
|- statistics            statistics about the results
```

