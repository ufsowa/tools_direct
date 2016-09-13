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
    
PTH_DEST=os.path.abspath(os.path.dirname(sys.argv[0]))
name=sys.argv[1]
pattern="*"+name+"*"
every=int(sys.argv[2])
stop=float(sys.argv[3])
match=name+'.dat'

PTH_WORK=os.getcwd()
files=get_files(pattern)

print "IN gen_bin.py: " 
print PTH_WORK
print PTH_DEST

data=[];size=0;STEP0=1;TIME0=0;
licz=0;minus=0;dziel=0;
print files

for file_name in files:
    part=int(file_name.strip(match))
    for line in open(file_name,'r'):
	if(line != "\n"):
#	    asplit=[x for x in line.split()]
	    row_split=[float(x) for x in line.split()]
	    fsplit=[x for x in row_split]
	    STEP=STEP0+row_split[0];TIME=TIME0+row_split[1];
	    STEP=int(STEP);
	    if((STEP % every == 0) and (STEP <= stop)):
		name=PTH_WORK+"/../"+str(long(STEP))+".step"
		fout=open(name,"a")
		fout.write("%f %f " % (STEP,TIME))
		for i in fsplit[2:]:
		    fout.write("%s " % (i))
		fout.write("\n")
		fout.close()
    if(part>0):
	STEP0=STEP;TIME0=TIME;



