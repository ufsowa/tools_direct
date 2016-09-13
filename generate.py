#!/usr/bin/env python

import math
import matplotlib.pyplot as plt
import numpy as np

def gen_pkt(x,D,t):
    C0=0.2
    Cs=0.8
    Cx = (Cs-C0)*(1.0 -  math.erf(x/2.0/(np.sqrt(D*t))))/2.0 + C0
    return Cx

D=2.0;time=1.0;N=620.0
x=np.arange(-20,20,0.1)
A=[];B=[];V=[];V1=[];V2=[];
OUT=open("0hist.dat","a")

for i in x:
    a=0;b=0;v=0;v1=0;v2=0;
    if(abs(i)<15):
	Cs=0.8;C0=0.2;
	a = (Cs-C0)*(1.0 -  math.erf(i/2.0/(np.sqrt(D*time))))/2.0 + C0
	a=a*N
	Cs=0.2;C0=0.8;
	b = (Cs-C0)*(1.0 -  math.erf(i/2.0/(np.sqrt(D*time))))/2.0 + C0
	b = b*N
	Cs=1.0;C0=0.0;
	v1 = (Cs-C0)*(1.0 -  math.erf((i+15)/2.0/(np.sqrt(0.3*time))))/2.0 + C0
	v1 = v1*N
	Cs=0.0;C0=1.0;
	v2 = (Cs-C0)*(1.0 -  math.erf((i-15)/2.0/(np.sqrt(0.3*time))))/2.0 + C0
	v2 = v2*N
    else:
	v=N

    A.append(a)
    B.append(b)
    V.append(v)
    V1.append(v1)
    V2.append(v2)



tmp=[e1 + e2 for e1,e2 in zip(V1,V2)]
V=[e1 + e2 for e1,e2 in zip(V,tmp)]
for i in range(0,len(x)):
    OUT.write("%f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f\n" % (1,0,0,x[i],x[i]+1,V[i],A[i],B[i],1,2,3,1,2,3,1,2,3))
OUT.write("\n")
for i in range(0,len(x)):
    OUT.write("%f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f\n" % (2,0,0,x[i],x[i]+1,V[i],A[i],B[i],1,2,3,1,2,3,1,2,3))

plt.plot(x,A,'.-')
plt.plot(x,B,'.-')
plt.plot(x,V,'.-')
plt.show()