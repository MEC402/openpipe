

import json

from openpipeAPI.ORM.BL import BL
from openpipeAPI.ORM.ORM import ORM
from openpipeAPI.ORM.TO import TO

orm=ORM()
tables = TO().getClasses()
tags = tables["tag_tags"]
tag= tables["tag"]
res=orm.executeSelect("""SELECT value FROM artmaster.metaTag where tagName='openpipe_canonical_tags' group by value""")
i=1
for r in res['data']:
    print(r['value'][0])
    orm.insert(tags(id=i,value=r['value'][0],topic_id=i))
    orm.insert(tag(id=i,name="openpipe_name"))
    i=i+1
orm.commitClose()
