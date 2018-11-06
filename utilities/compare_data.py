# Compare the difference between new and old data
#

from config import ROOT

NEW = ROOT + "data_fin.txt"
OLD = ROOT + "CC_extracted_data.txt"
EXPORT = ROOT + "result.txt"

# Object containing the data of a transcript
class Item(object):
	def __init__(self, data):
		self.data = data
		self.filename = int(data[0])
		self.ticker = data[1]
		self.date = data[2]
		self.time = data[3]
		self.PresWordNum	= int(data[4])
		self.PresCharNum  	= int(data[5])					
		self.QandAWordNum	= int(data[6])
		self.QandACharNum	= int(data[7])
		self.ShortWords		= int(data[8])
		self.LongWords		= int(data[9])
		self.NegWordsPres	= int(data[10])
		self.NegWordsQA		= int(data[11])
		self.NegWordsTotal	= int(data[12])

	def __str__(self):
		s = str(self.data[0])
		for i in range(4, 13):
			s += '\t' + str(self.data[i])
		s += '\n'
		return s


def load_dataset(path):
	dataset = {}
	with open(path, 'r') as f:
		for line in [l for l in f.readlines()[1:] if l != '\n']:
			data = [d for d in line.replace('\n', '').split('\t') if d]
			try:
				item = Item(data)
				dataset[item.filename] = item
			except Exception as e:
				print(e)
		f.close()
	return dataset


# Get the difference between two records
def compare(item1, item2):
	data = []
	for i in range(4):
		data.append(item1.data[i])
	data.append(item1.PresWordNum	- item2.PresWordNum	)	
	data.append(item1.PresCharNum  	- item2.PresCharNum )
	data.append(item1.QandAWordNum	- item2.QandAWordNum)
	data.append(item1.QandACharNum	- item2.QandACharNum)
	data.append(item1.ShortWords	- item2.ShortWords	)			
	data.append(item1.LongWords		- item2.LongWords	)		
	data.append(item1.NegWordsPres	- item2.NegWordsPres)
	data.append(item1.NegWordsQA	- item2.NegWordsQA	)			
	data.append(item1.NegWordsTotal	- item2.NegWordsTotal)	

	return Item(data)


def main():
	new = load_dataset(NEW)
	old = load_dataset(OLD)
	result = {}
	for key in old:
		if key in new:
			item = compare(new[key], old[key])
			result[item.filename] = item

	with open(EXPORT, 'w', encoding='utf8') as f:
		f.write("filename\tPresWordNum\tPresCharNum\tQandAWordNum\tQandACharNum\tShortWords\tLongWords\tNegWordsPres\tNegWordsQA\tNegWordsTotal\n")
		for key in result:
			f.write(str(result[key]))
		f.close()


if __name__ == "__main__":
	main()