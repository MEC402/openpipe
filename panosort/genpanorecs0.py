#!/usr/bin/python

#genpanorecs.py
#
# given a list of IMG files that form a collection of panoramas
# walk through the image list and generate records of what panorama
# the images belong too.
#
#
# panorama rules
#
#  Every image belongs to one panorama.
#  Every panorama must have at least one image.
#  Panoramas with less than 4 images are considered invalid.
#  Images with sequental file names need to overlap by at least 30% to
#    be in the same panorama.
#  Image with sequential file names need to have been taken within 2 minutes
#  of each other to be in he same panorama.

import sys;
import glob;
from panorec import panoRec;
import csv

def printUsage():
    print("genpanorecs.py <imagelist file>");

print("Generate Panorama Records from Image File List");

#check arguments and abort if incomplete
if len(sys.argv) != 3:
   printUsage();
   exit(1);


#read in the list of image files into an array
flist = sys.argv[1];
print("read image list from ",flist);
with open(flist) as f:
    filelist = f.readlines();

print(len(filelist));

#create an empty panorama database
panolist = [];
#create output csv file
csvfile = open(sys.argv[2],'w');
panwriter = csv.writer(csvfile,delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL);

#now classify each image into a panorama record
#first create an initial panorama Record.
curpanorec = panoRec(0);
#add the very first image into the record ->this defines the basic panoram.
#this first image is now classified.
curpanorec.addImage(filelist[0].strip(),0);
myfindex = 0;
panoid = 0;
for nximg in filelist[1:]:
    #have panorec object check to see if the current image is part of the current panoram
    snximg = nximg.strip();
    myfindex += 1;
    if curpanorec.inPano(snximg) == True:
        #if the image is in the panorama add it to the record.
        curpanorec.addImage(snximg,myfindex);
    else:
        #else this image is not in the current panorama
        #append the current record to the panorama list
        print("End Pano " + str(len(curpanorec.imglist)));
        panolist.append(curpanorec);
        curpanorec.consolidatePanoRec();
        curpanorec.outRec(panwriter);
        csvfile.flush();
        #create a new record and assign current image to it
        panoid += 1;
        curpanorec = panoRec(panoid);
        curpanorec.addImage(snximg,myfindex);


#now output the panorama database to a file/output
print(len(panolist));
for ap in panolist:
    ap.consolidatePanoRec(); # this compresses the filenames to compressed sequences.
    ap.printRec(); # now output the string representation of the panorama record.
    print("next record");

#all finished.
