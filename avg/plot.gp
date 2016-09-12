#!/usr/bin/gnuplot

name='coef.avg'
plot name u 1:($4-$5*1.6)

pause -1