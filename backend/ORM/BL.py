from ORM.ORM import ORM
from ORM.TO import TO
import requests


class BL:
    tables = TO().getClasses()

    def getCanonicalTags(self):
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
        queryStatement = """select * from asset"""
        assets = orm.executeSelect(queryStatement)["data"]
        for asset in assets:
            print(asset["id"])
            if asset["metaDataId"] is None:
                orm.insert(AssetDefect(assetId=asset["id"], defectId=1))
            else:
                queryStatement = """select metaTag.id as metaTagID, metaTag.tagName, metaTag.value from  metaTag where metaDataId=""" + str(
                    asset["metaDataId"])
                results = orm.executeSelect(queryStatement)
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
        start = (page - 1) * pageSize
        step = pageSize

        orm = ORM()
        queryStatement = "SELECT id,metaDataId,shortName FROM asset where insertTime between \'" + changeStart + "\' and \'" + changeEnd + "\' limit " + str(start) + "," + str(step)
        results = orm.executeSelect(queryStatement)
        rows=[]
        for row in results['data']:
            rowInfo = {"id": row['id'], "metaDataId": row['metaDataId'], "name": row['shortName']}
            metaDataId = row['metaDataId'][0]
            queryStatement = "select tagName,value from metaTag where metaDataId="
            if metaDataId:
                queryStatement = queryStatement+str(metaDataId)
                tags=orm.executeSelect(queryStatement)['data']
                for metaTagRow in tags:
                    rowInfo[metaTagRow['tagName'][0]] = [metaTagRow['value'][0]]
                rows.append(rowInfo)
            # rows.append(rowInfo)
        results["data"] = rows
        return results

    def getAsset(self, assetID):
        orm = ORM()
        queryStatement = "SELECT * FROM artmaster.asset join metaTag on metaTag.metaDataId=asset.metaDataId where asset.id="+str(int(assetID))
        results = orm.executeSelect(queryStatement)
        rows=[]
        results['total']=1
        rowInfo = {"id": results['data'][0]['id'], "metaDataId": results['data'][0]['metaDataId'], "name": results['data'][0]['shortName']}
        for row in results['data']:
            rowInfo[row['tagName'][0]] = [row['value'][0]]
        results["data"] = rows
        return results

    def insertUserAsset(self, shortName, fileName, uri):
        orm = ORM()
        Images = self.tables["images"]
        return orm.insert(Images(shortName=shortName,fileName=fileName,uri=uri))


    def insertIntoAsset(self, shortName, uri, idAtSource, sourceId, metaDataId, scope):
        orm = ORM()
        Asset = self.tables["asset"]
        return orm.insert(
            Asset(shortName=shortName, uri=uri, IdAtSource=idAtSource, sourceId=sourceId, metaDataId=metaDataId,
                  scope=scope))

    def insertIntoCollectionMember(self, assetId, collectionId, searchTerm):
        orm = ORM()
        CollectionMember = self.tables["collectionMember"]
        return orm.insert(CollectionMember(assetId=assetId, collectionId=collectionId, searchTerm=searchTerm))

    def insertIntoCollection(self, name):
        orm = ORM()
        Collection = self.tables["collection"]
        return orm.insert(Collection(name=name))

    def insertIntoMetaData(self):
        orm = ORM()
        MetaData = self.tables["metaData"]
        return orm.insert(MetaData())

    def insertIntoMetaTags(self, data):
        orm = ORM()
        MetaTag = self.tables["metaTag"]
        metaDataId = data['metaDataId']
        results = []
        for key in data.keys():
            if key != 'metaDataId':
                value = data[key]
                results.append(orm.insert(MetaTag(metaDataId=str(metaDataId), tagName=str(key), value=str(value))))
        print(results)
        return 1


    def getAssetMetaTags(self,id):
        result = {}
        orm = ORM()
        queryStatement = "select metaTag.id, asset.id as assetId, tagName, value from asset join metaTag on asset.metaDataId=metaTag.metaDataId where asset.id="+id
        results = orm.executeSelect(queryStatement)
        return results


    def getAllCollections(self,limit):
        result = {}
        orm = ORM()
        if limit == -1:
            queryStatement = "select * from collection"
        else:
            queryStatement = "select * from collection LIMIT "+ limit
        results = orm.executeSelect(queryStatement)
        return results

    def getCollectionByID(self,id):
        url="http://mec402.boisestate.edu/cgi-bin/openpipe/data/folder/"
        result = {}
        orm = ORM()
        queryStatement = "SELECT collection.*, assetId FROM collection join collectionMember on collection.id=collectionMember.collectionId where collection.id="+str(int(id))
        results = orm.executeSelect(queryStatement)
        result['total']=1
        result['id']=results['data'][0]['id']
        result['name'] = results['data'][0]['name']
        result['layoutType'] = results['data'][0]['layoutType']
        result['insertTime'] = results['data'][0]['insertTime']
        result['lastModified'] = results['data'][0]['lastModified']
        result['assets']=[]
        for r in results['data']:
            result['assets'].append(url+str(r['assetId'][0]))
        return result

    def getRangeOfCollections(self,start, end):
        result = {}
        orm = ORM()
        queryStatement = "select * from collection LIMIT "+start+","+end
        results = orm.executeSelect(queryStatement)
        return result

    def getPublicAsssetsInCollection(self, collectionId, page, pageSize):
        orm = ORM()
        start = (page - 1) * pageSize
        step = pageSize
        queryStatement =  "SELECT assetId,asset.metaDataId FROM collectionMember JOIN asset ON collectionMember.assetId = asset.id WHERE scope=0 and collectionId ="+str(collectionId)+" limit "+str(start)+","+str(step)
        results = orm.executeSelect(queryStatement)
        rows=[]
        for row in results['data']:
            rowInfo = {"id": row['assetId'], "metaDataId": row['metaDataId']}
            metaDataId = row['metaDataId'][0]
            queryStatement = "select tagName,value from metaTag where metaDataId="
            if metaDataId:
                queryStatement = queryStatement+str(metaDataId)
                tags=orm.executeSelect(queryStatement)['data']
                for metaTagRow in tags:
                    rowInfo[metaTagRow['tagName'][0]] = [metaTagRow['value'][0]]
                rows.append(rowInfo)
            # rows.append(rowInfo)
        results["data"] = rows
        return results

    def getAllAssetIDs(self):
        url="http://mec402.boisestate.edu/cgi-bin/openpipe/data/asset/"
        result = []
        orm = ORM()
        queryStatement = "select id from asset"
        results = orm.executeSelect(queryStatement)
        for r in results['data']:
            result.append(url+str(r['id'][0]))
        results['data']=result
        return results

    def getAllFolderIDs(self):
        url="http://mec402.boisestate.edu/cgi-bin/openpipe/data/folder/"
        result = []
        orm = ORM()
        queryStatement = "select id from collection"
        results = orm.executeSelect(queryStatement)
        for r in results['data']:
            result.append(url+str(r['id'][0]))
        results['data']=result
        return results

    def getGUIDInfo(self,tableName,id):
        orm=ORM()
        if(tableName not in ["asset","folder"]):
            return "entity does not exist"
        elif tableName=="asset" :
            if id is not None and id!="":
                return self.getAsset(id)
            else:
                return self.getAllAssetIDs()
        elif tableName=="folder":
            if id is not None and id!="":
                return self.getCollectionByID(id)
            else:
                return self.getAllFolderIDs()
        return {"data":"bad GUID"}

