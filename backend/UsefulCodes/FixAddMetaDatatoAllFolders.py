from sqlalchemy import and_

from openpipeAPI.ORM.ORM import ORM
from openpipeAPI.ORM.TO import TO

orm = ORM()
tables = TO().getClasses()
MetaData = tables["metaData"]
Folder = tables["collection"]

res = orm.executeSelect(
    """select * from collection where metadataid is null""")

for r in res['data']:
    print( r["id"][0])
    mid = orm.insert(MetaData(tableName="collection",eid=r["id"][0]))
    orm.session.query(Folder).filter(Folder.id == r["id"][0]).update({"metaDataId": mid})

# print(i,j,i+j)
orm.commitClose()
