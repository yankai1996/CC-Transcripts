# Count words in each transcript according to given dictionary 
#

import os
import shutil
from config import ROOT

DICT_PATH = ROOT + "dict/negativelist.txt"
# DICT_PATH = ROOT + "dict/FinNegWords.txt"
INFO_PATH = ROOT + "info/"
PRES_PATH = ROOT + "Pres/"
QA_PATH = ROOT + "QA/"
EXPORT_PATH = ROOT + "Havard/"
# EXPORT_PATH = ROOT + "FinDict/"


# remove punctuations, convert to lower case,  and strip
def purify(t):
	t = re.sub(r"(\"|“|”|\?|!|\n|--)", ' ', t)
	t = re.sub(r"((,|\.|:|;|) )", ' ', t)
	t = re.sub(r" +", ' ', t)
	t = t.lower().strip()
	return t


class Dictionary(object):

	def __init__(self, path):
		self.dict = {}
		with open(path, 'r', encoding='utf8') as f:
			for word in [x.replace('\n', '') for x in f.readlines()]:
				self.dict[word] = True

	def has(self, word):
		if word in self.dict:
			return True
		return False


class Counter(object):

	def __init__(self, dictionary):
		self.dictionary = dictionary

	def run(self, info_filename):
		order = ['PresWordNum', 
			'PresCharNum',
			'QandAWordNum',
			'QandACharNum',
			'ShortWords',
			'LongWords',
			'NegWordsPres',
			'NegWordsQA',
			'NegWordsTotal'
			]
		result = {}
		for i in order:
			result[i] = 0

		pres_path = PRES_PATH + info_filename[:-4] + "-Pres.txt"
		qa_path = QA_PATH + info_filename[:-4] + "-QA.txt"

		with open(pres_path, 'r') as f:
			t = purify(f.read())
			words = [w for w in t.split(' ') if w != '']
			result['PresWordNum'] = len(words)
			result['PresCharNum'] = len(''.join(words))
			for word in words:
				if self.dictionary.has(word):
					result['NegWordsPres'] += 1
				if len(word) <= 3:
					result['ShortWords'] += 1
				elif len(word) >= 7:
					result['LongWords'] += 1
			f.close()

		with open(qa_path, 'r') as f:
			t = purify(f.read())
			words = [w for w in t.split(' ') if w != '']
			result['QandAWordNum'] = len(words)
			result['QandACharNum'] = len(''.join(words))
			for word in words:
				if self.dictionary.has(word):
					result['NegWordsQA'] += 1
				if len(word) <= 3:
					result['ShortWords'] += 1
				elif len(word) >= 7:
					result['LongWords'] += 1
			f.close()

		result['NegWordsTotal'] = result['NegWordsPres'] + result['NegWordsQA']

		export_file = EXPORT_PATH + info_filename
		shutil.copyfile(INFO_PATH + info_filename, export_file)
		with open(export_file, 'a', encoding='utf8') as f:
			f.write('\n')
			for i in order:
				f.write("%s: %d\n" % (i, result[i]))
			f.close()

		# print(result)


def test():
	counter = Counter(Dictionary(DICT_PATH))
	total = 0
	for filename in [f for f in os.listdir(INFO_PATH) if f.endswith(".txt")]:
		if total > 5:
			break
		total += 1
		
		pres_path = PRES_PATH + filename[:-4] + "-Pres.txt"
		qa_path = QA_PATH + filename[:-4] + "-QA.txt"

		with open(pres_path, 'r') as f:
			t = strip(f.read())
			words = [w for w in t.split(' ') if w != '']
			the = [w for w in words if w == 'the']
			a = [w for w in words if w == 'a']
			temp = [w for w in words if w == 'to']
			print(len(the), len(a), len(temp))
			f.close

	print(total)


def main():
	dictionary = Dictionary(DICT_PATH);
	counter = Counter(dictionary)

	total = 0
	for filename in [f for f in os.listdir(INFO_PATH) if f.endswith(".txt")]:
		# if total > 5:
		# 	break
		total += 1
		if total % 10000 == 0:
			print(total)
		counter.run(filename)

	print(total)

if __name__ == "__main__":
	main()	
	# test()