# Construct the dictionary (corpus) based on the tokenized transcripts
# 

from config import ROOT, ML_PRES, ML_QA # import file path
import os
import time
from sas7bdat import SAS7BDAT
from progressbar import progressbar


# This function decides which files will be used to construct the dictionary
# You might need to modify it according to your purpose
def get_filenames():
	with SAS7BDAT('data_fin_merged.sas7bdat') as f:
		return [str(int(row[0])) for row in f if type(row[0]) != str]
	# return [f[:-4] for f in os.listdir(ROOT + "info/") if f.endswith(".txt")]

def get_wordset(path):
	with open(path, 'r') as f:
		return set(f.read().strip().split())

def main():

	dictionary = {}

	print("Reading files...")
	filenames = get_filenames()
	for filename in progressbar(filenames):
		pres_wordset = get_wordset(ML_PRES + filename + "-Pres.txt")
		qa_wordset = get_wordset(ML_QA + filename + "-QA.txt")
		wordset = pres_wordset | qa_wordset

		for word in wordset:
			if word not in dictionary:
				dictionary[word] = 1
			else:
				dictionary[word] += 1
		
	total = len(filenames)
	with open("dictionary.txt", 'w') as f:
		for word in sorted(dictionary):
			frequency = dictionary[word] / total
			if 0.01 <= frequency <= 0.99:
				f.write(word + '\n')

def test():
	l = get_filenames()
	print(l[:5])
	print(l[-5:])

if __name__ == "__main__":
	start = time.time()
	main()
	# test()
	end = time.time()
	print('Time consuming: %.3f seconds.' % (end - start))