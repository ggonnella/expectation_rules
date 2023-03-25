DATADIR=/local/gonnella/data/prok_complete_genomes/accessions

default: bacteria.pmid.list \
	       archaea.pmid.list

%.pmid.list: ${DATADIR}/gbasm_rsasm_gbseq.%.tsv
	./query.sh $< 1 > $*.query_out
	./postprocess.sh $*.query_out > $@
	rm $*.query_out

EDIRECTPATH=${HROOT}/edirect

%.pubmed_records.multi.xml: %.pmid.list
	${EDIRECTPATH}/efetch -db pubmed -mode xml -input $< > $@

%.pubmed_records.merged.xml: %.pubmed_records.multi.xml
	./merge_multixml.py $< PubmedArticleSet > $@

%.pubmed_records.xml: %.pubmed_records.merged.xml
	xml_pp $< > $@

%.pmid_journal_title.tsv: %.pubmed_records.xml
	cat $< | ${EDIRECTPATH}/xtract -pattern PubmedArticle \
		-element MedlineCitation/PMID Journal/Title ArticleTitle > $@

%.n_pmid_per_journal.tsv: %.pubmed_records.xml
	cat $< | \
		(2>/dev/null ${EDIRECTPATH}/xtract -pattern PubmedArticle -element Journal/Title) | \
		sort | uniq -c | sort -k1nr | ./uniq_counts_to_tsv.py /dev/stdin > $@

%.pmid_journal_title.sorted.tsv: %.pmid_journal_title.tsv %.n_pmid_per_journal.tsv
	./tsv_left_outer_join.py $*.pmid_journal_title.tsv 2 \
		$*.n_pmid_per_journal.tsv 2 | \
		sort -t$$'\t' -k4,4nr -k2,2 -k1,1nr | cut -d $$'\t' -f 1,2,3 > $@

%.pmcid.list: %.pmid.list
	${EDIRECTPATH}/elink -db pubmed -target pmc -input $< | \
		${EDIRECTPATH}/efetch -format uid > $@

%.pmc_fulltext.multi.xml: %.pmcid.list
	${EDIRECTPATH}/efetch -format full -mode xml -db pmc -input $< > $@

%.pmc_fulltext.merged.xml: %.pmc_fulltext.multi.xml
	./merge_multixml.py $< pmc-articleset > $@

%.pmc_fulltext.xml: %.pmc_fulltext.merged.xml
	xml_pp $< > $@

%.pmc_fulltext.txt: %.pmc_fulltext.xml
	./extract_fulltext.py $< > $@

%.txt.gz: %.txt
	gzip -9 $<

%.xml.gz: %.xml
	gzip -9 $<

#
# Recipe for using Refseq IDs instead of Genbank IDs
# (using column 2 of the input file instead of column 1)
#
# Results: Did not change the results for the archaea (not tried for bacteria)
# Therefore it is not made by default
#
%.R.pmid.list: ${DATADIR}/gbasm_rsasm_gbseq.%.tsv
	./query.sh $< 2 > $*.query_out
	./postprocess.sh $*.query_out > $@
	rm $*.query_out

