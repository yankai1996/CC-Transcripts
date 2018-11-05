# Tokenize the transcripts and add 'NOT_' tags
# The imported transcripts should have been cleaned
#

from getwords import GetWords
from config import ROOT, ML_PRES, ML_QA
import os
import time
from progressbar import progressbar

# path1: input path, path2: output path
def preprocess(path1, path2):
	print("Reading: %s\nExporting: %s" % (path1, path2))

	filenames = [f for f in os.listdir(path1) if f.endswith(".txt")]
	for filename in progressbar(filenames):
		with open(path1 + filename, 'r') as rf:
			words = GetWords(rf.read())[0]
			with open(path2 + filename, 'w') as wf:
				wf.write(' '.join(words))


if __name__ == "__main__":
	start = time.time()
	preprocess(ROOT + "Pres/", ML_PRES)
	preprocess(ROOT + "QA/", ML_QA)
	end = time.time()
	print('Time consuming: %.3f seconds.' % (end - start))