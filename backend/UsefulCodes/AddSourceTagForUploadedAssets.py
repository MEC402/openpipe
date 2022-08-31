
from backend.openpipeAPI.ORM.ORM import ORM

from backend.openpipeAPI.ORM.TO import TO

orm = ORM()
tables = TO().getClasses()
MetaTag = tables["metaTag"]

def getAllUploadedAssets():
    res = orm.executeSelect("""Select * from metaTag where tagName='openpipe_canonical_fullImage' and value like '%assets/uploads%';""")
    return res

def addLocalSource(mid):
    for r in mid:
        orm.insert(MetaTag(metaDataId=r, tagName="openpipe_canonical_source", value='Local'))
    orm.commitClose()

def addLargeImageTag(assetData):
    for a in assetData['data']:
        orm.insert(MetaTag(metaDataId=a['metaDataId'][0], tagName="openpipe_canonical_largeImage", value=a['value'][0]))
    orm.commitClose()


def updateDates(assetData):
    for a in assetData['data']:
        orm.update(MetaTag(metaDataId=a['metaDataId'][0], tagName="openpipe_canonical_largeImage", value=a['value'][0]))
    orm.commitClose()


# addLargeImageTag(getAllUploadedAssets())


mids=[7126,7127,7129,7130,7131,7132,7133,7134,7135,7136,7137,7138,7139,7146,7147,7290,7291,7292,7294,7295,7296,7297,7298,7301,7302,7303,7304,7305,7306,7307,7308,7309,7310]
print(len(mids))
addLocalSource(mids)