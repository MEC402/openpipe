import json
from operator import or_

from backend.openpipeAPI.ORM.ORM import ORM
from backend.openpipeAPI.ORM.TO import TO

orm = ORM()
tables = TO().getClasses()
Asset = tables["asset"]
CollectionMember = tables["collectionMember"]
MetaTag = tables["metaTag"]


stm = """SELECT 
    metaTag.id AS mid,
    metaTag.metaDataId AS mdid,
    metaTag.tagName,
    metaTag.value,
    dupm.*
FROM
    metaTag
        JOIN
    (SELECT 
        asset.id AS assetId,
            asset.shortName,
            asset.IdAtSource AS ids,
            asset.metaDataId AS assetMD,
            dup.*
    FROM
        asset         
    JOIN (SELECT 
        IdAtSource, COUNT(IdAtSource), sourceId
    FROM
        asset
    GROUP BY IdAtSource , sourceId
    HAVING COUNT(IdAtSource) > 1
        AND COUNT(sourceId)) AS dup ON asset.IdAtSource = dup.IdAtSource) AS dupm ON metaTag.metaDataId = dupm.assetMD;"""

res = orm.session.execute(stm)

i = 1

map = {}

for r in res:
    mid = r[0]
    mdid = r[1]
    tagName = r[2]
    value = r[3]
    assetId = r[4]
    shortName = r[5]
    ids = r[6]
    assetMD = r[7]
    idAtSource = r[8]
    count = r[9]
    sourceId = r[10]

    if idAtSource in map:
        if mdid in map[idAtSource]:
            map[idAtSource][mdid].append({"tagName":tagName,"value":value,"assetId":assetId})
            if (tagName=="openpipe_canonical_latitude" or tagName=="openpipe_canonical_longitude") and value!="":
                map[idAtSource]["wid"]=assetId
                map[idAtSource]["wmid"]=mdid
        else:
            map[idAtSource][mdid]=[{"tagName":tagName,"value":value,"assetId":assetId}]
            if (tagName=="openpipe_canonical_latitude" or tagName=="openpipe_canonical_longitude") and value!="":
                map[idAtSource]["wid"]=assetId
                map[idAtSource]["wmid"]=mdid

    else:
        map[idAtSource]={mdid:[{"tagName":tagName,"value":value,"assetId":assetId}]}
        if (tagName == "openpipe_canonical_latitude" or tagName == "openpipe_canonical_longitude") and value != "":
            map[idAtSource]["wid"] = assetId
            map[idAtSource]["wmid"] = mdid

win=[]
for k in map.keys():
    if "wid" in map[k]:
        win.append(map[k]["wid"])
    else:
        print()
        first=next(iter(map[k]))
        map[k]["wid"]=map[k][first][0]["assetId"]
        map[k]["wmid"]=first
        print("for id ",k,"winner is ",map[k]["wid"])

for k in map.keys():
    ids=[]
    mids=[]
    for kk in map[k].keys():
        if kk !="wid" and kk !="wmid":
            ids.append(map[k][kk][0]["assetId"])
            mids.append(kk)
    map[k]["ids"]=ids
    map[k]["mids"] = mids

l=0
for k in map.keys():
    print(k)
    print(map[k]["wid"],map[k]["ids"],map[k]["mids"])
    asset_ids = map[k]["ids"]

    orm.session.query(CollectionMember).filter(CollectionMember.assetId.in_(asset_ids)).update({"assetId": map[k]["wid"], "note":"dup"},synchronize_session=False)
    map[k]["mids"].remove(map[k]["wmid"])
    orm.session.query(Asset).filter(Asset.metaDataId.in_(map[k]["mids"])).delete(synchronize_session=False)
    orm.session.query(MetaTag).filter(MetaTag.metaDataId.in_(map[k]["mids"])).delete(synchronize_session=False)
    print("_____________________________")
    l+=len(map[k]["ids"])

print("total substitutes", l)
orm.commitClose()

# print(json.dumps(map))

#
# print(map)
# print(len(map))
# print(map[435980])
# print(len(map[435980]))
print("The array size is ",len(win))