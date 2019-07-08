#!/usr/bin/pythomatchsfolders.py
#
# given a directory of folders that are panoramas
# check each panorama against the others to see if is stereo pair.
#
#
# panorama stereo match
#
#  if have same number of panoramas in pano records and more than 32 then:
#   flip the first image and compare it against the pair match.
#   if difference between the two is small then consider a stereo match.
#   will need to use ImageMagick for  this.

import sys;
import glob;
from panorec import panoRec;
import csv
import imgoverlap

#check content of images against each other.
def stereoMatch(folder1,folder2,topdir):
#create list of images
    srcname = folder1+'/*.RW2';
    imglist1 = list(glob.iglob(srcname,recursive=False));
    srcname = folder2+'/*.RW2';
    imglist2 = list(glob.iglob(srcname,recursive=False));

#now calculate the difference between them
    #lookup the two images
    ahi = 68;
    print(ahi);
    img1 = imglist1[ahi].strip();
    img2 = imglist2[ahi].strip();
    print(img1,img2);
    res = imgoverlap.imgRotComp(img1,img2);
    if res == True:
      ahi += 1;
      img1 = imglist1[ahi].strip();
      img2 = imglist2[ahi].strip();
      print(img1,img2);
      res = imgoverlap.imgRotComp(img1,img2);
      if res == True:
         ahi += 1;
         img1 = imglist1[ahi].strip();
         img2 = imglist2[ahi].strip();
         print(img1,img2);
         res = imgoverlap.imgRotComp(img1,img2);
         return res;
    return res;

def printUsage():
    print("matchstereopairs.py <panodir> ");

print("Traverse the panorama list and find matching stereo panoramas");

#check arguments and abort if incomplete
if len(sys.argv) != 2:
   printUsage();
   exit(1);

#first read in the list of folder
#read in the list of image files into an list
topdir = sys.argv[1];
srcdir = topdir+'/pano*';
folderlist=[];
for filename in glob.iglob(srcdir,recursive=False):
    if ("ready" not in filename):
       folderlist.append(filename);
    print(filename);

#now traverse the folders
#this is O(n^2) so will be slow.
for i in range(len(folderlist)):
    print(i);
    for j in range(i+1,len(folderlist)):
         #check the pano folders for a stero match
         print ("Checking Stereo Match %d %d %s" % (i,j,folderlist[i]));
         if stereoMatch(folderlist[i],folderlist[j],topdir) == True:
              #adjust records
              print("%s %s match" % (folderlist[i],folderlist[j]));
              break;
