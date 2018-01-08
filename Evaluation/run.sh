#!/bin/bash

######################################################
#                                                    #
#    Author              : WU Kaixin                 #
#    Date                : 2017/11/12                #
#    Email               : wukaixin_neu@163.com      #
#    Last Modified in    : Neu NLP lab., Shenyang    #
#                                                    #
######################################################


## Wrap your translation result into sgm file
./tools/wrap_xml.pl zh data/src.sgm CommitSystem < data/hyp > data/hyp.sgm

## Calculate BLEU score for the translation result
[ ! -s score ] && mkdir score
./tools/mt-score-main.py -rs data/ref.sgm -hs data/hyp.sgm -ss data/src.sgm --id commit | tee score/commit.score

