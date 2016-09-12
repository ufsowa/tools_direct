#!/usr/bin/env bash

export LC_ALL=C

MY_PTH=$PWD
MY_FILE="vel.dat"
rm vel.dat
cd ..

function plot_d {
    new_name=${1%%.*}
    new_name=${new_name##*_}
#    if [ $new_name -le 100 ]; then
    gnuplot -e "
	set terminal jpeg;
	plot [:][:] '$1' u 4:7 w lp
    " > $MY_PTH/$new_name.jpeg
#    fi
}

files=`ls *.vel`

for i in $files;
do
    cat $i >> $MY_PTH/$MY_FILE
done

cd $MY_PTH
sort -n -k 1,1 $MY_FILE > tmp; mv tmp $MY_FILE