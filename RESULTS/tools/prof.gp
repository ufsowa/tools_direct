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
	plot [:] '$1' u (\$3):(\$7/\$2) w lp
#	plot [0.1:0.9] '$1' u 4:((\$7 - 1.0/\$8)) w lp

	pause -1
    " > to_plot
    gnuplot to_plot

#$MY_PTH/$new_name.jpeg
#    fi
}

function plot_Ns {
    new_name=${1%%.*}
    new_name=${new_name##*_}
    echo "
	FILES='$@'
	print FILES
	
	set palette model HSV defined ( 0 0 1 1, 1 1 1 1 )
	plot [:] '$1' u (\$4):(\$6/(\$6+\$7)):2 w p pt 6 ps 1 palette notitle,\
		'$2' u (\$4):(\$6/(\$6+\$7)):2 w l lc -1 t 'A',\
		'$1' u (\$4):(\$7/(\$6+\$7)):2 w p pt 6 ps 1 palette notitle,\
		'$2' u (\$4):(\$7/(\$6+\$7)):2 w l lc 1 t 'B'


#	     for [ data in FILES ] data u (4:(\$7/(\$6+\$7)):2 w p pt 4 ps 2 palette t data
    pause -1
    " > to_plot
    gnuplot to_plot
}


function plot_N {
    new_name=${1%%.*}
    new_name=${new_name##*_}
    echo "
	FILES='$@'
	print FILES
	set palette model HSV defined ( 0 0 1 1, 1 1 1 1 )
	plot [:] for [ data in FILES ] data u (\$4):(\$6/(\$7+\$6)):2 w l palette notitle,\
	     for [ data in FILES ] data u (\$4):(\$7/(\$7+\$6)):2 w l palette notitle
    pause -1
    " > to_plot
    gnuplot to_plot
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
    new_name=${1%%.*}
    new_name=${new_name##*_}
    echo "
	FILES='$@'
	print FILES
	set palette model HSV defined ( 0 0 1 1, 1 1 1 1 )
	plot [:][:] for [ data in FILES ] data u 4:(\$5/(\$7+\$5+\$6)):2 w l palette notitle
    pause -1
    " > to_plot
    gnuplot to_plot
}


files=`ls *.avg`
#plot_N $files
plot_cv $files

files=`ls *.step`
#plot_N $files
plot_cv 1000.step


#for i in $files;
#do
#    smooth=${i%%.*}.avg
#    plot_Ns $i $smooth
#done
