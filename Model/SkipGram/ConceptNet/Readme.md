
* gzip -k -d conceptnet-assertions-5.6.0.csv
* grep -P '(/en/.*?){4}' conceptnet-assertions-5.6.0.csv > ConceptNetEnglish.csv
* cut ConceptNetEnglish.csv -f1 > ConceptNetEnglish.csv
