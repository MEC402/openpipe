#!/usr/bin/python

# pptogen -- generate a Hugin pto file capable of being loaded into Autopano or cp_find
#

import sys;
import glob;
import ntpath;

def printUsage():
    print("pptogen <panodirectory>");

#check arguments and abort if incomplete
if len(sys.argv) != 2:
   printUsage();
   exit(1);

#first traverse the directory and get list of files
topdir = sys.argv[1];

count = 0;
srcdir = topdir+'/**/*.png';
filelist =[]
for filename in glob.iglob(srcdir,recursive=True):
    count += 1;
    #print(filename);
    filelist.append(filename)


#print("Number of files=",count);
#check if number of files != 136
if count != 136:
    print("Error:Number of files=",count);
    exit(1);

#have the files ready for processing
#first output the header of the pto file
ptohead= """
# hugin project file
#hugin_ptoversion 2
p f2 w16384 h8192 v360  E0 R0 n"TIFF_m c:LZW"
m i0
"""
print(ptohead)

#now output the image list
#imgtemplate="""
#i w3016 h4016 f0 v=0 Ra=0 Rb=0 Rc=0 Rd=0 Re=0 Eev0 Er1 Eb1 r0 p%s y%s TrX0 TrY0 TrZ0 Tpy0 Tpp0 j0 a=0 b=0 c=0 d=0 e=0 g=0 t=0 Va=1 Vb=0 Vc=0 Vd=0 Vx=0 Vy=0  Vm5 n"%s"
##-hugin  cropFactor=1
#"""

imgtemplate="i w3016 h4016 f0 v66 r0 p%s y%s n\"%s\""

for i in range(8):
 for j in range(17):
  afname = filelist[i*8+j]
  afname = ntpath.basename(afname)
  pitch = (i % 8) * 180.0/8.0 - 90.0
  yaw = (j % 17) * 360.0/17.0 - 180.0 
  print (imgtemplate % (pitch,yaw, afname))

#now output the variable section
hvariables= """
# specify variables that should be optimized
v Ra0
v Rb0
v Rc0
v Rd0
v Re0
v Vb0
v Vc0
v Vd0
"""
#print (hvariables)

vtemplate="""
v Eev%s
v r%s
v p%s
v y%s
"""

#for i in range(136):
#   tcn = i+1
#   print (vtemplate % (tcn,tcn,tcn,tcn), end="")


#now we print out simple linking control points
lnk="c n%s N%s x1972.7170535 y1024.08424 X472.2120 Y967.298 t0"

print("""
# control points
""")

for i in range(8):
   for j in range(17):
     print(lnk %(i*17+j,i*17 + ((j+1)%17)))

for i in range(17):
   for j in range(8):
     print(lnk %(j*17+i,((j+1)*17+i)%136))

#finally ouput various parameters
print ("""
#hugin_optimizeReferenceImage 0
#hugin_blender enblend
#hugin_remapper nona
#hugin_enblendOptions 
#hugin_enfuseOptions 
#hugin_hdrmergeOptions -m avg -c
#hugin_verdandiOptions 
#hugin_outputLDRBlended true
#hugin_outputLDRLayers false
#hugin_outputLDRExposureRemapped false
#hugin_outputLDRExposureLayers false
#hugin_outputLDRExposureBlended false
#hugin_outputLDRStacks false
#hugin_outputLDRExposureLayersFused false
#hugin_outputHDRBlended false
#hugin_outputHDRLayers false
#hugin_outputHDRStacks false
#hugin_outputLayersCompression LZW
#hugin_outputImageType tif
#hugin_outputImageTypeCompression LZW
#hugin_outputJPEGQuality 90
#hugin_outputImageTypeHDR exr
#hugin_outputImageTypeHDRCompression LZW
#hugin_outputStacksMinOverlap 0.7
#hugin_outputLayersExposureDiff 0.5
#hugin_outputRangeCompression 0
#hugin_optimizerMasterSwitch 1
#hugin_optimizerPhotoMasterSwitch 21
""")
