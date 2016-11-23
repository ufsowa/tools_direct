#!/usr/bin/env python

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

import libs.base as tools


name=sys.argv[1]
grid=float(sys.argv[2])
step=float(sys.argv[3])
points=float(sys.argv[4])
st=float(sys.argv[5])
ed=float(sys.argv[6])
name_out=name.replace('all','avg')
fout=open(name_out,'a')

data=np.loadtxt(name, unpack=True)

#step=np.mean(data[0])/1000.0
#time=np.mean(data[1])

x=data[3]

#x=raw[st<=raw]
#x=x[x<=ed]
time=data[1]
#time=np.interp(x,raw,time)

DATA=[];nr_col=4;
for col in data[4:]:
#    y=np.interp(x,raw,col)
    y=col
    if(nr_col==4 or nr_col==6 or nr_col==7):
	y=y/time

    ID=np.isfinite(y)
    myy=y[ID]
    myx=x[ID]
    
    new_x,new_y=tools.move_avg(myx,myy,grid,step,points,"plot")		#concnetrations

#    tmp_x,tmp_y=tools.move_avg(myx,myy,0.1,0.01,3.0)
#    new_x=tmp_x;new_y=tmp_y;
#    new_x,new_y=tools.fit_data(myx,myy,1000,301,3)
#    new_x,new_y=tools.move_avg(new_x,new_y,1.0,0.5,2.0)
#    new_x,new_y=tools.smooth_data(myx,myy,1000,301,3,0,"plot")

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

