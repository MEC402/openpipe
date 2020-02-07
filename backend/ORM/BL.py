from ORM import ORM
from TO import TO


class BL:
    tables = TO().getClasses()

    def getAssetsWithoutImages(self):
        orm = ORM()
        queryStatement = "select metaTag.id as metaTagID, metaTag.metaDataId,tagName,value, asset.id as assetID, shortName, IdAtSource, asset.sourceId " \
                         "from metaTag join asset on metaTag.metaDataId=asset.metaDataId " \
                         "where (tagName='openpipe_canonical_largeImage' and (value is null or value='' or value='http://mec402.boisestate.edu/assets/largeImage.jpg')) " \
                         "or (tagName='openpipe_canonical_smallImage' and (value is null or value='' or value='http://mec402.boisestate.edu/assets/smallImage.jpg'))"
        results = orm.executeSelect(queryStatement)
        fieldNames = results[0]
        rows = results[1]
        jsonRes = {'total': len(rows), 'data': []}
        for r in rows:
            row = {}
            for i in range(len(fieldNames)):
                row[fieldNames[i]] = r[i]
            jsonRes['data'].append(row)
        return jsonRes

