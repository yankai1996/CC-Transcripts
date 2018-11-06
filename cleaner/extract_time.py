# Extract conference call date and time from transcript
# 

import os
import time
import re
import random
import shutil
from config import ROOT

DIR_PATH = ROOT + "no_ticker/"
MV_PATH = ROOT + "done/"
INFO_PATH = ROOT + "info/"

PATTERN = r"[A-Z][a-z,\s]*?[0-9]{,2}[a-z,\s]*?20[01][0-9][,\s]*?[0-9]{1,2}:[0-9]{2}(\s*?[AaPp]\.?[Mm])?"
# PATTERN = r"[A-Z][a-z,\s]*?[0-9]{,2}[a-z,\s]*?00[01][0-9][,\s]*?[0-9]{1,2}:[0-9]{2}(\s*?[AaPp]\.?[Mm])?"

def get_info_name(filename):
	return INFO_PATH + filename[:filename.find('-')] + ".txt"


def detect(f):
	t = f.read()
	t = t[:t.find("<strong>")].replace('\n', '')
	if re.search(PATTERN, t):
		return True
	return False

def check_time():
	total, count = 0, 0
	for filename in [f for f in os.listdir(DIR_PATH) if f.endswith(".txt")]:
		total += 1
		if total % 10000 == 0:
			print("%s/%s" % (count, total))
		with open(DIR_PATH + filename, 'r', encoding='utf8') as f:
			if detect(f):
				# os.rename(DIR_PATH + filename, MV_PATH + filename)
				count += 1
	print("%s/%s" % (count, total))


def search(f):
	t = f.read()
	t = t[:t.find("<strong>")].replace('\n', '')
	return re.search(PATTERN, t)


def extract_time(filename, s):
	MONTH = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
	
	MM, DD, YY = "", "", ""
	
	for i in range(12):
		if s.startswith(MONTH[i]):
			MM = "%02d" % (i+1)
			break
	if not MM:
		return False

	# dd_yy = re.search(r"[0-9]{,2}[a-z,\s]*?00[01][0-9]", s)
	dd_yy = re.search(r"[0-9]{,2}[a-z,\s]*?20[01][0-9]", s)
	if not dd_yy:
		return False
	dd_yy = dd_yy.group()
	YY = dd_yy[-2:]
	DD = re.findall(r"\d+", dd_yy[:-4])
	if not DD:
		return False
	DD = "%02d" % int(DD[0])

	# with open(DIR_PATH + filename, 'r', encoding='utf8') as yf:
	# 	line = yf.readlines()[1]
	# 	result = re.search(r"20[0-9]{2}", line)
	# 	if result:
	# 		YY = result.group()[-2:]
	# 	yf.close()

	raw_time = re.search(r"[0-9]{1,2}:[0-9]{2}(\s*?[AaPp]\.?[Mm])?", s).group()
	hh_mm = re.findall(r"\d+", raw_time)
	hh, mm = int(hh_mm[0]), int(hh_mm[1])
	if re.search(r"[Pp]", raw_time):
		hh += 12

	time = "%s/%s/%s\n%02d:%02d:00" % (MM, DD, YY, hh, mm)
	with open(get_info_name(filename), 'a') as f:
		f.write(time)
		f.close()
		os.rename(DIR_PATH + filename, MV_PATH + filename)
		return True
	# print(s)
	# print(time)
	return False



def main():
	total, count = 0, 0
	for filename in [f for f in os.listdir(DIR_PATH) if f.endswith(".txt")]:
		# if total > 10:
		# 	break
		total += 1
		if total % 10000 == 0:
			print("%s/%s" % (count, total))
		with open(DIR_PATH + filename, 'r', encoding='utf8') as f:
			s = search(f)
			if s:
				print(s.group())
			if s and extract_time(filename, s.group()):
				count += 1
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
				wf.write(title + "[MISSING]\n")
				wf.close()
				count += 1
			f.close()
	print("%s/%s" % (count, total)) 

if __name__ == "__main__":
	# check_time()
	# create_info()
	main()
	# test()
	pass


