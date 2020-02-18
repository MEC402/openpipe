from ORM import ORM
from TO import TO
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
                queryStatement = """select metaTag.id as metaTagID, metaTag.tagName, metaTag.value from  metaTag where metaDataId=""" + str(asset["metaDataId"])
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
        queryStatement ="""SELECT assetId,assetDefect.metaDataId,metaTagId,metaTagName,metaTagValue,defectType, asset.shortName as assetName, source.sourceName FROM assetDefect join defect on assetDefect.defectId=defect.id join asset on assetDefect.assetId=asset.id join source on asset.sourceId=source.id order by assetId asc;"""
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

BL().getAssetsWithFaultyImageLink()