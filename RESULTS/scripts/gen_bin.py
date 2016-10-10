#!/usr/bin/env python

import sys
import os
import fnmatch


def get_files(pattern):
    files=()
    for file in os.listdir('.'):
	if fnmatch.fnmatch(file,pattern):
	    files+=(file,)
    files=sorted(files)
    return files
    
name=sys.argv[1]
pattern="*"+name+"*"
every=int(sys.argv[2])
stop=float(sys.argv[3])
match=name+'.dat'
PTH_DEST=(sys.argv[4])

PTH_WORK=os.getcwd()
files=get_files(pattern)

print "IN gen_bin.py: " 
print PTH_WORK
print PTH_DEST

data=[];size=0;STEP0=0;TIME0=0.0;
licz=0;minus=0;dziel=0;
print files

for file_name in files:
    part=int(file_name.strip(match))
    for line in open(file_name,'r'):
	if(line != "\n"):
#	    asplit=[x for x in line.split()]
	    row_split=[float(x) for x in line.split()]
#	    fsplit=[x for x in row_split]
	    X = (row_split[4]+row_split[3])/2.0
	    STEP=STEP0+row_split[0];TIME=TIME0+row_split[1];
	    STEP=int(STEP);
	    if((STEP % every == 0) and (STEP <= stop)):
		name=PTH_DEST+"/"+str(long(STEP))+".step"
		fout=open(name,"a")
		fout.write("%f %f %f" % (STEP,TIME,X))
		for i in row_split[4:]:
		    fout.write(" %f" % (i))
		fout.write("\n")
		fout.close()
    if(part>0):
	STEP0=STEP;TIME0=TIME;



