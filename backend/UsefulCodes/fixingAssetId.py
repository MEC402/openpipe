

import json

from openpipeAPI.ORM.BL import BL
from openpipeAPI.ORM.ORM import ORM
from openpipeAPI.ORM.TO import TO

orm=ORM()
tables = TO().getClasses()
tags = tables["tag_tags"]
tag= tables["tag"]
res=orm.executeSelect("""SELECT * FROM asset join metaTag on asset.metaDataId=metaTag.metaDataId where tagName='openpipe_canonical_id'""")
i=1
for r in res['data']:
    print(r['value'][0])
    orm.session.query(MetaTag).filter(MetaTag.id == int(r['id'][0])).update(
        {"value": newValue})
    i=i+1

print(i)
orm.commitClose()