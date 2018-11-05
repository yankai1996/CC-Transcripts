# Method that tokenizes a given string and add 'NOT_' tags
# References old_code/Lasso/news4_Text_preProc.py
# 
# E.g.
# >>> s = "I don't know why there are so many 'NOT' tags."
# >>> GetWords(s)
# >>> ['do', 'NOT_know', 'NOT_why', 'NOT_many', 'NOT_tag']
#

import nltk
from nltk.corpus import wordnet
import re

SpesWords=['during',
'versus',
'since',
'year-over-year',
'towards',
'without',
'against',
'upon',
'capex',
'sg&a',
'among',
'year-to-date',
'r&d',
'non-gaap',
'non-cash',
'toward',
'seasonality',
'g&a',
'financials',
'p&l',
'annualized',
'timeframe',
'unless',
'q&a',
'near-term',
'merrill',
'double-digit',
'pre-tax',
'quarter-over-quarter',
'quarter-to-quarter',
'onto',
'm&a',
'and/or',
'full-year',
'stock-based',
'longer-term',
'rollout',
'via',
'inline',
'to-date',
'year-on-year',
'breakeven',
'pretax',
'libor',
'high-end',
'opex',
'non-recurring',
'third-party',
'offline',
'mark-to-market',
'ought',
'weisel',
'directionally',
'single-digit',
'after-tax',
'multi-year',
'incrementally',
'standalone',
'three-year',
'proactively',
'in-house',
'keybanc',
'anytime',
'dilutive',
'top-line',
'same-store',
'year-to-year',
'five-year',
'year-ago',
'non-core',
'payout',
'multi',
'well-positioned',
'go-forward',
'non-operating',
'securitization',
'reinvest',
's&p',
'opportunistically',
'pre',
'congrats',
'apples-to-apples',
'mid-s',
'reinvestment',
'value-added',
'mid-year',
'mid-teens',
'bottom-line',
'roadmap',
'd&a',
'double-digits',
'anecdotally',
'run-rate',
'broad-based',
'start-up',
'suntrust',
'whereby',
'charge-offs',
'bb&t',
'analytics',
'net-net',
'mid-single',
'ramp-up',
'yearend',
'transactional',
'six-month',
'book-to-bill',
'non-performing',
'low-end',
'back-end',
'front-end',
'single-digits',
'break-even',
'lumpiness',
'realignment',
'non-interest',
'quarter-on-quarter',
'backend',
'quarter-end',
'subprime',
'quarter-by-quarter',
'wedbush',
'canaccord',
'deleveraging',
'pick-up',
'topline',
'catch-up',
'month-to-month',
'annualize',
'best-in-class',
'thirdquarter',
'consumables',
'in-store',
'aftermarket',
'multiyear',
'sell-through',
'stats',
'sub-prime',
'high-quality',
'charge-off',
'company-wide',
'dd&a',
'alittle',
'carryover',
'mid-point',
'share-based',
'transformational',
'c&i',
'prior-year',
'de-leveraging',
'go-to-market',
'reinvesting',
'next-generation',
'time-to-time',
'lifecycle',
'cannibalization',
'impactful',
'industry-leading',
'non-accrual',
'fourthquarter',
'cross-selling',
'markdowns',
'avondale',
'e&p',
'three-month',
'buy-back',
'nonrecurring',
'extinguishment',
'nine-month',
'resellers',
'destocking',
'mortgage-backed',
'reinvested',
'exclusivity',
'pushback',
'build-out',
'comparables',
'craig-hallum',
'industry-wide',
'deleverage',
'win-win',
'in-process',
'markdown',
'renegotiation',
'acquisition-related',
'deepwater',
'companywide',
'cost-cutting',
'non-strategic',
'reseller',
'seamlessly',
'prospectively',
'year-and-a-half',
're-pricing',
'de-stocking',
'favorability',
'rollouts',
'decision-making',
'on-demand',
'predominately',
'affordability',
'barnett',
'end-user',
'back-to-school',
'micro-cap',
'non-recourse',
'non-residential',
'securitized',
'virtualization',
'billable',
'repricing',
'web-based',
'company-owned',
'loan-to-value',
'multi-family',
'true-up',
'broadpoint',
'issuer-sponsored',
'pre-opening',
'definitively',
'non-performers',
'reoccur',
'cross-sell',
'debt-to-capital',
'long-standing',
'counterparties',
'franchisee',
'non-traditional',
'on-time',
'ratably',
'counterparty',
'ourbusiness',
'quo',
'secondquarter',
'admin',
'amit',
'bolt-on',
'fall-off',
'in-line',
'mid-continent',
'securitizations',
'asset-backed',
'brean',
'multi-channel',
'stat',
'wholly-owned',
'ecommerce',
'fourth-quarter',
'risk-based',
'second-half',
'debt-to-ebitda',
'kindof',
'mid-market',
'mid-term',
'reimbursable',
'pershare',
'tuck-in',
'end-market',
'market-by-market',
'rebalancing',
'ten-year',
'buy-backs',
'outstandings',
'payouts',
'renegotiations',
'renewables',
'run-off',
'tolerability',
'mid-size',
'annualizing',
'littlebit',
'non-accruals',
'nonperforming',
'reprice',
'sarbanes-oxley',
'conferencing',
'cyclicality',
'noncash',
'performance-based',
'timeframes',
'unhedged',
'de-leverage',
'anincrease',
'bottomline',
'flow-through',
'mid-to-high',
'pre-clinical',
'pro-forma',
'right-size',
'all-in-all',
'benchmarking',
'standout',
'asset-based',
'outperformance',
'reengineering',
'equity-based',
'mid-range',
'rebalance',
'customization',
'fee-based',
'high-volume',
'market-leading',
'distributable',
'first-quarter',
'optionality',
'underperformance']

def GetWords(raw, File_tag=''):
		
	raw = raw.lower()
	raw = re.sub(r"[$\"0-9]", '', raw)
	raw = re.sub(r"[\.,!\?]", ' ! ', raw)
	raw = re.sub(r"\s((a)|(an)|(the))\s", ' ', raw)

	raw=raw.replace('food and drug administration','fda')


	raw = raw.replace("won't", 'will not')
	raw = raw.replace("can't", 'cannot')
	raw = raw.replace("i'm", 'i am')
	raw = raw.replace("ain't", 'is not')
	raw = raw.replace("'ll", ' will')
	raw = raw.replace("n't", ' not')
	raw = raw.replace("'ve", ' have')
	raw = raw.replace("'s", ' is')
	raw = raw.replace("'re", ' are')
	raw = raw.replace("'d", ' would')
	
	frTolk=nltk.word_tokenize(raw)
		
	NegSet = ['t','n\'t','no','not','isn','aren','don','doesn','didn','wasn','weren','shan','hasn','haven','hadn','cann','couldn','shouldn','wouldn','mustn','mightn']
	PreposSet = ['aboard',	'about',	'above',	'across',	'after',	'against',	'along',	'amid',	'among',	'anti',	'around',	'as',	'at',	'before',	'behind',	'below',	'beneath',	'beside',	'besides',	'between',	'beyond',	'but',	'by',	'concerning',	'considering',	'despite',	'down',	'during',	'except',	'excepting',	'excluding',	'following',	'for',	'from',	'in',	'inside',	'into',	'like',	'minus',	'near',	'of',	'off',	'on',	'onto',	'opposite',	'outside',	'over','out',	'past',	'per',	'plus',	'regarding',	'round',	'save',	'since',	'than',	'through',	'to',	'toward',	'towards',	'under',	'underneath',	'unlike',	'until',	'up',	'upon',	'versus',	'via',	'with',	'within',	'without']
	PronounSet = ['all',	'another',	'another',	'any',	'anybody',	'anyone',	'anything',	'both',	'each',	'each',	'either',	'everybody',	'everyone',	'everything',	'he',	'her',	'hers',	'herself',	'him',	'himself',	'his',	'i',	'it',	'its',	'itself','me',	'mine',	'myself',	'neither',	'no',	'nobody',	'none',	'nothing',	'one',	'other',	'others','our',	'ours',	'ourselves',	'she',	'some',	'somebody',	'someone',	'something','the',	'that',	'their',	'theirs',	'them',	'themselves',	'these',	'they',	'this',	'those','there',	'us',	'we',	'what',	'whatever',	'which',	'whichever',	'who',	'whoever',	'whom',	'whomever',	'whose',	'you',	'yours','your',	'yourself',	'yourselves']
	SkeepSet = ["am","is","are",'to','okey','thank','thanks']
	DelSet = ['yes',' thanks',' thank','and','as','but','or','so','because','million','dollars','transcript','transcripts','ip','hi','le','ov',	'op',	'al',	'ev',	'ye',	'ad',	'av',	'ex',	'un',	'aw',	'en',	'ag',	'eq',	'el',	'ar',	'ey',	'id',	'im',	'ap',	'er',	'ir',	'od',	'ii',	'ow',	'ab',	'aa',	'ik',	'ic',	'ep',	'eb',	'af',	'oc',	'eg',	'il',	'em',	'ug',	'ed',	'ac',	'ax',	'ol',	'iv',	'oi',	'yu',	'om',	'ub',	'ut',	'ot',	'ea',	'ib',	'ig',	'az',	'eo',	'oa',	'uc',	'uz',	'ix',	'et',	'ob',	'um',	'ah',	'es',	'ew',	'ia',	'ox',	'ud',	'uf',	'ur']
	
	typos = []
	tokens_YesNeg = []
	Bigrams_YesNeg = []
	DictCountList = []
	
	prevWord = ''
	currWord = ''
	tag = ''
	SaveBigram = 0
	verb = 0 
	PrevTypo = 0
	PredPrepos = 0
	
	pos_set = ['v','n','a','r']
	
	for word in frTolk:
		if word in NegSet: 
			tag='NOT_'
			prevWord=''
			continue
			
		if (word.find('!')>-1): 
			tag=''
			currWord=''
			prevWord=''
			continue
		if word in SkeepSet or not word.isalpha() or len(word)==1:
			continue
		if (word in DelSet) or (word in PronounSet):
			prevWord=''
			continue
		currWord=word
		
			
		if len(wordnet.synsets(word))==0:
			if (word in SpesWords):					
				word=File_tag+tag+word
				tokens_YesNeg=tokens_YesNeg+[word]
				DictCountList=DictCountList+[word]
				
			if (word in PreposSet):
				SaveBigram=1
				
			if (prevWord != '' and SaveBigram==1 and currWord != ''  and not (prevWord in PreposSet)) : 
				Bigrams_YesNeg=Bigrams_YesNeg+[tag+prevWord+' '+currWord]
				prevWord=currWord
			else:
				prevWord=''
			
			continue
			
		else:
			pos_to_use=''
			num_of_lemmas=0
			for p in pos_set:
				tmp=len(wordnet.synsets(word,pos=p))
				if tmp>num_of_lemmas:
					num_of_lemmas=tmp
					pos_to_use=p

			lemma=wordnet.morphy(word, pos_to_use)	
			
			if pos_to_use=='v':	verb=1					
			else: verb=0
				
			currWord=lemma
		
			w=File_tag+tag+lemma	
			tokens_YesNeg=tokens_YesNeg+[w]		
			DictCountList=DictCountList+[lemma]
			
			if (prevWord != '') and (currWord != '') and not (prevWord in PreposSet) :
				Bigrams_YesNeg=Bigrams_YesNeg+[tag+prevWord+' '+currWord]	
				
				
			prevWord=currWord
			PredPrepos=0
			PrevTypo=0

	return 	[tokens_YesNeg,DictCountList]


def main():
	def test(s):
		print(GetWords(s))

	test("This is not a good idea.")
	test("I can't agree more...")
	test("let's try another string, shall we?")
	test("I don't know why there are so many 'NOT' tags.")
	test("")


if __name__ == "__main__":
	main()