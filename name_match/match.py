from sas7bdat import SAS7BDAT
import csv
import re
from company_name_similarity import CompanyNameSimilarity
from progressbar import progressbar

COMN_FILE = 'conm.sas7bdat'
CASENAMES_FILE = 'casename.sas7bdat'

comn, casenames = [], []

with SAS7BDAT(COMN_FILE) as f:
	for row in f:
		comn.append(row[0])
comn = comn[2:]
print(comn[:5])

with SAS7BDAT(CASENAMES_FILE) as f:
	for row in f:
		name = row[0]
		formatted = re.sub(r'[,\.]', '', name)
		casenames.append([name, formatted])
casenames = casenames[1:]
print(casenames[:5])

def match_by(fn, base=1):
	rows = []
	with open('matched.csv', 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['CASENAME', 'COMN', 'Similarity'])
		for cn in progressbar(casenames):
			formatted = cn[1]
			match = comn[0]
			ratio = fn(formatted, match)
			for c in comn[1:]:
				new_ratio = fn(formatted, c)
				if new_ratio > ratio:
					ratio = new_ratio
					match = c
			row = [cn[0], match, ratio/base]
			rows.append(row)
			writer.writerow(row)


if __name__ == "__main__":
	cm = CompanyNameSimilarity()
	match_by(cm.match_score)

