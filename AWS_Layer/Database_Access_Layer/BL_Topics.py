import json

from DataAccess import DataAccess as da
from TO import TO
from Schemas import FolderSchema


def getTopicByType(typeCode, page, pageSize):
    page = int(page)
    pageSize = int(pageSize)
    if page < 1:
        page = 1
    start = (page - 1) * pageSize
    step = pageSize

    tables = TO().getClasses()
    TopicTable = tables["topic"]
    MetaTag = tables["metaTag"]

    session = da().getSession()
    rows = session.query(TopicTable).filter(TopicTable.code == typeCode).count()

    q1 = session.query(TopicTable.id, TopicTable.name, TopicTable.type, TopicTable.code). \
        filter(TopicTable.code == typeCode). \
        order_by(TopicTable.name). \
        offset(start). \
        limit(step). \
        subquery()

    resultSet = session.query(q1, MetaTag.metaDataId, MetaTag.tagName, MetaTag.value, MetaTag.id). \
        join(MetaTag, MetaTag.topic_id == q1.c.id). \
        all()

    session.close()

    topicData = {}
    for t in resultSet:
        topicId = t[0]
        topicName = t[1]
        topicTypename = t[2]
        topicCode = t[3]
        metaDataId = t[4]
        tagName = t[5]
        value = t[6]
        tagId = t[7]

        if topicId not in topicData:
            topicData[topicId] = {"topicId": topicId,
                                  "topicName": topicName,
                                  "topicTypename": topicTypename,
                                  "topicCode": topicCode,
                                  "aliases": [{
                                      "metaDataId": metaDataId,
                                      "tagName": tagName,
                                      "value": value,
                                      "tagId": tagId
                                  }]}
        else:
            topicData[topicId]["aliases"].append({"metaDataId": metaDataId,
                                                  "tagName": tagName,
                                                  "value": value,
                                                  "tagId": tagId})

    response = {"total": rows, "data": list(topicData.values())}
    return response


def getTopicAssets(topicId, page, pageSize):
    page = int(page)
    pageSize = int(pageSize)
    if page < 1:
        page = 1
    start = (page - 1) * pageSize
    step = pageSize

    tables = TO().getClasses()
    TopicTable = tables["topic"]
    MetaTagTable = tables["metaTag"]

    session = da().getSession()
    rows = session.query(MetaTagTable.metaDataId). \
        filter(MetaTagTable.topic_id == topicId). \
        distinct(). \
        count()

    assets = session.query(MetaTagTable.id, MetaTagTable.metaDataId, MetaTagTable.tagName, MetaTagTable.value). \
        filter(MetaTagTable.topic_id == topicId). \
        order_by(MetaTagTable.metaDataId). \
        offset(start). \
        limit(step). \
        all()

    session.close()

    topicData = []
    for t in assets:
        topicData.append({"metaTagId": t[0], "metaDataId": t[1], "tagName": t[2], "value": t[3]})

    response = {"total": rows, "data": topicData}
    return response


def getAssetInfoByMetaDataId(metaDataId):
    tables = TO().getClasses()
    MetaTagTable = tables["metaTag"]

    session = da().getSession()
    tags = session.query(MetaTagTable.id, MetaTagTable.tagName, MetaTagTable.value). \
        filter(MetaTagTable.metaDataId == metaDataId). \
        all()
    session.close()

    tagData = []
    for t in tags:
        tagData.append({"id": t[0], "tagName": t[1], "value": t[2]})

    response = {"total": len(tagData), "data": tagData}
    return response


print(getTopicByType(400, 1, 10))
