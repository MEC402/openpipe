#
# transform a directory of tile files with _L, and Left names
#
# for a directory of tile panoramas group _L and _R and convert into /left,/right format
# also group Left,Right pairs and convert into similar structure
# for non stereo move into left directory ignoring duplicates

import glob;
import sys;
import os;
import shutil;

def checkArgs(argv):
#    print "this is the name of the script: ", argv[0];
#    print "Number of argument in: ", len(argv);
    if (len(argv) != 3):
      print (argv[0] + ": {panodirectory}");
      sys.exit(1);

def listPanoDir(adir):
    # simply list all of the files in the directory
    panofiles = glob.glob(adir+"/*")
    return panofiles;

checkArgs(sys.argv);
targdir = sys.argv[2];
#first we get a list of the files contained in the directory
panofileslist = listPanoDir(sys.argv[1]);
#print (panofileslist);

#then we process all of the ones with _L in the name
Lreslist =[];
for pf in panofileslist:
    if pf.endswith("_L"):
        Lreslist.append(pf);

print (Lreslist);
for apf in Lreslist:
    panofileslist.remove(apf);
    rpf = apf.replace("_L","_R");
    if rpf in panofileslist:
        panofileslist.remove(rpf);

#then we process all of the ones with Left in the name
Leftreslist =[];
for pf in panofileslist:
    if "Left" in pf:
        Leftreslist.append(pf);
print (Leftreslist);

for apf in Leftreslist:
    panofileslist.remove(apf);
    rpf = apf.replace("Left","Right");
    if rpf in panofileslist:
       panofileslist.remove(rpf);

#then we process the remaining
print (panofileslist);

# we have the lists for everything now we need to make the directorys and copy the folders
for apf in Lreslist:
    # get base name
    bpf = os.path.basename(apf);
    # remove the _L
    bpfnol = bpf.replace("_L","");
    print (bpfnol);
    #create target location
    directory = os.path.dirname(targdir+"\\"+bpfnol+"\\");
    print (directory);
    #if not os.path.exists(directory):
    #    os.makedirs(directory);

    # copy _L to panoLRdbase/rlctiles/basename/left
    shutil.copytree(apf,targdir+"\\"+bpfnol+"\\left");
    #os.system(cpstring);
    # if _R exists in panodbase/rlctiles then copy to
    # panoLRdbase/rlctiles/right
    rpf = apf.replace("_L","_R");
    if os.path.exists(rpf):
       shutil.copytree(rpf,targdir+"\\"+bpfnol+"\\right");


for apf in Leftreslist:
    # get base name
    bpf = os.path.basename(apf);
    # remove the _L
    bpfnol = bpf.replace("Left","");
    print (bpfnol);
    #create target location
    directory = os.path.dirname(targdir+"\\"+bpfnol+"\\");
    print (directory);
    if not os.path.exists(directory):
#    print (targdir+"\\" + bpfnol + "\\left");
       shutil.copytree(apf,targdir+"\\"+bpfnol+"\\left");
    #os.system(cpstring);
    # if _R exists in panodbase/rlctiles then copy to
    # panoLRdbase/rlctiles/right
       rpf = apf.replace("Left","Right");
       if os.path.exists(rpf):
          shutil.copytree(rpf,targdir+"\\"+bpfnol+"\\right");

for apf in panofileslist:
    # get base name
    bpf = os.path.basename(apf);
    # remove the _L
    bpfnol = bpf;
    print (bpfnol);
    #create target location
    directory = os.path.dirname(targdir+"\\"+bpfnol+"\\");
    print (directory);
    if not os.path.exists(directory):
        shutil.copytree(apf,targdir+"\\"+bpfnol+"\\left");
