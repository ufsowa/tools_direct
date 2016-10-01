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

WORK_PATH=os.getcwd()
files=get_files(pattern)

data=[];size=0;STEP0=0;TIME0=0;
licz=0;minus=0;dziel=0;
print files

for file_name in files:
    part=int(file_name.strip(match))
    for line in open(file_name,'r'):
	if(line != "\n"):
#	    asplit=[x for x in line.split()]
	    row_split=[float(x) for x in line.split()]
	    points=row_split[-1]
	    fsplit=[x/points for x in row_split]
	    if(not all(v == 0 for v in fsplit)):
		if(part==0 and dziel == 0):
		    minus=fsplit[0];dziel=fsplit[1]
		STEP=STEP0+fsplit[0];TIME=TIME0+fsplit[1]
		licz=int((STEP-minus)/dziel)
		if((licz % every == 0) and (STEP > stop)):
		    name="../"+str(long(STEP))+".step"
		    fout=open(name,"a")
		    fout.write("%f %f " % (STEP,TIME))
		    for i in fsplit[2:]:
			fout.write("%s " % (i))
		    fout.write("\n")
		    fout.close()
    STEP0=STEP;TIME0=TIME;



