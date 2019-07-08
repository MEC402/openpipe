#!/usr/bin/python

#panoxtract.py
#
# given a list of panoramas extract all of them with 136 images into distinct folders
#
#

import sys;
import glob;
from panorec import panoRec;
import csv
import imgoverlap
import os

def printUsage():
    print("panoxtract.py <imagelist file> <panodb.csv> <targdir>");

print("Traverse the panorama list and find matching stereo panoramas");

#check arguments and abort if incomplete
if len(sys.argv) != 4:
   printUsage();
   exit(1);

#first read in the image file
#read in the list of image files into an list
flist = sys.argv[1];
print("read image list from ",flist);
with open(flist) as f:
    filelist = f.readlines();

print(len(filelist));


#second read in the CSV file and keep as a record set.
panoreclist=[];
with open(sys.argv[2], newline='') as csvfile:
    preader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in preader:
        if len(row) == 4:
           print("Row:" +str( row));
           aprec = panoRec(0);
           aprec.fromList(row);
           print(aprec);
           panoreclist.append(aprec);
csvfile.close();

targbasedir=sys.argv[3];

#now traverse the records in the CSV file and extract the 136 image panoramas
for i in range(len(panoreclist)):
    print(i);
    if panoreclist[i].panoLength() == 136:
        #create a new folder with pano name
        newfolder = targbasedir+"/pano"+str(i);
        print(newfolder);
        os.mkdir(newfolder);

        #cp images into that folder
        for j in panoreclist[i].myseq.numlist:
            imgname = filelist[j].rstrip();
            print(imgname);
            print(j);
            cmd = "cp " + imgname +" " + newfolder+"/";
            print(cmd);
            os.system(cmd);

        #rotate folders

