#
# pimgdir.py
#
# pimgdir.py
#
# create a new ingest folder for a newly ingested set of images

import sqlite3;
import os;
import sys;
import glob;
import datetime;
import pipeconfig


#create a new Folder record in the ingests table"
def newFolderRecord(dbcursor,folderbase):
    dbcursor.execute("SELECT max(rowid) FROM ingests;")
    resnume = dbcursor.fetchall();
    (id,) = resnume[0];
    arowid = "folder1";
    if (id is None):
        imgfolder = 'folder1';
    else:
        imgfolder = 'folder' + str(id + 1);
        arowid = "folder"+str(id+1)
#    print(imgfolder);
    os.mkdir(pipeconfig.GBASE + "/" + folderbase + "/" + imgfolder)
    eyen = "\'" + eye + "\'"
    sqlstring = "INSERT INTO ingests VALUES (%s,%s,%s,%s,%s);" % ("\'date\'","\'"+folderbase+"\'","\'"+imgfolder+"\'",eyen,"'none'")
    dbcursor.execute(sqlstring)
#    print( sqlstring)
    #dbcursor.commit();
#    dbcursor.execute('SELECT rowid, * FROM panoramas WHERE panoname=-1')
#    panores = pdbcursor.fetchall();
    return arowid;



def printUsage():
    print("pimgdir [left | right]")

#parse command line options
#print (sys.argv)
if (len(sys.argv) < 1):
 printUsage();
 exit(-1)

eye = "none";
if (len(sys.argv) == 2):
    eye = sys.argv[1];

#print (eye);

#load database configuration information


#first extract the list of images not classified into panoramas.
dbase = pipeconfig.GBASE + "/" + pipeconfig.GPIPE + "/" + pipeconfig.GDBASE
pdb = sqlite3.connect(dbase)
pdbcursor = pdb.cursor();

afolder = newFolderRecord(pdbcursor,pipeconfig.GPIPE+"/storage")
print(afolder)

#finished
pdb.commit();
pdb.close()
