from sqlalchemy import and_

from openpipeAPI.ORM.ORM import ORM
from openpipeAPI.ORM.TO import TO

orm = ORM()
tables = TO().getClasses()
MetaTag = tables["metaTag"]
res = orm.executeSelect(
    """SELECT metaTag.metaDataId,value FROM artmaster.asset join metaTag on asset.metaDataId=metaTag.metaDataId where sourceId=3 and tagname='principalMakers';""")
i = 0
j = 0
for r in res['data']:
    print(r)

    orm.session.query(MetaTag).filter(
        and_(MetaTag.metaDataId == r["metaDataId"][0], MetaTag.tagName == 'openpipe_canonical_biography')).update(
        {"value": r['value'][0]})

# print(i,j,i+j)
orm.commitClose()
