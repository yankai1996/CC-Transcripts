# Organize all data to a single table
# 

import os
from config import ROOT

DATA_PATH = ROOT + "FinDict/"
EXPORT_PATH = ROOT + "data_fin.txt"
# DATA_PATH = ROOT + "Havard/"
# EXPORT_PATH = ROOT + "data_havard.txt"


def main():

	filenames = [f for f in os.listdir(DATA_PATH) if f.endswith(".txt")]
	sort_method = lambda x: int(x[:-4])
	filenames.sort(key=sort_method)

	items = [
		'filename',
		'symbol',
		'CC_Date',
		'CC_Time',
		'PresWordNum', 
		'PresCharNum',
		'QandAWordNum',
		'QandACharNum',
		'ShortWords',
		'LongWords',
		'NegWordsPres',
		'NegWordsQA',
		'NegWordsTotal',
		'PERMNO',
		'CUSIP',
		'ComnName'
	]

	with open(EXPORT_PATH, 'w', encoding='utf8') as f:
		for i in items:
			f.write(i + '\t')
		f.write('\n')

		count = 0

		for filename in filenames:
			count += 1
			if count % 10000 == 0:
				print(count)
			with open(DATA_PATH + filename, 'r') as df:
				f.write(filename[:-4] + '\t')
				data = df.readlines()
				for d in [d for d in data[1:] if d != '\n']:
					f.write(d.split(': ')[-1].replace('\n', '\t'))
				df.close()
			f.write('\n')
		f.close()
		print(count)


if __name__ == "__main__":
	main()	