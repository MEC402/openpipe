import cv2
import sys
from os.path import isfile

if len(sys.argv) != 4:
  print("Incorrect number of arguments!")
  print("Usage: python find_rig.py filename rotation[0=counterclockwise, 1=clockwise] output_filename")
  exit("Terminated")

if not isfile(sys.argv[1]):
    exit("File not found!")

img = cv2.imread(sys.argv[1])

if int(sys.argv[2]) == 0:
    img = cv2.rotate(img,cv2.ROTATE_90_COUNTERCLOCKWISE)
else:
    img = cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE)

cv2.imwrite(sys.argv[3], img)
