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

panofiles = glob.glob(basedir+"/*/thumb.png")

print (panofiles);

cmdlist = [];
for ap in panofiles:
    rap = ap.replace("\\","/");
    acmd = "aws s3 cp  "+ap + " s3://silvrcity.com/rlc/"+ rap + " " ;
    cmdlist.append(acmd);
    print (acmd);

print (cmdlist);
for acmd in cmdlist:
    os.system(acmd);
