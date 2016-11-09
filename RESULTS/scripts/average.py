#!/usr/bin/env python

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

import libs.base as tools


name=sys.argv[1]
grid=float(sys.argv[2])
step=float(sys.argv[3])
no_points=float(sys.argv[4])
name_out=name.replace('step','avg')
fout=open(name_out,'a')

data=np.loadtxt(name, unpack=True)
step=np.mean(data[0])
time=np.mean(data[1])

XF=data[2];
X=data[3];

V=data[4];
A=data[5];
B=data[6];
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
L=bL[0]+(bL[1])*2.5
P=bP[0]-(bP[1])*2.5
#SAMPLE_BORDER.append(L); SAMPLE_BORDER.append(P);
#x=np.arange(L,P,dX)
points = np.where((X > L)  & (X<P))
x=X[points]
xf=np.interp(x,X,XF)

#plt.plot(X,XF,'x');plt.plot(x,xf,'o'); plt.show();

DATA=[]; nr_col=4;
for col in data[nr_col:]:
    y=np.array(col[points])
    tryb='noplot'
    if(nr_col >= 8 and nr_col<=7):
	tryb='plot'
    new_x=[];new_xf=[];new_y=[];
    if(nr_col >= 4 and nr_col <= 6):
	new_x,new_y=tools.move_avg(x,y,grid,step,no_points,tryb)		#concnetrations
    elif(nr_col >= 7 and nr_col <= 18):
#	tmp_xf,tmp_y=tools.smooth_data(xf,y,2000,11,2,0,"plot")
#	new_xf=np.interp(new_x,x,xf)
#	new_y=np.interp(new_xf,tmp_xf,tmp_y)
	new_xf,new_y=tools.move_avg(xf,y,grid,step,no_points,tryb)		#fluxes		-> need other parameters becouse of gauss shape
	if len(DATA[2])==0:
	    DATA[2]=new_xf;
    elif(nr_col >= 19 and nr_col <= 20):
	new_x,new_y=tools.move_avg(x,y,grid,step,no_points,tryb)		#events
    else:
	continue;
#    new_x,new_y=tools.fit_data(x,y,1000,301,3)
#    new_x,new_y=tools.move_avg(new_x,new_y,1.0,0.5,2.0)
#    new_x,new_y=tools.smooth_data(tmp_x,tmp_y,1000,301,3,0,tryb)

    if(len(DATA)==0):
	STEP=np.ones_like(new_x)*step
	TIME=np.ones_like(new_x)*time
	DATA.append(STEP)
	DATA.append(TIME)
	DATA.append(new_xf)
	DATA.append(new_x)
    DATA.append(new_y)
    nr_col+=1;
np.savetxt(fout, np.transpose(DATA) )

#plt.plot(X,XF,'x');plt.plot(DATA[3],DATA[2],'o'); plt.show();

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

