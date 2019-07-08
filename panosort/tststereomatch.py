#!/usr/bin/python

#tststereomatch.py
#
# check the matchstereopans command line script.
# check one panorama against a list of panos and see if works.
#
#

import sys;
import glob;
from panorec import panoRec;
import csv

def printUsage():
    print("genpanorecs.py <imagelist file>");

print("Generate Panorama Records from Image File List");

#check arguments and abort if incomplete
if len(sys.argv) != 3:
   printUsage();
   exit(1);
