from sqlalchemy import and_, func

from backend.openpipeAPI.ORM.ORM import ORM
from backend.openpipeAPI.ORM.TO import TO


def bulkUpdate(mappings, TableClass, batchSize):
    updateSize = len(mappings)
    biteSize = batchSize
    q = int(updateSize / biteSize)
    r = updateSize % biteSize

    orm = ORM()

    for i in range(0, q):
        print("************** commiting to DB **************")
        orm.session.bulk_update_mappings(TableClass, mappings[i * biteSize:i * biteSize + biteSize])
        orm.session.flush()
        orm.session.commit()
        print("************** Done commiting to DB **************")
    orm.session.bulk_update_mappings(TableClass, mappings[q * biteSize:q * biteSize + r])
    orm.commitClose()


def fixAssetModifiedDates():
    orm = ORM()
    tables = TO().getClasses()
    Asset = tables["asset"]
    mappings = []

    res = orm.executeSelect(
        """select asset.id as assetId , max(metaTag.lastModified) as d from asset join metaTag on asset.metaDataId=metaTag.metaDataId group by asset.metaDataId""")

    for r in res['data']:
        print(r)
        info = {'id': r["assetId"][0], "lastModified": r['d'][0]}
        mappings.append(info)
    bulkUpdate(mappings, Asset, 1000)
    orm.commitClose()


def fixFolderModifiedDates():
    orm = ORM()
    tables = TO().getClasses()
    Folder = tables["collection"]
    mapping = []

    res = orm.executeSelect(
        """select collectionMember.collectionId as fid,max(asset.lastModified) as d from asset join collectionMember on asset.id=collectionMember.assetId group by collectionMember.collectionId;""")

    for r in res['data']:
        print(r)
        mapping.append({"id": r["fid"][0], "lastModified": r['d'][0]})

    bulkUpdate(mapping, Folder, 1000)
    orm.commitClose()


def update_assets_date_in_folder(folderId):
    orm = ORM()
    tables = TO().getClasses()
    Asset = tables["asset"]
    stm = "select asset.id from asset join collectionMember on assetId=asset.id where collectionId=:fid;"
    resultSet = orm.session.execute(stm, {"fid": folderId})
    for i in resultSet:
        orm.session.query(Asset).filter(Asset.id == i[0]).update(
            {"lastModified": orm.session.scalar(func.current_timestamp().select())})
    orm.session.commit()
    orm.commitClose()


def update_asset_dates_all_folders(folderId):
    orm = ORM()
    tables = TO().getClasses()
    Asset = tables["asset"]
    stm = "select asset.id from asset join collectionMember on assetId=asset.id where collectionId=:fid;"
    resultSet = orm.session.execute(stm, {"fid": folderId})
    for i in resultSet:
        orm.session.query(Asset).filter(Asset.id == i[0]).update(
            {"lastModified": orm.session.scalar(func.current_timestamp().select())})
    orm.session.commit()
    orm.commitClose()


def fix_assets_with_dates_smaller_than_tag_dates():
    print("Fix started.")
    orm = ORM()
    tables = TO().getClasses()
    Asset = tables["asset"]
    stm = "select * from (select asset.id as assetId ,date(asset.lastModified) as ld, date(max(metaTag.lastModified)) as d from asset join metaTag on asset.metaDataId=metaTag.metaDataId group by asset.metaDataId) as a where ld<d;"
    resultSet = orm.session.execute(stm, )
    print("Fetched Data.")
    mapping = []
    currentDate = orm.session.scalar(func.current_timestamp().select())
    for i in resultSet:
        mapping.append({"id": i[0], "lastModified": currentDate})

    print("number of assets that need modification: "+str(len(mapping)))

    orm.bulkUpdate(mapping, Asset, 100)
    orm.session.commit()
    orm.session.close()
    print("Fix Ended.")


fix_assets_with_dates_smaller_than_tag_dates()
#
# fixAssetModifiedDates()


#
# fixFolderModifiedDates()


# update_assets_date_in_folder(240)



