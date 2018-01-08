#!/bin/bash

######################################################
#                                                    #
#    Author              : WU Kaixin                 #
#    Date                : 2017/11/17                #
#    Email               : wukaixin_neu@163.com      #
#    Last Modified in    : NEU NLP lab., Shenyang    #
#                                                    # 
#          Usage:  ./run_chrF.sh infile              #
#                                                    #
######################################################


decode_file=$1
tmp_file=${decode_file}.tmp
out_file=${decode_file}.out

ref_file=./ref.nogen
src_gen_file=./src.gen.tran

#step1: BPE Merge
sed -i 's/@@ //g' $decode_file
echo -e "BPE merge done...\n"

#step2: Replace ". . ." with "…"
sed -i 's/\. \. \./…/g' $decode_file
echo -e "Remove special tokens done...\n"

#step3: Repalce generalize labels
python AI-replace-lable-smt.py \
	--result $decode_file \
	--trans $src_gen_file \
	--outfile $tmp_file
echo -e "Repalce generalize labels done...\n"

#step4 char segment
python3 char_seg.py --inZH $tmp_file --outZH $out_file 

#step5: multi-bleu
bleu=`perl multi-bleu.perl $ref_file < $out_file`
echo $bleu

rm $tmp_file


