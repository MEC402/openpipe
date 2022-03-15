import json

from backend.openpipeAPI.ORM.ORM import ORM
from backend.openpipeAPI.ORM.TO import TO

orm=ORM()
tables = TO().getClasses()
Asset = tables["asset"]

stm="""SELECT 
    asset.*, value, displayName, source.id AS sid
FROM
    artmaster.asset
        JOIN
    metaTag ON asset.metaDataId = metaTag.metaDataId
        JOIN
    source ON value = sourceName
WHERE
    sourceId = 'undefined'
        AND tagName = 'openpipe_canonical_source';"""


res=orm.executeSelect(stm)
i=1


for r in res['data']:

    print(r['id'][0],r['sid'][0],i)
    orm.session.query(Asset).filter(Asset.id == int(r['id'][0])).update({"sourceId": r['sid'][0]})
    i = i + 1

print(i)
orm.commitClose()