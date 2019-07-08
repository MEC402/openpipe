#!/usr/bin/python

#python code for generating png tiles in the marzipano compatible layout
# gentiles Image_prefix
#

import sys;
import os;
import glob;
import ntpath;


def mktiles(basename, imgprefix):

# loop over each level
# build directory structure
# generate arguments to magick
  os.makedirs(basename);
  for level in range(1,5):
      os.mkdir(basename+str(level));
      #             4   5   0   2   1   3
      for face in {"u","d","b","f","l","r"}:
          adirname = basename + str(level) + "/" + face;
          filename = imgprefix+"."+face+".png";
          os.mkdir(adirname);
          h = pow(2,(level-1));
          tsize = h*512;
          for row in range(0,h):
              #path to an image is {basedir}/{level_number}/{facename}/{row#}/{col#}.png
              adirname = basename + str(level) + "/" + face + "/" + str(row);
              os.mkdir(adirname);
              offsety = row * 512;
              for col in range(0,h):
                  offsetx = col*512;
                  print("%d %s %d %d" % (level,face,row,col));
                  outfile = adirname+"/"+str(col)+".png";
#                  cmdline = "magick convert %s -resize %dx%d -crop 512x512+%d+%d %s" % (filename,tsize,tsize,offsetx,offsety,outfile);
                  cmdline = "convert %s -resize %dx%d -crop 512x512+%d+%d %s" % (filename,tsize,tsize,offsetx,offsety,outfile);
                  print(cmdline);
                  os.system(cmdline);

#get the list of panos to cut
#panoheads = glob.glob("d:/base/panoramas/RLC/RLC-2017/Cubes/*.b.png");
#now cut the tails off of each string
#panotails =[];
#for p in panoheads:
#    pt = ntpath.basename(p);
#    pt = pt[:-6];
#    panotails.append(pt);

#generate the actual tiles
#for p in panotails:
#    addir = "d:\\base\\panoramas\\rlctilesColor\\"+p+"\\";
#    imgpref = "d:\\base\\panoramas\\RLC\\RLC-2017\\Cubes\\"+p;
#    print (addir); print (imgpref);

if len(sys.argv) != 3:
    print("gentiles.py imgpref outdir");
    sys.exit(-1);

mktiles(sys.argv[2],sys.argv[1]);
