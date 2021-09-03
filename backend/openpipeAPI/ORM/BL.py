import json
import sys

import requests
import time

from sqlalchemy import and_
from sqlalchemy.orm import aliased

from backend.openpipeAPI.ORM.ORM import ORM
from backend.openpipeAPI.ORM.Schema import FolderSchema
from backend.openpipeAPI.ORM.TO import TO


class BL:
    sourceTable = {'MET': 1, 'Rijk': 2, 'Cleveland': 3}
    tables = TO().getClasses()

    def getCanonicalTags(self) -> json:
        """ Get all the canonical tags from DB and Returns a json obj.

            Returns
            -------
            JSON
                {
                ...,
                tagName:Default value,
                ...
                }
        """
        # select all CanonicalTags by Passing in the Class
        canonicalTags = ORM().selectAll(self.tables["canonicalMetaTag"])
        res = {}
        for c in canonicalTags:
            res[c.name] = c.default
        return res

    def getAssetsWithoutImages(self):
        orm = ORM()
        queryStatement = "select metaTag.id as metaTagID, metaTag.metaDataId,tagName,value, asset.id as assetID, shortName, IdAtSource, asset.sourceId, sourceName " \
                         "from metaTag join asset on metaTag.metaDataId=asset.metaDataId join source on asset.sourceId=source.id " \
                         "where (tagName='openpipe_canonical_largeImage' and (value is null or value='' or value='http://mec402.boisestate.edu/assets/largeImage.jpg')) " \
                         "or (tagName='openpipe_canonical_smallImage' and (value is null or value='' or value='http://mec402.boisestate.edu/assets/smallImage.jpg'))"
        results = orm.executeSelect(queryStatement)
        return results

    def getAssetsWithBadMetaTags(self):
        orm = ORM()
        AssetDefect = self.tables["assetDefect"]
        canonicalTags = self.getCanonicalTags()
        queryStatement = """select * from asset limit 10"""
        assets = orm.executeSelect(queryStatement)["data"]
        for asset in assets:
            print(asset["id"][0])
            if asset["metaDataId"][0] is None:
                orm.insert(AssetDefect(assetId=asset["id"][0], defectId=1))
            else:
                queryStatement = """select metaTag.id as metaTagID, metaTag.tagName, metaTag.value from  metaTag where metaDataId=""" + str(
                    asset["metaDataId"])
                results = orm.executeSelect(queryStatement)
                res = {}
                for row in results["data"]:
                    if "openpipe_canonical_" in row["tagName"][0]:
                        if row["value"][0] == canonicalTags[row["tagName"][0]] or row["value"][0] is None or str(
                                row["value"][0]).strip() == "":
                            orm.insert(AssetDefect(assetId=asset["id"][0], metaDataId=asset["metaDataId"][0],
                                                   metaTagId=row["metaTagID"][0], metaTagName=row["tagName"][0],
                                                   metaTagValue=row["value"][0], defectId=3))
                        res[row["tagName"][0]] = row["value"][0]
                missingCanonicals = set(canonicalTags.keys()).difference(res.keys())
                for mc in missingCanonicals:
                    orm.insert(
                        AssetDefect(assetId=asset["id"][0], metaDataId=asset["metaDataId"][0], metaTagName=mc,
                                    defectId=2))
        orm.commitClose()

    def getAssetReport(self, collectionId):
        results = {"total": 0, "data": []}
        orm = ORM()
        queryStatement = "SELECT asset.id,asset.metaDataId,shortName,verified,Note FROM asset join collectionMember on asset.id=collectionMember.assetId where asset.verified=0 and collectionId=" + str(
            collectionId)
        newcon = orm.simpConnect()
        results = orm.executeSelectPersist(queryStatement, newcon)
        rows = []
        for row in results['data']:
            rowInfo = {"id": row['id'], "metaDataId": row['metaDataId'], "name": row['shortName'],
                       "verified": row["verified"], "note": row["Note"]}
            print(row["Note"])
            metaDataId = row['metaDataId'][0]
            queryStatement = "select tagName,value,verified,note from metaTag where metaDataId="
            if metaDataId:
                queryStatement = queryStatement + str(metaDataId)
                tags = orm.executeSelectPersist(queryStatement, newcon)['data']
                rowInfo["tags"] = tags
                rows.append(rowInfo)
            # rows.append(rowInfo)
        results["data"] = rows
        newcon.close()
        return results

    def getAssetsWithFaultyImageLink(self):
        orm = ORM()
        AssetDefect = self.tables["assetDefect"]
        queryStatement = "select metaTag.id as metaTagID, metaTag.metaDataId,tagName,value, asset.id as assetID, shortName, IdAtSource, asset.sourceId, sourceName " \
                         "from metaTag join asset on metaTag.metaDataId=asset.metaDataId join source on asset.sourceId=source.id " \
                         "where (tagName='openpipe_canonical_largeImage') " \
                         "or (tagName='openpipe_canonical_smallImage')"
        results = orm.executeSelect(queryStatement)
        for r in results["data"]:
            request = requests.head(r["value"])
            if request.status_code == 200:
                print('Web site exists')
            else:
                orm.insert(AssetDefect(assetId=r["assetID"], metaDataId=r["metaDataId"],
                                       metaTagId=r["metaTagID"], metaTagName=r["tagName"],
                                       metaTagValue=r["value"], defectId=4))

    def getAllAssets(self, page, pageSize, changeStart, changeEnd):
        if (page < 1):
            page = 1
        start = (page - 1) * pageSize
        step = pageSize

        results = {"total": 0, "data": []}

        if int(page) < 0:
            return results

        orm = ORM()
        queryStatement = "SELECT id,metaDataId,shortName FROM asset where insertTime between \'" + changeStart + "\' and \'" + changeEnd + "\' limit " + str(
            start) + "," + str(step)
        t0 = time.time()
        newcon = orm.simpConnect()
        results = orm.executeSelectPersist(queryStatement, newcon)
        rows = []
        for row in results['data']:
            rowInfo = {"id": row['id'], "metaDataId": row['metaDataId'], "name": row['shortName']}
            metaDataId = row['metaDataId'][0]
            queryStatement = "select tagName,value from metaTag where metaDataId="
            if metaDataId:
                queryStatement = queryStatement + str(metaDataId)
                tags = orm.executeSelectPersist(queryStatement, newcon)['data']
                for metaTagRow in tags:
                    rowInfo[metaTagRow['tagName'][0]] = [metaTagRow['value'][0]]
                rows.append(rowInfo)
            # rows.append(rowInfo)
        results["data"] = rows
        newcon.close()
        t1 = time.time()
        # print("broken")
        # print(t1-t0)
        return results

    def getAllAssetsWithGUID(self, page, pageSize, changeStart, changeEnd, none):
        tables = TO().getClasses()
        MetaTag = tables["metaTag"]
        Asset = tables["asset"]

        guidmap = {"city": "500", "classification": "600",
                   "culture": "700", "genre": "800", "medium": "900", "nation": "a00",
                   "artist": "400", "title": "000", "tags": "000"
                   }
        guidURL = "http://mec402.boisestate.edu/cgi-bin/openpipe/data/"
        sguidURL = "http://mec402.boisestate.edu/"
        if (page < 1):
            page = 1
        start = (page - 1) * pageSize
        step = pageSize

        results = {"total": 0,
                   "guidbase": "http://mec402.boisestate.edu/",
                   "data": []}

        if int(page) < 0:
            return results

        t0 = time.time()

        orm = ORM()
        q1 = orm.session.query(Asset). \
            filter(Asset.lastModified.between(changeStart, changeEnd)). \
            offset(start). \
            limit(step). \
            subquery()

        q1 = aliased(Asset, q1)

        resultSet = orm.session.query(q1, MetaTag).join(MetaTag, q1.metaDataId == MetaTag.metaDataId). \
            filter(MetaTag.tagName.like("%{}%".format("openpipe_canonical_"))). \
            order_by(q1.metaDataId)

        orm.executeSelect("""select * from metaTag join (select * from asset WHERE asset.`lastModified` BETWEEN '1900-1-1' AND '2030-1-1'LIMIT 1, 100) as a on a.metaDataId=metaTag.metadataId where tagName like '%openpipe_canonical%';""")

        print(resultSet)

        t1 = time.time()

        # print(t1 - t0)

        assetMetaDataMap = {}
        print(len(resultSet))

        for r in resultSet:
            assetInfo = r[0]
            metaTagInfo = r[1]
            # print(assetInfo.metaDataId, metaTagInfo.metaDataId)
            tagName = metaTagInfo.tagName.split("_")[2]

            tagGuid = {str(metaTagInfo.topic_code) + "/" + str(metaTagInfo.topic_id):metaTagInfo.value}

            if metaTagInfo.topic_name is None and none == 1:
                if tagName == "id":
                    tagGuid = "100" + "/" + str(assetInfo.id)
                else:
                    tagGuid = {"ba0" + "/" + str(metaTagInfo.id):metaTagInfo.value}


            if assetInfo.metaDataId not in assetMetaDataMap:
                assetMetaDataMap[assetInfo.metaDataId] = {"id": "100/" + str(assetInfo.id),
                                                          "metaDataId": assetInfo.metaDataId,
                                                          "name": assetInfo.shortName,
                                                          "openpipe_canonical": {
                                                              tagName: tagGuid
                                                          }}
            else:
                assetMetaDataMap[assetInfo.metaDataId]["openpipe_canonical"][tagName] = tagGuid

        results["data"] = list(assetMetaDataMap.values())
        results["total"] = len(results["data"])

        return results
        # results['guidbase'] = sguidURL
        # sguidURL = ""
        # rows = []
        # for row in results['data']:
        #     # rowInfo = {"id": row['id'], "metaDataId": row['metaDataId'], "name": row['shortName']}
        #     rowInfo = {"metaDataId": row['metaDataId'], "name": row['shortName']}
        #     metaDataId = row['metaDataId'][0]
        #     queryStatement = "select id,tagName,value,topic_name,topic_id,topic_code from metaTag where metaDataId="
        #     if metaDataId:
        #         queryStatement = queryStatement + str(metaDataId)
        #         tags = orm.executeSelectPersist(queryStatement, newcon)['data']
        #         canonicalTagObj = {}
        #         for metaTagRow in tags:
        #             print(metaTagRow)
        #             if "openpipe_canonical_" in metaTagRow['tagName'][0]:  # Only Canonical Tags have topics
        #                 tagName = metaTagRow['tagName'][0].split("_")[2]
        #                 if metaTagRow['topic_name'][0] is None:
        #                     if none == 1:
        #                         print("None value:", none)
        #                         canonicalTagObj[tagName] = {
        #                             sguidURL + "ba0" + "/" + str(metaTagRow['id'][0]): metaTagRow['value'][0]}
        #                     else:
        #                         pass
        #                 else:
        #                     canonicalTagObj[tagName] = {
        #                         guidURL + str(metaTagRow['topic_code'][0]) + "/" + str(metaTagRow['topic_id'][0]):
        #                             metaTagRow['value'][0]}
        #
        #         rowInfo["openpipe_canonical"] = canonicalTagObj
        #         rowInfo["openpipe_canonical"]["id"] = sguidURL + "100/" + str(row['id'][0])
        #         rows.append(rowInfo)
        # results["data"] = rows
        # newcon.close()
        # t1 = time.time()
        # # print("broken")
        # # print(t1-t0)
        # return results

    def getAllAssetsWithGUID1(self, page, pageSize, changeStart, changeEnd):
        guidURL = "http://mec402.boisestate.edu/cgi-bin/openpipe/data/"
        if (page < 1):
            page = 1
        start = (page - 1) * pageSize
        step = pageSize

        results = {"total": 0, "data": []}

        if int(page) < 0:
            return results

        orm = ORM()
        queryStatement = "SELECT id,metaDataId,shortName FROM asset where insertTime between \'" + changeStart + "\' and \'" + changeEnd + "\' limit " + str(
            start) + "," + str(step)
        t0 = time.time()
        newcon = orm.simpConnect()
        results = orm.executeSelectPersist(queryStatement, newcon)
        rows = []
        for row in results['data']:
            rowInfo = {"id": row['id'], "metaDataId": row['metaDataId'], "name": row['shortName']}
            metaDataId = row['metaDataId'][0]
            queryStatement = "select id,tagName,value,topic_name,topic_id from metaTag where metaDataId="
            if metaDataId:
                queryStatement = queryStatement + str(metaDataId)
                tags = orm.executeSelectPersist(queryStatement, newcon)['data']
                canonicalTagObj = {}
                for metaTagRow in tags:
                    if "openpipe_canonical_" in metaTagRow['tagName'][0]:
                        tagName = metaTagRow['tagName'][0].split("_")[2]
                        if metaTagRow['topic_name'][0] is None:
                            canonicalTagObj[tagName] = {
                                guidURL + "metaTag" + "/" + str(metaTagRow['id'][0]): metaTagRow['value'][0]}
                        else:
                            canonicalTagObj[tagName] = {
                                guidURL + str(metaTagRow['topic_name'][0]) + "/" + str(metaTagRow['topic_id'][0]):
                                    metaTagRow['value'][0]}
                    # rowInfo[metaTagRow['tagName'][0]] = [metaTagRow['value'][0]]
                rowInfo["openpipe_canonical"] = canonicalTagObj
                rows.append(rowInfo)
            # rows.append(rowInfo)
        results["data"] = rows
        newcon.close()
        t1 = time.time()
        # print("broken")
        # print(t1-t0)
        return results

    def getAssetbyMetaData(self, assetMetaDataID):
        orm = ORM()
        queryStatement = "SELECT * FROM artmaster.asset join metaTag on metaTag.metaDataId=asset.metaDataId where asset.metaDataId=" + str(
            int(assetMetaDataID))
        results = orm.executeSelect(queryStatement)
        if results['total'] > 0:
            results['total'] = 1
            rowInfo = {"id": results['data'][0]['id'], "metaDataId": results['data'][0]['metaDataId'],
                       "name": results['data'][0]['shortName']}
            for row in results['data']:
                rowInfo[row['tagName'][0]] = [row['value'][0]]

            results["data"] = [rowInfo]
            return results
        else:
            return {"total": 0, "data": []}

    def getAsset(self, assetID):
        orm = ORM()
        queryStatement = "SELECT * FROM artmaster.asset join metaTag on metaTag.metaDataId=asset.metaDataId where asset.id=" + str(
            int(assetID))
        results = orm.executeSelect(queryStatement)
        if results['total'] > 0:
            results['total'] = 1
            rowInfo = {"id": results['data'][0]['id'], "metaDataId": results['data'][0]['metaDataId'],
                       "name": results['data'][0]['shortName']}
            for row in results['data']:
                rowInfo[row['tagName'][0]] = [row['value'][0]]

            results["data"] = [rowInfo]
            return results
        else:
            return {"total": 0, "data": []}

    def insertUserAsset(self, shortName, fileName, uri):
        orm = ORM()
        Images = self.tables["images"]
        return orm.insert(Images(shortName=shortName, fileName=fileName, uri=uri))

    def insertIntoAsset(self, shortName, uri, idAtSource, sourceId, metaDataId, scope):
        orm = ORM()
        Asset = self.tables["asset"]
        MetaData = self.tables["metaData"]
        result = orm.insert(
            Asset(shortName=shortName, uri=uri, IdAtSource=idAtSource, sourceId=sourceId, metaDataId=metaDataId,
                  scope=scope))
        orm.session.query(MetaData).filter(MetaData.id == metaDataId).update({"tableName": "asset", "eid": result})
        orm.commitClose()
        return result

    def insertIntoCollectionMember(self, assetId, collectionId, searchTerm):
        orm = ORM()
        CollectionMember = self.tables["collectionMember"]
        result = orm.insert(CollectionMember(assetId=assetId, collectionId=collectionId, searchTerm=searchTerm))
        orm.commitClose()
        return result

    def insertIntoCollection(self, name):
        orm = ORM()
        Collection = self.tables["collection"]
        MetaData = self.tables["metaData"]
        mid = orm.insert(MetaData())
        result = orm.insert(
            Collection(name=name, image='http://mec402.boisestate.edu/assets/blue-folder.png', metaDataId=mid))
        orm.session.query(MetaData).filter(MetaData.id == mid).update({"tableName": "asset", "eid": result})
        orm.commitClose()
        return result

    def insertIntoMetaData(self):
        orm = ORM()
        MetaData = self.tables["metaData"]
        result = orm.insert(MetaData())
        orm.commitClose()
        return result

    def insertIntoMetaTags(self, data):
        orm = ORM()
        MetaTag = self.tables["metaTag"]
        metaDataId = data["metaDataId"]
        results = []
        for key in data.keys():
            if key != 'metaDataId':
                value = data[key]
                results.append(MetaTag(metaDataId=metaDataId, tagName=key.encode('utf-8', 'surrogateescape'),
                                       value=value.encode('utf-8', 'surrogateescape')))
        orm.bulkInsert(results)
        orm.commitClose()
        return 1

    def addAsset(self, asset):
        orm = ORM()
        MetaTag = self.tables["metaTag"]
        MetaData = self.tables["metaData"]
        Asset = self.tables["asset"]
        asset["metaDataId"] = orm.insert(MetaData())
        assetId = orm.insert(
            Asset(shortName=asset["openpipe_canonical_title"][0], uri='', IdAtSource=asset["openpipe_canonical_id"][0],
                  sourceId=self.sourceTable[asset['openpipe_canonical_source'][0]], metaDataId=asset["metaDataId"],
                  scope=0))
        orm.session.query(MetaData).filter(MetaData.id == asset["metaDataId"]).update(
            {"tableName": "asset", "eid": assetId})
        results = []
        print(asset)
        for key in asset.keys():
            if key != 'metaDataId':
                if str(key).find("openpipe") >= 0:
                    value = asset[key][0]
                else:
                    value = asset[key]
                results.append(MetaTag(metaDataId=asset["metaDataId"], tagName=str(key), value=str(value)))
        orm.bulkInsert(results)
        orm.commitClose()
        return assetId

    def addAssetsToFolder(self, folderId, assetIds, searchTerm):
        orm = ORM()
        FolderMember = self.tables["collectionMember"]
        folderMembers = []
        for assetId in assetIds:
            folderMembers.append(FolderMember(assetId=assetId, collectionId=folderId, searchTerm=searchTerm))
        orm.bulkInsert(folderMembers)
        orm.commitClose()

    def getAssetMetaTags(self, id):
        result = {}
        orm = ORM()
        queryStatement = "select metaTag.id, asset.id as assetId, tagName, value from asset join metaTag on asset.metaDataId=metaTag.metaDataId where asset.id=" + id
        results = orm.executeSelect(queryStatement)
        return results

    def getAllCollections(self, limit):
        guidURL = "http://mec402.boisestate.edu/cgi-bin/openpipe/data/"
        rows = []
        result = {}
        orm = ORM()
        newcon = orm.simpConnect()
        if limit == -1:
            queryStatement = "select collection.*,count(collectionMember.assetId) as assetCount from collection left join collectionMember on collection.id=collectionMember.collectionId group by collection.id order by collection.name asc;"
        else:
            queryStatement = "select collection.*,count(collectionMember.assetId) as assetCount from collection left join collectionMember on collection.id=collectionMember.collectionId group by collection.id LIMIT " + str(
                limit) + " order by collection.name asc"
        results = orm.executeSelectPersist(queryStatement, newcon)
        for row in results['data']:
            rowInfo = row
            metaDataId = row['metaDataId'][0]
            queryStatement = "select id,tagName,value from metaTag where metaDataId="
            if metaDataId:
                queryStatement = queryStatement + str(metaDataId)
                tags = orm.executeSelectPersist(queryStatement, newcon)['data']
                canonTags = {}
                for metaTagRow in tags:
                    canonTags[metaTagRow['tagName'][0]] = [metaTagRow['value'][0]]
                rowInfo['metaTags'] = canonTags
                rows.append(rowInfo)
        results["data"] = rows
        newcon.close()
        return results

    def getAllFolders(self):
        orm = ORM()
        tables = TO().getClasses()
        FolderTable = tables["collection"]
        folders = orm.session.query(FolderTable).order_by(FolderTable.name).all()
        folders_schema = FolderSchema(many=True)
        folders = folders_schema.dump(folders)
        return {"total": len(folders), "data": folders}

    def getCollectionByID(self, id):
        url = "http://mec402.boisestate.edu/cgi-bin/openpipe/data/asset/"
        result = {}

        if isinstance(id, int) != True:
            if id.isnumeric() != True:
                return {"total": 0, "data": [], "error": "no such collection"}

        orm = ORM()
        queryStatement = "SELECT collection.*, assetId FROM collection join collectionMember on collection.id=collectionMember.collectionId where collection.id=" + str(
            int(id))
        results = orm.executeSelect(queryStatement)
        if results['total'] == 0:
            return {"total": 0, "data": [], "error": "no such collection"}

        result['total'] = 1
        result['id'] = results['data'][0]['id']
        result['name'] = results['data'][0]['name']
        result['layoutType'] = results['data'][0]['layoutType']
        result['insertTime'] = results['data'][0]['insertTime']
        result['lastModified'] = results['data'][0]['lastModified']
        result['assets'] = []
        for r in results['data']:
            result['assets'].append(url + str(r['assetId'][0]))
        return result

    def getRangeOfCollections(self, start, end):
        result = {}
        orm = ORM()
        queryStatement = "select * from collection LIMIT " + start + "," + end
        results = orm.executeSelect(queryStatement)
        return result

    def getPublicAssetsInCollection(self, collectionId, page, pageSize):
        orm = ORM()
        start = (page - 1) * pageSize
        step = pageSize
        queryStatement = "SELECT assetId,asset.metaDataId,asset.verified as assetVerified FROM collectionMember JOIN asset ON collectionMember.assetId = asset.id WHERE scope=0 and collectionId =" + str(
            collectionId) + " limit " + str(start) + "," + str(step)
        results = orm.executeSelect(queryStatement)
        rows = []
        for row in results['data']:
            metaDataId = row['metaDataId'][0]
            rowInfo = {"id": row['assetId'], "metaDataId": row['metaDataId'], "assetVerified": row['assetVerified']}
            queryStatement = "select tagName,value from metaTag where metaDataId="
            if metaDataId:
                queryStatement = queryStatement + str(metaDataId)
                tags = orm.executeSelect(queryStatement)['data']
                for metaTagRow in tags:
                    rowInfo[metaTagRow['tagName'][0]] = [metaTagRow['value'][0]]
                rows.append(rowInfo)
            # rows.append(rowInfo)
            rowInfo["id"] = row['assetId']
        results["data"] = rows
        return results

    def getAllAssetIDs(self):
        url = "http://mec402.boisestate.edu/cgi-bin/openpipe/data/asset/"
        result = []
        orm = ORM()
        queryStatement = "select id from asset"
        results = orm.executeSelect(queryStatement)
        for r in results['data']:
            result.append(url + str(r['id'][0]))
        results['data'] = result
        return results

    def getAllFolderIDs(self):
        url = "http://mec402.boisestate.edu/cgi-bin/openpipe/data/folder/"
        result = []
        orm = ORM()
        queryStatement = "select id from collection"
        results = orm.executeSelect(queryStatement)
        for r in results['data']:
            result.append(url + str(r['id'][0]))
        results['data'] = result
        return results

    def getAssetbyMetaData(self, assetMetaDataID):
        orm = ORM()
        queryStatement = "SELECT * FROM artmaster.asset join metaTag on metaTag.metaDataId=asset.metaDataId where asset.metaDataId=" + str(
            int(assetMetaDataID))
        results = orm.executeSelect(queryStatement)
        if results['total'] > 0:
            results['total'] = 1
            rowInfo = {"id": results['data'][0]['id'], "metaDataId": results['data'][0]['metaDataId'],
                       "name": results['data'][0]['shortName']}
            for row in results['data']:
                rowInfo[row['tagName'][0]] = [row['value'][0]]

            results["data"] = [rowInfo]
            return results
        else:
            return {"total": 0, "data": []}

    def getAllTopicMembers(self, topicName, topicCode):
        if topicName == 'asset':
            return self.getAllAssetIDs()
        elif topicName == 'folder':
            return self.getAllFolderIDs()
        else:
            orm = ORM()
            tables = TO().getClasses()
            Topic = tables["topic"]
            topicResultSet = orm.session.query(Topic).filter(Topic.type == topicName).all()
            res = {"total": 0, "data": []}
            resArr = []
            for t in topicResultSet:
                resArr.append(str(t.code) + "/" + str(t.id))
            res["total"] = len(resArr)
            res["data"] = resArr
            return res

    def getGUIDInfo(self, guidName, guidId):
        orm = ORM()
        tables = TO().getClasses()
        GUIDType = tables["guidType"]
        Topic = tables["topic"]
        MetaTag = tables["metaTag"]
        guidTypeResultSet = orm.session.query(GUIDType).all()

        guidMap = {}
        for gt in guidTypeResultSet:
            guidMap[gt.name] = gt.code

        if guidName not in guidMap.keys():
            return {"total": 0, "data": [], "error": "invalid topic"}
        elif guidId is None or guidId == "" or guidId == " ":
            return self.getAllTopicMembers(guidName, guidMap[guidName])
        else:
            topicResultSet = orm.session.query(Topic).filter(Topic.id == guidId).all()
            if guidName == 'asset':
                return self.getAsset(guidId)
            elif guidName == 'folder':
                return self.getCollectionByID(guidId)
            elif guidName == 'metaData':
                return self.getAssetbyMetaData(guidId)
            else:
                metaTagResultSet = orm.session.query(MetaTag).filter(MetaTag.topic_id == guidId).all()
                otherAliases = set([])
                assetMetaDataIdWithTopic = set([])
                for alias in metaTagResultSet:
                    otherAliases.add(alias.value)
                    assetMetaDataIdWithTopic.add(guidMap["metaData"] + "/" + str(alias.metaDataId))
                    # print(alias.value,alias.id,alias.metaDataId)
                return {"total": 1, "topicName": topicResultSet[0].name, "topicAliases": list(otherAliases),
                        "topicAssets": list(assetMetaDataIdWithTopic)}

    def deleteMetaTag(self, metaDataId, tagName, value):
        orm = ORM()
        MetaTag = self.tables["metaTag"]
        orm.session.query(MetaTag).filter(MetaTag.metaDataId == metaDataId, MetaTag.tagName == tagName
                                          , MetaTag.value == value).delete()
        orm.commitClose()
        return {"data": 1}

    def deleteFolderMember(self, collectionId, assetId):
        orm = ORM()
        CollectionMember = self.tables["collectionMember"]
        orm.session.query(CollectionMember).filter(CollectionMember.collectionId == collectionId
                                                   , CollectionMember.assetId == assetId).delete()
        orm.commitClose()
        return {"data": 1}

    def deleteFolder(self, collectionId):
        orm = ORM()
        Collection = self.tables["collection"]
        CollectionMember = self.tables["collectionMember"]
        orm.session.query(CollectionMember).filter(CollectionMember.collectionId == collectionId).delete()
        orm.session.query(Collection).filter(Collection.id == collectionId).delete()
        orm.commitClose()
        return {"data": 1}

    def updateFolder(self, folderId, newName, newImage, newVerified):
        orm = ORM()
        Collection = self.tables["collection"]
        orm.session.query(Collection).filter(Collection.id == folderId).update(
            {"name": newName, "image": newImage, "verified": newVerified})
        orm.commitClose()
        return {"data": 1}

    def updateMetaTag(self, metaDataId, oldTagName, oldValue, newTagName, newValue):
        orm = ORM()
        MetaTag = self.tables["metaTag"]
        orm.session.query(MetaTag).filter(MetaTag.metaDataId == metaDataId, MetaTag.tagName == oldTagName
                                          , MetaTag.value == oldValue).update \
            ({"metaDataId": metaDataId, "tagName": newTagName, "value": newValue})
        orm.commitClose()
        return {"data": 1}

    def insertMetaTag(self, metaDataId, tagName, value):
        orm = ORM()
        MetaTag = self.tables["metaTag"]
        result = orm.insert(MetaTag(metaDataId=metaDataId, tagName=tagName, value=value))
        orm.commitClose()
        return result

    def insertIntoImages(self, shortName, fileName, uri):
        orm = ORM()
        Images = self.tables["images"]
        result = orm.insert(Images(shortname=shortName, filename=fileName, uri=uri))
        orm.commitClose()
        return result

    def addArtist(self, name, nationality, aliases):
        orm = ORM()
        Artist = self.tables["artist"]
        result = orm.insert(Artist(name=name, nationality=nationality, otherNames=aliases))
        orm.commitClose()
        return result

    def getArtist(self, id):
        result = {"total": 0, "data": [], "error": "invalid id"}
        if isinstance(id, int) != True:
            if id.isnumeric():
                orm = ORM()
                queryStatement = "select * from artist where id=" + id
                #          print(queryStatement,file=sys.stderr)
                result = orm.executeSelect(queryStatement)
        return result

    def getTopic(self, atopic, id):
        result = {"total": 0, "data": [], "error": "invalid id"}
        if isinstance(id, int) != True:
            if id.isnumeric():
                orm = ORM()
                queryStatement = 'select * from ' + atopic + '_tags where topic_id=' + id
                #          print(queryStatement,file=sys.stderr)
                result = orm.executeSelect(queryStatement)
        return result

    def getAllTopicIDs(self, atopic):
        url = "http://mec402.boisestate.edu/cgi-bin/openpipe/data/" + atopic + "/"
        result = []
        orm = ORM()
        queryStatement = "select id from " + atopic
        results = orm.executeSelect(queryStatement)
        for r in results['data']:
            result.append(url + str(r['id'][0]))
        results['data'] = result
        return results

    def getAllArtistIDs(self):
        url = "http://mec402.boisestate.edu/cgi-bin/openpipe/data/artist/"
        result = []
        orm = ORM()
        queryStatement = "select id from artist"
        results = orm.executeSelect(queryStatement)
        for r in results['data']:
            result.append(url + str(r['id'][0]))
        results['data'] = result
        return results

    def getTagMapping(self):
        orm = ORM()
        queryStatement = "select tagMap.id as mapId, sourceID,sourceName,tagID,canonicalMetaTag.name as tagName, tagMap from tagMap join source on tagMap.sourceID=source.id join canonicalMetaTag on canonicalMetaTag.id=tagID;"
        results = orm.executeSelect(queryStatement)
        return results

    def updateTagMapping(self, mapId, mapVal):
        orm = ORM()
        TagMap = self.tables["tagMap"]
        orm.session.query(TagMap).filter(TagMap.id == mapId).update({"tagMap": mapVal})
        orm.commitClose()
        return {"data": 1}

    def getMoments(self):
        orm = ORM()
        queryStatement = "select asset.id as assetId from asset join (select * from  metaTag where tagname='openpipe_canonical_moment' and value != '0') as a on asset.metaDataId=a.metaDataId;"
        results = orm.executeSelect(queryStatement)
        rows = []
        url = "http://mec402.boisestate.edu/cgi-bin/openpipe/data/asset/"
        for r in results['data']:
            id = r['assetId'][0]
            rows.append(url + str(id))
        return {'total': len(rows), 'data': rows}

    def saveFolderLayout(self, data):
        orm = ORM()
        FolderMembers = self.tables["collectionMember"]
        fid = data['folderId']
        assets = data['data']
        for d in data:
            orm.session.query(FolderMembers).filter(
                and_(FolderMembers.collectionId == fid, FolderMembers.assetId == d['assetId'])).update(
                {"geometry": d['geometry'], 'wall': d['wall']})
        orm.commitClose()
        return {"data": 1}

    def saveUploadAsset(self, data):
        orm = ORM()
        FolderMembers = self.tables["collectionMember"]
        Images = self.tables["images"]
        Asset = self.tables["asset"]
        MetaData = self.tables["metaData"]
        MetaTag = self.tables["metaTag"]

        videoIconURL = "http://mec402.boisestate.edu/assets/videoIcon.png"

        shortName = data["shortName"]
        uri = data["uri"]
        folderId = data["folderId"]
        assetType = data["assetType"]

        videoTypes = ['.264', '.3g2', '.3gp', '.3gp2', '.3gpp', '.3gpp2', '.3mm', '.3p2', '.60d', '.787', '.89', '.aaf',
                      '.aec', '.aep', '.aepx',
                      '.aet', '.aetx', '.ajp', '.ale', '.am', '.amc', '.amv', '.amx', '.anim', '.aqt', '.arcut', '.arf',
                      '.asf', '.asx', '.avb',
                      '.avc', '.avd', '.avi', '.avp', '.avs', '.avs', '.avv', '.axm', '.bdm', '.bdmv', '.bdt2', '.bdt3',
                      '.bik', '.bin', '.bix',
                      '.bmk', '.bnp', '.box', '.bs4', '.bsf', '.bvr', '.byu', '.camproj', '.camrec', '.camv', '.ced',
                      '.cel', '.cine', '.cip',
                      '.clpi', '.cmmp', '.cmmtpl', '.cmproj', '.cmrec', '.cpi', '.cst', '.cvc', '.cx3', '.d2v', '.d3v',
                      '.dat', '.dav', '.dce',
                      '.dck', '.dcr', '.dcr', '.ddat', '.dif', '.dir', '.divx', '.dlx', '.dmb', '.dmsd', '.dmsd3d',
                      '.dmsm', '.dmsm3d', '.dmss',
                      '.dmx', '.dnc', '.dpa', '.dpg', '.dream', '.dsy', '.dv', '.dv-avi', '.dv4', '.dvdmedia', '.dvr',
                      '.dvr-ms', '.dvx', '.dxr',
                      '.dzm', '.dzp', '.dzt', '.edl', '.evo', '.eye', '.ezt', '.f4p', '.f4v', '.fbr', '.fbr', '.fbz',
                      '.fcp', '.fcproject',
                      '.ffd', '.flc', '.flh', '.fli', '.flv', '.flx', '.gfp', '.gl', '.gom', '.grasp', '.gts', '.gvi',
                      '.gvp', '.h264', '.hdmov',
                      '.hkm', '.ifo', '.imovieproj', '.imovieproject', '.ircp', '.irf', '.ism', '.ismc', '.ismv',
                      '.iva', '.ivf', '.ivr', '.ivs',
                      '.izz', '.izzy', '.jss', '.jts', '.jtv', '.k3g', '.kmv', '.ktn', '.lrec', '.lsf', '.lsx', '.m15',
                      '.m1pg', '.m1v', '.m21',
                      '.m21', '.m2a', '.m2p', '.m2t', '.m2ts', '.m2v', '.m4e', '.m4u', '.m4v', '.m75', '.mani', '.meta',
                      '.mgv', '.mj2', '.mjp',
                      '.mjpg', '.mk3d', '.mkv', '.mmv', '.mnv', '.mob', '.mod', '.modd', '.moff', '.moi', '.moov',
                      '.mov', '.movie', '.mp21',
                      '.mp21', '.mp2v', '.mp4', '.mp4v', '.mpe', '.mpeg', '.mpeg1', '.mpeg4', '.mpf', '.mpg', '.mpg2',
                      '.mpgindex', '.mpl',
                      '.mpl', '.mpls', '.mpsub', '.mpv', '.mpv2', '.mqv', '.msdvd', '.mse', '.msh', '.mswmm', '.mts',
                      '.mtv', '.mvb', '.mvc',
                      '.mvd', '.mve', '.mvex', '.mvp', '.mvp', '.mvy', '.mxf', '.mxv', '.mys', '.ncor', '.nsv', '.nut',
                      '.nuv', '.nvc', '.ogm',
                      '.ogv', '.ogx', '.osp', '.otrkey', '.pac', '.par', '.pds', '.pgi', '.photoshow', '.piv', '.pjs',
                      '.playlist', '.plproj',
                      '.pmf', '.pmv', '.pns', '.ppj', '.prel', '.pro', '.prproj', '.prtl', '.psb', '.psh', '.pssd',
                      '.pva', '.pvr', '.pxv',
                      '.qt', '.qtch', '.qtindex', '.qtl', '.qtm', '.qtz', '.r3d', '.rcd', '.rcproject', '.rdb', '.rec',
                      '.rm', '.rmd', '.rmd',
                      '.rmp', '.rms', '.rmv', '.rmvb', '.roq', '.rp', '.rsx', '.rts', '.rts', '.rum', '.rv', '.rvid',
                      '.rvl', '.sbk', '.sbt',
                      '.scc', '.scm', '.scm', '.scn', '.screenflow', '.sec', '.sedprj', '.seq', '.sfd', '.sfvidcap',
                      '.siv', '.smi', '.smi',
                      '.smil', '.smk', '.sml', '.smv', '.spl', '.sqz', '.srt', '.ssf', '.ssm', '.stl', '.str', '.stx',
                      '.svi', '.swf', '.swi',
                      '.swt', '.tda3mt', '.tdx', '.thp', '.tivo', '.tix', '.tod', '.tp', '.tp0', '.tpd', '.tpr', '.trp',
                      '.ts', '.tsp', '.ttxt',
                      '.tvs', '.usf', '.usm', '.vc1', '.vcpf', '.vcr', '.vcv', '.vdo', '.vdr', '.vdx', '.veg', '.vem',
                      '.vep', '.vf', '.vft',
                      '.vfw', '.vfz', '.vgz', '.vid', '.video', '.viewlet', '.viv', '.vivo', '.vlab', '.vob', '.vp3',
                      '.vp6', '.vp7', '.vpj',
                      '.vro', '.vs4', '.vse', '.vsp', '.w32', '.wcp', '.webm', '.wlmp', '.wm', '.wmd', '.wmmp', '.wmv',
                      '.wmx', '.wot', '.wp3',
                      '.wpl', '.wtv', '.wve', '.wvx', '.xej', '.xel', '.xesc', '.xfl', '.xlmv', '.xmv', '.xvid', '.y4m',
                      '.yog', '.yuv', '.zeg',
                      '.zm1', '.zm2', '.zm3', '.zmv']

        imageTypes = ['.ras', '.xwd', '.bmp', '.jpe', '.jpg', '.jpeg', '.xpm', '.ief', '.pbm', '.tif', '.gif', '.ppm',
                      '.xbm', '.tiff', '.rgb', '.pgm', '.png', '.pnm']

        assetGroup = "Unknown"

        if "." + str(assetType).lower() in videoTypes:
            assetGroup = "video"
        elif "." + str(assetType).lower() in imageTypes:
            assetGroup = "image"

        metaDataId = orm.insert(MetaData())

        assetId = orm.insert(
            Asset(shortName=shortName, uri=uri, sourceId=666, metaDataId=metaDataId, scope=0, type=assetGroup))

        fileName = "Local_uploaded_asset_" + str(assetId) + "." + str(assetType)

        imageId = orm.insert(Images(shortname=shortName, filename=fileName, uri=uri, type=assetGroup))

        orm.session.query(MetaData).filter(MetaData.id == metaDataId).update({"tableName": "asset", "eid": assetId})

        fmid = orm.insert(FolderMembers(assetId=assetId, collectionId=folderId, searchTerm="Local_Asset_Upload"))

        canonTags = orm.executeSelect("""SELECT * FROM artmaster.canonicalMetaTag where req='yes';""")
        tags = []
        print(canonTags)
        for d in canonTags["data"]:
            if d["name"][0] == 'openpipe_canonical_title':
                tags.append(MetaTag(metaDataId=metaDataId, tagName=str(d["name"][0]), value=str(shortName)))
            elif d["name"][0] == 'openpipe_canonical_fullImage':
                tags.append(MetaTag(metaDataId=metaDataId, tagName=str(d["name"][0]), value=str(uri + fileName)))
            elif d["name"][0] == 'openpipe_canonical_smallImage':
                if assetGroup == "image":
                    tags.append(MetaTag(metaDataId=metaDataId, tagName=str(d["name"][0]), value=str(uri + fileName)))
                elif assetGroup == "video":
                    tags.append(MetaTag(metaDataId=metaDataId, tagName=str(d["name"][0]), value=str(videoIconURL)))
                else:
                    tags.append(MetaTag(metaDataId=metaDataId, tagName=str(d["name"][0]), value=str(d["default"][0])))
            else:
                tags.append(MetaTag(metaDataId=metaDataId, tagName=str(d["name"][0]), value=str(d["default"][0])))
        orm.bulkInsert(tags)
        orm.commitClose()
        return fileName

    def getFolderLayout(self, folderId):
        orm = ORM()
        stm = "select assetId, collectionId, asset.metaDataId, geometry, wall, type, value from (select * from collectionMember where collectionId=" + str(
            folderId) + ") as a join asset on a.assetId=asset.id join metaTag on metaTag.metaDataId=asset.metaDataId where tagName='openpipe_canonical_smallImage'"
        res = orm.executeSelect(stm)
        return res

    def getTopics(self, page, pageSize):

        if (page < 1):
            page = 1
        start = (page - 1) * pageSize
        step = pageSize

        if int(page) < 0:
            return []

        orm = ORM()
        stm = "select * from topic where code!='b00' order by type limit " + str(start) + "," + str(step)

        allTopicTypes = orm.executeSelect(stm)

        guidmap = {"city": "500", "classification": "600",
                   "culture": "700", "genre": "800", "medium": "900", "nation": "a00",
                   "artist": "400", "title": "000", "tags": "000", "metaTag": "b00"
                   }

        repAssetId = 10

        finalRes = {
            "availableTopics": ["artist", "genre", "city", "classification", "culture", "medium", "nation", "metaTag"]}
        for t in allTopicTypes['data']:
            topicType = t['type'][0]
            topicId = t['id'][0]
            topicInfo = {"id": topicId,
                         "value": t['name'][0],
                         "biography": t['description'][0],
                         "guid": "http://mec402.boisestate.edu/" + guidmap[topicType] + "/" + str(topicId),
                         "representativeAssetId": "100/" + str(repAssetId)}

            if topicType in finalRes.keys():
                finalRes[topicType]["data"].append(topicInfo)
                finalRes[topicType]["total"] = finalRes[topicType]["total"] + 1
            else:
                finalRes[topicType] = {"total": 1, "data": [topicInfo]}
                # finalRes["availableTopics"].append(topicType)

        return finalRes

# help(BL().getCanonicalTags())
