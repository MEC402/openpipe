from backend.openpipeAPI.ORM.ORM import ORM
from backend.openpipeAPI.ORM.TO import TO


def find_loose_topics():

    session = ORM().session
    stm = "select * from topic where id not in (select topic_id from metaTag where topic_id is not null);"
    resultSet = session.execute(stm, )
    ids=[]
    for r in resultSet:
        ids.append(r[0])
    print("Number of Topics with no assets: {}".format(len(ids)))

    tables = TO().getClasses()
    Topic = tables["topic"]

    session.query(Topic).filter(Topic.id.in_(ids)).delete(synchronize_session=False)
    session.commit()
    session.close()

find_loose_topics()