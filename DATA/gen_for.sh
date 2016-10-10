#!/usr/bin/env bash

#VARIABLES
NAME="couple_"
DEST=${PWD}"/data/"
SRC=$PWD/scripts
f_step="$PWD/step.input"

cd ${DEST}
for i in ${NAME}*; do
    STEP=`awk -v stech=$i 'BEGIN{out=-1}{if($1==stech){out=1}}END{if(out>=0){print out}else{print "NULL"}}' $f_step`
    if [ $STEP != "NULL" ];then
	cd $i
	echo $i
	$SRC/generate 5
	cd ${DEST}
    fi
done
