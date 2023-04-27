import ast
import json
import re
import sys


#this is a hack: the mods to sys.path should be done in a config element
sys.path.append('o:/builds_codebase/openpipe2/')

import  backend.openpipeAPI.ORM.ORM

from backend.openpipeAPI.ORM.ORM import ORM
from backend.openpipeAPI.ORM.TO import TO

stm = """ SELECT * from metaTag
            inner join asset on metaTag.metaDataId=asset.metaDataId
               where tagName='openpipe_canonical_displayDate' and sourceId=1 and value='';

"""

mappings=[]
orm = ORM()
tables = TO().getClasses()
MetaTag = tables["metaTag"]
#res = orm.executeSelectParam(stm, {})
res = orm.executeSelect(stm)
print(stm)
print(res)
for r in res["data"]:
    print(r)

#orm.bulkUpdate(mappings, MetaTag, 1000)



