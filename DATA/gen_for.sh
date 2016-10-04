#!/usr/bin/env bash

#VARIABLES
NAME="couple_"
DEST=${PWD}"/data/"
SRC=$PWD/scripts

cd ${DEST}
for i in ${NAME}*; do
    cd $i
    echo $i
    $SRC/generate 1 5
    cd ${DEST}
done
