#
# generate preview.jpg files

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


checkArgs(sys.argv);
basedir = sys.argv[1];

panofiles = glob.glob(basedir+"/*")

print (panofiles);

cmdlist = [];
for ap in panofiles:
    bfiles = glob.glob(ap+"/left/1/*/0/0.png");
    acmd = "magick montage  +label -geometry 256x256+0+0 -tile 1x6 -strip -interlace Plane "+" ".join(bfiles) + " " + ap + "/left/preview.png";
    cmdlist.append(acmd);
    print (acmd);
    rfiles = glob.glob(ap+"/right/1/*/0/0.png");
    if (len(rfiles) > 0):
     acmd = "magick montage  +label -geometry 256x256+0+0 -tile 1x6 -strip -interlace Plane "+" ".join(rfiles) + " " + ap + "/right/preview.png";
     cmdlist.append(acmd);

print (cmdlist);
for acmd in cmdlist:
    os.system(acmd);
