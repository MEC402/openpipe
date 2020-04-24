import json

import Slack
from ORM.ORM import ORM
from ORM.TO import TO
import requests


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

        results = orm.executeSelect(queryStatement, ())
        return results

    def getAssetsWithBadMetaTags(self):
        orm = ORM()
        AssetDefect = self.tables["assetDefect"]
        canonicalTags = self.getCanonicalTags()
        queryStatement = """select * from asset"""
        assets = orm.executeSelect(queryStatement)["data"]
        for asset in assets:
            print(asset["id"])
            if asset["metaDataId"] is None:
                orm.insert(AssetDefect(assetId=asset["id"], defectId=1))
            else:
                queryStatement = """select metaTag.id as metaTagID, metaTag.tagName, metaTag.value from  metaTag 
                where metaDataId=%s """
                data_tuple = (str(asset["metaDataId"]),)
                results = orm.executeSelect(queryStatement, data_tuple)
                res = {}
                for row in results["data"]:
                    if "openpipe_canonical_" in row["tagName"]:
                        if row["value"] == canonicalTags[row["tagName"]] or row["value"] is None or str(
                                row["value"]).strip() == "":
                            orm.insert(AssetDefect(assetId=asset["id"], metaDataId=asset["metaDataId"],
                                                   metaTagId=row["metaTagID"], metaTagName=row["tagName"],
                                                   metaTagValue=row["value"], defectId=3))
                        res[row["tagName"]] = row["value"]
                missingCanonicals = set(canonicalTags.keys()).difference(res.keys())
                for mc in missingCanonicals:
                    orm.insert(
                        AssetDefect(assetId=asset["id"], metaDataId=asset["metaDataId"], metaTagName=mc, defectId=2))

    def getAllImages(self):
        orm = ORM()
        queryStatement = "SELECT * from images limit 10;"
        results = orm.executeSelect(queryStatement,())
        orm.commitClose()
        return results

    def getAssetReport(self):
        orm = ORM()
        queryStatement = """SELECT assetId,assetDefect.metaDataId,metaTagId,metaTagName,metaTagValue,defectType, asset.shortName as assetName, source.sourceName FROM assetDefect join defect on assetDefect.defectId=defect.id join asset on assetDefect.assetId=asset.id join source on asset.sourceId=source.id order by assetId asc;"""
        results = orm.executeSelect(queryStatement)
        return results

    def getAssetsWithFaultyImageLink(self):
        orm = ORM()
        AssetDefect = self.tables["assetDefect"]
        queryStatement = "select metaTag.id as metaTagID, metaTag.metaDataId,tagName,value, asset.id as assetID, shortName, IdAtSource, asset.sourceId, sourceName " \
                         "from metaTag join asset on metaTag.metaDataId=asset.metaDataId join source on asset.sourceId=source.id " \
                         "where (tagName='openpipe_canonical_largeImage') " \
                         "or (tagName='openpipe_canonical_smallImage')"
        results = orm.executeSelect(queryStatement, ())
        for r in results["data"]:
            request = requests.head(r["value"])
            if request.status_code == 200:
                print('Web site exists')
            else:
                orm.insert(AssetDefect(assetId=r["assetID"], metaDataId=r["metaDataId"],
                                       metaTagId=r["metaTagID"], metaTagName=r["tagName"],
                                       metaTagValue=r["value"], defectId=4))

    def getAllAssets(self, page, pageSize, changeStart, changeEnd):
        Slack.sendMessage("getAllAssets")
        start = (page - 1) * pageSize
        step = pageSize
        f = 0
        t = 0
        orm = ORM()
        queryStatement = "SELECT id,metaDataId,shortName FROM asset where insertTime between %s and %s limit %s,%s"
        data_tuple = (changeStart, changeEnd, start, step)
        results = orm.executeSelect(queryStatement, data_tuple)
        rows = []
        for row in results['data']:
            rowInfo = {"id": row['id'], "metaDataId": row['metaDataId'], "name": row['shortName']}
            metaDataId = row['metaDataId'][0]
            queryStatement = "select tagName,value from metaTag where metaDataId=%s"
            if metaDataId:
                res = orm.executeSelect(queryStatement, (str(metaDataId),))
                tags = res['data']
                f = f + res["fetch"]
                t = t + res["for"]
                for metaTagRow in tags:
                    rowInfo[metaTagRow['tagName'][0]] = [metaTagRow['value'][0]]
                rows.append(rowInfo)
            # rows.append(rowInfo)
        results["data"] = rows
        Slack.sendMessage("total fetch")
        Slack.sendMessage(f)
        Slack.sendMessage("total for")
        Slack.sendMessage(t)
        return results

    def getAsset(self, assetID):
        orm = ORM()
        queryStatement = "SELECT * FROM artmaster.asset join metaTag on metaTag.metaDataId=asset.metaDataId where asset.id=%s"
        results = orm.executeSelect(queryStatement, (assetID,))
        if results['total'] > 0:
            results['total'] = 1
            rowInfo = {"id": results['data'][0]['id'], "metaDataId": results['data'][0]['metaDataId'],
                       "name": results['data'][0]['shortName']}
            for row in results['data']:
                rowInfo[row['tagName'][0]] = [row['value'][0]]

            results["data"] = [rowInfo]
            return results
        return {"total": 0, "data": []}

    def insertUserAsset(self, shortName, fileName, uri):
        orm = ORM()
        Images = self.tables["images"]
        return orm.insert(Images(shortName=shortName, fileName=fileName, uri=uri))

    def insertIntoAsset(self, shortName, uri, idAtSource, sourceId, metaDataId, scope):
        orm = ORM()
        Asset = self.tables["asset"]
        result = orm.insert(
            Asset(shortName=shortName, uri=uri, IdAtSource=idAtSource, sourceId=sourceId, metaDataId=metaDataId,
                  scope=scope))
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
        result = orm.insert(Collection(name=name, image='http://mec402.boisestate.edu/assets/blue-folder.png'))
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

    def getAssetMetaTags(self, assetId):
        result = {}
        orm = ORM()
        queryStatement = "select metaTag.id, asset.id as assetId, tagName, value from asset join metaTag on asset.metaDataId=metaTag.metaDataId where asset.id=%s"
        results = orm.executeSelect(queryStatement, (assetId,))
        return results

    def getAllCollections(self, limit):
        result = {}
        orm = ORM()
        if limit == -1:
            queryStatement = "select * from collection"
            results = orm.executeSelect(queryStatement, ())
        else:
            queryStatement = "select * from collection LIMIT %s "
            results = orm.executeSelect(queryStatement, (limit,))
        return results

    def getCollectionByID(self, collectionId):
        url = "http://mec402.boisestate.edu/cgi-bin/openpipe/data/asset/"
        result = {}
        orm = ORM()
        queryStatement = "SELECT collection.*, assetId FROM collection join collectionMember on collection.id=collectionMember.collectionId where collection.id=%s"
        results = orm.executeSelect(queryStatement, (collectionId,))
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
        queryStatement = "select * from collection LIMIT %s,%s"
        results = orm.executeSelect(queryStatement, (start, end))
        return result

    def getPublicAssetsInCollection(self, collectionId, page, pageSize):
        orm = ORM()
        start = (page - 1) * pageSize
        step = pageSize
        queryStatement = "SELECT assetId,asset.metaDataId FROM collectionMember JOIN asset ON collectionMember.assetId = asset.id WHERE scope=0 and collectionId =%s limit %s,%s"
        results = orm.executeSelect(queryStatement, (collectionId, start, step))
        rows = []
        for row in results['data']:
            metaDataId = row['metaDataId'][0]
            rowInfo = {"id": row['assetId'], "metaDataId": row['metaDataId']}
            queryStatement = "select tagName,value from metaTag where metaDataId=%s"
            if metaDataId:
                queryStatement = queryStatement
                tags = orm.executeSelect(queryStatement, (metaDataId,))['data']
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
        results = orm.executeSelect(queryStatement, ())
        for r in results['data']:
            result.append(url + str(r['id'][0]))
        results['data'] = result
        return results

    def getAllFolderIDs(self):
        url = "http://mec402.boisestate.edu/cgi-bin/openpipe/data/folder/"
        result = []
        orm = ORM()
        queryStatement = "select id from collection"
        results = orm.executeSelect(queryStatement, ())
        for r in results['data']:
            result.append(url + str(r['id'][0]))
        results['data'] = result
        return results

    def getGUIDInfo(self, tableName, id):
        orm = ORM()
        if tableName not in ["asset", "folder", "artist"]:
            return "entity does not exist"
        elif tableName == "asset":
            if id is not None and id != "":
                return self.getAsset(id)
            else:
                return self.getAllAssetIDs()
        elif tableName == "folder":
            if id is not None and id != "":
                return self.getCollectionByID(id)
            else:
                return self.getAllFolderIDs()
        elif tableName == "artist":
            if id is not None and id != "":
                return self.getArtist(id)
            else:
                return self.getAllArtistIDs()
        return {"data": "bad GUID"}

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

    def updateFolder(self, folderId, newName, newImage):
        orm = ORM()
        Collection = self.tables["collection"]
        orm.session.query(Collection).filter(Collection.id == folderId).update({"name": newName, "image": newImage})
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
        result = {}
        orm = ORM()
        queryStatement = "select * from artist where id=%s"
        result = orm.executeSelect(queryStatement, (id,))
        return result

    def getAllArtistIDs(self):
        url = "http://mec402.boisestate.edu/cgi-bin/openpipe/data/artist/"
        result = []
        orm = ORM()
        queryStatement = "select id from artist"
        results = orm.executeSelect(queryStatement, ())
        for r in results['data']:
            result.append(url + str(r['id'][0]))
        results['data'] = result
        return results

# help(BL().getCanonicalTags())
