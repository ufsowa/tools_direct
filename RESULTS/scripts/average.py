#!/usr/bin/env python

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

import libs.base as tools


name=sys.argv[1]
types=int(sys.argv[2])
grid=float(sys.argv[3])
every=float(sys.argv[4])
no_points=float(sys.argv[5])
name_out=name.replace('step','avg')
fout=open(name_out,'a')

data=np.loadtxt(name, unpack=True)
step=np.mean(data[0])
time=np.mean(data[1])

XF=data[2];
X=data[3];
V=data[4];
ATOMS=[]; ALL=[]; TOT=[]; STECH=[];
for i in np.arange(5,(5+types),1):
    ATOMS.append(data[i])

ATOMS=np.array(ATOMS)

#print ATOMS
#V=data[4];
#A=data[5];
#B=data[6];
#C=data[7];
for i in ATOMS:
    if(len(TOT)==0):
	TOT=i
    else:
	TOT=TOT+i;
TOT=np.array(TOT)
#print TOT

for i in ATOMS:
    c=i/TOT;
#[float(x)/float(y) if y else float(0) for x,y in zip(i,TOT)]
    STECH.append(c)

ALL=TOT+V;cv=V/ALL;c=TOT/ALL;

STECH=np.array(STECH)

L=X[0];P=X[-1];
#plt.plot(X,XF,'x');

CROSS=tools.cross(X,c,cv)
#print CROSS, L, P

for i in range(0,len(CROSS),1):
    x0=CROSS[i];Ldx=X[0];Pdx=X[-1];
    if((i+1)<len(CROSS)):
	Pdx=x0+abs(x0+CROSS[i+1])/8.0
    else:
	Pdx=X[-1]

    if((i-1)>=0):
	Ldx=x0-abs(x0-CROSS[i-1])/8.0
    else:
	Ldx=X[0]
#    print "f:", i,x0,Ldx,Pdx,L,P
    new_x=np.arange( Ldx,Pdx,0.1)

    CV=np.interp(new_x,X,cv)
    C=np.interp(new_x,X,c)
#    plt.plot(new_x,CV);plt.plot(new_x,C);plt.show();
    
    b=tools.convolute_x0(new_x,C,CV)
#    print b
    tmpP=b[0]+(b[1])*3.5
    tmpL=b[0]-(b[1])*3.5

    VL=np.interp(tmpL,X,cv)
    VP=np.interp(tmpP,X,cv)

    if(VL>VP):
	if( (tmpP > L) and (tmpP < P) ):
	    L=tmpP

    if(VL<VP):
	if( (tmpL < P) and (tmpL > L) ):
	    P=tmpL

    #print i,VL,VP, tmpL,tmpP,L,P

points = np.where((X >= L)  & (X<=P))
x=X[points]
xf=np.interp(x,X,XF)

#plt.plot(X,XF,'--');plt.plot(x,xf,'o'); plt.show();

DATA=[]; nr_col=4;
for col in data[nr_col:]:
    y=np.array(col[points])
    tryb='noplot'
    if(nr_col >= 8 and nr_col<=7):
	tryb='plot'
    new_x=[];new_xf=[];new_y=[];
    if(nr_col >= 4 and nr_col <= 6):
	new_x,new_y=tools.move_avg(x,y,grid,every,no_points,tryb)		#concnetrations
    elif(nr_col >= 7 and nr_col <= 18):
#	tmp_xf,tmp_y=tools.smooth_data(xf,y,2000,11,2,0,"plot")
#	new_xf=np.interp(new_x,x,xf)
#	new_y=np.interp(new_xf,tmp_xf,tmp_y)
	new_xf,new_y=tools.move_avg(xf,y,grid,every,1,tryb)		#fluxes		-> need other parameters becouse of gauss shape
	if len(DATA[2])==0:
	    DATA[2]=new_xf;
    elif(nr_col >= 19 and nr_col <= 20):
	new_x,new_y=tools.move_avg(x,y,grid,every,no_points,tryb)		#events
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

