import sys
import json

#for ap in sys.path:
#  print (ap)

#this is a hack: the mods to sys.path should be done in a config element
#sys.path.append('d:/builds/op/openpipe/')
sys.path.append('D:\\builds\\openpipe\\backend')
sys.path.append('D:\\builds\\openpipe\\backend\\assetSources')
sys.path.append('D:\\builds\\openpipe')

#sys.path.append('d:/builds/op/openpipe/backend/assetSources')

#for ap in sys.path:
#  print (ap)

from openpipeAPI.ORM.ORM import ORM
from backend.openpipeAPI.ORM.TO import TO
from backend.assetSources.FormatConvert import formatHelp
from backend.assetSources.FormatConvert import FormatConvert

orm = ORM()
tables = TO().getClasses()
AssetTab = tables["asset"]
MetaTag = tables["metaTag"]
MetaData = tables["metaData"]

mappings = []

assetList = orm.session.query(AssetTab)

#list of all asset metadatIds
assetDict = {}

#list of asset canonical dimension 
dimDict = {}

#list of MET Dimensions tags
metDict ={}
metassets = 0
metmisses = 0

#list of Cleveland Dimensions tags
clevDict = {}
clevassets = 0
clevmisses = 0

#list of Rijks Dimensions tags
rijksDict = {}
rijksassets = 0
rijksmisses = 0

#list of assets without canonical dimensions tag
nocanon = {}

#list of MET assets missing museum dimension tag
nometdim = {}

#handle mislabeled source items
sourceDict = {}


for ae in assetList:
    mdid = str(ae.metaDataId)
    assetDict[mdid] = ae
#    print (mdid)

assetMetaDataList = orm.session.query(MetaTag).filter(MetaTag.tagName == "openpipe_canonical_physicalDimensions")
assetMetList = orm.session.query(MetaTag).filter(MetaTag.tagName == "measurements")
assetClevList = orm.session.query(MetaTag).filter(MetaTag.tagName == "dimensions")
assetRijksList = orm.session.query(MetaTag).filter(MetaTag.tagName == "dimensions")
sourceList = orm.session.query(MetaTag).filter(MetaTag.tagName == "openpipe_canonical_source")

for amd in assetMetaDataList:
    mdid = str(amd.metaDataId)
    dimDict[mdid] = amd
#    print(amd.id, amd.metaDataId, amd.value, amd.tagName)

for amd in assetMetList:
    mdid = str(amd.metaDataId)
    metDict[mdid] = amd
#    print(amd.id, amd.metaDataId, amd.value, amd.tagName)

for amd in assetClevList:
    mdid = str(amd.metaDataId)
    clevDict[mdid] = amd
#    print(amd.id, amd.metaDataId, amd.value, amd.tagName)

for amd in assetRijksList:
    mdid = str(amd.metaDataId)
    rijksDict[mdid] = amd
#    print(amd.id, amd.metaDataId, amd.value, amd.tagName)

for amd in sourceList:
    mdid = str(amd.metaDataId)
    sourceDict[mdid] = amd
#    print(amd.id, amd.metaDataId, amd.value, amd.tagName)

updateddims = {}
#now we update the physical Dimensions
# convert each museum type into correct format and store in physical dimension
for ae in assetList:
   print (":" + ae.sourceId + ":")

   mdid = str(ae.metaDataId)

   #handle broken sourceid if possible
   if ae.sourceId == 'undefined':
       asrc = sourceDict[mdid]
       print (asrc.value)
       if asrc.value == 'The Metropolitan Museum of Art':
           ae.sourceId = "1"
       if asrc.value == 'Cleveland Museum of Art':
           ae.sourceId = "3"
       if asrc.value == 'Rijksmuseum Amsterdam':
           ae.sourceId = "2"
       print(ae.sourceId)

   if mdid in dimDict:
    candim = dimDict[mdid]
    dimstring = "-1.0,-1.0,-1.0"

    if ae.sourceId == "1":
       metassets += 1
#       print("Met")
#       print(mdid)
       if mdid in metDict:
         rawent = metDict[mdid]
         dimitem = rawent.value
         #here we convert rawent into Dimension information
         dimstring = FormatConvert.getMetDimensionsString(dimitem)
         #store the dimensions away
         if dimstring != "-1.0,-1.0,-1.0":
           candim.value = dimstring
           updateddims[mdid] = candim
#         print (candim.value)

       else:
          metmisses += 1
          nometdim[mdid] = ae



    elif ae.sourceId == "2":
       rijksassets += 1
       print("RIJKS")
       print(mdid)
       if mdid in rijksDict:
         rawent = rijksDict[mdid]
         dimitem = rawent.value
         #here we convert rawent into Dimension information
         dimstring = FormatConvert.getRijksDimString(dimitem)
         #store the dimensions away
         if dimstring != "-1.0,-1.0,-1.0":
           candim.value = dimstring
           updateddims[mdid] = candim
           print (candim.value)

       else:
          rijksmisses += 1
          nometdim[mdid] = ae
    elif ae.sourceId == "3":
       clevassets += 1
       print("CLEV")
       print(mdid)
       if mdid in clevDict:
         rawent = clevDict[mdid]
         dimitem = rawent.value
         #here we convert rawent into Dimension information
         dimstring = FormatConvert.getClevDimString(dimitem)
         if mdid == '12479':
             print(dimstring)
         #store the dimensions away
         if dimstring != "-1.0,-1.0,-1.0":
           candim.value = dimstring
           updateddims[mdid] = candim
           print (candim.value)

       else:
          clevmisses += 1
          nometdim[mdid] = ae
#    else:
#       print("unknown")
#       candim.value = dimstring
#       print(candim.value)
   else:
      nocanon[mdid] = ae

print(f"Assets without canonical Dimension tag: %d/%d" % (len(nocanon),len(assetDict)))
print("Met Assets without any museum measurements tag:" + str(len(nometdim))+"/"+str(metassets))
print("Update  Dims:" + str(len(updateddims)))
print(f"Met %d Rijks %d Cleveland %d" % (metassets,rijksassets,clevassets))
print(f"Misses of Met %d Rijks %d Cleveland %d" % (metmisses,rijksmisses,clevmisses))


# now we update all the canonical physical dimensions

mappings = []
for akey in updateddims:
    amd = updateddims[akey]
    #print(amd.id, amd.metaDataId, amd.value, amd.tagName)
    mappings.append({"id": amd.id, "value": amd.value, "note": "revised"})



updateSize=len(mappings)
biteSize=1000
q=int(updateSize / biteSize)
r= updateSize % biteSize

for i in range(0,q):
     print("************** commiting to DB **************")
     print(f"Block %d" % (i))
     orm.session.bulk_update_mappings(MetaTag, mappings[i*biteSize:i*biteSize+biteSize])
     orm.session.flush()
     orm.session.commit()
     print("************** Done commiting to DB **************")
print(f"Block %d" %(q))
orm.session.bulk_update_mappings(MetaTag,mappings[q*biteSize:q*biteSize+r])
orm.commitClose()
