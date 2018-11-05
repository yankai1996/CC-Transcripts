from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import csv
from company_name_similarity import CompanyNameSimilarity

FILE_PATH = "matched.csv"

def main():
	rows = []

	with open(FILE_PATH, newline='') as f:
		print("Reading...")
		reader = csv.reader(f)
		rows = [row for row in reader][1:]
		f.close()

	print(len(rows), "records")
	print(rows[:5])

	cm = CompanyNameSimilarity()

	with open('match_double_checked.csv', 'w', newline='') as f:
		writer = csv.writer(f)
		writer.writerow(['CASENAME', 'COMN', 'Similarity', 'token_sort_ratio'])
		for row in rows:
			# if float(row[-1]) <= 0:
			# 	continue
			similarity = cm.match_score(row[0], row[1])
			if similarity <= 0:
				continue
			ratio = fuzz.token_sort_ratio(cm.normalize_company_name(row[0]), cm.normalize_company_name(row[1])) / 100
			row.append(ratio)
			writer.writerow([row[0], row[1], similarity, ratio])
		f.close()


if __name__ == "__main__":
	main()	