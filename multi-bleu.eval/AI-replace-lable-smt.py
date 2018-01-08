#coding:utf-8
import sys
import argparse
import re
reload(sys)
sys.setdefaultencoding('utf-8')

def parse_args():
	tips =   "######################################################################\n"
	tips +=  "# Function            : Replace Generalize Label in SMT Result       #\n"
	tips +=  "# Author              : Bojie Hu                                     #\n"
	tips +=  "# Email               : hubojie1993@163.com                          #\n"
	tips +=  "# Date                : 10/8/2017                                    #\n"
	tips +=  "# Last Modified in    : Neu NLP lab., Shenyang                       #\n"
	tips +=  "######################################################################\n"
	
	parser = argparse.ArgumentParser(description = tips,formatter_class= argparse.RawDescriptionHelpFormatter)
	parser.add_argument("--result", help="SMT Result with Generalize Label")
	parser.add_argument("--trans", help="Preprocessed file with Trans.")
	parser.add_argument("--outfile",help="Out File")
	return parser.parse_args()

def StartProcess(options):
	resultFile = open(options.result)
	transFile = open(options.trans)
	outfile = open(options.outfile,"w")
	lineNo = 0
	
	while(1):
		resultLine = resultFile.readline()
		transLine = transFile.readline()
		lineNo+=1
		if (not resultLine) or (not transLine):
			break
		result = resultLine.strip()
		trans = transLine.strip()
		results = result.split()
		trans = trans.split(' |||| ')
		p=re.compile(r'{.*?}')
		
		if len(trans) < 2:
			outfile.write(result+"\n")
			continue
		
		labelDict = {}
		for m in p.finditer(trans[1]):
			segs=m.group().replace('{',"").replace('}',"").split(" ||| ")
			labelDict[segs[3]] = segs[2]
		
		for (i,word) in enumerate(results):
			if word in labelDict:
				results[i] = labelDict[word]
		
		outfile.write(" ".join(results)+"\n")

	resultFile.close()
	transFile.close()
	outfile.close()
	
if __name__ == '__main__':
	StartProcess(parse_args())
