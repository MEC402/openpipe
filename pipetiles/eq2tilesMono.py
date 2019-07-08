#!/usr/bin/python
#################################
# eq2tiles.py
#
# this program takes a Stereo Pair and generates a stereo tile set
# that can be loaded by Marzipano and tileViewer
#
# author: steve cutchin, Boise State University
#
# eq2tiles imgdirectory imgpref tiledirectory
#
# imgdirectory is the source directory for the equirectangular panoramas.
# imgprefix is the filname with out the '_{L,R}.tiff' component
# tiledirectory is the directory where the final tiles will end up
#   the tiles will be located in tiledirectory/imgprefix/
#
#
# planned extension option to update JSON file in tiledirectory
#
##################################################
import sys;
import glob;
import os;

#temporary directory for intermediary files
Gimgtmpdir="/data/scratch/"

def printUsage():
    print("Usage: eq2tiles.py <imgdirectory> <imgpref> <tiledirectory>");

# first step is to check the arguments
# eq2tiles imgdirectory imgprefix tiledirectory
#print len(sys.argv);
#check proper number of arguments
if len(sys.argv) != 4:
   printUsage();
   exit(-1);

#check if temporary directory available
if os.path.isdir(Gimgtmpdir) == False:
   print("No Temp Directory: " + Gimgtmpdir);
   exit(-1);

#check if imgdirectory exists
imgdir =sys.argv[1];
if os.path.isdir(imgdir) == False:
   print("No Image Directory: " + imgdir);
   exit(-1);


#check if imgfiles exist
imgpref = sys.argv[2];
imgfileL = imgdir + "/"+imgpref+".png";

if os.path.exists(imgfileL) == False:
   print("No Image File: " + imgfileL);
   exit(-1);

#check if tiledirectory exists
tiledir =sys.argv[3];
if os.path.isdir(tiledir) == False:
   print("No Image Directory: " + tiledir);
   exit(-1);

# convert the equirectangular tif images into png files.
#convertleft = "convert " + imgfileL + " " + Gimgtmpdir +"/" + imgpref+"_L.png";
#print(convertleft);
#os.system(convertleft);
#convertright = "convert " + imgfileR + " " + Gimgtmpdir +"/" + imgpref+"_R.png";
#os.system(convertright);


#test for success
eqleftpng = imgdir + "/" + imgpref +".png"
if os.path.exists(eqleftpng) == False:
   print("Convert Failed: " + eqleftpng);
   exit(-1);

# convert the equirectangular png files into individual faces 
# use panorama program
os.system("panorama -i " + eqleftpng + " -o " + Gimgtmpdir + "/" + imgpref +" -r 16384");

# rename face files to input format for gentiles
# face list for output of panorama 0=back,1=left,2=front,3=right,4=up,5=down
baseleft = Gimgtmpdir + "/" + imgpref;
os.system("mv " + baseleft+"_0.png " + baseleft+".b.png");
os.system("mv " + baseleft+"_1.png " + baseleft+".l.png");
os.system("mv " + baseleft+"_2.png " + baseleft+".f.png");
os.system("mv " + baseleft+"_3.png " + baseleft+".r.png");
os.system("mv " + baseleft+"_4.png " + baseleft+".u.png");
os.system("mv " + baseleft+"_5.png " + baseleft+".d.png");

# call gentiles.py on face files
os.system("./gentiles.py " + baseleft + " " + tiledir + "/"+imgpref+"/left/");

#optional remove intermediary files

#finished 
