# Preprocess

Data cleaning of the dataset ConceptNet

## Prerequisite:

Download dataset and save it in an accessible location with additional storage space. (~ 10 GB)
wget https://s3.amazonaws.com/conceptnet/downloads/2018/edges/conceptnet-assertions-5.6.0.csv.gz

## Steps for preprocessing:

* gzip -k -d conceptnet-assertions-5.6.0.csv
* grep -P '(/en/.*?){4}' conceptnet-assertions-5.6.0.csv > ConceptNetEnglish.csv
* cut ConceptNetEnglish.csv -f1 > ConceptNetEnglish_cut.csv
* mv ConceptNetEnglish_cut.csv ConceptNetEnglish.csv
* sed 's/^...//' ConceptNetEnglish.csv

