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

compressionCount=0

for canonicalTag in canonicalTagResultSet["data"]:
    print("**********************************************")
    canonicalTagName = canonicalTag["name"][0]
    # banCanonicals = ["openpipe_canonical_id", "openpipe_canonical_fullImage", "openpipe_canonical_smallImage",
    #                  "openpipe_canonical_largeImage", "openpipe_canonical_biography",
    #                  "openpipe_canonical_sourceLargeImage",
    #                  "openpipe_canonical_sourceSmallImage", "openpipe_canonical_sourceFullImage",
    #                  "openpipe_canonical_thumbnailImage", "openpipe_canonical_thumbnailImageDimensions",
    #                  "openpipe_canonical_defaultImage", "openpipe_canonical_webImage",
    #                  "openpipe_canonical_defaultImageDimensions", "openpipe_canonical_webImageDimensions",
    #                  "openpipe_canonical_galleryImage", "openpipe_canonical_galleryImageDimensions"]

    tagName = canonicalTagName.split("_")[2].lower()

    metaTagData=set()

    if tagName in guidCodeMap:
        print(canonicalTag)

        guidCode = guidCodeMap[tagName]
        guidName = tagName
        print(tagName, guidCode)

        # canonicalTagName="openpipe_canonical_genre"
        topicMetaTagResultSet = orm.executeSelect(
            "select distinct value from metaTag where tagName=\'" + canonicalTagName + "\'")

        for topicMetaTag in topicMetaTagResultSet["data"]:
            topicValue = re.sub(r"\([^()]*\)", "", str(topicMetaTag["value"][0]).strip()).strip().lower()
            print(topicValue)
            # topicValue = re.sub(r'[^\w]', ' ', topicValue) causes odd results
            if len(metaTagData) == 0:
                # print("its empty")
                metaTagData.add(topicValue)
                # print(topicValue)
            else:
                for mt in metaTagData.copy():
                    # print(mt, topicValue)
                    if topicValue.startswith(mt) or mt.startswith(topicValue):
                        # print("in here")
                        compressionCount+=1
                        if len(topicValue)<len(mt) and len(topicValue)>0:
                            print(topicValue+"___________"+mt)
                            metaTagData.remove(mt)
                            metaTagData.add(topicValue)
                        elif len(mt)<=0:
                            metaTagData.remove(mt)
                            metaTagData.add(topicValue)

                    elif topicValue not in metaTagData:
                        # print("hi")
                        metaTagData.add(topicValue)

        for m in metaTagData:
            # print(m)
            insertDataArray.append(Topic(name=m, type=guidName, code=guidCode))
        print(metaTagData)
        # print(insertDataArray)


# orm.bulkInsert(insertDataArray)
# print("insertSize = "+str(len(insertDataArray)))
#
# print("compressionCount = "+str(compressionCount))
# orm.commitClose()
