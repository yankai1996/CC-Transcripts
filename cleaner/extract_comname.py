# Extract company name from transcript
#

import os
import time
import re
from sas7bdat import SAS7BDAT
from config import ROOT

DIR_PATH = ROOT + "info_temp/"
FIN_PATH = ROOT + "FinDict/"
HAVARD_PATH = ROOT + "Havard/"
DONE_PATH = ROOT + "info_done/"
TODO_PATH = ROOT + "info_todo/"


def extract_method1(line):
	m = re.search(r"\sQ[0-9]\s", line)
	if m:
		line = line[:m.span()[0]]
		m2 = re.search(r"\(.*?\)", line)
		if m2:
			line = line[:m2.span()[0]].strip()
		return line
	m = re.search(r"\sF[0-9]?Q[0-9]", line)
	if m:
		line = line[:m.span()[0]]
		m2 = re.search(r"\(.*?\)", line)
		if m2:
			line = line[:m2.span()[0]].strip()
		return line
	return ''

def extract_method2(line):
	# pattern = r"Wall Street Analyst"
	# pattern = r"'s?.*?Presents"
	# pattern = r"'?s? (CEO)|(Management) Discuss"
	pattern = r"'?s? (C.O)|([Mm]anagement) [Hh]ost"
	# pattern = r"'?s? (C.O|[Mm]anagement) [Pp]resent"
	# pattern = r"Present"
	# pattern = r"- (Shareholder)|(Analyst)"
	# pattern = r"\([A-Z]*?\)"
	m = re.search(pattern, line)
	if m:
		line = line[:m.span()[0]]
		m2 = re.search(r"\(.*?\)", line)
		if m2:
			line = line[:m2.span()[0]].strip()
		return line.strip()
	return ''

def extract_method3(line):
	# pattern = r"(Corp)|(Inc)\.?"
	# pattern = r"Company"
	# pattern = r"(Ltd\.?)|(Limited)"
	pattern = r"Group"
	m = re.search(pattern, line)
	if m:
		line = line[:m.span()[1]]
		m2 = re.search(r"\(.*?\)", line)
		if m2:
			line = line[:m2.span()[0]].strip()
		return line.strip()
	return ''

def extract_comname(line):
	return extract_method1  (line)
	
def append(filename, comname):
	with open(FIN_PATH + filename, 'a') as f:
		f.write(comname)
	with open(HAVARD_PATH + filename, 'a') as f:
		f.write(comname)


def main():
	total, count = 0, 0
	for filename in [f for f in os.listdir(TODO_PATH) if f.endswith(".txt")]:
		with open(TODO_PATH + filename, 'r') as f:
			line = f.readline()
			comname = extract_comname(line)
			if comname:
				count += 1
				append(filename, comname)
				os.rename(TODO_PATH + filename, DONE_PATH + filename)
		total += 1
		if total % 10000 == 0:
			print("%s/%s" % (count, total))
	print("%s/%s" % (count, total))



def check_extracted():
	count, total = 0, -1
	with SAS7BDAT(ROOT + 'unmerged.sas7bdat') as f:
		for row in f:
			total += 1
			if total == 0:
				continue
			filename = str(row[0])[:-1] + 'txt'
			if os.path.isfile(DONE_PATH + filename):
				count += 1
			else:
				os.rename(DIR_PATH + filename, TODO_PATH + filename)
	print("%s/%s" % (count, total))


if __name__ == "__main__":
	main()
	# check_extracted();
	pass


