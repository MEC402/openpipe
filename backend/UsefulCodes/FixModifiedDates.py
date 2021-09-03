from sqlalchemy import and_

from openpipeAPI.ORM.ORM import ORM
from openpipeAPI.ORM.TO import TO


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
    mapping=[]

    res = orm.executeSelect(
        """select collectionMember.collectionId as fid,max(asset.lastModified) as d from asset join collectionMember on asset.id=collectionMember.assetId group by collectionMember.collectionId;""")

    for r in res['data']:
        print(r)
        mapping.append({"id":r["fid"][0],"lastModified": r['d'][0]})

    bulkUpdate(mapping, Folder, 1000)
    orm.commitClose()


fixAssetModifiedDates()

fixFolderModifiedDates()
