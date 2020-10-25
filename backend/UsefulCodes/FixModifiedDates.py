from sqlalchemy import and_

from openpipeAPI.ORM.ORM import ORM
from openpipeAPI.ORM.TO import TO


def fixAssetModifiedDates():
    orm = ORM()
    tables = TO().getClasses()
    Asset = tables["asset"]
    res = orm.executeSelect("""select asset.id as assetId , max(metaTag.lastModified) as d from asset join metaTag on asset.metaDataId=metaTag.metaDataId group by asset.metaDataId""")

    for r in res['data']:
        print(r)

        orm.session.query(Asset).filter(Asset.metaDataId == r["assetId"][0]).update({"lastModified": r['d'][0]})

    # print(i,j,i+j)
    orm.commitClose()


def fixFolderModifiedDates():
    orm = ORM()
    tables = TO().getClasses()
    Folder = tables["collection"]
    res = orm.executeSelect("""select collectionMember.collectionId as fid,max(asset.lastModified) as d from asset join collectionMember on asset.id=collectionMember.assetId group by collectionMember.collectionId;""")

    for r in res['data']:
        print(r)

        orm.session.query(Folder).filter(Folder.id == r["fid"][0]).update({"lastModified": r['d'][0]})

    # print(i,j,i+j)
    orm.commitClose()

# fixAssetModifiedDates()


fixFolderModifiedDates()


