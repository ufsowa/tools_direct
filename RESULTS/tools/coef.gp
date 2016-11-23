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

#	plot [0.1:0.9] '$1' u (1.0-\$4):(-(16.0*\$6/\$5)/\$2) w lp
#	plot [0.1:0.9] '$1' u (\$4):(\$7/\$2) w lp
#	plot [0.1:0.9] '$1' u 4:((\$7 - 1.0/\$8)) w lp
	unset key

	FILES='$@'
	print FILES
	plot [0:][:] for [ data in FILES ] data u (\$4):(\$7/\$2) w lp t data,\
		'D_maning' u 1:(\$3*0.05) w p pt 6,\
		'D_maa.dat' u (\$1-0.05):(\$4*0.027) w p pt 6



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


function plot_v {
    new_name=${1%%.*}.jpeg
    new_name=${new_name##*_}

    y0=`awk '{print $3}' $1`
    echo "
	#set terminal jpeg;
	unset key
	Y0='$y0'
	FILES='$@'
	print FILES, Y0
	plot for [ data in FILES] data u (sqrt(\$2)):((\$3)) w p ps 2 pt 6 lc 1
	pause -1
    " > to_plot
    gnuplot to_plot
}

files=`ls *.vel`
plot_v $files

files=`ls *.coef`
plot_d $files

#for i in $files;
#do
#    plot_d $i
#done
