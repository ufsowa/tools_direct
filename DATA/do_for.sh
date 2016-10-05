#!/usr/bin/env bash

# input variables
MANY="5"
NID="nst"
f_step="$PWD/step.input"
NAME="couple_"

# paths
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
    outputs="Created: $stech $STEP"
    if [ $STEP != "NULL" ];then
    mkdir -p ${DEST}/$i
    fi
done

cd ${DEST}
for i in ${NAME}*; do
    cp -R -u ${TEMPLATE}/* $i
    cd $i/template
    sed -i 's/NAZWA/'${NID}'_SAMPLE/' run_sim
    outputs=$outputs" | Pepared: $i $stech $STEP"
    cd ${DEST}
done

echo $outputs