from sqlalchemy import and_

from openpipeAPI.ORM.ORM import ORM
from openpipeAPI.ORM.TO import TO


def markEmptyCanonicalMetaTags():
    orm = ORM()
    tables = TO().getClasses()
    MetaTag = tables["metaTag"]
    res = orm.executeSelect(
        """select metaTag.id,tagname,value from asset join metaTag on asset.metaDataId=metaTag.metaDataId where tagName like 'openpipe_canonical_%' and value=''""")
    i = 0
    n = len(res['data'])
    for r in res['data']:
        print(i, n)
        orm.session.query(MetaTag).filter(MetaTag.id == int(r['id'][0])).update({"note": 5})
        i += 1
    orm.commitClose()

def updateAllPD():
    orm = ORM()
    tables = TO().getClasses()
    MetaTag = tables["metaTag"]
    orm.session.query(MetaTag).filter(MetaTag.tagName == 'openpipe_canonical_physicalDimensions').update({"value": '10,10,1'})
    orm.commitClose()



def updateAllBio():
    orm = ORM()
    tables = TO().getClasses()
    MetaTag = tables["metaTag"]
    orm.session.query(MetaTag).filter(and_(MetaTag.tagName == 'openpipe_canonical_biography'),MetaTag.value=='').update({"value": 'Bio not Available'})
    orm.commitClose()

def markAssetsWithWrongNumberofCanonicalTags():
    orm = ORM()
    tables = TO().getClasses()
    Asset = tables["asset"]
    res = orm.executeSelect(
        """select * from (select asset.id,asset.shortName,count(metaTag.id) as count from asset join metaTag on asset.metaDataId=metaTag.metaDataId where tagName like 'openpipe_canonical_%' group by asset.id) as a where a.count!=22""")
    i = 0
    n = len(res['data'])
    for r in res['data']:
        print(i, n)
        count = r['count'][0]
        id = r['id'][0]
        if count > 22:
            orm.session.query(Asset).filter(Asset.id == int(id)).update({"Note": 7})
        elif count < 22:
            orm.session.query(Asset).filter(Asset.id == int(id)).update({"Note": 6})
        i += 1
    orm.commitClose()


# markEmptyCanonicalMetaTags()

# markAssetsWithWrongNumberofCanonicalTags()

# updateAllPD()

updateAllBio()