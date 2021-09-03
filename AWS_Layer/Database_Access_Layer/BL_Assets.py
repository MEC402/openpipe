from sqlalchemy import and_, func
from sqlalchemy.orm import aliased

from DataAccess import DataAccess as da
from TO import TO
from Schemas import AssetSchema, MetaTagSchema


def getAllAssets(page, pageSize, changeStart, changeEnd):
    if (page < 1):
        page = 1
    start = (page - 1) * pageSize
    step = pageSize

    results = {"total": 0, "data": []}

    if int(page) < 0:
        return results

    tables = TO().getClasses()
    AssetTable = tables["asset"]
    MetaTagTable = tables["metaTag"]

    session = da().getSession()
    assets = session.query(AssetTable).filter(
        and_(AssetTable.lastModified >= changeStart, AssetTable.lastModified <= changeEnd)).offset(start).limit(
        step).all()

    metaTag_schema = MetaTagSchema()
    assets_schema = AssetSchema(many=True)

    response = {"total": len(assets), "data": []}
    assets = assets_schema.dump(assets)

    for asset in assets:
        metaTag = session.query(MetaTagTable).filter(MetaTagTable.metaDataId == asset["metaDataId"])
        metaTag_ser = metaTag_schema.toJson(metaTag)
        response["data"].append({**asset, **metaTag_ser})
    session.close()
    return response


def test(page, pageSize, changeStart, changeEnd, none):
    stm = "select * from metaTag join (select * from asset WHERE asset.`lastModified` BETWEEN '" + changeStart + "' AND '" + changeEnd + "'LIMIT " + page + ", " + pageSize + ") as a on a.metaDataId=metaTag.metadataId where tagName like '%openpipe_canonical%';"

    r = da().executeSelect(stm)
    print(r[0])


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

    session = da().getSession()

    q1 = session.query(Asset.id, Asset.metaDataId, Asset.verified). \
        join(CollectionMember, Asset.id == CollectionMember.assetId). \
        filter(CollectionMember.collectionId == folderId). \
        offset(start). \
        limit(step). \
        subquery()

    resultSet = session.query(q1, MetaTag.tagName, MetaTag.value, MetaTag.id). \
        join(MetaTag, MetaTag.metaDataId == q1.c.metaDataId). \
        all()

    assetMetaDataMap = {}

    for r in resultSet:
        assetId = r[0]
        mid = r[1]
        verified = r[2]
        tagName = r[3]
        value = r[4]

        if assetId not in assetMetaDataMap:
            assetMetaDataMap[assetId] = {"assetId": assetId,
                                         "metaDataId": mid,
                                         "assetVerified": verified,
                                         tagName: value}
        else:
            assetMetaDataMap[assetId][tagName] = value

    results["data"] = list(assetMetaDataMap.values())
    results["total"] = len(results["data"])

    return results


def getFolders(page, pageSize):
    page = int(page)
    pageSize = int(pageSize)
    if page < 1:
        page = 1
    start = (page - 1) * pageSize
    step = pageSize

    tables = TO().getClasses()
    FolderTable = tables["collection"]
    CollectionMember = tables["collectionMember"]

    session = da().getSession()
    folderResultSet = session.query(FolderTable).order_by(FolderTable.name).offset(start).limit(
        step).all()

    folderAssetNum = session.query(CollectionMember.collectionId, func.count(CollectionMember.assetId)). \
        group_by(CollectionMember.collectionId). \
        order_by(CollectionMember.collectionId).\
        all()

    folderMap = {}
    resultMap = []

    for fn in folderAssetNum:
        folderMap[int(fn[0])] = fn[1]

    print(folderMap)
    print(len(folderMap.keys()))

    for folder in folderResultSet:

        if folder.id not in folderMap:
            folderMap[folder.id]=0

        r = {"id": folder.id,
             "name": folder.name,
             "image": folder.image,
             "layoutType": folder.layoutType,
             "metaDataId": folder.metaDataId,
             "verified": folder.verified,
             "assetCount": folderMap[int(folder.id)]}
        resultMap.append(r)

    session.close()

    response = {"total": len(resultMap), "data": resultMap}

    return response


def update_test():
    tables = TO().getClasses()
    MetaTag = tables["metaTag"]

    session=da().session
    session.query(MetaTag).filter(and_(MetaTag.metaDataId==4,MetaTag.tagName=='reign')).update({"value":""})
    session.query(MetaTag).filter(and_(MetaTag.metaDataId == 4, MetaTag.tagName == 'region')).update({"value": ""})
    session.commit()
    session.close()

update_test()
