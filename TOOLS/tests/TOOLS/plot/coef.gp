#!/usr/bin/env bash

MY_PTH=$PWD
rm *.jpeg
#cd ..

function plot_d {
    new_name=${1%%.*}
    new_name=${new_name##*_}
#    if [ $new_name -le 100 ]; then
    echo "
#	plot [0.1:0.9][:] '$1' u 4:((\$5+\$6)) w l
#	plot '$1' u 4:5 w lp,'$1' u 4:6 w lp,'$1' u 4:(1.0/\$8) w lp

	plot [0.1:0.9] '$1' u (1.0-\$4):(-(16.0*\$6/\$5)/\$2) w lp
#	plot [0.1:0.9] '$1' u (1.0-\$4):(-\$7/\$2) w lp
#	plot [0.1:0.9] '$1' u 4:((\$7 - 1.0/\$8)) w lp

	pause -1
    " > to_plot
    gnuplot to_plot

#$MY_PTH/$new_name.jpeg
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
	plot [:][:0.02] '$1' u 3:(\$4/(\$4+\$5+\$6)) w lp
    " > $MY_PTH/$new_name.jpeg
}

files=`ls *.coef`

for i in $files;
do
    plot_d $i
done
