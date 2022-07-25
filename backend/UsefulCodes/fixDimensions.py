import sys
import json

#for ap in sys.path:
#  print (ap)

#this is a hack: the mods to sys.path should be done in a config element
#sys.path.append('d:/builds/op/openpipe/')
sys.path.append('D:\\builds\\op\\openpipe\\backend')
sys.path.append('D:\\builds\\op\\openpipe')

#sys.path.append('d:/builds/op/openpipe/backend/assetSources')

#for ap in sys.path:
#  print (ap)

from openpipeAPI.ORM.ORM import ORM
from backend.openpipeAPI.ORM.TO import TO

orm = ORM()
tables = TO().getClasses()
AssetTab = tables["asset"]
MetaTag = tables["metaTag"]
MetaData = tables["metaData"]

mappings = []

assetList = orm.session.query(AssetTab)

assetDict = {}
dimDict = {}
metDict ={}
clevDict = {}
rijskDict = {}


for ae in assetList:
    mdid = str(ae.metaDataId)
    assetDict[mdid] = ae
    print (mdid)

assetMetaDataList = orm.session.query(MetaTag).filter(MetaTag.tagName == "openpipe_canonical_physicalDimensions")
assetMetList = orm.session.query(MetaTag).filter(MetaTag.tagName == "measurements")
assetClevList = orm.session.query(MetaTag).filter(MetaTag.tagName == "dimensions")
assetRijksList = orm.session.query(MetaTag).filter(MetaTag.tagName == "dimensions")

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
    rijskDict[mdid] = amd
#    print(amd.id, amd.metaDataId, amd.value, amd.tagName)

#now we update the physical Dimensions
# convert each museum type into correct format and store in physical dimension
for ae in assetList:
   print (":" + ae.sourceId + ":")
   mdid = str(ae.metaDataId)
   if mdid in dimDict:
    candim = dimDict[mdid]
    dimstring = "-1.0,-1.0,-1.0"

    if ae.sourceId == "1":
       print("Met")
       print(mdid)
       if mdid in metDict:
         rawent = metDict[mdid]
         dimitem = rawent.value
         jimitem = dimitem.replace("{","{\"").replace(":","\":\"").replace(",","\",\"").replace("}","\"}").replace("\"{","{").replace("}\"","}").replace("\",\" ",", ").replace("\\"," ")
         print(jimitem)
         try:
            dimjson = json.loads(jimitem)
            print(dimjson)
         except Exception:
            print("Broken")
       #here we convert rawent into Dimension information


#    elif ae.sourceId == "2":
#       print("Rijks")
#    elif ae.sourceId == "3":
#       print("Cleveland")
#    else:
#       print("unknown")
       candim.value = dimstring
       print(candim.value)


#for amd in assetMetaDataList:
#    print(amd.id, amd.metaDataId, amd.value, amd.tagName)

#    id = amd.id
#    mid = amd.metaDataId
#    value = str(amd.value).split(" ")
#    if len(value) != 5:
#        print(id,value,"Bad format")
#        mappings.append({"id":id,"value":None,"note":"bad date"})
#    else:
#        if not value[1].isnumeric():
#            print(id, value, "Bad Year")
#            mappings.append({"id": id, "value": None, "note": "bad date"})



# updateSize=len(mappings)
# biteSize=1000
# q=int(updateSize / biteSize)
# r= updateSize % biteSize
#
# for i in range(0,q):
#     print("************** commiting to DB **************")
#     orm.session.bulk_update_mappings(MetaTag, mappings[i*biteSize:i*biteSize+biteSize])
#     orm.session.flush()
#     orm.session.commit()
#     print("************** Done commiting to DB **************")
# orm.session.bulk_update_mappings(MetaTag,mappings[q*biteSize:q*biteSize+r])
# orm.commitClose()
