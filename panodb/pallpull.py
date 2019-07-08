#
# pallpull.py
#
# pallpull.py targetdir
#
# extract all panoramas with 136 images into a set of named subdirectories in the targetdir

import sqlite3;
import os;
import sys;
import glob;
import pipeconfig

def printUsage():
    print("pallpull targetdir")

#parse command line options
print (sys.argv)
if (len(sys.argv) != 2):
 printUsage();
 exit(-1)

targdir = sys.argv[1];


#add the list of image files into the image file table.
dbase = pipeconfig.GBASE + "/" + pipeconfig.GPIPE + "/" + pipeconfig.GDBASE
pdb = sqlite3.connect(dbase)
pdbcursor = pdb.cursor();

#first get a list of all the panoramas and their names
pdbcursor.execute("SELECT rowid,* FROM panoramas WHERE numimages=136");
panolist = pdbcursor.fetchall()

#pdb.execute('''CREATE TABLE ingests (date text, basefolder text, folder text)''')
for apano in panolist:
  print (apano)
  panodir = targdir+"\\"+apano[2];
  cmdline = "mkdir %s" % (panodir)
  os.system(cmdline);
  print(cmdline)
  pdbcursor.execute("SELECT * FROM images WHERE panorama=%s" % (apano[0]))
  imglist = pdbcursor.fetchall()

  for aimg in imglist:
    imgfile = pipeconfig.GBASE + "/" + pipeconfig.GPIPE + "/storage/" + aimg[1] + "/" + aimg[2]
    cmdline = "cp  %s %s" % (imgfile,panodir)
    print (cmdline)
    os.system(cmdline)


pdb.commit();
pdb.close();



#finished
