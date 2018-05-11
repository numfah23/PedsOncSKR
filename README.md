# PedsOncSKR
Symbolic Methods project: Domain Coverage and SemRep Evaluation for Knowledge Integration in Pediatric Oncology

This github repository contains code and data for our project.

# Code
## SemRep WebAPI
The Java-based API used to run SemRep was not included in this repo but can be downloaded and installed [here](https://ii.nlm.nih.gov/Web_API/index.shtml)

Note that access to this tool requires a [UMLS Terminology Services (UTS) account](https://uts.nlm.nih.gov/home.html)

## Scripts
### preprocess_clintrials.py and preprocess_textbook.py
These python files are used to split the data into multiple files to make it compatible with SemRep (input file can not exceed 10,000 characters in length per request)

### semrep_command.txt
This text file contains all the code used to run the SemRep WebAPI. The steps involved in this process include:
1. Remove non ASCII characters
2. Run SemRep WebAPI (compile before, if changes were made)
3. Triple extraction part 1: keep rows with "relation"
4. Triple extraction part 2: run get_triples.py script to get triples

### get_triples.py
This python script extracts triples from files created in the process of running blocks of code in semrep_command.txt. Make sure to manually specify inside the python file what input files to run the script on.

### plots_for_triples.py
This python script creates all the plots reported in our final paper and final presentation using the data provided in this github repository.
Running this code generates all the plots in the plots directory.

# Results
## Metamap folder
### ClinicalTrialsMetaMapResults.pdf, PubMedMetaMapResults.pdf, TextbookMetaMapResults.pdf 
These files show MetaMap output accuracy by highlighting mapped phrases with the following color scheme:
1. Yellow: correct match with best concept
2. Green: partial match
3. Pink: incorrect
4. Purple: not mapped


## SemRep folder
### SemRepGSComparison.xlsx
This file contains SemRep and MetaMap evaluation results 

The different worksheets in this file contain the following information:
1. PubMed MetaMap Matches, NCT MetaMap Matches, and Textbook MetaMap Matches: which parts of the gold standard concepts were mapped by MetaMap (shown bolded)
2. MetaMap Comparison:
  * Summary statistics for MetaMap matchings of gold standard concepts (from PubMed MetaMap Matches, NCT MetaMap Matches, and Textbook MetaMap Matches)
  * Summary statistics for accuracy of MetaMap output (data from Metamap folder)
3. SemRep Internal Eval: assign automated SemRep triples to one of the following
  * True and useful (T+)
  * True but not useful (T-)
  * False (F)
4. SemRep Comparison: summary statistics for SemRep vs. gold standard (used to calculate precision and recall)

### semmeddb_combined_triples.csv, clintrials_combined_triples.csv, textbook_combined_triples.csv
These files contain triples automatically extracted via SemRep WebAPI on all the data

### subset_triples.csv
These files contain triples automatically extracted via SemRep WebAPI on the subset of data that was also used to create the gold standard triples

### PubMedGS_Triples.csv, ClinTrialGS_Triples.csv, TextBookGS_Triples.csv
These files contain triples manually extracted on the subset of data

### IdealSemanticRelations_csv.csv
This file contains examples of desired ontologic predications for pediatric ALL used to make an ideal semantic network
