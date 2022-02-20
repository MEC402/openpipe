import json

from sqlalchemy import and_

from DataAccess import DataAccess as da
from TO import TO
from Schemas import AssetSchema, MetaTagSchema, FolderSchema


def getAllFolderIDs():
    results = {"total": 0, "data": []}

    tables = TO().getClasses()
    FolderTable = tables["collection"]

    session = da().getSession()
    folderIds = session.query(FolderTable.id).order_by(FolderTable.name).all()

    response = {"total": len(folderIds), "data": [fid[0] for fid in folderIds]}

    session.close()
    return response


def getFolderByID(fid):
    tables = TO().getClasses()
    FolderTable = tables["collection"]

    session = da().getSession()
    folder = session.query(FolderTable).filter(FolderTable.id == fid).all()
    response = FolderSchema().dumps(folder[0])

    session.close()
    return response


def getFolders(page, pageSize):
    page = int(page)
    pageSize = int(pageSize)
    if page < 1:
        page = 1
    start = (page - 1) * pageSize
    step = pageSize

    results = {"total": 0, "data": []}

    tables = TO().getClasses()
    FolderTable = tables["collection"]

    session = da().getSession()
    rows = session.query(FolderTable).count()
    folderResultSet = session.query(FolderTable).order_by(FolderTable.name).offset(start).limit(
        step).all()

    folders = FolderSchema(many=True).dumps(folderResultSet)

    session.close()

    response = {"total": rows, "data": json.loads(folders)}

    return response


def getFolderLayout(folderId):
    tables = TO().getClasses()
    FolderMembers = tables["collectionMember"]
    MetaTag = tables["metaTag"]
    Asset = tables["asset"]

    session = da().getSession()
    # rows = session.query(FolderMembers).filter(FolderMembers.collectionId == folderId).count()

    q1 = session.query(FolderMembers.id, FolderMembers.assetId, FolderMembers.collectionId, FolderMembers.geometry,
                       FolderMembers.wall, Asset.metaDataId). \
        filter(FolderMembers.collectionId == folderId, FolderMembers.geometry != None). \
        join(Asset, Asset.id == FolderMembers.assetId). \
        subquery()

    q2 = session.query(MetaTag.metaDataId, MetaTag.value). \
        filter(MetaTag.tagName == 'openpipe_canonical_largeImage'). \
        subquery()

    resultSet = session.query(q1, q2). \
        join(q2, q2.c.metaDataId == q1.c.metaDataId, isouter=True). \
        all()

    session.close()

    layoutData = []
    for t in resultSet:
        fmid = t[0]
        aid = t[1]
        fid = t[2]
        geometry = t[3]
        wall = t[4]
        mid = t[5]
        image = t[7]

        layoutData.append({"folderMemberId": fmid,
                           "assetId": aid,
                           "folderId": fid,
                           "geometry": geometry,
                           "wall": wall,
                           "assetMetaDataId": mid,
                           "image": image
                           })

    response = {"total": len(layoutData), "data": layoutData}
    return response


def deleteFolderAsset(assetId, folderId):
    tables = TO().getClasses()
    FolderMembers = tables["collectionMember"]

    result = 0
    session = da().getSession()
    result = session.query(FolderMembers).filter(FolderMembers.assetId==assetId,FolderMembers.collectionId==folderId).delete()
    session.commit()
    session.close()

    return result


print(deleteFolderAsset(2619,25))
