from sqlalchemy import and_

from openpipeAPI.ORM.ORM import ORM
from openpipeAPI.ORM.TO import TO

orm = ORM()
tables = TO().getClasses()
MetaData = tables["metaData"]
res = orm.executeSelect(
    """SELECT id,metaDataId FROM artmaster.asset""")
i = 0
j = 0
for r in res['data']:
    print( r["id"][0], r["metaDataId"][0])
    orm.session.query(MetaData).filter(MetaData.id == r["metaDataId"][0]).update({"tableName": "asset", "eid": r["id"][0]})

# print(i,j,i+j)
orm.commitClose()
