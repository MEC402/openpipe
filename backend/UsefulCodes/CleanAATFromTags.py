import json

from openpipeAPI.ORM.BL import BL
from openpipeAPI.ORM.ORM import ORM
from openpipeAPI.ORM.TO import TO

orm=ORM()
tables = TO().getClasses()
MetaTag = tables["metaTag"]
res=orm.executeSelect("""SELECT * FROM artmaster.metaTag where tagName='openpipe_canonical_tags' and value like '%{%'""")
for r in res['data']:
    newValue=r['value'][0].split(":")[1].split(",")[0].replace("'",'').strip()
    print(newValue)
    orm.session.query(MetaTag).filter(MetaTag.id == int(r['id'][0])).update(
        {"value": newValue})
orm.commitClose()