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

3_process_extracts       analysis of the expectation rules extracted in step2
|
|- 3_1_group_definitions     definitions of organism groups
|  |
|  |- statistics             statistics about the definitions
|
|- 3_2_contents_definitions  definitions of genome contents
|  |
|  |- statistics             statistics about the definitions
|
|- 3_3_rules_definitions     definitions of rules based on the 3_1 and 3_2
|  |
|  |- statistics             statistics about the definitions
|

scripts                  scripts are contained here and linked in the
                         protocols and statistics directories

results                  final EGC files with the rules collections
```
