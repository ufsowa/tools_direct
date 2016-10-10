#!/usr/bin/env bash

# input variables
MANY="5"
NID="kirk"
NAME="couple_"

# paths
f_step="$PWD/step.input"
SOURCE=${PWD}"/../INPUTS"
DEST=${PWD}"/data"
TEMPLATE=${PWD}"/template"
STEP="NULL"
ST=$PWD

#main body
echo "$SOURCE" > $ST/scripts/PTH_SRC

mkdir -p $DEST
cd ${SOURCE}
for i in ${NAME}*; do
    STEP=`awk -v stech=$i 'BEGIN{out=-1}{if($1==stech){out=1}}END{if(out>=0){print out}else{print "NULL"}}' $f_step`
    if [ $STEP != "NULL" ];then
	outputs="Created: $stech $STEP"
	mkdir -p ${DEST}/$i
    fi
done

cd ${DEST}
for i in ${NAME}*; do
    STEP=`awk -v stech=$i 'BEGIN{out=-1}{if($1==stech){out=1}}END{if(out>=0){print out}else{print "NULL"}}' $f_step`
    if [ $STEP != "NULL" ];then
	rm -r $i/*
	cp -r ${TEMPLATE}/* $i
	cd $i/template
	sed -i 's/NAZWA/'${NID}'_SAMPLE/' run_sim
	outputs=$outputs" | Prepared: $i $stech $STEP"
	cd ${DEST}
    fi
done

echo $outputs