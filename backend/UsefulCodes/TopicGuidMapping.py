import re

from sqlalchemy import and_

from backend.openpipeAPI.ORM.ORM import ORM
from backend.openpipeAPI.ORM.TO import TO

orm = ORM()
tables = TO().getClasses()
MetaTag = tables["metaTag"]
Topic = tables["topic"]

guidMappingResultSet = orm.executeSelect(
    """SELECT * FROM artmaster.guidType;""")

guidCodeMap = {}

for guidMap in guidMappingResultSet["data"]:
    guidCodeMap[guidMap["name"][0]] = str(guidMap["code"][0])

print(guidCodeMap)

topicsResultSet = orm.executeSelect(
    """SELECT * FROM artmaster.topic;""")

topicHashMap = {}

for topic in topicsResultSet["data"]:
    topicCode = str(topic["code"][0])
    if topicCode in topicHashMap:
        topicHashMap[topicCode].append(topic)
    else:
        topicHashMap[topicCode] = [topic]

print(topicHashMap.keys())
# print(topicHashMap["400"])

metaTagResultSet = orm.executeSelect(
    """SELECT * FROM artmaster.metaTag where tagName like 'openpipe_canonical_%' order by metaDataId asc;""")

# stm= """select asset.metaDataId from asset  join collectionMember on asset.id=assetId where collectionId=222"""
# metaTagResultSet = orm.executeSelect(stm)

updateDataArray = {}

banCanonicals = ["openpipe_canonical_id", "openpipe_canonical_fullImage", "openpipe_canonical_smallImage",
                 "openpipe_canonical_largeImage", "openpipe_canonical_biography", "openpipe_canonical_sourceLargeImage",
                 "openpipe_canonical_sourceSmallImage", "openpipe_canonical_sourceFullImage",
                 "openpipe_canonical_thumbnailImage", "openpipe_canonical_thumbnailImageDimensions",
                 "openpipe_canonical_defaultImage", "openpipe_canonical_webImage",
                 "openpipe_canonical_defaultImageDimensions", "openpipe_canonical_webImageDimensions",
                 "openpipe_canonical_galleryImage", "openpipe_canonical_galleryImageDimensions"]

i = 0
mappings = []

mids=()
for d in metaTagResultSet["data"]:
    mids+=(d['metaDataId'][0],)

print(mids)

# resultSet = orm.session.query(MetaTag).filter(MetaTag.tagName.like("openpipe_canonical_%")).order_by(MetaTag.metaDataId)

resultSet = orm.session.query(MetaTag).\
    filter(and_(MetaTag.tagName.like("openpipe_canonical_%"),
                MetaTag.metaDataId.in_(mids))).\
    order_by(MetaTag.metaDataId).all()

print(len(resultSet))


for tag in resultSet:

    tagName = tag.tagName.split("_")[2].lower()

    tagValue = re.sub(r"\([^()]*\)", "", str(tag.value).strip()).strip().lower()

    if tagName in guidCodeMap:
        guidCode = guidCodeMap[tagName]

        print(tagName, guidCode, tag.metaDataId)

        for topicMetaTag in topicHashMap[str(guidCode)]:
            topicName = topicMetaTag["name"][0]
            topicCode = topicMetaTag["code"][0]
            topicId = topicMetaTag["id"][0]
            topicType = topicMetaTag["type"][0]
            # print(topicName, tagValue)
            if tagValue == topicName or tagValue.startswith(topicName):
                info = {'id': tag.id, "topic_name": topicType, "topic_id": topicId, "topic_code": topicCode,
                        "note": "tpu"}
                mappings.append(info)
                print(tag.metaDataId, tag.tagName)
                break
print(len(mappings))
updateSize=len(mappings)
biteSize=1000
q=int(updateSize / biteSize)
r= updateSize % biteSize

for i in range(0,q):
    print("************** commiting to DB **************")
    orm.session.bulk_update_mappings(MetaTag, mappings[i*biteSize:i*biteSize+biteSize])
    orm.session.flush()
    orm.session.commit()
    print("************** Done commiting to DB **************")
orm.session.bulk_update_mappings(MetaTag,mappings[q*biteSize:q*biteSize+r])
orm.commitClose()
