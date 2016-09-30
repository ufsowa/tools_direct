#!/usr/bin/env bash

# input variables
MANY="2"
f_step="$PWD/step.input"
files="stech"
NAME="couple_"

# paths
SOURCE=${PWD}"/../INPUTS/"
DEST=${PWD}"/data/"
TEMPLATE=${PWD}"/template"
STEP="NULL"
ST=$PWD

#main body
mkdir -p $DEST
cd ${SOURCE}
for i in ${NAME}*; do
    STEP=`awk -v stech=$i 'BEGIN{out=-1}{if($1==stech){out=1}}END{if(out>=0){print out}else{print "NULL"}}' $f_step`
    outputs="Created: $stech $STEP"
    if [ $STEP != "NULL" ];then
    mkdir -p ${DEST}${i}
    fi
done

cd ${DEST}
for i in ${NAME}*; do
    cp -R -u ${TEMPLATE}/* $i
    cd $i/template
    sed -i 's/NAZWA/c_SAMPLE/' run_sim
    outputs=$outputs" | Pepared: $i $stech $STEP"
    cd ${DEST}
done

cd ${SOURCE}
for i in ${NAME}*; do
    cd $i
    GOAL=${DEST}/$i/inputs
    if [ -d $GOAL ]; then
	L=${GOAL}/left
	R=${GOAL}/right
	cd lside
	for file in $(ls -p *${files}.xyz | grep -v / | tail -${MANY}); do
	    cp $file ${L}
	done
        outputs=$outputs" | Inputs-> L: "`ls $L |wc -l`
	cd ../pside
	for file in $(ls -p *${files}.xyz | grep -v / | tail -${MANY}); do
	    cp $file ${R}
	done
        outputs=$outputs" R: "`ls $R |wc -l`
        cd ..
    fi
done

echo $outputs