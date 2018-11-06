# Remove detected ads from the transcripts
# 

import os
import io
import re
from config import ROOT

DIR_PATH = ROOT + "source/"
EXPORT_PATH = ROOT + "source/"

PATTERN = r"To sponsor a Seeking Alpha transcript[\s\S]*?\n"
# PATTERN = r"<strong>Q.*?A<trong>"
# PATTERN = r"Read all investor conference presen[\s\S]*?To sponsor an investor conference presentation transcript.*?\n"
# PATTERN = r"THE INFORMATION CONTAINED HERE IS A TEXTUAL REPRESENTATION.*\n"
# PATTERN = r"<strong>\s*?</strong>"
# PATTERN = r"Looking for innovative way to invest in[\s\S]*?To sponsor a Seeking Alpha transcript.*\n"

def find_pattern(s):
	if s[s.find(PATTERN1):s.find(PATTERN2)]:
		return True
	return False

def remove_ads(filename):
	after = ""
	with open(DIR_PATH + filename, 'r') as f:
		ads = False
		for line in f.readlines():
			if line.find(PATTERN1) >= 0:
				ads = True
			elif line.find(PATTERN2) >= 0:
				ads = False
				continue
			if not ads:
				after += line
	with open(EXPORT_PATH + filename, "w", encoding="utf8") as f:
		f.write(after)
		f.close()

def find_regex(t):
	if re.search(PATTERN, t):
		return True
	return False

def remove_ads_regex(t, filename):
	t = re.sub(PATTERN, '', t)
	with open(EXPORT_PATH + filename, 'w', encoding='utf-8') as f:
		f.write(t)
		f.close()


def main():
	total, count = 0, 0
	for filename in [f for f in os.listdir(DIR_PATH) if f.endswith(".txt")]:
		with open(DIR_PATH + filename, 'r') as f:
			t = f.read()
			if total % 10000 == 0:
				print("%s/%s" % (count, total))
			total += 1
			if find_regex(t):
				# print(f)
				os.rename(DIR_PATH + filename, ROOT + filename)
				# remove_ads_regex(t, filename)
				count += 1

	print("%s/%s" % (count, total))


if __name__ == "__main__":
    main()