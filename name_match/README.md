# Name Match

Given two lists of company names: `casename.sas7bdat` is composed of the irregular expression of the company names, `conm.sas7bdat` contains the standard names of the companies. Matching these two lists to find the standard name for each company in `casename.sas7bdat`.

## Usage

1. Run `python3 match.py` to find the matching string with the maximum similarity. The algorithm combines jaccard distance, tfidf score and levenshtein distance.

2. Run `python3 double_check.py` to simply check the similarity between the best-matching pairs. This algorithm calculate the sort ration (Module: `fuzzywuzzy`).


## P.S.

This task is out of the scope of the CC-Transcripts project.

Assigned by Dr. Gu for her PhD student.