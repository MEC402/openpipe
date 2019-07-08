#
# ppull.py
#
# ppull.py panoid targetdir
#
# extract the images associated with the given panorama to the target direcotry

import sqlite3;
import os;
import sys;
import glob;
import pipeconfig

def printUsage():
    print("ppull panonumber targetdir")

#parse command line options
print (sys.argv)
if (len(sys.argv) != 3):
 printUsage();
 exit(-1)

panoid = sys.argv[1];
targdir = sys.argv[2];


#add the list of image files into the image file table.
dbase = pipeconfig.GBASE + "/" + pipeconfig.GPIPE + "/" + pipeconfig.GDBASE
pdb = sqlite3.connect(dbase)
pdbcursor = pdb.cursor();
#pdb.execute('''CREATE TABLE ingests (date text, basefolder text, folder text)''')
pdbcursor.execute("SELECT * FROM images WHERE panorama=%s" % (panoid))
imglist = pdbcursor.fetchall()

pdb.commit();
pdb.close();

for aimg in imglist:
    imgfile = pipeconfig.GBASE + "/" + pipeconfig.GPIPE + "/storage/" + aimg[1] + "/" + aimg[2]
    cmdline = "cp  %s %s" % (imgfile,targdir)
    print (cmdline)
    os.system(cmdline)






#finished
