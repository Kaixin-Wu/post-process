# ambyer

import sys
import argparse
import codecs


def parse_args():
    tips  = "######################################################################\n"
    tips += "# Function            : segment zh lines to characters               #\n"
    tips += "# Author              : AmbyerHan                                    #\n"
    tips += "# Email               : amberhan0301@163.com                         #\n"
    tips += "# Date                : 11/10/2017                                   #\n"
    tips += "# Last Modified in    : Neu NLP lab., Shenyang                       #\n"
    tips += "######################################################################\n"

    parser = argparse.ArgumentParser(description=tips, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--inZH', '-zh', required = True, metavar = 'PATH', dest = 'fin', default = None, help = 'the input file which is segmented by words')
    parser.add_argument('--outZH', '-ozh', required = True, metavar = 'PATH', dest = 'fot', default = None, help = 'the out file which is segmented by words')
    return (parser.parse_args())


def isDigitOrLiteral(word):
    return all(ord(ch) < 128 for ch in word)

def segmenter(line):
    """
    :param line: a line that with or without segmented by words
    :return: a list that segmented by char
    """
    seg = []
    eng = 0
    ln = (line.strip().split(' ')) # .decode("utf-8")
    for words in ln:
        if isDigitOrLiteral(words):
            seg.append(words)
            eng += 1
        else:
            word = tuple(words)
            for w in word:
                seg.append(w)
    return seg, eng


def main(args):
    n = 0
    for ln in args.fin:
        words, t = segmenter(ln)

        argdic.fot.write(' '.join(words) + '\n')
        n += t
    print('%d' % n)

if __name__ == "__main__":
    argdic = parse_args()

    argdic.fin = open(argdic.fin, 'r', encoding = "UTF-8")
    argdic.fot = open(argdic.fot, 'w', encoding = "UTF-8")

    print('processing...')
    main(argdic)
    print('done...')

    argdic.fin.close()
    argdic.fot.close()