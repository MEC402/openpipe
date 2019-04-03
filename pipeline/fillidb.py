#!/usr/bin/python
#
# fill image database entries in table
#

import glob
import sys
import os
import json

#local classes
from adam import Adam

def checkArgs(argv):
#    print "this is the name of the script: ", argv[0];
#    print "Number of argument in: ", len(argv);
    if (len(argv) < 2):
      print (argv[0] + ": {panodirectory}");
      sys.exit(1);

def matchlist(aroot):
      if aroot.endswith("_thmb.jpg"):
         return 0
      if aroot.endswith(".jpg"):
         return 1
      return 0

def listImages(aroot):
    d = []
    if os.path.isdir(aroot):
#      for x in matchlist(aroot):
      for x in os.listdir(aroot):
       ad = listImages(os.path.join(aroot,x))
       d = d + ad
    elif matchlist(aroot):
       d = [aroot]
    return d

#convert filename into database entry sequence
urprefix = "http://cs.boisestate.edu/~scutchin/wmui/"

Gimgidcount = 1

def printrec(ax):
   global Gimgidcount
   myid = str(Gimgidcount)
   Gimgidcount += 1
   myshortname = os.path.basename(ax);
   myshortname = os.path.splitext(myshortname)[0]
   myfilename = os.path.basename(ax)
   myuri = urprefix+ax  # need to convert to relative for final work
   res = " VALUES (\"%s\",\"%s\",\"%s\",\"%s\")" % (myid,myshortname,myfilename,myuri)
   return res

checkArgs(sys.argv);
imgdir = sys.argv[1];

#connect to database
adb = Adam()
adb.connect("artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com","artmaster","ArtMaster51","artmaster")

#traverse the directory and create a list of images
imglist = listImages(imgdir)

#output the insert  command
for x in imglist:
    imgrec = printrec(x)
    adb.executeSql("insert into images " + imgrec)
   

#execut sql on the database
