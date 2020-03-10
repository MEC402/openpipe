from ORM.BL import BL


class OpenPipePy:
    def addAsset(self, shortName, uri, idAtSource, sourceId, metaDataId, scope):
        if shortName is None or uri is None or idAtSource is None or sourceId is None or metaDataId is None or scope is None:
            return {"result": "Fail"}
        else:
            return {"result": BL().insertIntoAsset(dict["shortName"], dict["uri"], dict["idAtSource"],
                                            dict["sourceId"], dict["metaDataId"], dict["scope"])}
