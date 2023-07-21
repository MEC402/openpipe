import time

from backend.openpipeAPI.ORM.ORM import ORM


def getAllAssetsWithGUID(page, pageSize, changeStart, changeEnd, none):
    guidmap = {"city": "500", "classification": "600",
               "culture": "700", "genre": "800", "medium": "900", "nation": "a00",
               "artist": "400", "title": "f00", "tags": "f00"
               }
    guidURL = "http://mec402.boisestate.edu/cgi-bin/openpipe/data/"
    sguidURL = "http://mec402.boisestate.edu/"
    if (page < 1):
        page = 1
    start = (page - 1) * pageSize
    step = pageSize

    results = {"total": 0, "data": []}

    if int(page) < 0:
        return results

    orm = ORM()
    queryStatement = "SELECT id,metaDataId,shortName FROM asset where lastModified between \'" + changeStart + "\' and \'" + changeEnd + "\' limit " + str(
        start) + "," + str(step)
    t0 = time.time()
    newcon = orm.simpConnect()
    results = orm.executeSelectPersist(queryStatement, newcon)
    results['guidbase'] = sguidURL
    sguidURL = ""
    rows = []
    for row in results['data']:
        # rowInfo = {"id": row['id'], "metaDataId": row['metaDataId'], "name": row['shortName']}
        rowInfo = {"metaDataId": row['metaDataId'], "name": row['shortName']}
        metaDataId = row['metaDataId'][0]
        queryStatement = "select id,tagName,value,topic_name,topic_id,topic_code from metaTag where metaDataId="
        if metaDataId:
            queryStatement = queryStatement + str(metaDataId)
            tags = orm.executeSelectPersist(queryStatement, newcon)['data']
            canonicalTagObj = {}
            for metaTagRow in tags:
                # print(metaTagRow)
                if "openpipe_canonical_" in metaTagRow['tagName'][0]:  # Only Canonical Tags have topics
                    tagName = metaTagRow['tagName'][0].split("_")[2]
                    if metaTagRow['topic_name'][0] is None:
                        if none == 1:
                            # print("None value:",none)
                            canonicalTagObj[tagName] = [{
                                sguidURL + "ba0" + "/" + str(metaTagRow['id'][0]): metaTagRow['value'][0]}]
                        else:
                            pass
                    else:
                        final_guid = sguidURL + str(metaTagRow['topic_code'][0]) + "/" + str(metaTagRow['topic_id'][0])
                        if tagName in canonicalTagObj:
                            canonicalTagObj[tagName][final_guid] = metaTagRow['value'][0]
                        else:
                            canonicalTagObj[tagName] = {final_guid: metaTagRow['value'][0]}

            rowInfo["openpipe_canonical"] = canonicalTagObj
            rowInfo["openpipe_canonical"]["id"] = sguidURL + "100/" + str(row['id'][0])
            rows.append(rowInfo)
    results["data"] = rows
    newcon.close()
    t1 = time.time()
    # print("broken")
    # print(t1-t0)
    return results

print(getAllAssetsWithGUID(1,10,"2023-01-06","2033-06-02",1))