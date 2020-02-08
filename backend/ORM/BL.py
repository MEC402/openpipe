from ORM import ORM
from TO import TO


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
        queryStatement ="""SELECT assetId,metaDataId,metaTagId,metaTagName,metaTagValue,defectType FROM assetDefect join defect on assetDefect.defectId=defect.id order by assetId asc;"""
        results = orm.executeSelect(queryStatement)
        return results

vf = BL().getAssetsWithBadMetaTags()
