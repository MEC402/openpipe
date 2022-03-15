from backend.openpipeAPI.ORM.ORM import ORM
from backend.openpipeAPI.ORM.TO import TO

stm = """SELECT 
    *
FROM
    metaTag
WHERE
    (tagName = 'openpipe_canonical_largeImageDimensions'
        OR tagName = 'openpipe_canonical_largeImage'
        OR tagName = 'openpipe_canonical_smallImage'
        OR tagName = 'openpipe_canonical_smallImageDimensions'
        OR tagName = 'openpipe_canonical_fullImage'
        OR tagName = 'openpipe_canonical_fullImageDimensions')
        and value not like'%Sleeping Cat%'
ORDER BY metaDataId;
"""

orm = ORM()
tables = TO().getClasses()
MetaTag = tables["metaTag"]
res = orm.executeSelect(stm)
orm.commitClose()
data = {}
for r in res['data']:
    mid = r["metaDataId"][0]
    tagName = r["tagName"][0]
    value = r["value"][0]
    if mid in data:
        data[mid][tagName] = value
    else:
        data[mid] = {tagName: value}

print(data)
insertDataArray = []

for metadataId in data:
    print(metadataId)

    if "openpipe_canonical_smallImage" in data[metadataId]:
        insertDataArray.append(MetaTag(metaDataId=metadataId, tagName="openpipe_canonical_thumbnailImage",
                                       value=data[metadataId]["openpipe_canonical_smallImage"], note="NewImageTag"))
        insertDataArray.append(MetaTag(metaDataId=metadataId, tagName="openpipe_canonical_thumbnailImageDimensions",
                                       value=data[metadataId]["openpipe_canonical_smallImageDimensions"],
                                       note="NewImageTag"))

    if "openpipe_canonical_largeImage" in data[metadataId]:
        insertDataArray.append(MetaTag(metaDataId=metadataId, tagName="openpipe_canonical_defaultImage",
                                       value=data[metadataId]["openpipe_canonical_largeImage"], note="NewImageTag"))
        insertDataArray.append(MetaTag(metaDataId=metadataId, tagName="openpipe_canonical_webImage",
                                       value=data[metadataId]["openpipe_canonical_largeImage"], note="NewImageTag"))
        insertDataArray.append(MetaTag(metaDataId=metadataId, tagName="openpipe_canonical_defaultImageDimensions",
                                       value=data[metadataId]["openpipe_canonical_largeImageDimensions"],
                                       note="NewImageTag"))
        insertDataArray.append(MetaTag(metaDataId=metadataId, tagName="openpipe_canonical_webImageDimensions",
                                       value=data[metadataId]["openpipe_canonical_largeImageDimensions"],
                                       note="NewImageTag"))

        ld = data[metadataId]["openpipe_canonical_largeImageDimensions"].split(",")
        lW = int(ld[0])
        lH = int(ld[1])

    else:
        pass # move to next one if Large image doesnt Exists

    if "openpipe_canonical_fullImageDimensions" in data[metadataId]:
        fd = data[metadataId]["openpipe_canonical_fullImageDimensions"].split(",")
        fW = int(fd[0])
        fH = int(fd[1])

    fullRes = fW * fH
    largeRes = lW * lH

    if fullRes > largeRes:
        if fullRes <= 33177600:  # fullRes is less Equal 8K= 7680 by 4320 = 33177600
            insertDataArray.append(MetaTag(metaDataId=metadataId, tagName="openpipe_canonical_galleryImage",
                                           value=data[metadataId]["openpipe_canonical_fullImage"], note="NewImageTag"))
            insertDataArray.append(MetaTag(metaDataId=metadataId, tagName="openpipe_canonical_galleryImageDimensions",
                                           value=data[metadataId]["openpipe_canonical_fullImageDimensions"],
                                           note="NewImageTag"))
        else:
            insertDataArray.append(MetaTag(metaDataId=metadataId, tagName="openpipe_canonical_galleryImage",
                                           value=data[metadataId]["openpipe_canonical_largeImage"], note="NewImageTag"))
            insertDataArray.append(MetaTag(metaDataId=metadataId, tagName="openpipe_canonical_galleryImageDimensions",
                                           value=data[metadataId]["openpipe_canonical_largeImageDimensions"],
                                           note="NewImageTag"))
    else:
        insertDataArray.append(MetaTag(metaDataId=metadataId, tagName="openpipe_canonical_galleryImage",
                                       value=data[metadataId]["openpipe_canonical_largeImage"], note="NewImageTag"))
        insertDataArray.append(MetaTag(metaDataId=metadataId, tagName="openpipe_canonical_galleryImageDimensions",
                                       value=data[metadataId]["openpipe_canonical_largeImageDimensions"],
                                       note="NewImageTag"))


insertSize=len(insertDataArray)
biteSize=1000
q=int(insertSize/biteSize)
r=insertSize%biteSize

orm1 = ORM()
for i in range(0,q):
    print(orm1.bulkInsert(insertDataArray[i*biteSize:i*biteSize+biteSize]))
orm1.bulkInsert(insertDataArray[q*biteSize:q*biteSize+r])
orm1.commitClose()
