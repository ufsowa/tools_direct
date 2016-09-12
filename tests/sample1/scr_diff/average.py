#!/usr/bin/env python

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

import lib_diff as tools


name=sys.argv[1]
name_out=name.replace('step','avg')
fout=open(name_out,'a')

data=np.loadtxt(name, unpack=True)
step=np.mean(data[0])
time=np.mean(data[1])

X=data[4];
dX=X[1]-X[0];
V=data[5];
A=data[6];
B=data[7];
TOT=A+B;
ca=[float(x)/float(y) if y else float(0) for x,y in zip(A,TOT)]
cb=[float(x)/float(y) if y else float(0) for x,y in zip(B,TOT)]
TOT=A+B+V;cv=V/TOT;c=(A+B)/TOT
p0=np.median(X)
x=np.arange(X[0],p0,0.1)
CV=np.interp(x,X,cv)
C=np.interp(x,X,c)
bL=tools.convolute_x0(x,C,CV)
x=np.arange(p0,X[-1],0.01)
CV=np.interp(x,X,cv)
C=np.interp(x,X,c)
bP=tools.convolute_x0(x,C,CV)
L=bL[0]+(bL[1])*1.5
P=bP[0]-(bP[1])*1.5
#SAMPLE_BORDER.append(L); SAMPLE_BORDER.append(P);
#x=np.arange(L,P,dX)
points = np.where((X > L)  & (X<P))
x=X[points]

DATA=[]; nr_col=5;
for col in data[5:]:
    y=col[points]
    tryb='noplot'
    if(nr_col >= 5 and nr_col<=7):
	tryb='plot'

    tmp_x,tmp_y=tools.move_avg(x,y,2.0,1.0,2.0,tryb)
#    new_x,new_y=tools.fit_data(x,y,1000,301,3)
#    new_x,new_y=tools.move_avg(new_x,new_y,1.0,0.5,2.0)

    new_x,new_y=tools.smooth_data(tmp_x,tmp_y,1000,301,3,0,tryb)

    if(len(DATA)==0):
	STEP=np.ones_like(new_x)*step
	TIME=np.ones_like(new_x)*time
	DATA.append(STEP)
	DATA.append(TIME)
	DATA.append(new_x)
    DATA.append(new_y)
    nr_col+=1;
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

