from backend.openpipeAPI.ORM.ORM import ORM
from backend.openpipeAPI.ORM.TO import TO

orm = ORM()
tables = TO().getClasses()
MetaTag = tables["metaTag"]
MetaData = tables["metaData"]

insertDataArray = []

assetMetaDataList = orm.session.query(MetaTag).filter(MetaTag.tagName == "openpipe_canonical_date")
for amd in assetMetaDataList:
    mid = amd.metaDataId
    value = str(amd.value).split(" ")
    if len(value) != 5:
        print(mid,value,"Bad format")
        insertDataArray.append(MetaTag(metaDataId=mid,tagName="openpipe_canonical_displayDate", value="", topic_id=-1,note="bad date"))
    else:
        if not value[1].isnumeric():
            print(mid, value, "Bad Year")
            insertDataArray.append(
            MetaTag(metaDataId=mid, tagName="openpipe_canonical_displayDate", value="", topic_id=-1, note="bad date"))

    if len(value) == 5 and value[1].isnumeric():
        year = str(int(value[1])) + " " + value[0]
        print(mid, value, year)
        insertDataArray.append(MetaTag(metaDataId=mid,tagName="openpipe_canonical_displayDate", value=year, topic_id=-1))

insertSize = len(insertDataArray)
biteSize = 1000
q = int(insertSize / biteSize)
r = insertSize % biteSize

orm1 = ORM()
for i in range(0, q):
    print(orm1.bulkInsert(insertDataArray[i * biteSize:i * biteSize + biteSize]))
orm1.bulkInsert(insertDataArray[q * biteSize:q * biteSize + r])
orm1.commitClose()
