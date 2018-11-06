# Remove the name list from the beginning of transcripts
#

import os
import re
from config import ROOT

DIR_PATH = ROOT + "Pres/"
EXPORT_PATH = ROOT + "clean/"

PATTERN1 = r"<strong>.*?Operator"
PATTERN2 = r"<strong>.*?Analyst[\s\S]*?<strong>"
PATTERN3 = r"<strong>.*?Executive[\s\S]*?<strong>"


def remove(filename, t):
	result = re.search(PATTERN1, t)
	if not result:
		result = re.search(PATTERN2, t)
		if not result:
			result = re.search(PATTERN3, t)
			if not result:
				return False
		i = result.span()[1]
		t = t[i:]
	else:
		i = result.span()[0]
		t = t[i:]
	
	with open(EXPORT_PATH + filename, 'w') as wf:
		wf.write(t)
		wf.close()
		os.rename(DIR_PATH + filename, ROOT + "done/" + filename)
		# print(filename)
		# print(t[:100])
		return True
	return False

def main():
	total, count = 0, 0
	for filename in [f for f in os.listdir(DIR_PATH) if f.endswith(".txt")]:
		# if total > 10:
		# 	break
		total += 1
		if total % 10000 == 0:
			print("%s/%s" % (count, total))
		with open(DIR_PATH + filename, 'r') as f:
			t = f.read()
			if remove(filename, t):
				count += 1
			f.close()

	print("%s/%s" % (count, total))

if __name__ == "__main__":
	main()
