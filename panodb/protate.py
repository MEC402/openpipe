#
# protate.py
#
# protate.py degree targdir
#
# rotate all the files in the specified directory

#import sqlite3;
import os;
import sys;
import glob;

def printUsage():
    print("protate angle targetdir")

#parse command line options
print (sys.argv)
if (len(sys.argv) != 3):
 printUsage();
 exit(-1)

rotangle = sys.argv[1];
targdir = sys.argv[2];

cmdline = "cd %s; magick convert -rotate %s -format png *.RW2 " % (targdir, rotangle)
print(cmdline)
os.system(cmdline)




# magick mogrify -rotate 90 -format png *.RW2



#finished
