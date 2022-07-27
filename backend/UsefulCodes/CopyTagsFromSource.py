import json

from backend.openpipeAPI.ORM.ORM import ORM
from backend.openpipeAPI.ORM.TO import TO

orm = ORM()
tables = TO().getClasses()
MetaTags = tables["metaTag"]

stm = """select * from metaTag where metaDataId in(
select asset.metaDataId from asset) order by metaDataId;"""

# join collectionMember on asset.id=assetId where collectionId=222

tagResultSet = orm.executeSelect(stm)
tags = {}

for t in tagResultSet["data"]:
    mid = t["metaDataId"][0]
    tagName = t["tagName"][0]
    value = t["value"][0]
    tagId = t['id'][0]
    if mid not in tags:
        tags[mid] = {tagName: {"value": value, "id": tagId}}
    else:
        tags[mid][tagName] = {"value": value, "id": tagId}

print("fetched data")
count = 0
updates = []
for tm in tags:
    t = tags[tm]
    if 'openpipe_canonical_source' in t and "openpipe_canonical_displayDate" in t:
        if t['openpipe_canonical_source']["value"] == "The Metropolitan Museum of Art":
            if str(t['openpipe_canonical_displayDate']["value"]).strip() == '':
                updates.append({'id': t["openpipe_canonical_displayDate"]["id"],
                                "value": t['objectDate']["value"]})

        elif t['openpipe_canonical_source']["value"] == "Cleveland Museum of Art":
            if str(t['openpipe_canonical_displayDate']["value"]).strip() == '':
                updates.append({'id': t["openpipe_canonical_displayDate"]["id"],
                                "value": t["creation_date"]["value"]})

    #     if t["wall_description"]["value"] != "null":
    #         updates.append({'id': t["openpipe_canonical_biography"]["id"],
    #                         "value": t["wall_description"]["value"]})
    #     else:
    #         updates.append({'id': t["openpipe_canonical_biography"]["id"],
    #                         "value": ""})
    #
    # elif t['openpipe_canonical_source']["value"] == "Rijksmuseum Amsterdam":
    #     if t["plaqueDescriptionEnglish"]["value"] != "null":
    #         updates.append({'id': t["openpipe_canonical_biography"]["id"],
    #                         "value": t["plaqueDescriptionEnglish"]["value"]})
    #     else:
    #         updates.append({'id': t["openpipe_canonical_biography"]["id"], "value": ""})

print(len(tags))
print(len(updates))

orm.bulkUpdate(updates, MetaTags, 1000)

