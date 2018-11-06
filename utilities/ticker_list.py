# Get all company tickers in the dataset
#

from config import ROOT
import random
from sas7bdat import SAS7BDAT


def get_list():
	with open(ROOT + "tickers.txt", 'w', encoding='utf8') as wf:
		with open(ROOT + "data_fin.txt", 'r') as rf:
			tickers = set([l.split('\t')[1] for l in rf.readlines()])
			print(len(tickers))
			print(random.sample(tickers, 10))
			for t in tickers:
				wf.write(t + '\n')


def get_list2():
	with open("tickers2.txt", 'w', encoding='utf8') as wf:
		with SAS7BDAT("data_fin_merged.sas7bdat") as rf:
			l = [row[1] for row in rf]
			print(l[:5])
			tickers = set(l[1:])
			for t in tickers:
				wf.write(t + '\n')


if __name__ == "__main__":
	get_list2()
