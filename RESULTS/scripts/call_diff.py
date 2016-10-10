#!/usr/bin/env python


# Program zaklada na wejsciu dane ciagle ze wzgledu na x = (1,2,3,4,...). Nie takie x = (1,1,1,2,2,3,3,4,5,..)
# Program opracowuje dane usrednione z kilku probek. W danych mamy wypadkowy profil.
#

import libs.base as prep
import libs.call as call
import sys
import os

name=sys.argv[1]
#new_st=int(sys.argv[2])
#step=int(sys.argv[3])
#DELTA=float(sys.argv[4])
#pattern="*"+name+"*"

WORK_PATH=os.getcwd()
#os.chdir("./../")
#files=prep.get_files(pattern)
files=[];files.append(name)
DATA,SIZE=prep.read_data(files)
os.chdir(WORK_PATH)


hist,new_st = prep.str2double(DATA)

call.x0(hist)
call.diff()

#print call.out_name1,call.out_name2


#if(step==0):
#    STEP=POINTS-1
#if(step>0):
#    STEP=step
#if(step<0):
#    print("Error in par step<0\n")
#    exit(1)

#for iter in range(0,POINTS,STEP):
#    start = new_st
#    end=start + 2*SIZE
#    if(end >= len(DATA)):
#	end=len(DATA)
#    print start,end,new_st
#    print hist[0]
#    print hist[-1]


#http://www.robots.ox.ac.uk/~sjrob/ox_teach.html