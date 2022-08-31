import json

from backend.openpipeAPI.ORM.ORM import ORM
from backend.openpipeAPI.ORM.TO import TO

orm = ORM()
tables = TO().getClasses()
Asset = tables["asset"]

undefined_source_assets_stm = """SELECT 
    asset.id, asset.metaDataId, asset.IdAtSource, tagName, value
FROM
    asset
        JOIN
    metaTag ON asset.metaDataId = metaTag.metaDataId
WHERE
    idAtSource = 'undefined'
        AND (tagName = 'openpipe_canonical_source'
        OR tagName='id' OR tagName='objectID' )
ORDER BY asset.metaDataId;"""

res = orm.session.execute(undefined_source_assets_stm)

i = 1

map = {}

for r in res:
    aid = r[0]
    mid = r[1]
    idAtSource = r[2]
    tagName = r[3]
    value = r[4]

    if "openpipe_canonical_" in tagName:
        source = -1
        if value == "The Metropolitan Museum of Art":
            source = 1
        elif value == "Rijksmuseum Amsterdam":
            source = 2
        elif value == "Cleveland Museum of Art":
            source = 3

        if aid in map:
            map[aid]["source"] = source
        else:
            map[aid] = {"source": source}
    elif tagName == "id":
        if aid in map:
            map[aid]["sid"] = value
        else:
            map[aid] = {"sid": value}
    elif tagName == "objectID":
        if aid in map:
            map[aid]["sid"] = value
        else:
            map[aid] = {"sid": value}

update = []
for m in map:
    if "sid" in map[m]:
        update.append({"id": m, "IdAtSource": map[m]["sid"], "sourceId": map[m]["source"]})
    else:
        print(map[m])

# print(update, len(update))
orm.bulkUpdate(update, Asset, 1000)
orm.commitClose()
