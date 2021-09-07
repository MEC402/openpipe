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

    session = da().getSession()
    topic = session.query(TopicTable.id, TopicTable.name, TopicTable.type, TopicTable.code). \
        filter(TopicTable.code == typeCode). \
        order_by(TopicTable.name). \
        offset(start). \
        limit(step). \
        all()

    session.close()

    topicData = []
    for t in topic:
        topicData.append({"id": t[0], "name": t[1], "typeName": t[2], "code": t[3]})

    response = {"total": len(topicData), "data": topicData}
    return response


print(getTopicByType(400, 1, 10))
