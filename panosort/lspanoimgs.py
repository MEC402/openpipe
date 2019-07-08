#!/usr/bin/python

# lspanoimgs -- generate a list of all of the RW2 images ina directory tree.
#            -- this is used to begin the next step of identifying pano sets

import sys;
import glob;

def printUsage():
    print("lspanoimgs <topdirectory>");

#check arguments and abort if incomplete
if len(sys.argv) != 2:
   printUsage();
   exit(1);

#now traverse the directory structure and generate the file list
topdir = sys.argv[1];

count = 0;
srcdir = topdir+'/**/*.RW2';
for filename in glob.iglob(srcdir,recursive=True):
    count += 1;
    print(filename);


#print("Number of files=",count);
