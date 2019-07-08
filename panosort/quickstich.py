#!/usr/bin/python

#quickstitch.py
#
# Do a simple quick stitch usen basic opencv codes.
#

import sys;
import glob;
from panorec import panoRec;
import cv2;

def printUsage():
    print("quickstitch.py  <imagelist file> <panorecdb file> <panofilenameout>");

print("Generate Panorama from Image File List");

#check arguments and abort if incomplete
if len(sys.argv) != 4:
   printUsage();
   exit(1);


#read in the list of image files into an array
flist = sys.argv[1];
print("read image list from ",flist);
with open(flist) as f:
    filelist = f.readlines();

print(len(filelist));

#read in the panorama records

panorecs = [];

#panorama file name
panfile = sys.argv[3];

#convert panorec images to png images
pngpanofiles=[];


#now set up and stitch

stitcher = cv2.createStitcher(False)
foo = cv2.imread("side1.png")
bar = cv2.imread("side2.png")
result = stitcher.stitch((foo,bar))
print(result);
cv2.imwrite("result.jpg", result[1])
