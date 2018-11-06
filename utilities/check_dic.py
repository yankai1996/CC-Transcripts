import sys

havard, lm = sys.argv[1], sys.argv[2]

havardDic = {}

havardCount, lmCount, included = 0, 0, 0



with open(havard) as f:
	for line in f.readlines():
		havardDic[line] = 1
		havardCount += 1

with open(lm) as f:
	for line in f.readlines():
		lmCount += 1
		if line in havardDic:
			included += 1

print("%s: %s words, %s: %s words.\n%s words included" \
	% (havard, havardCount, lm, lmCount, included))
