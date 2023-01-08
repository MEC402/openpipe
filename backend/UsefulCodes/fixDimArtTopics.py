#dedupMain.py

#main routines for performing the 'deduping' process
#  deduping really means identifying 'known' canon_topic tags and using standardized
# values throughout the asset database

import hjson
import sys
from parse  import *
import re
import json

import assetAssess

#this is a hack: the mods to sys.path should be done in a config element
sys.path.append('d:/builds/openpipe/backend')
sys.path.append('d:/builds/openpipe/backend/assetSources')

from openpipeAPI.ORM.BL import BL
from openpipeAPI.ORM.ORM import ORM
from openpipeAPI.ORM.TO import TO
from assetSources import MuseumsR


print("Fix Dim, Artist, Medium Begin")

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

getalltags="select * from asset join metaTag on asset.metaDataId=metaTag.metaDataId order by asset.metaDataId;"
allassets = aorm.executeSelect(getalltags)
alltags = allassets['data']
print("number of all assets=%d" % (len(allassets['data'])))
if len(allassets['data']) == 0:
        sys.exit(-1)

print("number of assets=%d" % (len(myassets['data'])))

#sys.exit(-1)

#now we generate canon topic status information
canontopics=['artist']
canonstate=['unknown','formatted', 'probably', 'verified', 'locked']

#if 1 == 1:
if 0 == 1:
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
 print("Asset Report End")

#generate properly formatted tags from Museum sources
# now we need to go through each asset get its canonical_topics
# properly formatted whenever possible

print("-----------------")
print("Begin Formatting Canonical Tags")
print("-----------------")
# load up the Museum information
amuseumReg = MuseumsR.MuseumsR()
amuseumReg.loadMuseums()

#load up source to Museum object mapping
asourcemap = amuseumReg.getSourceMap()
print(asourcemap)

#get every asset

#for each asset
assetcount = 0
curtagrow = 0
canonresults = []
for anasset in myassets['data']:
#   print(anasset)
# get the source museums set of canonical tags properly formated.

#this needs to be a smart map that dynamically maps source id to museum object a case number is a problem.
   mytags = []
   sourceid = anasset['sourceId'][0]
   metadataid = anasset['metaDataId'][0]

   if sourceid in asourcemap:
       print ("SOURCEID",sourceid)
       amuseum = asourcemap[sourceid]
       print(amuseum, "sourceid",sourceid,metadataid)
#       print(anasset)

       #this call returns a list of canonical tags for the given museum
       # mapped from the tags the museum defines as appropriate.
#       mytags = amuseum.getMappedCanonTags(anasset,aorm,allassets,mdataindex)
       mytags,curtagrow = amuseum.getMappedCanonTags(metadataid,aorm,alltags,curtagrow)
#       print(curtagrow)
       if mytags == None:
           print("no tags")
       else:
           print ("BRICKME",mytags)
           for atag in mytags:
               mytags[atag]['metaDataId'] = metadataid
               if atag == 'openpipe_canonical_physicalDimensions':
                  print(atag)
           print ("BRICKME2",mytags)
   else:
     while curtagrow < len(alltags) and alltags[curtagrow]['metaDataId'][0] == metadataid:
#       print (sourceid, alltags[curtagrow]['metaDataId'][0], metadataid,curtagrow)
       curtagrow += 1

   assetcount += 1
   if assetcount %100 == 0:
       print("assetcount = %d" % (assetcount))
print("-----------------")
print("Ready to Update Canon Tags")

sys.exit(-1)

#now we generate the series of sql strings to update values.

print("Number of records to update = %d" % (len(canonresults)))
fullcount = 0
fulstmt = ""
for uprec in canonresults:
#    print(uprec)
    for akey in uprec:
     if 'value' in uprec[akey]:
       avalue = uprec[akey]['value']
#       print(len(avalue))
       if isinstance(uprec[akey]['value'],list):
#           print("isList")
           if len(uprec[akey]['value']) == 1:
               avalue = uprec[akey]['value'][0]

       escstring = avalue.replace('"','')
       midstring = escstring.encode("ascii","ignore")
       escstring = midstring.decode()
       sqlstmt ="update metaTag set value='%s' , status='formatted' where metaDataId='%s' and tagName='%s'; " % (escstring, uprec[akey]['metaDataId'],akey)
       print(sqlstmt)
       fulstmt += sqlstmt
#       print(sqlstmt)
#       print(oenres)
#       if fullcount == 5:
#           sys.exit(-1)
       fullcount += 1
       if fullcount %10 == 0:
           print("fullcount = ",fullcount)
           updateres= aorm.updateSqlMulti(fulstmt)
           fulstmt = ""
#updateres= aorm.updateSqlMulti(fulstmt)
#print(updateres)

print("-----------------")
print("Completed Updating Canonical Tags")



#generate oracles from the set of properly formatted canonical topic values


#clean up all canon tags based on newly generated oracles


#mark tags in canon values as 'known' or unknown


print("Dedup Done")
