#!/usr/bin/python
#
# generate panorama JSON file from a directory listing

import glob;
import sys;
import os;
import json;

def checkArgs(argv):
#    print "this is the name of the script: ", argv[0];
#    print "Number of argument in: ", len(argv);
    if (len(argv) < 2):
      print (argv[0] + ": {panodirectory}");
      sys.exit(1);


def printPano(panofile,aname,anavlist,aicon):
  idname = os.path.basename(panofile);
  rpanofile = panofile.replace("\\","/");
  print ("{\"id\": \""+idname+"\",")
  print (" \"name\": \""+aname+"\",")
  print (" \"left\": \""+rpanofile+"/left/%d/%d/%d/%d.png\",")
  print (" \"right\": \""+rpanofile+"/right/%d/%d/%d/%d.png\",")
  print (" \"thumb\": \""+rpanofile+"/left/1/f/0/0.png\",")
  print (" \"icon\": \""+aicon+"\",")
  if (len(anavlist) > 1):
     yvnl = anavlist[2];
     print (" \"yaw\": "+ str(yvnl["yaw"])+",")
  else:
     print (" \"yaw\": 0.0,")

  print (" \"navlink\": [");
  gyaw = 0.0;
  afirst = 0;
  for anl in anavlist[3:]:
      ayaw = gyaw;
      apitch = 0.0;
      acon = "generic-128x128.png";
      if "yaw" in anl:
          ayaw = anl["yaw"];
          apitch = anl["pitch"];
      if "icon" in anl:
          acon = anl["icon"];
      if (afirst != 0):
           print (",");
      print("{ \"id\": \""+anl["id"]+"\", \"yaw\": "+str(ayaw)+", \"pitch\": " +str(apitch)+" }");
      gyaw += 0.1;
      afirst = 1;
  print (" ]}");

checkArgs(sys.argv);
panodir = sys.argv[1];
#load up name file
namelist =[];
if (len(sys.argv)  == 3):
    with open(sys.argv[2]) as json_fp:
      namelist = json.load(json_fp);
#BarDinning_L
#for np in namelist:
#    print (np);
#print (namelist["BarDinning_L"]);
#sys.exit(1);
#print panodir
panofiles = glob.glob(panodir+"/*")
# print header of JSON file
print ("{\n\"title\": \"Panoramas\",")
print ("\"panos\": [")
print
first=0
for file_name in panofiles:
    if (first != 0):
       print (",")
    aname = os.path.basename(file_name)
    navlist = [];
    acon = "generic-128x128.png";
    if (len(namelist) > 0):
        if (aname in namelist):
          #print (namelist[aname]);
          navlist = namelist[aname];
          acon = namelist[aname][1];
          aname = namelist[aname][0];

    #print (aname);
    printPano(file_name,aname,navlist,acon);
    first = 1


#print closing parts of JSON file
print ("]")
print ("}")
