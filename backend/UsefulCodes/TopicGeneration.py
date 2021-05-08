import re

from sqlalchemy import and_

from backend.openpipeAPI.ORM.ORM import ORM
from backend.openpipeAPI.ORM.TO import TO

orm = ORM()
tables = TO().getClasses()
MetaData = tables["metaData"]
Topic = tables["topic"]

guidMappingResultSet = orm.executeSelect(
    """SELECT * FROM artmaster.guidType;""")

guidCodeMap = {}

for guidMap in guidMappingResultSet["data"]:
    guidCodeMap[guidMap["name"][0]] = str(guidMap["code"][0])

print(guidCodeMap)

canonicalTagResultSet = orm.executeSelect(
    """SELECT * FROM artmaster.canonicalMetaTag;""")

insertDataArray = []
miscMetaTagData = set([])

for canonicalTag in canonicalTagResultSet["data"]:
    print("**********************************************")
    print(canonicalTag)
    canonicalTagName = canonicalTag["name"][0]
    topicMetaTagResultSet = orm.executeSelect(
        "select distinct value from metaTag where tagName=\'" + canonicalTagName + "\'")
    banCanonicals = ["openpipe_canonical_id", "openpipe_canonical_fullImage", "openpipe_canonical_smallImage",
                     "openpipe_canonical_largeImage", "openpipe_canonical_biography",
                     "openpipe_canonical_sourceLargeImage",
                     "openpipe_canonical_sourceSmallImage", "openpipe_canonical_sourceFullImage",
                     "openpipe_canonical_thumbnailImage", "openpipe_canonical_thumbnailImageDimensions",
                     "openpipe_canonical_defaultImage", "openpipe_canonical_webImage",
                     "openpipe_canonical_defaultImageDimensions", "openpipe_canonical_webImageDimensions",
                     "openpipe_canonical_galleryImage", "openpipe_canonical_galleryImageDimensions"]

    tagName = canonicalTagName.split("_")[2].lower()

    metaTagData=set()

    if tagName in guidCodeMap:
        guidCode = guidCodeMap[tagName]
        guidName = tagName
    else:
        guidCode = guidCodeMap["metaTag"]
        guidName = "metaTag"

    print(tagName, guidCode)

    for topicMetaTag in topicMetaTagResultSet["data"]:
        topicValue = re.sub(r"\([^()]*\)", "", str(topicMetaTag["value"][0]).strip()).strip().lower()
        if canonicalTag["name"][0] in banCanonicals:
            pass
        elif guidName == "metaTag":
            if topicValue not in miscMetaTagData:
                miscMetaTagData.add(topicValue)
                insertDataArray.append(Topic(name=topicValue, type=guidName, code=guidCode))
        else:
            if topicValue not in metaTagData:
                metaTagData.add(topicValue)
                insertDataArray.append(Topic(name=topicValue, type=guidName, code=guidCode))

    print(len(miscMetaTagData))

orm.bulkInsert(insertDataArray)

orm.commitClose()
