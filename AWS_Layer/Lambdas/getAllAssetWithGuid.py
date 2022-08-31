import json

from DataAccess import DataAccess as da
from TO import TO
from Schemas import FolderSchema
from sqlalchemy.orm import aliased


def getAllAssetsWithGUID(page, pageSize, changeStart, changeEnd, none):
    tables = TO().getClasses()
    MetaTag = tables["metaTag"]
    Asset = tables["asset"]
    guidmap = {"city": "500", "classification": "600",
               "culture": "700", "genre": "800", "medium": "900", "nation": "a00",
               "artist": "400", "title": "000", "tags": "000"
               }
    guidURL = "http://mec402.boisestate.edu/cgi-bin/openpipe/data/"
    sguidURL = "http://mec402.boisestate.edu/"
    if (page < 1):
        page = 1
    start = (page - 1) * pageSize
    step = pageSize

    results = {"total_assets": 0,
               "assets_in_page": 0,
               "guidbase": "http://mec402.boisestate.edu/",
               "data": []}

    if int(page) < 0:
        return results

    session = da().getSession()

    rows = session.query(Asset). \
        filter(Asset.lastModified >= changeStart, Asset.lastModified <= changeEnd).count()

    q1 = session.query(Asset). \
        filter(Asset.lastModified.between(changeStart, changeEnd)). \
        offset(start). \
        limit(step). \
        subquery()

    q1 = aliased(Asset, q1)

    resultSet = session.query(q1, MetaTag).join(MetaTag, q1.metaDataId == MetaTag.metaDataId). \
        filter(MetaTag.tagName.like("%{}%".format("openpipe_canonical_"))). \
        order_by(q1.metaDataId). \
        all()

    # print(t1 - t0)

    assetMetaDataMap = {}
    print(len(resultSet))

    for r in resultSet:
        assetInfo = r[0]
        metaTagInfo = r[1]
        # print(assetInfo.metaDataId, metaTagInfo.metaDataId)
        tagName = metaTagInfo.tagName.split("_")[2]

        tagGuid = {str(metaTagInfo.topic_code) + "/" + str(metaTagInfo.topic_id): metaTagInfo.value}
        if metaTagInfo.topic_name is None and none == 1:
            if tagName == "id":
                tagGuid = "100" + "/" + str(assetInfo.id)
            else:
                tagGuid = {"ba0" + "/" + str(metaTagInfo.id): metaTagInfo.value}

        if assetInfo.metaDataId not in assetMetaDataMap:
            assetMetaDataMap[assetInfo.metaDataId] = {"guid": "100/" + str(assetInfo.id),
                                                      "metaDataId": [assetInfo.metaDataId],
                                                      "name": [assetInfo.shortName],
                                                      "openpipe_canonical": {
                                                          tagName: tagGuid
                                                      }}
        else:
            assetMetaDataMap[assetInfo.metaDataId]["openpipe_canonical"][tagName] = tagGuid

    results["total_assets"] = rows
    results["data"] = list(assetMetaDataMap.values())
    results["assets_in_page"] = len(results["data"])

    return results


def lambda_handler(event, context):
    dict = event['queryStringParameters']

    if dict is None:
        dict = {"a": "b"}

    if 'p' not in dict.keys():
        dict['p'] = 1

    if 'ps' not in dict.keys():
        dict['ps'] = 10

    if 'changeStart' not in dict.keys():
        dict['changeStart'] = '1900-01-01'

    if 'changeEnd' not in dict.keys():
        dict['changeEnd'] = '5000-01-01'

    if 'type' not in dict.keys():
        dict['type'] = 1

    if 'verify' not in dict.keys():
        dict['verify'] = 0

    data = getAllAssetsWithGUID(int(dict["p"]), int(dict["ps"]), dict['changeStart'], dict['changeEnd'],
                                int(dict['type']))

    if dict['verify'] == 1:

    # encode in utf8 before sending
    # json.dumps("ברי צקלה", ensure_ascii=False).encode('utf8')

    return {
        'isBase64Encoded': False,
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            'Content-Type': 'application/json',
        },
        'body': json.dumps(data, ensure_ascii=False).encode('utf8')
    }