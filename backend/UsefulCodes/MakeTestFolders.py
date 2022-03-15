from backend.openpipeAPI.ORM.ORM import ORM
from backend.openpipeAPI.ORM.TO import TO

orm = ORM()
tables = TO().getClasses()
CM = tables["collectionMember"]


sfid=212
mfid=213
lfid=214

ss=[16,128,512]

assetResultSet = orm.executeSelect(
    """select * from asset where metaDataId in (select metaDataId from metaTag where tagName='openpipe_canonical_largeImage' and value like '%mec402%' and value not like '%http://mec402.boisestate.edu/assets/largeImage.jpg%') order by id desc;""")


ss=assetResultSet['data'][0:16]

ms=assetResultSet['data'][16:144]

ls=assetResultSet['data'][144:656]



print(len(ss))
print(len(ms))
print(len(ls))

insertDataArray=[]

for i in ss:
    aid=i['id'][0]
    insertDataArray.append(CM(assetId=aid, collectionId=sfid, searchTerm="test"))


for i in ms:
    aid=i['id'][0]
    insertDataArray.append(CM(assetId=aid, collectionId=mfid, searchTerm="test"))

for i in ls:
    aid=i['id'][0]
    insertDataArray.append(CM(assetId=aid, collectionId=lfid, searchTerm="test"))


print(len(insertDataArray))

orm1 = ORM()
orm1.bulkInsert(insertDataArray)
orm1.commitClose()
