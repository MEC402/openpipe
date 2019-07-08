#
# pingest.py
#
# pingest.py indirectory ingestdir
#
# ingest all of the image .RW2 files into the given ingestdirector
# and add the images into the image TABLE

import sqlite3;
import os;
import sys;
import glob;
import pipeconfig

def printUsage():
    print("pingest ImageDirectory IngestDir [left | right]")

#parse command line options
print (sys.argv)
if (len(sys.argv) < 3):
 printUsage();
 exit(-1)

imgdir = sys.argv[1];
ingdir = sys.argv[2];
eye ="none"

if (len(sys.argv) == 4):
    eye = sys.argv[3];
    if (eye != "left") & (eye != "right"):
        printUsage()
        exit(-1)


#load database configuration information


#A better method for ingest would be to update table with each file copy.
#however we will use a lasy method because it will run faster.

#first copy the entire fi#imagedir = ingdir + "/" + "*.RW2"
#cp file tree from indirectory to ingestdir
cmdline = "cp -r %s %s" % (imgdir,ingdir)
os.chdir(pipeconfig.GBASE+"/" + pipeconfig.GPIPE + "/storage")
os.system(cmdline)
print (cmdline)

#second get a file list from the ingestdirectory
#imagedir = ingdir + "/" + "*.RW2"
imagedir = ingdir + "/*/*.RW2"
print(imagedir);
walklist = os.walk(ingdir)
print (walklist)
imglist = [];
for root,dirs,files in walklist:
    for name in files:
        if name.endswith(".RW2"):
           imglist.append((root,name))

print (imglist)

#add the list of image files into the image file table.
dbase = pipeconfig.GBASE + "/" + pipeconfig.GPIPE+"/"+pipeconfig.GDBASE
pdb = sqlite3.connect(dbase)
pdbcursor = pdb.cursor();
#pdb.execute('''CREATE TABLE ingests (date text, basefolder text, folder text)''')
#pdbcursor.execute("DELETE FROM images;")

for root,name in imglist:
    rootq = "\'"+root+"\'"
    namen = "\'" +name + "\'"
    eyen = "\'" +eye + "\'"
    sqlstring = "INSERT INTO images VALUES (%s,%s,%s,%d,%d,%s);" % ("\'date\'",rootq,namen,-1,-1,eyen)
    pdbcursor.execute(sqlstring)
    print( sqlstring)
pdb.commit();
pdb.close();


#finished
