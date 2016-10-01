#!/usr/bin/env python

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

import lib_diff as tools


name=sys.argv[1]
name_out=name.replace('all','avg')
fout=open(name_out,'a')

data=np.loadtxt(name, unpack=True)

#step=np.mean(data[0])/1000.0
#time=np.mean(data[1])

x=data[3]
time=data[1]

DATA=[];nr_col=4;
for col in data[4:]:
    y=col
    if(nr_col==4 or nr_col==6 or nr_col==7):
	y=y/time

    tmp_x,tmp_y=tools.move_avg(x,y,0.1,0.01,10.0)
    new_x=tmp_x;new_y=tmp_y;
#    new_x,new_y=tools.fit_data(x,y,1000,301,3)
#    new_x,new_y=tools.move_avg(new_x,new_y,1.0,0.5,2.0)
#    new_x,new_y=tools.smooth_data(tmp_x,tmp_y,1000,301,3,0)

    if(len(DATA)==0):
	DATA.append(new_x)
    DATA.append(new_y)
    nr_col+=1
np.savetxt(fout, np.transpose(DATA) )

#for key in sorted(AVG):
#    AVG[key]=AVG[key]/NUM[key]
#    np.savetxt(fout, AVG[key][None] )

#wait=input("wiat..")


#ID=0;AVG=dict();NUM=dict()
#for x in data[4]:
#    row=data[:,ID]
#    if x in AVG:
#	old=AVG[x]
#	new=old+row
#	AVG[x]=new
#	NUM[x]+=1
#    else:
#	AVG[x]=row
#	NUM[x]=1
#    ID+=1

