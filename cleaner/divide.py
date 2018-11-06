# Divide transcript to Pres and QA
#

import os
import time
import re
import random
import shutil
from config import ROOT

DIR_PATH = ROOT + "source/"
PRES_PATH = ROOT + "Pres/"
QA_PATH = ROOT + "QA/"
DONE_PATH = ROOT + "done/"

PATTERN = r"\n(<strong>)?Question(s?)[-\s–]*(([Aa]nd)|(&amp;))?[-\s–]*[Aa]nswer[\s\S]*?\n"
# PATTERN = r"\n(<strong>)?\s*?Question(s?)[-\s–]*(([Aa]nd)|(&amp;))?[-\s–]*[Aa]nswer.*?>"

def get_pres_name(filename):
	return PRES_PATH + filename[:filename.find('-')]  + "-Pres.txt"

def get_qa_name(filename):
	return QA_PATH + filename[:filename.find('-')]  + "-QA.txt"

def divide(t, filename):
	s = re.search(PATTERN, t)
	if not s:
		return False
	i, j = s.span()
	with open(get_pres_name(filename), 'w', encoding='utf8') as f:
		f.write(t[:i])
		f.close()
	with open(get_qa_name(filename), 'w', encoding='utf8') as f:
		f.write(t[j:])
		f.close()
		return True
	return False

def main():
	total, count = 0, 0
	for filename in [f for f in os.listdir(DIR_PATH) if f.endswith(".txt")]:
		total += 1
		if total % 10000 == 0:
			print("%s/%s" % (count, total)) 
		with open(DIR_PATH + filename, 'r', encoding='utf8') as f:
			t = f.read()
			if divide(t, filename):
				os.rename(DIR_PATH + filename, DONE_PATH + filename)
				count += 1
			f.close()
	print("%s/%s" % (count, total))


if __name__ == "__main__":
	main()


