cut -f 6 ../pubmed-queries-joined.tsv | sort | uniq -c | sort -n -r > hydro.n_pmid_per_journal.tsv
