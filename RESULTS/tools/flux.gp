#!/usr/bin/env bash

MY_PTH=$PWD
rm *.jpeg
#cd ..

function plot_F {
    new_name=${1%%.*}
    new_name=${new_name##*_}
    echo "
	FILES='$@'
	print FILES
	
#	set palette model HSV defined ( 0 0 1 1, 1 1 1 1 )
	plot [:] '$1' u 4:8 w p pt 6 t '$1',\
		'$2' u 4:8 w l t '$2',\
		'$1' u 4:9 w p pt 6 ps 1 t '$1',\
		'$2' u 4:9 w l t '$2',\
		'$1' u 4:10 w p pt 6 ps 1 t '$1',\
		'$2' u 4:10 w l t '$2'


#	     for [ data in FILES ] data u (4:(\$7/(\$6+\$7)):2 w p pt 4 ps 2 palette t data
    pause -1
    " > to_plot
    gnuplot to_plot
}


function plot_Fd {
    new_name=${1%%.*}
    new_name=${new_name##*_}
    echo "
	FILES='$@'
	print FILES
	
#	set palette model HSV defined ( 0 0 1 1, 1 1 1 1 )
	plot [40:70] '$1' u 4:14 w p pt 6 notitle,\
		'$2' u 4:14 w l lc -1 t 'V',\
		'$1' u 4:15 w p pt 6 ps 1 notitle,\
		'$2' u 4:15 w l lc 1 t 'A',\
		'$1' u 4:16 w p pt 6 ps 1 notitle,\
		'$2' u 4:16 w l lc 2 t 'B2'


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
	plot [-0.2:0.2] for [ data in FILES ] data u ((\$3-49.5)/(2.0*sqrt(\$2))):(\$5/(\$5+\$6)) w p t data,\
	     for [ data in FILES ] data u ((\$3-49.5)/(2.0*sqrt(\$2))):(\$6/(\$5+\$6)) w p t data
    pause -1
    " > to_plot
    gnuplot to_plot
}

#files=`ls *.avg`
#plot_N $files
files=`ls 1000.step`
#plot_Ns $files

for i in $files;
do
    smooth=${i%%.*}.avg
    plot_F $i $smooth
done
