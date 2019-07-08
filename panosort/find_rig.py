import cv2
import numpy as np
import sys
from os.path import isfile

if len(sys.argv) != 2:
  print("Incorrect number of arguments!")
  print("Usage: python find_rig.py filename")
  exit("Terminated")

scale = 0.25 # Value to downsize the original images

if not isfile(sys.argv[1]):
  exit("File not found!")

# Read the images and resize them
img = cv2.imread(sys.argv[1])
img = cv2.resize(img, (int(img.shape[0]*scale), int(img.shape[1]*scale)))
tmp = cv2.imread('lever.ppm')
tmp = cv2.resize(tmp, (int(tmp.shape[0]*scale), int(tmp.shape[1]*scale)))

# Compute template matching with squared difference normed
res = cv2.matchTemplate(img,tmp,cv2.TM_SQDIFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

#print(min_val, min_loc)

# Decide wheter the rig is at the right or left
if min_loc[0] < img.shape[0]/2:
    print(True) # lEFT sid
else:
    print(False) # RIGHT side
