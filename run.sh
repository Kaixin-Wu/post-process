#!/bin/bash

######################################################
#                                                    #
#    Author              : WU Kaixin                 #
#    Date                : 2017/11/15                #
#    Email               : wukaixin_neu@163.com      #
#    Last Modified in    : NEU NLP lab., Shenyang    #
#                                                    # 
#            Usage:  ./run.sh infile                 #
#                                                    #
######################################################

decode_file=$1
tmp_file1=${decode_file}.tmp1
tmp_file2=${decode_file}.tmp2
out_file=${decode_file}.out
hyp=hyp
target=./Evaluation/data/


#step1: Repalce Generalize Labels 
python Postprocess-FunctionSets.py -replaceGen \
       --result $decode_file \
       --trans valid.en.gen.d2y.out.ord \
       --outfile $tmp_file1


#step2: BPE Merge
sed -i 's/@@ //g' $tmp_file1
echo -e "BPE Merge done...\n"


#step3: Chinese Detokenization
python Postprocess-FunctionSets.py -detoken \
       --infile $tmp_file1 \
       --outfile $tmp_file2 


#step4: Replace Special tokens
python Postprocess-FunctionSets.py -replaceSpe -log \
       --infile $tmp_file2 \
       --repdict repdict \
       --outfile $out_file 

rm $tmp_file1  $tmp_file2

cp $out_file $hyp
mv $hyp $target

