import json

from DataAccess import DataAccess as da
from TO import TO
from Schemas import FolderSchema
from sqlalchemy.orm import aliased
from sqlalchemy import String


def getFolderAssets(page, pageSize, folderId):
    tables = TO().getClasses()
    MetaTag = tables["metaTag"]
    Asset = tables["asset"]
    CollectionMember = tables["collectionMember"]

    if (page < 1):
        page = 1
    start = (page - 1) * pageSize
    step = pageSize

    results = {"total": 0, "data": []}

    if int(page) < 0:
        return results

    print(folderId)

    session = da().getSession()
    rows = session.query(CollectionMember).filter(CollectionMember.collectionId == folderId).count()

    print(rows)

    q1 = session.query(Asset.id, Asset.metaDataId, Asset.verified, Asset.score, Asset.type). \
        join(CollectionMember, Asset.id == CollectionMember.assetId). \
        filter(CollectionMember.collectionId == folderId). \
        offset(start). \
        limit(step). \
        subquery()

    resultSet = session.query(q1, MetaTag.tagName, MetaTag.value, MetaTag.id). \
        join(MetaTag, MetaTag.metaDataId == q1.c.metaDataId). \
        all()

    session.close()

    assetMetaDataMap = {}
    print(resultSet)

    for r in resultSet:
        assetId = r[0]
        mid = r[1]
        verified = r[2]
        score = r[3]
        assetType = r[4]
        tagName = r[5]
        value = str(r[6])
        mtid= r[7]

        if assetId not in assetMetaDataMap:
            assetMetaDataMap[assetId] = {"assetId": assetId,
                                         "metaDataId": mid,
                                         "assetVerified": verified,
                                         "assetScore": score,
                                         "assetType": assetType,
                                         "metaTags":{tagName: {mtid:value}}
                                         }
        else:
            if tagName in assetMetaDataMap[assetId]["metaTags"]:
                assetMetaDataMap[assetId]["metaTags"][tagName][mtid]=value
            else:
                assetMetaDataMap[assetId]["metaTags"][tagName] = {mtid:value}

    results["data"] = list(assetMetaDataMap.values())
    results["total"] = rows
    return results


def lambda_handler(event, context):
    dict = event['queryStringParameters']

    if 'p' not in dict.keys():
        dict['p'] = 1

    if 'ps' not in dict.keys():
        dict['ps'] = 10

    data = getFolderAssets(int(dict["p"]), int(dict["ps"]), dict["folderId"])

    return {
        'isBase64Encoded': False,
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            'Content-Type': 'application/json',
        },
        'body': json.dumps(data)
    }


test={
  "queryStringParameters": {
    "p": 1,
    "ps": 100,
    "folderId": 272
  }
}

r=lambda_handler(test,None)

print(r)