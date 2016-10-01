#!/usr/bin/env python


# Program zaklada na wejsciu dane ciagle ze wzgledu na x = (1,2,3,4,...). Nie takie x = (1,1,1,2,2,3,3,4,5,..)
# Program opracowuje dane usrednione z kilku probek. W danych mamy wypadkowy profil.
#

import os
import fnmatch
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erf, erfinv,erfc, erfcinv
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter

def get_files(pattern):
    files=()
    for file in os.listdir('.'):
	if fnmatch.fnmatch(file,pattern):
	    files+=(file,)
    files=sorted(files)
    return files
    
def read_data(files):
    data=[];size=0;
    for file_name in files:
	data_tmp=[]
	for line in open(file_name,'r'):
	    if(line != "\n"):
		data_tmp.append(line)
	    else:
		tmp_size=len(data_tmp)
		if(size == 0 ):
		    size = tmp_size
		if(tmp_size < size):
		    size = tmp_size
#		print size, data_tmp[-1]
	data+=data_tmp
#	print "koniec file:", file_name,len(data)
#	print data[-1]
    return data,size

def str2double(str_obj):
    tmp=[]; size = 0; bufor = 0;
    for line in str_obj:
	asplit=[float(x) for x in line.split()]
	if(size == 0):
	    bufor = asplit[0];
	if(asplit[0] == bufor):
	    size+=1;
	    tmp.append(asplit)
    tmp=np.asarray(tmp)
    new=tmp.transpose()
#    print "str2double:", tmp.shape, new.shape
#    print new
    return new,size

def divide(a,b):
    with np.errstate(divide='ignore', invalid='ignore'):
	c = np.true_divide(a,b)
	c[c == np.inf] = 0
	c = np.nan_to_num(c)
    return c


def plot(x,y,stri='o'):
    iter=0
    for i in y:
	plt.plot(x,i,stri,label=str(iter),linewidth=2.0)
	iter+=1
    plt.legend();plt.draw();

def ferc(x):
    return erfc(x)/2

def fercinv(x):
    return erfcinv(x*2)

def norm_data(y):
    norm=[]
    YL=max(y);YR=min(y);
    norm.append(YL); norm.append(YR);
    new_y = (y - YR)/(YL - YR)
    return new_y, norm

def trans_data(y):
    new_y=fercinv(y)
#    new_y=ferc(new_y)
#    print zip(y,new_y)
    return new_y

def set_borders(x,y):
    border=[]
    ids=np.where(np.isfinite(y))[0]
    L=x[ (ids[0]-1) ]; P=x[ (ids[-1]+1) ]
    border.append(L); border.append(P)
    return border

def fit_data_inv(inx,iny,order=2):
    ids=np.where(np.isfinite(iny))[0]
    y=iny[ids]
    x=inx[ids]
    coef=np.polyfit(y,x,deg=order)
    fit=np.poly1d(coef)
    return x,fit

def fit_data(inx,iny,order=2):
#    ids=np.where(np.isfinite(iny))[0]
#    y=iny[ids]
#    x=inx[ids]
#    coef=np.polyfit(x,y,deg=order)
#    fit=np.poly1d(coef)
    fit=interp1d(inx,iny,kind=order,bounds_error=False,fill_value="extrapolate")

    return fit

def functionCx(x,fit,x0=0.0):
    shift_x = np.ones_like(x)*x0
    new_x = x + shift_x
    y=fit(new_x)
    return y

def functionXc(c,fit,x0=0.0):
    x=fit(c) + x0
    return x

#def functionCx(x,fit,x0=0.0):
#    y=ferc(fit(x+x0))
#    return y
#
#def functionXc(c,fit,x0=0.0):
#    up=trans_data(c)		#zamienilem c na u'. Znajdz x dla tego u' z fitu x(u')
#    x=fit(up) + x0
#    return x

def func(x, A, B, x0, sigma):
    return A+B*np.tanh((x-x0)/sigma)

def smooth_data(x,y,grid=1000,window=101,order=3,der=0,tryb='noplot'):
    xx = np.linspace(x.min(),x.max(), grid)

    # interpolate + smooth
    itp = interp1d(x,y, kind='linear')
    window_size, poly_order = window, order
    yy_sg = savgol_filter(itp(xx), window_size, poly_order,deriv=der,mode='mirror')
#    fit, _ = curve_fit(func, x, y)
#    yy_fit = func(xx, *fit)

    if(tryb=='plot'):
	fig, ax = plt.subplots(figsize=(13, 10))
	ax.plot(x, y, 'r.', label= 'Unsmoothed curve')
	ax.plot(xx, yy_sg, 'k', label= "Smoothed curve")
	#ax.plot(xx, yy_fit, 'b--', label=r"$f(x) = A + B \tanh\left(\frac{x-x_0}{\sigma}\right)$")
	plt.legend(loc='best')
	plt.show()

    return xx,yy_sg


def gaussian(i,j,dx):
    r=i-j;
    A=1.0/(dx*np.sqrt(2.0*np.pi))
    return A*np.exp(-(r*r/(2.0*dx*dx)))

def move_avg(x,y,step=1.0,ile=3,tryb='noplot'):
    grid=x[1]-x[0]
    size=grid*ile
    dense_x = np.arange(min(x),max(x)+step,step)
    new_x=[]; new_y=[]; w =[];
    for i in dense_x:
	new_size=size
	tmp = np.around((x - i),decimals=5)							#tmp is the same as x shifted to new 0 located on i
	zero = np.where( tmp == round(0.0,5))[0]
	left = np.where( (round(-size,5) < tmp ) & (tmp < round(0.0,5)) )[0]
	right = np.where( (round(0.0,5) < tmp ) & (tmp < round(size,5)) )[0]
	idn=np.append(left,zero); idn=np.append(idn,right)
	tmp_y0 = y[zero]; tmp_x0 = x[zero];
	tmp_yl = y[left]; #tmp_xl = x[left]; 
	tmp_yr = y[right]; #tmp_xr = x[right]; 
	idl=np.where(np.isinf(tmp_yl))[0]; idr=np.where(np.isinf(tmp_yr))[0]
	LS = len(idl); RS = len(idr);
	if( LS > 0 or RS > 0):
	    new_size=size*0.1
	    left = np.where( (round(-new_size,5) < tmp ) & (tmp < round(0,5)))[0]
	    right = np.where( (round(0,5) < tmp) & (tmp < round(new_size,5)))[0]
#	    tmp_yl = y[left]; tmp_xl = x[left]; 
#	    tmp_yr = y[right]; tmp_xr = x[right]; 
#	    new_size=size

#	tmp_x=np.append(tmp_xl,tmp_x0); tmp_x=np.append(tmp_x,tmp_xr)
#	tmp_y=np.append(tmp_yl,tmp_y0); tmp_y=np.append(tmp_y,tmp_yr)

	if(len(left)==0):
	    left = np.where( (round(-grid,5) < tmp ) & (tmp < round(0,5)))[0]
	if(len(right)==0):
	    right = np.where( (round(0,5) < tmp) & (tmp < round(grid,5)))[0]

#	if ( len(left) > len(right) ):
#	    left=left[-len(right):]
#	if ( len(left) < len(right) ):
#	    right=right[:len(left)]

	tmp_yl = y[left]; tmp_xl = x[left]; 
	tmp_yr = y[right]; tmp_xr = x[right]; 

	tmp_x=np.append(tmp_xl,tmp_x0); tmp_x=np.append(tmp_x,tmp_xr)
	tmp_y=np.append(tmp_yl,tmp_y0); tmp_y=np.append(tmp_y,tmp_yr)

#	print i,left,zero,right, -size, size
#	print LS,RS,tmp_yl,tmp_yr
#	print tmp_x,tmp_y

#	plt.plot(tmp_x, gaussian(tmp_x,i,grid*0.5), '-', label= 'Raw curve')
#	plt.plot(tmp, y, 'k.', label= "Shifted curve")
#	plt.legend(loc='best')
#	plt.show()

	if(len(tmp_y)>0):
	    w = [gaussian(i,j,grid) for j in tmp_x]
	    N =np.average(tmp_y,weights=w)
	    new_x.append(i)
	    new_y.append(N)

    if(tryb=='plot'):
	fig, ax = plt.subplots(figsize=(13, 10))
	ax.plot(x, y, 'r.', label= 'Unsmoothed curve')
	ax.plot(new_x, new_y, 'k', label= "Smoothed curve")
	plt.legend(loc='best')
	plt.show()

    return np.array(new_x),np.array(new_y)

def myrange(st=0.0,ed=1.0,delta=0.001):
    dx=delta/1000.0
    new_cl=np.arange(st,0.001,dx)
    new_cr=np.arange(0.999, (ed + dx) ,dx)
    new_c0=np.arange(0.001,0.999,delta)
    new_c=np.append(new_cl,new_c0); new_c=np.append(new_c,new_cr);
    return new_c

def baseline(x,y,p):
    p0=0
    L=p0-2.*p
    X=np.arange(x[0],L,0.1)
    Y=np.interp(X,x,y)
    med1 = float(np.median(Y))
    mad1 = np.median(np.absolute(Y - med1))
    L=p0+2.*p
    X=np.arange(L,x[-1],0.1)
    Y=np.interp(X,x,y)
    med2 = float(np.median(Y))
    mad2 = np.median(np.absolute(Y - med2))
    return med1,med2

def splot(CA,CB,flag="min"):
    y=[];
    if(len(CA)!=len(CB)):
	print "error in splot. Different sizes",len(CA),len(CB)
	exit();
    if(flag=="min"):
	for i in range(0,len(CA)):
	    y.append(mini(CA[i],CB[i]))
    if(flag=="max"):
	for i in range(0,len(CA)):
	    y.append(maxi(CA[i],CB[i]))
    return y

def convolute_x0(X,CA,CB,flag=True):
    y=splot(CA,CB)
    return FWHM(X,y,flag)

def mini(x1,x2):
    a=abs(x1);b=abs(x2)
    if(a>=b):
        return x2
    if(a<b):
        return x1

def maxi(x1,x2):
    a=abs(x1);b=abs(x2)
    if(a<=b):
        return x2
    if(a>b):
        return x1

def FWHM(X,Y,flag=True):
    max_y=max(Y);min_y=min(Y);
    ind=Y.index(max_y);idx=X[ind];left_idx=0;right_idx=0;
    half_max=max_y/2.0
    min_y=max(Y[0],Y[-1])
    avg_h=(max_y+min_y)/2.0
    if(half_max < avg_h ):
	half_max = avg_h
    yh=np.ones_like(X)*half_max
    if(flag):
	d = (np.sign(half_max - np.array(Y[0:-1])) - np.sign(half_max - np.array(Y[1:])))/2.0
	d=np.append(d,0)
#	plt.plot(X[0:len(d)],abs(d),X,yh,'-');plt.plot(X,Y);plt.show();
	left_idx = X[d > 0][0]
	right_idx = X[d < 0][-1]

    return [idx,(right_idx-left_idx)]


#fit multiple gaussians
#http://stackoverflow.com/questions/10143905/python-two-curve-gaussian-fitting-with-non-linear-least-squares
#http://stackoverflow.com/questions/26936094/python-load-data-and-do-multi-gaussian-fit