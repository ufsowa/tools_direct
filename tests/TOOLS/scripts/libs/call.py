#!/usr/bin/env python

import base as prep
import numpy as np
from scipy.integrate import quad
from scipy.misc import derivative

############## Global basic variables ############
	#files
out_name1="coef.tmp"
OUT_DIF=open(out_name1,"a")
out_name2="vel.tmp"
OUT_VEL=open(out_name2,"a")

	#profil
STEP=0
TIME=0
X_cent=[]
X0_init=[]
SAMPLE_BORDER=[]
NORMA=[]
TRYB=0;
	#fit
FIT_BORDER=[]			#keeps range for A profile y(x) if 0.0 |< x >| 1.0
FIT=[]		#keeps polynominal representation for A profile
X_MOVE=0.0
##################################################

def reset_global_var():
    global STEP; STEP=0
    global TIME; TIME=0
    global X0_init;X0_init=[]
    global SAMPLE_BORDER;SAMPLE_BORDER=[]
    global NORMA;NORMA=[]
    global FIT_BORDER;FIT_BORDER=[]
    global FIT; FIT=[]
    global X_MOVE; X_MOVE=0.0;

def x0(hist):
    reset_global_var();
    x=0.0
    global STEP; global TIME; global X_cent; global X0_init; global NORMA; global SAMPLE_BORDER;
    global FIT_BORDER; global FIT; global TRYB;
    STEP=hist[0][0]
    TIME=hist[0][1]
    X=hist[:,2]
    dX=X[1]-X[0]
    V=hist[:,3]
    B=hist[:,4]
    A=hist[:,5]
    TOT=A+B;
    ca=[float(x)/float(y) if y else float(0) for x,y in zip(A,TOT)]
    cb=[float(x)/float(y) if y else float(0) for x,y in zip(B,TOT)]
    TOT=A+B+V;cv=V/TOT;c=(A+B)/TOT
    L=X[0]
    P=X[-1]
    SAMPLE_BORDER.append(L); SAMPLE_BORDER.append(P);
    x=np.arange(L,P,dX)
    CA=np.interp(x,X,ca)
    CB=np.interp(x,X,cb)
    X0_init=prep.convolute_x0(x,CA,CB)
    x=x-X0_init[0]
#    T=prep.ferc(x)
#    prep.plot(x,(CA,CB))

    nCA,norm_a=prep.norm_data(CA);
    nCB,norm_b=prep.norm_data(CB);
    NORMA.append(norm_a); NORMA.append(norm_b);

#    Xa,aCB=prep.move_avg(x,nCB,dX,1.0,2.0);
#    Xa,aCA=prep.move_avg(x,nCA,dX,1.0,2.0);
    Xa=x;aCA=nCA;aCB=nCB;

    if(TRYB):
	prep.plot(x,(nCA,nCB))
	prep.plot(Xa,(aCA,aCB))
	prep.plt.show()

#    CB=prep.trans_data(aCB);
#    CA=prep.trans_data(aCA);
#    T=trans_data(T);
#    prep.plot(CA,(Xa,))

#    garbage,CB=prep.move_avg(Xa,CB,dX,2.0,3.0);
#    X,CA=prep.move_avg(Xa,CA,dX,2.0,3.0);
    X=x


#    fit_border_B=prep.set_borders(x,CB);
#    fit_border_A=prep.set_borders(x,CA);
#    FIT_BORDER.append(fit_border_A);FIT_BORDER.append(fit_border_B)

#    xt,T=move_avg(x,T,dX/2.0,dX*3.0);
#    prep.plot(CA,(X,),'.')
#    garbage,fit_A=prep.fit_data(X,CA,7);
#    X,fit_Ai=prep.fit_data_inv(X,CA,7);

    first_fit_A=prep.fit_data(x,nCA,order='linear')
    first_fit_Ai=prep.fit_data(nCA,x,order='linear')

    if(TRYB):
	prep.plot(nCA,(first_fit_Ai(nCA),),'-')
	prep.plot(nCA,(x,),'.')
	prep.plt.show()
	prep.plot(x,(first_fit_A(x),),'-')
	prep.plot(x,(nCA,),'.')
	prep.plt.show()

    first_dyA=cal_poch(x,first_fit_A)


    X_MOVE=optimal(first_fit_Ai);
    x=x+X_MOVE
    X_cent=x

#    print X_MOVE
    fit_A=prep.fit_data(x,nCA,order='linear')
    fit_Ai=prep.fit_data(nCA,x,order='linear')
    FIT.append(fit_Ai);FIT.append(fit_A);

    if(TRYB):
	prep.plot(nCA,(first_fit_Ai(nCA),),'-')
	prep.plot(nCA,(fit_Ai(nCA),),'-o')
	prep.plt.show()

#    new_c=prep.myrange()
#    yA=prep.functionXc(new_c,fit_Ai)
#    yB=functionXc(new_c,fit_B)
#    dyA=cal_poch(new_c,fit_A)
#    print len(aCA),len(x)
#    prep.plot(aCA,(Xa,),'o')
#    prep.plot(new_c,(yA,),'-')
#    prep.plt.show()

    dyA=cal_poch(x,fit_A)

    xtoplt=np.ones_like(dyA)*X_MOVE

    if(TRYB):
	prep.plt.plot(xtoplt,dyA,'-')
	prep.plot(X,(first_dyA,),'.')
	prep.plot(x,(dyA,),'.-')
	prep.plt.show()

    return 0

def diff():
    global X_MOVE, NORMA, TRYB;
    step=STEP;time=TIME
    p=X0_init
    x=X_cent
    ai=FIT[0]
    a=FIT[1]
    stech_scale=NORMA[0]; 
    YL=stech_scale[0]; YR=stech_scale[1];
    norma=YL-YR;

    p0=p[0];pw=p[1];
    DER_R=0.0


#    new_c=np.arange(0.0,1.01,0.01)
#    dyA=cal_poch(prep.functionXc(new_c,ai),a)
#    xtoplt=np.ones_like(dyA)*X_MOVE
#    prep.plt.plot(xtoplt,dyA,'-')
#    prep.plot(prep.functionXc(new_c,ai),(dyA,),'o-')
#    dyA=cal_poch(prep.functionXc(new_c,ai,X_MOVE),a,X_MOVE)
#    prep.plot(prep.functionXc(new_c,ai,X_MOVE),(dyA,),'.-')
#    prep.plt.show()

    results=[]
    results.append(p0);results.append(pw);
    OUT_VEL.write("%f %f" % (step,time))
    for i in results:
	OUT_VEL.write(" %f" % (i))
    OUT_VEL.write("\n")
    STECH=[];DIFF=[];
    for stech in np.arange(0.01,1.0,0.01):
	x_tmp=prep.functionXc(stech,ai)
	DER=cal_poch(x_tmp,a)
	if(DER_R == 0.0 and np.isfinite(DER)):
	    DER_R=DER
	INT,err=quad(prep.functionXc,a=0.0, b=stech, args=(ai))
	coef=-0.5*INT/DER
	corr=DER/DER_R
#	stech=YR+stech*norma
	STECH.append(stech);DIFF.append(coef)
#	print stech,INT,DER,coef
	wynik=[x_tmp,stech,INT,DER,coef,corr]
	OUT_DIF.write("%f %f" % (step,time))
	for i in wynik:
	    OUT_DIF.write(" %f" % (i))
	OUT_DIF.write("\n")
    OUT_DIF.write("\n")

    if(TRYB):
	prep.plt.plot(STECH,DIFF); prep.plt.show();

    return 0

def cal_poch(x,fit,x_m=0.0):
    DERR=[]
    try:
	iterator = iter(x)
    except TypeError:
	derr=derivative(prep.functionCx,x, dx=0.5, args=(fit,x_m), order=21)
	return derr
    else:
	for i in x:
	    derr=derivative(prep.functionCx,i, dx=0.5, args=(fit,x_m), order=21)
	    DERR.append(derr)
	return np.array(DERR)

def optimal(fit_a):
    it=0;delta=1.0e-6;p=0.0;

    d,err=quad(prep.functionXc,a=0.0, b=1.0, args=(fit_a,p))
#    print d,err
    bp=0.0;bd=d;ile=1;dir=0;bdir=0;jump=0;p_tot=0;
    while(abs(d) > 1.0e-10):
	delta_p=abs(bp-p);delta_d=abs(bd-d);jump=bdir+dir;
	if(delta_p == 0):
	    delta_p=delta
	if(delta_d > 0):
	    ile=abs(d/delta_d)
	    if(jump==0):
		ile=ile/2.0
		it+=1
	#print jump,delta_p,bp,p,p_tot,"|",delta_d,bd,d,"=>",ile
	bp=p;bd=d;bdir=dir;
	if(d>0):
	    p=-delta_p*ile;
	    dir=-1;
	elif(d<0):
	    p=delta_p*ile;
	    dir=1;
	else:
	    break;
	p_tot+=p;
	d,err=quad(prep.functionXc,a=0.0, b=1.0, args=(fit_a,p_tot))
	#print d,p_tot
	if(it>100):
	    break;

#    new_c=prep.myrange(0.001)
#    yA=prep.functionXc(new_c,fit_a)
#    yAn=prep.functionXc(new_c,fit_a,p_tot)
#    dyA=cal_poch(new_c,fit_A)
#    prep.plot(new_c,(yA,yAn),'-')
#    prep.plt.show()

#	sys.stdout.write("%f %f %f %f %f %f %f %f\n" % (it,p0,P,Q,d,delta_p,delta_d,ile))
#	sys.stdout.flush()
    return p_tot
