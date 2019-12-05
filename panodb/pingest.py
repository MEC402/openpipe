#!/bin/python3
#
# pingest.py
#
# pingest.py indirectory masterdir
#
# ingest all of the image .RW2 files into the given ingestdirector
# and add the images into the image TABLE

import os
import sys
import glob
import getopt
import mysql.connector
from datetime import datetime

def printUsage():
    print("pingest [--nomove] ImageDirectory MasterDir ")

move=True
images=True

#parse command line options
print (sys.argv)
if (len(sys.argv) < 3):
 printUsage();
 exit(-1)

try: 
  optlist, args = getopt.getopt(sys.argv[1:], 'ni',["nomove","noimages"])
except getopt.GetoptError as err:
  sys.exit(-1)

for o,a in optlist:
    print (o)
    if o in ("-n", "--nomove"):
     move = False
    elif o in ("-i", "--noimages"):
     images = False


imgdir = args[0];
masterdir = args[1];

print(move)

BASEDIR="/WorldMuseum/masters"
BASEURL="http://mec402.boisestate.edu/wmuseum/masters/"

def isImage(aname):
   print(aname)
   ext = (".rw2",".cr2",".png",".jpg",".tif",".tiff")
   if aname.lower().endswith(ext):
      return True
   return False

#A more robust method for ingest would be to update table with each file copy.
#however we will use a lazy method because it will run faster.

if (move):
#first copy the entire folder to the masterdir
 cmdline = "cp -r %s %s" % (imgdir,masterdir)
 os.chdir(BASEDIR)
 os.system(cmdline)
 print (cmdline)
else:
 os.chdir(BASEDIR)
 print("skip copy")


print ("completed copying all of the files")

#second get a file list from the masterdir
#imagedir = ingdir + "/" + "*.RW2"

print(masterdir)
walklist = os.walk(masterdir)
print (walklist)
imglist = [];
for root,dirs,files in walklist:
    for name in files:
        if isImage(name):
           imglist.append((root,name))

#print (imglist)

#connect to the database
try:
   connection = mysql.connector.connect( host="artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com", user="artmaster", passwd="ArtMaster51", database="artmaster")

   cursor = connection.cursor()

except mysql.connector.Error as error:
        exit(-1)

#add the list of image files into the image file table.
if (images):
 sql_insert_query = """ INSERT INTO images (shortName, filename, uri,  master) VALUES (%s, %s, %s, %s)"""
 for root,name in imglist:
    shortname = os.path.splitext(os.path.basename(name))[0]
    auri = BASEURL+root+"/"+name
    insert_tuple_1 = (shortname,name, auri,masterdir)
    cursor.execute(sql_insert_query)
    print(insert_tuple_1)
 connection.commit()
else:
  print("skip images update")


#add the newly added images into the asset table as well
#first get the ids for the newly added images in the master dir
print("addassets")
sql_query = """ SELECT id from images where master='%s';""" % (masterdir)
cursor.execute(sql_query)
records = cursor.fetchall()
#print(records)

#then we traverse and create the asset record
sql_insert_query = """ INSERT INTO asset (shortName, uri, IdAtSource, sourceId, scope, timestamp) VALUES (%s, %s, %s, %s, %s, %s)"""
for i, imgid in enumerate(records):
    print(imgid, i) 
    shortName = os.path.splitext(os.path.basename(imglist[i][1]))[0]
    uri = BASEURL+imglist[i][0] + "/" + imglist[i][1] 
    idAtSource = imgid[0]
    sourceId = 666
    scope = 0
    insert_tuple_1 = (shortName, uri, idAtSource, sourceId, scope, datetime.now())
#    print (insert_tuple_1)
#    print ("\n")
    cursor.execute(sql_insert_query, insert_tuple_1)

connection.commit()
#finished
cursor.close()
connection.close()
