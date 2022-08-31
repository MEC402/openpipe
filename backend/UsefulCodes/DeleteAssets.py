import csv

from backend.openpipeAPI.ORM.ORM import ORM
from backend.openpipeAPI.ORM.TO import TO


def delete_assets():
    pass
    # tables = TO().getClasses()
    # Topic = tables["topic"]
    # MetaTag = tables["metaTag"]
    # Asset = tables["asset"]
    #
    # session = ORM().session
    # session.query(MetaTag).filter(MetaTag.topic_id.in_(data["mergeTopicIds"]))
    # session.query(Asset).filter(MetaTag.topic_id.in_(data["mergeTopicIds"])).update({"topic_id": topicId})
    # session.query(Topic).filter(Topic.id.in_(data["mergeTopicIds"])).delete()
    # session.commit()
    # session.close()


def delete_etc():
    tables = TO().getClasses()
    Topic = tables["topic"]
    MetaTag = tables["metaTag"]
    Asset = tables["asset"]
    MetaData = tables["metaData"]
    FolderMembers = tables["collectionMember"]

    assets = []
    assetIds = []
    mids = []

    with open("C:/Users/rezva/OneDrive/Desktop/deleted_Assets.csv", newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            assets.append({"id": row[0],
                           "shortName": row[1],
                           "uri": row[2],
                           "IdAtSource": row[3],
                           "sourceId": row[4],
                           "metaDataId": row[5],
                           "type": row[6],
                           "scope": row[7],
                           "verified": row[8],
                           "sysVerified": row[9],
                           "score": row[10],
                           "Note": row[11],
                           "insertTime": row[12],
                           "lastModified": row[13]
                           })
            assetIds.append(row[0])
            mids.append(row[5])

    assetIds.pop(0)
    mids.pop(0)
    assets.pop(0)

    print(len(assetIds))
    print(len(mids))

    session = ORM().session

    pre_del_mid_count = session.query(MetaData).count()
    pre_del_mtag_count = session.query(MetaTag).count()
    pre_del_fm_count = session.query(FolderMembers).count()

    session.query(MetaData).filter(MetaData.id.in_(mids)).delete(synchronize_session=False)
    session.query(MetaTag).filter(MetaTag.metaDataId.in_(mids)).delete(synchronize_session=False)
    session.query(FolderMembers).filter(FolderMembers.assetId.in_(assetIds)).delete(synchronize_session=False)

    # res=session.query(FolderMembers).filter(FolderMembers.assetId.in_(assetIds)).all()
    #
    # for a in res:
    #     print(a.collectionId, a.assetId)

    session.commit()
    session.close()

    session = ORM().session
    post_del_mid_count = session.query(MetaData).count()
    post_del_mtag_count = session.query(MetaTag).count()
    post_del_fm_count = session.query(FolderMembers).count()

    session.commit()
    session.close()
    print("Number of rows in MetaData  - diff:{}, pre:{}, post:{}".format(pre_del_mid_count - post_del_mid_count,
                                                                          pre_del_mid_count, post_del_mid_count))
    print("Number of rows in MetaTag   - diff:{}, pre:{}, post:{}".format(pre_del_mtag_count - post_del_mtag_count,
                                                                          pre_del_mtag_count, post_del_mtag_count))
    print("Number of rows in FolderMem - diff:{}, pre:{}, post:{}".format(pre_del_fm_count - post_del_fm_count,
                                                                          pre_del_fm_count, post_del_fm_count))


delete_etc()
