# # Remove operators' words from the transcripts
#
# Update: Only remove the subtitles
#

import os
import re
from config import ROOT

DIR_PATH = ROOT + "QA/"
EXPORT_PATH = ROOT + "clean/"
DONE_PATH = ROOT + "done/"

# PATTERN = r"<strong>.*?Operator.*?\n.*?\n"
# PATTERN = r"<strong>.*?Operator[\s\S]*?<strong>"
# PATTERN = r"<strong>.*?</strong>"
PATTERN = r"\[.*?\]"

def remove(filename, t):
	if not re.search(PATTERN, t):
		return False

	t = re.sub(PATTERN, "", t)
	
	with open(EXPORT_PATH + filename, 'w') as wf:
		wf.write(t)
		wf.close()
		os.rename(DIR_PATH + filename, DONE_PATH + filename)
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
