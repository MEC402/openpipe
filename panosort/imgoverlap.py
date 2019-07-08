#!/usr/bin/python

#compare two images and report if they overlap or not
# use open CV

#from skimage.measure import compare_ssim
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os;
import datetime;
import skimage.measure;
#import commands;

#use exif data to compare timestamp on image files
# if the time between two shots is more than 10 seconds then not the same panorama.
def chkOverlapTime(img1file,img2file):
#    cmds = "d:/bin/exiftool.exe -TAG -CreateDate " + img1file;
    cmds = "exiftool -TAG -CreateDate " + img1file;
    stamp1 = os.popen(cmds).read();
    dstamp1 = stamp1.split(':',1);
    dtime1 = datetime.datetime.strptime(dstamp1[1].strip(), "%Y:%m:%d %H:%M:%S");

#    os.system(cmds);
#    cmds = "d:/bin/exiftool.exe -TAG -CreateDate " + img2file;
    cmds = "exiftool -TAG -CreateDate " + img2file;
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
    if asecs > 10:
        return False;
    #else
    return True;

def imgRotComp(img1file,img2file):
    #first thing it may be necessary to convert the two input images to PNG
    cmds = "dcraw -c " + img1file + " | magick convert - /data/scratch/img1.png";
    print (cmds);
    os.system(cmds);
    cmds = "dcraw -c "+  img2file + " | magick convert - -rotate 180 /data/scratch/img2.png";
    print (cmds);
    os.system(cmds);
    #get the two images -- RW2 may not be supported
    img1 = cv2.imread("/data/scratch/img1.png",0);
    img2 = cv2.imread("/data/scratch/img2.png",0) # trainImage
    if img1 is None:
      print("Error loading image");
      return False;
    if img2 is None:
      print("Error loading image");
      return False;
    #assim = skimage.measure.compare_ssim(img1,img2);
    #print(assim);
    if not img1.shape == img2.shape:
        return False;

    res = cv2.norm(img1,img2,4);
    print(res);
    if res < 250000:
        return True;
    return False;

#see if two images share overlapping components
def testOverlap(img1file,img2file):
    #first thing it may be necessary to convert the two input images to PNG
    cmds = "magick convert " + img1file + " d:/tmp/img1.png";
    print (cmds);
    os.system(cmds);
    cmds = "magick convert " + img2file + " d:/tmp/img2.png";
    os.system(cmds);
    #get the two images -- RW2 may not be supported
    img1 = cv2.imread("d:/tmp/img1.png",0);
    img2 = cv2.imread("d:/tmp/img2.png",0) # trainImage
#    if img1 == None:
#      print("Error loading image");
#      return False;

    res = cv2.norm(img1,img2,2);
    print(res);
    if res > 500000000:
        return False;
    else:
        return True;
    # Initiate ORB detector
    orb = cv2.ORB_create()
    # find the keypoints and descriptors with ORB
    kp1, des1 = orb.detectAndCompute(img1,None)
    kp2, des2 = orb.detectAndCompute(img2,None)

    # create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    # Match descriptors.
    matches = bf.match(des1,des2)
    # Sort them in the order of their distance.
    matches = sorted(matches, key = lambda x:x.distance)
    print(len(matches));
    if len(matches) < 50:
        return False;
    ai = matches[0];
    print(ai.distance);
    if ai.distance > 45:
        return False;

    # Draw first 10 matches.
#    img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches[:200], None,flags=2)
#    plt.imshow(img3),plt.show()
    return True;


#testOverlap('side1.png','side2.png');
#testOverlap('o:/panmasters/cardmasters/anne_frank_shoot_march_27_2015\sd_anne_cam_c/P1140647.RW2',
#            "o:/panmasters\cardmasters/anne_frank_shoot_march_27_2015\sd_anne_cam_c\P1140646.RW2");
