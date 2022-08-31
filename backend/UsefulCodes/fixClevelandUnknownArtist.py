import ast
import json
import re

from backend.openpipeAPI.ORM.ORM import ORM
from backend.openpipeAPI.ORM.TO import TO

stm = """ SELECT 
    metaTag.tagName AS stn, metaTag.value AS sv, a.*
FROM
    metaTag
        JOIN
    (SELECT 
        metaTag.id AS cid,
            metaTag.metaDataId,
            tagName AS ctn,
            value AS cv
    FROM
        metaTag
    JOIN asset ON asset.metaDataId = metaTag.metaDataId
    WHERE
        sourceId = 3
            AND tagName = 'openpipe_canonical_artist'
            AND value LIKE '%unknown%') AS a ON metaTag.metaDataId = a.metaDataId
WHERE
    metaTag.tagName = 'creators'and metaTag.value != '[]';
"""

mappings=[]
orm = ORM()
tables = TO().getClasses()
MetaTag = tables["metaTag"]
res = orm.executeSelectParam(stm, {})
for r in res:
    print(r[2])
    info = {'id': r[2], "value": ''}
    mappings.append(info)

orm.bulkUpdate(mappings, MetaTag, 1000)



