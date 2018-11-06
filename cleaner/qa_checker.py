# Check how to devide the transcripts into two parts
# 

import os
import io
import time
import re
import random
import shutil
from config import ROOT

DIR_PATH = ROOT
QA_PATH = DIR_PATH + "QA/"
EMPTY_PATH = DIR_PATH + "empty/"
MV_PATH = QA_PATH
# MV_PATH = EMPTY_PATH


PATTERN = [
	"<strong>Question-and-Answer",
	"<strong>Question-And-Answer",
	"<strong>Questions-And-Answer",
	"Questions &amp; Answers",
	"<strong>Q&amp;A",
	"Question and Answer",
	"Question And Answer",
	"QUESTIONS AND ANSWERS",
	"QUESTION AND ANSWER"
]

RE_PATTERN = r"(<strong>)?Question(s?)[-\s–]*(([Aa]nd)|(&amp;))?[-\s–]*[Aa]nswer"


def detect_no(f):
	t = f.read()
	reg = r"To sponsor a Seeking Alpha transcript[\s\S]*?\n"
	if re.search(reg, t):
	 	return False
	return True

def detect_qa(f):
	t = f.read()
	if re.search(RE_PATTERN, t):
		# print(f)
		# time.sleep(2)
		# m = re.search(RE_PATTERN, t)
		# print(m.group())
		return True

	# elif t.find(PATTERN[-1]) > -1:
	# 	return True
	# elif t.find(PATTERN[-2]) > -1:
	# 	return True

	# t = f.readline()
	# if t.find("Q&A") > -1:
	# 	return True

	return False


def detect_empty(f):
	t = f.read()
	reg = r"The audio will stream live while the call.*replayed upon its completion"
	# reg = r"The following audio is from a conference call that will begin on(.*)The audio will stream live while the call is active, and can be replayed upon its completion"
	# reg = r"The audio is live-streaming while the call is active, and can be replayed upon its completion"
	if re.search(reg, t):
	 	# print(f)
	 	return True
	return False

def detect(f):
	# return detect_empty(f)
	# return detect_qa(f)
	return detect_qa(f)


def count_pattern():

	TO = os.path.expanduser("~/Downloads/clean/")

	pattern = "THE INFORMATION CONTAINED HERE IS A TEXTUAL"
	pattern_reg = r"\n.*?Operator.*?\n.*Our first question.*\n"

	def overwrite(t, filename):
		# t = t.replace(pattern, "<strong>Question-and-Answer Session</strong>")
		t = re.sub(pattern_reg, "\n<strong>Question-and-Answer Session</strong>\n", t)
		with io.open(TO + filename, 'w') as temp:
			temp.write(t)
			temp.close()

	regCount = 0

	counts = {}
	total = 0
	for filename in [f for f in os.listdir(DIR_PATH) if f.endswith(".txt")]:
		total += 1
		with io.open(DIR_PATH + filename, 'r+', encoding='utf8') as f:
			t = f.read()
			count = t.count(pattern)
			# if count > 0:
			# # # # 	print(f)
			# # # # 	if re.search(r"<strong>Question(.*)</strong>\n", t):
			# # # # 		regCount += 1
			# # # # 	# print(f)
			# # 	overwrite(t, filename)
			# # if count == 1:
			# # 	# print(f)
			# 	os.rename(DIR_PATH + filename, MV_PATH + filename)
			if not count in counts:
				counts[count] = 0
			counts[count] += 1
			f.close()
	print(counts, sum(counts.values()), '/', total)
	print(regCount)


def append():
	for filename in [f for f in os.listdir(DIR_PATH) if f.endswith(".txt")]:
		with io.open(DIR_PATH + filename, 'a', encoding='utf8') as f:
			f.write("\n<strong>Question-and-Answer Session</strong>\n")
			f.close()




def main():
	total, count = 0, 0
	for filename in [f for f in os.listdir(DIR_PATH) if f.endswith(".txt")]:
		total += 1
		with io.open(DIR_PATH + filename, 'r', encoding='utf8') as f:
			if detect(f):
				count += 1
				os.rename(DIR_PATH + filename, MV_PATH + filename) # move file
	print("%s/%s" % (count, total))

def test():
	t = "<strong>Question –and- Answer Session</strong>"
	# t = "<strong>Question-and-Answer Session</strong>"
	print(ord('-'))
	print(ord('—'))
	if re.search(RE_PATTERN, t):
		print("True")

if __name__ == "__main__":
	# append()
	main()
    # test()
    # count_pattern()


