#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import numpy as np
import re
import argparse

def usage_help():
    
    print 
    tips =   "##########################################################################\n"
    tips +=  "# Usage: option[-raplaceGen or -detoken or ...] arguments                #\n"
    tips +=  "#        -replaceGen --result result --trans trans --outfile outfile     #\n"
    tips +=  "#        -detoken --infile infile --outfile outfile                      #\n"
    tips +=  "#        -replaceSpe --infile infile --repdict dict --outfile outfile    #\n"
    tips +=  "#                                                                        #\n"
    tips +=  "#                                                                        #\n"
    tips +=  "# Function Description:                                                  #\n"
    tips +=  "#   replaceGen: Replace Generalize Label in NMT Result.                  #\n"
    tips +=  "#   detoken: Chinese Detokenization.                                     #\n"
    tips +=  "#   replaceSpe: Remove and Replace Special Strings in NMT Result.        #\n"
    tips +=  "##########################################################################\n"
    print tips

def parse_args():

    tips =   "##########################################################################\n"
    tips +=  "# Function            : Function Sets of Post-Process(Chinese).          #\n"
    tips +=  "# Author              : WU Kaixin                                        #\n"
    tips +=  "# Email               : wukaixin_neu@163.com                             #\n"
    tips +=  "# Date                : 11/11/2017                                       #\n"
    tips +=  "# Last Modified in    : NEU NLP lab., Shenyang                           #\n"
    tips +=  "#                                                                        #\n"
    tips +=  "# Usage: option[-replaceGen or -detoken or ...] arguments                #\n"
    tips +=  "#        -replaceGen --result result --trans trans --outfile outfile     #\n"
    tips +=  "#        -detoken --infile infile --outfile outfile                      #\n"
    tips +=  "#        -replaceSpe --infile infile --repdict dict --outfile outfile    #\n"
    tips +=  "#                                                                        #\n"
    tips +=  "#                                                                        #\n"
    tips +=  "# Function Description:                                                  #\n"
    tips +=  "#   replaceGen: Replace Generalize Label in NMT Result.                  #\n"
    tips +=  "#   detoken: Chinese Detokenization.                                     #\n"
    tips +=  "#   replaceSpe: Remove and Replace Special Strings in NMT Result.        #\n"
    tips +=  "##########################################################################\n"

    parser = argparse.ArgumentParser(description=tips, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-replaceGen", dest="replaceGen", action="store_true", help="Replace Generalize Label in NMT Result.")
    parser.add_argument("-detoken", dest="detoken", action="store_true", help="Chinese Detokenization.")
    parser.add_argument("-replaceSpe", dest="replaceSpe", action="store_true", help="Remove and Replace Special Strings in NMT Result.")  
    parser.add_argument("-log", dest="log", action="store_true", help="Recode Log Information.") 
    
    parser.add_argument("--infile", "-i", required=False, default=None, help="Input File.(detoken, replaceSpe)") 
    parser.add_argument("--result", required=False, default=None, help="NMT Result with Generalize Label.(repalceGen)")
    parser.add_argument("--trans", required=False, default=None, help="Preprocessed File with Trans.(replaceGen)")
    parser.add_argument("--outfile", "-o", required=False, default=None, help="Output File.(detoken, replaceGen, replaceSpe)")
    parser.add_argument("--repdict", required=False, default=None, help="Dict File, Replace Dict Which Contains Special Strings.(replaceSpe)") 
   
    options = parser.parse_args()
    if options.replaceGen:
        if not (options.result and options.trans and options.outfile):
            print >> sys.stderr, "\n[ERROR]: the command line paramters exists error..."
            print >> sys.stderr, "[Correct Usage]: -replaceGen --result result --trans trans --outfile outfile"
            usage_help()
            sys.exit(-1)

    if options.detoken:
        if not (options.infile and options.outfile):
            print >> sys.stderr, "\n[ERROR]: the command line paramters exists error..."
            print >> sys.stderr, "[Correct Usage]: -detoken --infile infile --outfile outfile"
            usage_help()
            sys.exit(-1)
    
    if options.replaceSpe:
        if not(options.infile and options.repdict and options.outfile):
            print >> sys.stderr, "\n[ERROR]: the command line paramters exists error..."
            print >> sys.stderr, "[Correct Usage]: -replaceSpe --infile infile --repdict dict --outfile outfile"
            usage_help()
            sys.exit(-1)

    return options

def startConvert(options):
   
    if options.replaceGen:
        replaceGen(options)
    
    if options.detoken:
        detoken(options)
    
    if options.replaceSpe:
        replaceSpe(options)

def replaceSpe(options):
     
    if options.log:
        logfile = open("log", "w")

    infile = open(options.infile)
    dictfile = open(options.repdict)
    outfile = open(options.outfile, "w")
    repdict = []
    
    for line in dictfile:
        repPair = line.strip().split("||||")
        repdict.append((repPair[0], repPair[1]))
    repdict.sort(key=lambda item: len(item[0]), reverse=True) 

    for i, line in enumerate(infile.readlines()):
        
        if (i+1) % 1000 == 0:
            print >> sys.stderr, "\r      Processed %d lines." % (i+1)
            sys.stderr.flush()

        line = line.strip()
        for item in repdict:
            if item[0] in line:
                line = line.replace(item[0], item[1])
                if options.log:
                    print >> logfile, "Row %d: %s ==> %s" % (i+1, item[0], item[1])
        
        print >> outfile, line.strip() + " "
    
    print >> sys.stderr, "replaceSpe done...\n"
    if options.log:
        logfile.close()     
    infile.close()
    dictfile.close()
    outfile.close()    

def replaceGen(options):
    resultfile = open(options.result)
    transfile = open(options.trans)
    outfile = open(options.outfile, "w")

    lineNum = 0
    for result, trans in zip(resultfile.readlines(), transfile.readlines()):
        
        if (lineNum+1) % 1000 == 0:
            print >> sys.stderr, "\r      Processed %d lines." % (lineNum+1)
            sys.stderr.flush()
        lineNum += 1

        if (not result.strip()) or (not trans.strip()):
            print("Blank line...")
            break

        lineGen = trans.strip().split(" |||| ")
        if len(lineGen) < 2:
            print >> outfile, result.strip()
            continue

        p = re.compile(r'{.*?}')
        genDict = {}

        resultTokenList = result.strip().split()
        for m in p.finditer(lineGen[1]):
            tags = m.group().replace("{","").replace("}","").split(" ||| ")
            genDict[tags[3]] = tags[2]

        for i, token in enumerate(resultTokenList):
            if genDict.get(token) is not None:
                resultTokenList[i] = genDict[token]
        
        print >> outfile, " ".join(resultTokenList)
    
    print >> sys.stderr, "replaceGen done...\n"    
    resultfile.close()
    transfile.close()
    outfile.close()

def detoken(options):
    
    infile = open(options.infile)
    outfile = open(options.outfile, "w")
    en2ch_dict = {",": "，", ".": "。", "?": "？", "!": "！", ";": "；", "(": "（", ")": "）", "…": "…… ", "\"": "\" "}

    for lineNum, line in enumerate(infile.readlines()):
        
        outLine = ""
        tokenList = line.strip().split()
        for token in tokenList:
            if en2ch_dict.get(token) is not None:
                outLine += en2ch_dict[token]
            else:
                outLine += token
        
        outLine = outLine.replace("。。。", "…… ")               ### remove special tags
        #print outLine
        print >> outfile, outLine

        if (lineNum+1) % 1000 == 0:
            print >> sys.stderr, "\r      Processed %d lines."% (lineNum+1)
            sys.stderr.flush()
    
    print >> sys.stderr, "detoken done...\n"
    infile.close()
    outfile.close()

if __name__ == "__main__":
    
    if len(sys.argv) <= 1:
        usage_help()
        sys.exit(-1)

    startConvert(parse_args())

