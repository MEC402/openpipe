#dedupMain.py

#main routines for performing the 'deduping' process
#  deduping really means identifying 'known' canon_topic tags and using standardized
# values throughout the asset database

import hjson
import sys
from parse  import *
import re

import assetAssess

#this is a hack: the mods to sys.path should be done in a config element
sys.path.append('e:/builds/openpipe/backend')

from openpipeAPI.ORM.BL import BL
from openpipeAPI.ORM.ORM import ORM
from openpipeAPI.ORM.TO import TO


print("Dedup Begin")

#first lets just generate some basic statistics about the current assets
#  report:
#     number of assets
#     number of canon_topic tags based on status with percentage
#     number of unique canon_topic values as a percent of total values
print("Asset Report Begin")
print("-----------------")
#connect to the federation
aorm = ORM()

numassets=-1
numcanons=-1
myassets = assetAssess.getAssets(aorm)
print("number of assets=%d" % (len(myassets['data'])))

#now we generate canon topic status information
canontopics=['artist']
canonstate=['unknown','formatted', 'probably', 'verified', 'locked']


#now get the list of canonical topics
mycanons = assetAssess.getCanons(aorm)
#get all metaTags that area canonical tag
myctags = assetAssess.getCanonTopics(aorm)
print("Number of Canonical Topic values=%d" %(len(myctags)))

totcount = 0
for ct in mycanons:
    ctcount = 0
    ulist =[]
    for st in canonstate:
       count= 0
       for i in myctags:
         if i['tagName'][0] == ct:
             ctcount += 1
             ulist.append(i['value'][0])
         if i['tagName'][0] == ct and i['status'][0] == st:
             count += 1
             totcount += 1
       
       if count != 0:
         print("Number of %s values for %s(%d) topic=%d" %(st,ct,ctcount,count))
 
    #here we will print out the numbers for unique canonical_values
    #get the list of tags for this canon_topic
    aulist = sorted(set(ulist))
    print("Unique values for %s = %d" % (ct, len(aulist)))
    if len(aulist) < 12:
        print(aulist)
    print("-----")
print("total canon topic tags by stats = %d" % (totcount))

print("-----------------")
print("Asset Repot End")

#generate properly formatted tags from Museum sources
# now we need to go through each asset get its canonical_topics
# properly formatted whenever possible

#get every asset

#for each asset
for anasset in myassets:
    
# get the source museums set of canonical tags properly formated.

#this needs to be a smart map that dynamically maps source id to museum object a case number is a problem.
   mytags = []
   if asource == '1':
       mytags = Museum.getCanonTags(anasset,aorm)

# here is where we put some smarts to not update depending on present value
# now update the canonical tags for this asset from the Museum set.
# we have a setof canonical tags from the Musem
   canTagData = assetAssess.getAssetCanonTags(anasset,aorm)
   for atag in mytags:
      #get teh canonical
      if canTagData['status'] != locked or canTagData['status'] != 'verified':
        canTagData['status'] = 'formatted'
        canTagData['value']= mytags['value']
# Could call format checker to confirm proper format

   assetAsses.updateAssetCanonTags(anasset,aorm)







#generate oracles from the set of properly formatted canonical topic values


#clean up all canon tags based on newly generated oracles


#mark tags in canon values as 'known' or unknown


print("Dedup Done")
