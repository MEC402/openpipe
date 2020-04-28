from openpipeAPI.ORM.BL import BL


# TODO: GetFolderLayout -> create the BL function
# TODO: Better Error reporting in Json
# TODO: Code Review
# TODO: Update/add/delete Canonical MetaTAg in BL
# TODO: Add user assets

class OpenPipePy:

    # **********************************************************************************************
    # ************************************** Assets ************************************************
    # **********************************************************************************************

    def addAsset(self, shortName, uri, idAtSource, sourceId, metaDataId, scope):
        if shortName is None or uri is None or idAtSource is None or sourceId is None or metaDataId is None or scope is None:
            return {"result": "Fail"}
        else:
            return {"result": BL().insertIntoAsset(shortName, uri, idAtSource, sourceId, metaDataId, scope)}

    def getAllAssets(self, page, pageSize, changeStart, changeEnd, type):
        return BL().getAllAssets(int(page), int(pageSize), changeStart, changeEnd)

    # **********************************************************************************************
    # ************************************** Folder Member *****************************************
    # **********************************************************************************************

    def addAssetToFolder(self, folderId, assetId, searchTerm):
        if assetId is None or folderId is None:
            return {"result": "Fail"}
        else:
            return {"result": BL().insertIntoCollectionMember(assetId, folderId, searchTerm)}

    def deleteFolderMember(self, folderId, assetId):
        if assetId is None or folderId is None:
            return {"result": "Fail"}
        else:
            return BL().deleteFolderMember(folderId, assetId)

    # **********************************************************************************************
    # ************************************** Folders ***********************************************
    # **********************************************************************************************

    def addFolder(self, name):
        if name is not None:
            return {"result": BL().insertIntoCollection(name)}
        else:
            return {"result": "Fail"}

    def updateFolder(self, folderId, newName, newImage):
        if folderId is None:
            return {"total": "", "data": [{}], "error": "Bad Folder ID"}
        else:
            return BL().updateFolder(folderId, newName, newImage)

    def deleteFolder(self, folderId):
        return BL().deleteFolder(folderId)

    def getFolder(self, folderId):
        if folderId <= 0:
            return {"total": [""], "data": [{"id": [""], "name": [""], "timeStamp": [""]}]}
        else:
            return BL().getCollectionByID(folderId)

    def getAllFolders(self, limit):
        return BL().getAllCollections(limit)

    def getPublicAssetsInFolder(self, folderId, page, pageSize):
        if folderId is None:
            return {"total": "", "data": [{}], "error": "Bad Folder ID"}
        else:
            return BL().getPublicAssetsInCollection(folderId, page, pageSize)

    # **********************************************************************************************
    # ************************************** MetaTags **********************************************
    # **********************************************************************************************

    def addMetaTag(self, metaDataId, tagName, value):
        if metaDataId is not None and tagName is not None and value is not None:
            return {"result": BL().insertMetaTag(metaDataId, tagName, value)}
        else:
            return {"result": "Fail"}

    def addBatchMetaTags(self, jsonData):
        return BL().insertIntoMetaTags(jsonData)

    def deleteMetaTag(self, metaDataId, tagName, value):
        if metaDataId is not None and tagName is not None and value is not None:
            return BL().deleteMetaTag(metaDataId, tagName, value)
        else:
            return {"result": "Fail"}

    # **********************************************************************************************
    # ********************************* CanonicalMetaTag *******************************************
    # **********************************************************************************************

    def updateCanonicalMetaTag(self, tagId, newName, newDefaultValue):
        return

    def getCanonicalMetaTags(self):
        return BL().getCanonicalTags()

    # **********************************************************************************************
    # ************************************** MetaData **********************************************
    # **********************************************************************************************

    def addMetaData(self):
        return {"result": BL().insertIntoMetaData()}

    # **********************************************************************************************
    # **************************************** GUID ************************************************
    # **********************************************************************************************

    def guid(self, guidRelativePath):
        guids = guidRelativePath.split("/")
        if len(guids) < 2:
            guids[1] = ""
        return BL().getGUIDInfo(guids[0], guids[1])
