# Preprocess

Data cleaning of the dataset ConceptNet

## Prerequisite:

Download dataset and save it in an accessible location with additional storage space. (~ 10 GB)


## Steps for preprocessing:

* gzip -k -d conceptnet-assertions-5.6.0.csv
* grep -P '(/en/.*?){4}' conceptnet-assertions-5.6.0.csv > ConceptNetEnglish.csv
* cut ConceptNetEnglish.csv -f1 > ConceptNetEnglish.csv
