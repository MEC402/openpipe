import json

from DataAccess import DataAccess as da
from TO import TO
from Schemas import FolderSchema
from sqlalchemy.orm import aliased
from sqlalchemy import and_
from sqlalchemy.sql import func


def insertOrUpdateMetaTags(mid, insertData, updateData):
    tables = TO().getClasses()
    MetaTag = tables["metaTag"]
    Asset = tables["asset"]

    session = da().session
    for d in updateData:
        session.query(MetaTag).filter(and_(MetaTag.metaDataId == mid, MetaTag.id == d)).update({"value": updateData[d]})

    for tagName in insertData:
        for v in insertData[tagName]:
            session.add(MetaTag(metaDataId=mid, tagName=tagName, value=v))

    session.query(Asset).filter(Asset.metaDataId == mid).update(
        {"lastModified": session.scalar(func.current_timestamp().select())})
    session.commit()
    session.close()

    return insertData


def lambda_handler(event, context):
    dict = json.loads(event['body'])
    # dict=event['body']
    print(dict)
    data = insertOrUpdateMetaTags(dict["metaDataId"], dict["insert"], dict["update"])

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


test = {
    "body": """{"metaDataId":13446,"insert":{"openpipe_canonical_medium":["paint"]},"update":{"1209283":"Porcelain1"}}"""
}

r = lambda_handler(test, None)

print(r)
