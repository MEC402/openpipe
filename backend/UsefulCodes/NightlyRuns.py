from sqlalchemy import and_

from openpipeAPI.ORM.ORM import ORM
from openpipeAPI.ORM.TO import TO


def fixPhysicalDimentions():
    orm = ORM()
    tables = TO().getClasses()
    MetaTag = tables["metaTag"]
    orm.session.query(MetaTag).filter(MetaTag.tagName == 'openpipe_canonical_physicalDimensions').update(
        {"value": '21.0,29.7,1.0'})
    orm.commitClose()


def fixSourceNames():
    orm = ORM()
    tables = TO().getClasses()
    MetaTag = tables["metaTag"]
    orm.session.query(MetaTag).filter(and_(MetaTag.tagName == 'openpipe_canonical_source',MetaTag.value=='Cleveland')).update(
        {"value": 'Cleveland Museum of Art'})
    orm.commitClose()


def addAllMuseumCanonicalToMapping():
    orm = ORM()
    tables = TO().getClasses()
    TagMap = tables["tagMap"]
    ids=list(range(2,21))
    ids.append(22)
    for i in ids:
        print(i)
        orm.insert(TagMap(tagID=i, sourceID=3))
    orm.commitClose()


addAllMuseumCanonicalToMapping()