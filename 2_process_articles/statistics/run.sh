for group in archaea bacteria hydro; do
  for klass in processed positive; do
    ./get_journal_names.py ../$group.${klass}_articles.pmids_list \
      | sort | uniq -c | sort -n -r > $group.$klass.journals
  done
done
