#!/usr/bin/python

#matchstereopairs.py
#
# given a pano database and file list
# check each panorama against the others to see if is stereo pair.
#
#
# panorama stereo match
#
#  don't care about panoramas with less then 32 images.
#  if have same number of panoramas in pano records and more than 32 then:
#   flip the first image and compare it against the pair match.
#   if difference between the two is small then consider a stereo match.
#   will need to use ImageMagick for  this.

import sys;
import glob;
from panorec import panoRec;
import csv
import imgoverlap

def stereoMatch(prec1,prec2,filelist):
#in here we use image magick to compare two images:
#convert first image to PNG
#convert second image to PNG but rotate 180'
#now calculate the difference between them
    #lookup the two images
    ahi = int(len(prec1.myseq.numlist)/2);
    print(ahi);
    img1 = filelist[prec1.myseq.numlist[ahi]].strip();
    img2 = filelist[prec2.myseq.numlist[ahi]].strip();
    print(img1,img2);
    res = imgoverlap.imgRotComp(img1,img2);
    if res == True:
      ahi += 1;
      img1 = filelist[prec1.myseq.numlist[ahi]].strip();
      img2 = filelist[prec2.myseq.numlist[ahi]].strip();
      print(img1,img2);
      res = imgoverlap.imgRotComp(img1,img2);
      if res == True:
         ahi += 1;
         img1 = filelist[prec1.myseq.numlist[ahi]].strip();
         img2 = filelist[prec2.myseq.numlist[ahi]].strip();
         print(img1,img2);
         res = imgoverlap.imgRotComp(img1,img2);
         return res;
    return res;

def printUsage():
    print("matchstereopairs.py <imagelist file> <panodb.csv>");

print("Traverse the panorama list and find matching stereo panoramas");

#check arguments and abort if incomplete
if len(sys.argv) != 3:
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

#now traverse the records in the CSV file and do the matching.
#this is O(n^2) so will be slow.
for i in range(len(panoreclist)):
    print(i);
    if panoreclist[i].panoLength() > 31:
        for j in range(i+1,len(panoreclist)):
            #compare the two images against each other as appropriate.
            if panoreclist[i].panoLength() == panoreclist[j].panoLength():
                print ("Possible Stereo Match %d %d %d" % (i,j,panoreclist[i].panoLength()));
                if stereoMatch(panoreclist[i],panoreclist[j],filelist) == True:
                    #adjust records
                    panoreclist[i].stereopair = panoreclist[j].myid;
                    panoreclist[j].stereopair = panoreclist[i].myid;
                    print("stereo match");
                    break;


#now output the panorecords
csvfile = open('matchpanorec.csv','w');
panwriter = csv.writer(csvfile,delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL);

for curpanorec in panoreclist:
    curpanorec.consolidatePanoRec();
    curpanorec.outRec(panwriter);
    csvfile.flush();
    #create a new record and assign current image to it

csvfile.close();
