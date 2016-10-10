#!/bin/bash


plot(){
    echo -e "
	B=95
	E=105
	S=0
	I=200
	file='$1'
	equi='$2'
	set hidden3d
	
	set ticslevel 0
	set zrange [:]
	set ytics scale 10
	set ytics 5
	set mytics 5
	set grid ytics
	set grid mytics

#        splot file every :100:20:100:80 u 2:4:(\$6/(\$6+\$7+\$8)) w l

#pause -1
#	stats file every :::1 using (\$9) nooutput
#	totalV= int (STATS_sum)
#	stats file every :::1 using (\$10) nooutput
#	totalA= int (STATS_sum)
#	stats file every :::1 using (\$11) nooutput
#	totalB= int (STATS_sum)
#	stats file every :::1 using (\$21) nooutput
#	total= int (STATS_sum)
#
#	print totalV,totalA,totalB,(totalV+totalA+totalB), total
#
#	stats equi every :::1 using (\$9) nooutput
#	totalV= int (STATS_sum)
#	stats equi every :::1 using (\$10) nooutput
#	totalA= int (STATS_sum)
#	stats equi every :::1 using (\$11) nooutput
#	totalB= int (STATS_sum)
#	print totalV,totalA,totalB,(totalV+totalA+totalB)
#
#sinks sample
#        splot file every :I:B:S:E u 2:4:((\$9 - \$12)/1) w l,\
#		file every :I:B:S:E u 2:4:((\$10 - \$13)/1) w l,\
#		file every :I:B:S:E u 2:4:((\$11 - \$14)/1) w l

#sinks lattice
#	splot file every :I:B:S:E u 2:4:((\$15 - \$18*1)/1) w l,\
#		file every :I:B:S:E u 2:4:((\$16 - \$19*1)/1) w l,\
#		file every :I:B:S:E u 2:4:((\$17 - \$20*1)/1) w l

#sinks lattice equi
#		splot equi every :100::100 u 2:4:((\$12)/1) w p,\
#		equi every :100::100 u 2:4:((\$13)/1) w p,\
#		equi every :100::100 u 2:4:((\$14)/1) w p

#lattice equi P
#		splot equi every :100:10:100:30 u 2:4:((\$15 - \$18)/1) w l,\
#		equi every :100:10:100:30 u 2:4:((\$16 - \$19)/1) w l,\
#		equi every :100:10:100:30 u 2:4:((\$17 - \$20)/1) w l

#eventy e
#        splot file every :I:B:S:E u 2:4:((\$15*0 + \$22*1)/1) w l


#profiles
        splot file every :I:B:S:E u 2:4:(\$6/(\$6+\$7+\$8)) w l,\
		file every :I:B:S:E u 2:4:(\$7/(\$6+\$7+\$8)) w l
#		file every :I:B:S:E u 2:4:(\$8/(\$6+\$7+\$8)) w l

#lattice + sample
#        splot file every :100::100 u 2:4:((\$15 + \$9)/1) w l,\
#		file every :100::100 u 2:4:((\$16 + \$10)/1) w l,\
#		file every :100::100 u 2:4:((\$17 + \$11)/1) w l

#lattice
#        splot file every :I:B:S:E u 2:4:((\$15*0 + \$18*1)/1) w l,\
#		file every :I:B:S:E u 2:4:((\$16*0 + \$19*1)/1) w l,\
#		file every :I:B:S:E u 2:4:((\$17*0 + \$20*1)/1) w l

#sample
#        splot file every :I:B:S:E u 2:4:((\$9 + \$12*0)/1) w l,\
#		file every :I:B:S:E u 2:4:((\$10 + \$13*0)/1) w l,\
#		file every :I:B:S:E u 2:4:((\$11 + \$14*0)/1) w l

#        splot file every :100:20:100:80 u 2:((\$4+\$5)/2.):((\$9 - \$12)/\$2) w l,\
#		file every :100:20:100:80 u 2:((\$4+\$5)/2.):((\$9 + \$12)/\$2) w l

#		file every :100:20:100:80 u 2:((\$4+\$5)/2.):(\$9/\$2) w l
#		file every :10:20:100:80 u 2:((\$4+\$5)/2.):(\$10/\$2) w l
#		file every :10:20:100:80 u 2:((\$4+\$5)/2.):(\$11/\$2) w l

	pause -1
    " > to_plot
    gnuplot to_plot
}


hist=`ls *hist.dat`
biny=`ls *bin.dat`

flux=($hist)
equi=($biny)


for (( i=0; i<=${#hist[*]}; i++ )); do
    echo ${flux[i]} ${equi[i]}
    plot ${flux[i]} ${equi[i]}
done;

#http://stackoverflow.com/questions/18583180/gnuplot-how-to-load-and-display-single-numeric-value-from-data-file
