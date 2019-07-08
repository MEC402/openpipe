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

def matchlist(aroot):
    fullist = os.listdir(aroot)
    reslist = []
    for x in fullist:
      fx = os.path.join(aroot,x)
      if os.path.isdir(fx):
         reslist.append(x)
      elif x.endswith("_thmb.png"):
          a=1 #ignore      
      elif x.endswith(".jpg"):
         reslist.append(x)
    return reslist

def printTree(aroot):
    d = {'name': os.path.basename(aroot)}
    if os.path.isdir(aroot):
      d['type'] = "directory"
      d['children'] = [printTree(os.path.join(aroot,x)) for x in matchlist(aroot)]
      d['thumb'] = os.path.basename(aroot)
      d['url'] = aroot;
    else:
      d['type'] = "file"
      d['thumb'] = aroot.replace(".jpg","_thmb.png") 
      d['url'] = aroot;
    return d

#refactor the dictory so that each node only has at most 16 children
def refactor(adict):
    bdict = {'name': adict['name']}
    if adict['type'] == "file":
      return adict
    #refactor each of the children
    rfchildren = [refactor(x) for x in adict['children']]
    #if more than 16 children have to split up
    if len(rfchildren) > 16:
       rfbchildren = []
       nnode = {'name': adict['name'] + "0"}
       nnode['children'] = []
       nnode['type'] = "directory"
       nnode['thumb'] = "thumb"
       nnode['url'] = "url"
       for i,ac in enumerate(rfchildren):
           nnode['children'].append(ac)
           if (i+1) % 16 == 0:
              rfbchildren.append(nnode)
              nnode = {'name': adict['name'] + str(i)}
              nnode['children'] = []
              nnode['type']= "directory"
              nnode['thumb'] = "thumb"
              nnode['url'] = "url"
       if len(nnode['children']) > 0:
          rfbchildren.append(nnode)
       rfchildren = rfbchildren  

    bdict['type'] = "directory"
    bdict['children'] = rfchildren
    bdict['thumb'] = adict['thumb']
    bdict['url'] = adict['url']
    return bdict

#do a post order traversal and add a thumb to the directory
def fixDirThumbs(adict):
    athumb=adict['thumb']
    if adict['type'] == "file": 
       return adict['thumb']
    for x in adict['children']:
       athumb = fixDirThumbs(x)
    adict['thumb'] = athumb
    return athumb
    

checkArgs(sys.argv);
panodir = sys.argv[1];

# print out opening of JSON file
print ("var treeData =\n")
print

#traverse list and generate tree
adict = printTree(panodir)
#reduce directories to only hold at most 16 images for better visual layout
bdict = refactor(adict)
#now put images in the direcotry sections Bottom up traversal
ignore = fixDirThumbs(bdict)
#dump out the json file
print json.dumps(bdict)

#print closing parts of JSON file
