#!/usr/bin/gnuplot

plot '1000002.step' u (($5+$6)/2):10, '1000002.avg' u 3:7

#'1000002.step' u (($5+$6)/2):8, '1000002.avg' u 3:5

pause -1