#
# panogen.py
#
# panogen.py
#
# Process the images in the Image Table and classify into Panorama sets.
# Adding new Panoramas into the panorama table as needed.

import sqlite3;
import os;
import sys;
import glob;
import datetime;
import exiftool;
import pipeconfig

#use exif data to compare timestamp on image files
# if the time between two shots is more than 10 seconds then not the same panorama.
def chkOverlapTime(img1file,img2file):
    cmds = "d:/bin/exiftool.exe -TAG -CreateDate " + img1file;
    stamp1 = os.popen(cmds).read();
    dstamp1 = stamp1.split(':',1);
    dtime1 = datetime.datetime.strptime(dstamp1[1].strip(), "%Y:%m:%d %H:%M:%S");

#    os.system(cmds);
    cmds = "d:/bin/exiftool.exe -TAG -CreateDate " + img2file;
    stamp2 = os.popen(cmds).read();
    dstamp2 = stamp2.split(':',1);
    dtime2 = datetime.datetime.strptime(dstamp2[1].strip(), "%Y:%m:%d %H:%M:%S");
#    os.system(cmds);
    if (dtime1 > dtime2):
        atd = dtime1 - dtime2;
        asecs = atd.total_seconds();
    else:
        atd = dtime2 - dtime1;
        asecs = atd.total_seconds();
#    print (asecs);
    #convert strings to time stamps.
    #if time difference between stamp1 and stamp2 is > 10 seconds return false.
    print (asecs)
    if asecs > 10:
        return False;
    #else
    return True;

def chkTime(atime1,atime2):
    dtime1 = datetime.datetime.strptime(atime1.strip(), "%Y:%m:%d %H:%M:%S");

#    os.system(cmds);
    dtime2 = datetime.datetime.strptime(atime2.strip(), "%Y:%m:%d %H:%M:%S");
#    os.system(cmds);
    if (dtime1 > dtime2):
        atd = dtime1 - dtime2;
        asecs = atd.total_seconds();
    else:
        atd = dtime2 - dtime1;
        asecs = atd.total_seconds();
#    print (asecs);
    #convert strings to time stamps.
    #if time difference between stamp1 and stamp2 is > 10 seconds return false.
    print (asecs)
    if asecs > 10:
        return False;
    #else
    return True;

#apanorama = newPanoRecord(pdbcursor);
#create a new panorama record in the panorama table"
def newPanoRecord(dbcursor):
    dbcursor.execute("SELECT max(rowid) FROM panoramas;")
    resnume = dbcursor.fetchall();
    (id,) = resnume[0];
    arowid = 1;
    if (id is None):
        panoname = 'pano1';

    else:
        panoname = 'pano' + str(id + 1);
        arowid = str(id+1)
        print(panoname);
    sqlstring = "INSERT INTO panoramas VALUES (%s,%s,%s,%s,%d);" % ("\'date\'","\'"+panoname+"\'","'left'","'right'",0)
    dbcursor.execute(sqlstring)
    print( sqlstring)
    #dbcursor.commit();
#    dbcursor.execute('SELECT rowid, * FROM panoramas WHERE panoname=-1')
#    panores = pdbcursor.fetchall();
    return arowid;


#setImagePanorama(pdbcursor,imgfirst,apanorama)
#for the given image record set its panorama id to the given panorama
def setImagePanorama(dbcursor, animage, apanorec):
    panoid = apanorec;
    imgid = animage[0];
    sqlstring = 'UPDATE images SET panorama=%s WHERE rowid=%s ' %(panoid,imgid)
    print(sqlstring)
    dbcursor.execute(sqlstring)
#    print(dbcursor,animage,apanorec)

# panoCheck(curimage,pastimage) == True):
def panoCheck(animage, pastimage):
    res=False;
    #check to see if these two images are in the same panorama
    # must be shot within a few seconds of each other
    # should overlap by 30%
    #generate full paths to images
#    img1file = animage[2]+"/" +animage[3]
#    img2file = pastimage[2]+"/"+pastimage[3];
    #get the times from the images
    print(animage[7],pastimage[7]);
    res = chkTime(animage[7],pastimage[7])
    #compare the times

    return res;

def setPanoLength(dbcursor, apanorec, alength):
    panoid = apanorec;
    sqlstring = 'UPDATE panoramas SET numimages=%d WHERE rowid=%s ' %(alength,panoid)
    print(sqlstring)
    dbcursor.execute(sqlstring)
#    print(dbcursor,animage,apanorec)

def printUsage():
    print("panogen")

#parse command line options
print (sys.argv)
if (len(sys.argv) != 1):
 printUsage();
 exit(-1)



#load database configuration information


#first extract the list of images not classified into panoramas.
dbase = pipeconfig.GBASE + "/" + pipeconfig.GPIPE + "/" + pipeconfig.GDBASE
pdb = sqlite3.connect(dbase)
pdbcursor = pdb.cursor();

pdbcursor.execute('SELECT rowid, * FROM images WHERE panorama=-1')
imglist = pdbcursor.fetchall();

print (imglist)
#now if the list of images is empty exit
if (len(imglist) == 0):
     exit(-1)

#pdb.execute('''CREATE TABLE ingests (date text, basefolder text, folder text)''')
#pdbcursor.execute("DELETE FROM images;")

imgfiles = [];
for aimage in imglist:
    imgpath = pipeconfig.GBASE + "/" + pipeconfig.GPIPE+ "/storage/" + aimage[2] + "/" + aimage[3];
    print(imgpath)
    imgfiles.append(imgpath)

with exiftool.ExifTool() as et:
    metadata = et.get_metadata_batch(imgfiles)

datestamps=[];
i=0
for d in metadata:
    aval = (  d["EXIF:CreateDate"], )
    bval = imglist[i]
    print (aval, bval)
    imglist[i] = bval + aval
    i = i + 1
#    print(d["EXIF:CreateDate"])
print( imglist)

#exit(0)

#images to sort so will create a least one new Panorama
#create a new panorama record
apanorama = newPanoRecord(pdbcursor)

#add the first image to this new panorama
imgfirst = imglist[0];
setImagePanorama(pdbcursor,imgfirst,apanorama)
pastimage = imgfirst
imgcount=1

#for second image onward,
#  if overlaps with past image add to current panorama
#   else create a new panorama record and start over with adding.
for curimage in imglist[1:]:
    if (panoCheck(curimage,pastimage) == True):
        setImagePanorama(pdbcursor,curimage,apanorama)
        imgcount += 1
    else:
        setPanoLength(pdbcursor,apanorama,imgcount)
        apanorama = newPanoRecord(pdbcursor);
        setImagePanorama(pdbcursor,curimage,apanorama)
        imgcount = 1
    pastimage = curimage


setPanoLength(pdbcursor,apanorama,imgcount)
#finished
pdb.commit();
pdb.close()
