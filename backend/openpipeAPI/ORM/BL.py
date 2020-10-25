import json
import sys

import requests
import time

from openpipeAPI.ORM.ORM import ORM
from openpipeAPI.ORM.TO import TO


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

    def getAllAssetsWithGUID(self, page, pageSize, changeStart, changeEnd):
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
            rowInfo = {"id": row['assetId'], "metaDataId": row['metaDataId'],"assetVerified": row['assetVerified']}
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

    #     def getGUIDInfo(self, tableName, id):
    #         orm = ORM()
    #         if (tableName == "entities"):
    #            return Topics().getCanonicalTagsJSON()
    #         entities = Topics().getCanonicalTagsList()
    #         entities.append("asset")
    #         entities.append("folder")
    # #        if (tableName not in ["asset", "folder","artist"]):
    #         if (tableName not in entities):
    #             return {"total" :0 , "data" :[], "error": "invalid topic"}
    #         elif tableName == "asset":
    #             if id is not None and id != "":
    #                 return self.getAsset(id)
    #             else:
    #                 return self.getAllAssetIDs()
    #         elif tableName == "folder":
    #             if id is not None and id != "":
    #                 return self.getCollectionByID(id)
    #             else:
    #                 return self.getAllFolderIDs()
    #         elif tableName == "artist":
    #             if id is not None and id != "":
    #                 return self.getArtist(id)
    #             else:
    #                 return self.getAllArtistIDs()
    #         else:
    #             if id is not None and id != "":
    #                 return self.getTopic(tableName,id)
    #             else:
    #                 return self.getAllTopicIDs(tableName)
    #
    #         return {"total" :0 , "data" :[], "error": "empty topic"}

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
        orm.session.query(Collection).filter(Collection.id == folderId).update({"name": newName, "image": newImage,"verified":newVerified})
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

# help(BL().getCanonicalTags())
