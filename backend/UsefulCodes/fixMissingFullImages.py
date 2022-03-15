import json

from backend.openpipeAPI.ORM.ORM import ORM
from backend.openpipeAPI.ORM.TO import TO

orm=ORM()
tables = TO().getClasses()
MetaTag = tables["metaTag"]

stm="""SELECT 
    a.id AS fid,
    a.tagname AS ftag,
    a.value AS fvalue,
    metaTag.tagname AS ltag,
    metaTag.value AS lvalues
FROM
    (SELECT 
        *
    FROM
        metaTag
    WHERE
        tagName = 'openpipe_canonical_sourceFullImage'
            AND value LIKE '%.py?id=%') AS a
        JOIN
    metaTag ON a.metaDataId = metaTag.metaDataId
WHERE
    metaTag.tagName = 'openpipe_canonical_largeImage'
ORDER BY a.metaDataId;
"""

res=orm.executeSelect(stm)
i=1


for r in res['data']:
    print(r['fid'][0],i)
    orm.session.query(MetaTag).filter(MetaTag.id == int(r['fid'][0])).update({"value": r['lvalue'][0]})
    i=i+1

print(i)
orm.commitClose()