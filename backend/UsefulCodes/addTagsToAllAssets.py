
import json

from openpipeAPI.ORM.BL import BL
from openpipeAPI.ORM.ORM import ORM
from openpipeAPI.ORM.TO import TO

# orm =ORM()
# tables = TO().getClasses()
# MetaTag = tables["metaTag"]
# res =orm.executeSelect("""SELECT metaDataId FROM artmaster.metaTag group by metaDataId""")
# for r in res['data']:
#     print(r["metaDataId"][0])
#     mid = r["metaDataId"][0]
#     orm.insert(MetaTag(metaDataId=mid, tagName="openpipe_canonical_biography", value="Openpipe Bio"))
#     orm.insert(MetaTag(metaDataId=mid, tagName="openpipe_canonical_physicalDimensions", value="0,0,0"))
# orm.commitClose()

#
# from openpipeAPI.ORM.ORM import ORM
# from openpipeAPI.ORM.TO import TO
#
# tables = TO().getClasses()
# orm = ORM()
# data=orm.executeSelect("select a.id,artist_tags.topic_id from (SELECT * FROM artmaster.metaTag where tagName='openpipe_canonical_artist') as a join artist_tags on a.value=artist_tags.value")
# MetaTag = tables["metaTag"]
# for d in data["data"]:
#     orm.session.query(MetaTag).filter(MetaTag.id == int(d["id"][0])).update({"topic_name": "artist", "topic_id": int(d["topic_id"][0])})
# orm.commitClose()


orm =ORM()
tables = TO().getClasses()
MetaTag = tables["metaTag"]
res =orm.executeSelect("""SELECT id FROM metaData where tableName='asset';""")
for r in res['data']:
    print(r["id"][0])
    mid = r["id"][0]
    orm.insert(MetaTag(metaDataId=mid, tagName="openpipe_canonical_moment", value=0))
orm.commitClose()