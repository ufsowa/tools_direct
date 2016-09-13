#!/usr/bin/env bash

MY_PTH=$PWD
rm *.jpeg
cd ..

function plot_c {
    new_name=${1%%.*}
    new_name=${new_name##*_}
#    if [ $new_name -le 100 ]; then
    gnuplot -e "
	set terminal jpeg;
	plot [:][:] '$1' u 3:(\$5/(\$5+\$6)) w lp,\
	'$1' u 3:(\$6/(\$5+\$6)) w lp
    " > $MY_PTH/$new_name.jpeg
#    fi
}

function plot_N {
    new_name=${1%%.*}
    new_name=${new_name##*_}
    if [ $new_name -le 100 ]; then
    gnuplot -e "
	set terminal jpeg;
	plot '$1' u ((\$5+\$6)/2.0):8 w lp,\
	'$1' u ((\$5+\$6)/2.0):9 w lp
    " > $MY_PTH/$new_name.jpeg
    fi
}

function plot_Nv {
    new_name=${1%%.*}
    new_name=${new_name##*_}
    if [ $new_name -le 100 ]; then
    gnuplot -e "
	set terminal jpeg;
	plot '$1' u ((\$5+\$6)/2.0):7 w lp
    " > $MY_PTH/$new_name.jpeg
    fi
}


function plot_cv {
    new_name=${1%%.*}.jpeg
    new_name=${new_name##*_}
    gnuplot -e "
	set terminal jpeg;
	plot [:][:0.01] '$1' u 3:(\$4/(\$4+\$5+\$6)) w lp
    " > $MY_PTH/$new_name.jpeg
}

files=`ls *.avg`

for i in $files;
do
    plot_c $i
done
