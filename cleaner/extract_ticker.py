# Extract ticker from transcript
# 

import os
import time
import re
import random
import shutil
from config import ROOT

MV_PATH = ROOT + "extractable/"
INFO_PATH = ROOT + "info/"

# PATTERN = r"\([A-Z0-9:\s.-]*?\)"
# PATTERN = r">[A-Z]*?<"
PATTERN = r"\[[A-Z0-9:\s.-]*?\]"

def get_info_name(filename):
	return INFO_PATH + filename[:filename.find('-')] + ".txt"


def detect(f):
	t = f.read()
	t = t[:t.find("<strong>")].replace('\n', '')
	if re.search(PATTERN, t):
		return True
	return False

def check_ticker():
	total, count = 0, 0
	for filename in [f for f in os.listdir(DIR_PATH) if f.endswith(".txt")]:
		total += 1
		if total % 10000 == 0:
			print("%s/%s" % (count, total))
		with open(DIR_PATH + filename, 'r', encoding='utf8') as f:
			if detect(f):
				os.rename(DIR_PATH + filename, MV_PATH + filename)
				count += 1
			f.close()
	print("%s/%s" % (count, total))


def search(f):
	t = f.read()
	t = t[:t.find("<strong>")].replace('\n', '')
	return re.search(PATTERN, t)

def extract_ticker(filename, s):
	s = s[1:-1].replace(' ','')
	i = s.find(':')
	if i > -1:
		s = s[i+1:]
	j = s.find('.')
	if j > -1:
		s = s[:j]
	k = s.find('-OLD')
	if k > -1:
		s = s[:k]
	with open(get_info_name(filename), 'a') as f:
		f.write(s + '\n')
		f.close()
		os.rename(DIR_PATH + filename, MV_PATH + filename)
	

def main():
	total, count = 0, 0
	for filename in [f for f in os.listdir(DIR_PATH) if f.endswith(".txt")]:
		total += 1
		if total % 10000 == 0:
			print("%s/%s" % (count, total))
		with open(DIR_PATH + filename, 'r', encoding='utf8') as f:
			s = search(f)
			if s:
				count += 1
				extract_ticker(filename, s.group())
			f.close()
	print("%s/%s" % (count, total))

def create_info():
	total, count = 0, 0
	for filename in [f for f in os.listdir(DIR_PATH) if f.endswith(".txt")]:
		total += 1
		if total % 10000 == 0:
			print("%s/%s" % (count, total))
		with open(DIR_PATH + filename, 'r', encoding='utf8') as f:
			title = f.readline()
			with open(get_info_name(filename), 'w', encoding='utf8') as wf:
				wf.write(title)
				wf.close()
				count += 1
			f.close()
	print("%s/%s" % (count, total)) 

if __name__ == "__main__":
	# main()
	# create_info()
	# test()
	pass


