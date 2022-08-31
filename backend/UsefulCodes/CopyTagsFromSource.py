import json
import re

from backend.openpipeAPI.ORM.ORM import ORM
from backend.openpipeAPI.ORM.TO import TO

orm = ORM()
tables = TO().getClasses()
MetaTags = tables["metaTag"]


# stm = """select * from metaTag where metaDataId in(
# select asset.metaDataId from asset) order by metaDataId;"""
#
# # join collectionMember on asset.id=assetId where collectionId=222
#
# tagResultSet = orm.executeSelect(stm)
# tags = {}
#
# for t in tagResultSet["data"]:
#     mid = t["metaDataId"][0]
#     tagName = t["tagName"][0]
#     value = t["value"][0]
#     tagId = t['id'][0]
#     if mid not in tags:
#         tags[mid] = {tagName: {"value": value, "id": tagId}}
#     else:
#         tags[mid][tagName] = {"value": value, "id": tagId}
#
# print("fetched data")
# count = 0
# updates = []
# for tm in tags:
#     t = tags[tm]
#     if 'openpipe_canonical_source' in t and "openpipe_canonical_displayDate" in t:
#         if t['openpipe_canonical_source']["value"] == "The Metropolitan Museum of Art":
#             if str(t['openpipe_canonical_displayDate']["value"]).strip() == '':
#                 updates.append({'id': t["openpipe_canonical_displayDate"]["id"],
#                                 "value": t['objectDate']["value"]})
#
#         elif t['openpipe_canonical_source']["value"] == "Cleveland Museum of Art":
#             if str(t['openpipe_canonical_displayDate']["value"]).strip() == '':
#                 updates.append({'id': t["openpipe_canonical_displayDate"]["id"],
#                                 "value": t["creation_date"]["value"]})

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

# print(len(tags))
# print(len(updates))
#
# orm.bulkUpdate(updates, MetaTags, 1000)

def copyMetMediumFromSource():
    stm = """select q.id as sId,p.id as dId,q.metaDataId as sMid, p.metaDataId as dMid, q.tagName as sTagName,q.value as sValue , p.tagName as dTagName,p.value as dValue from (select * from metaTag where tagName="openpipe_canonical_medium" and value="medium" and  metaDataId in
    (select metadataId from metaTag where tagName="openpipe_canonical_source" and value="The Metropolitan Museum of Art")) as q join  (select * from metaTag where tagName="medium" and  metaDataId in
    (select metadataId from metaTag where tagName="openpipe_canonical_source" and value="The Metropolitan Museum of Art")) as p on p.metadataId=q.metadataId;
    """

    updates = []
    resultSet = orm.session.execute(stm, {})
    for r in resultSet:
        sId = r[0]
        dId = r[1]
        sMid = r[2]
        dMid = r[3]
        sTagName = r[4]
        sValue = r[5]
        dTagName = r[6]
        dValue = r[7]
        # print(sValue,dValue)
        updates.append({"id": sId, "value": dValue, "note": "aug17"})

    print(len(updates))
    orm.bulkUpdate(updates, MetaTags, 100)
    orm.session.commit()
    orm.session.close()


def copyClevelandArtistFromSource():
    stm = """select q.id as sId,p.id as dId,q.metaDataId as sMid, p.metaDataId as dMid, q.tagName as sTagName,q.value as sValue , p.tagName as dTagName,p.value as dValue from (select * from metaTag where tagName="openpipe_canonical_artist" and value="" and  metaDataId in
(select metadataId from metaTag where tagName="openpipe_canonical_source" and value="Cleveland Museum of Art")) as q join  (select * from metaTag where tagName="creators" and  metaDataId in
(select metadataId from metaTag where tagName="openpipe_canonical_source" and value="Cleveland Museum of Art")) as p on p.metadataId=q.metadataId;"""

    updates = []
    resultSet = orm.session.execute(stm, {})
    for r in resultSet:
        sId = r[0]
        dId = r[1]
        sMid = r[2]
        dMid = r[3]
        sTagName = r[4]
        sValue = r[5]
        dTagName = r[6]
        dValue = r[7]

        name=dValue.split(",")
        if len(name)>1:
            a = re.search(r'description:(.*?), extent:', dValue)
            if a is not None:
                newArtist= a.group(1)
                if newArtist!="null":
                    updates.append({"id": sId, "value": newArtist,"note": "aug17"})
                print(sValue, newArtist)

    print(len(updates))
    print(updates)
    orm.bulkUpdate(updates, MetaTags, 100)
    orm.session.commit()
    orm.session.close()


# copyMetMediumFromSource()
copyClevelandArtistFromSource()
