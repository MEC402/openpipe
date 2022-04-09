import json

from backend.openpipeAPI.ORM.BL import BL
from backend.openpipeAPI.ORM.ORM import ORM
from backend.openpipeAPI.ORM.TO import TO


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

def add_tag_to_all_assets(tagName, value):
    orm = ORM()
    tables = TO().getClasses()
    MetaTag = tables["metaTag"]
    res = orm.executeSelect("""SELECT metaDataId FROM asset;""")
    toInsert = []

    for r in res['data']:
        print(r["metaDataId"][0])
        mid = r["metaDataId"][0]
        toInsert.append(MetaTag(metaDataId=mid, tagName=tagName, value=value, topic_id=-1))

    insertSize = len(toInsert)
    biteSize = 1000
    q = int(insertSize / biteSize)
    r = insertSize % biteSize

    for i in range(0, q):
        print(orm.bulkInsert(toInsert[i * biteSize:i * biteSize + biteSize]))
    orm.bulkInsert(toInsert[q * biteSize:q * biteSize + r])
    orm.commitClose()


tn = "openpipe_canonical_pgRating"
v = str([0] * 64).strip("[|]|, ").replace(', ', '')
add_tag_to_all_assets(tn, v)
