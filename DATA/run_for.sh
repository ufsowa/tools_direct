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
	name="run$i"
	#    screen -dmS "$name"
	#    screen -S $name -X screen /bin/bash -c "$SRC/run > log.run"
	$SRC/run > log.run
	cd ${DEST}
    fi
done

screen -ls
sleep 5s
echo "Print log.run:"
cd ${DEST}
for i in ${NAME}*; do
    cd $i
    echo $i
    name="run$i"
    tail -1 log.run
    cd ${DEST}
done
