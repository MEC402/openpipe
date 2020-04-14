import json


from ORM.BL import BL


class OpenPipePy:

   # **********************************************************************************************
    # ************************************** Assets ************************************************
    # **********************************************************************************************

    def addAsset(self, shortName, uri, idAtSource, sourceId, metaDataId, scope):
        if shortName is None or uri is None or idAtSource is None or sourceId is None or metaDataId is None or scope is None:
            return {"result": "Fail"}
        else:
            return {"result": BL().insertIntoAsset(shortName, uri, idAtSource,sourceId, metaDataId, scope)}


    def getAllAssets(self,p,ps,changeStart,changeEnd,type):
        return BL().getAllAssets(int(dict["p"]), int(dict["ps"]), dict['changeStart'], dict['changeEnd'])

    
    def addAssetIntoCollection(self, assetId, collectionId, searchTerm):
        if assetId is None or  collectionId is None or searchTerm is None:
           return {"result": "Fail"}
        else:
             return {"result": BL().insertIntoCollectionMember(dict["assetId"],dict["collectionId"],dict["searchTerm"])}    
    def addUserAssets(self,shortName, uri, idAtSource, sourceId, metaDataId, scope):
      return (BL().insertIntoImages(shortName, fileName, uri))

    def getAssetsReport(self):
      return (BL().getAssetReport())

    def getAssetsWithoutImages(self):
      return (BL().getAssetsWithoutImages())

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

    def deleteFolder(self,collectionId):
      if collectionId is None:
        return {"result": "Fail"}
      else:
        return(BL().deleteFolder(collectionId))


def updateFolder(self,collectionId,newName,newImage):
    if collectionId is None or newName is None or newImage is None:
        return {"result": "Fail"}
    else:
        return (BL().updateFolder(dict["collectionId"], dict["newName"], dict["newImage"]))

   # **********************************************************************************************
    # ************************************** MetaTag ************************************************
    # **********************************************************************************************

  def addCanonicalMetaTag(self, name):
	    if name is None:
		     return {"result": "Fail"}

	  else:
		    return {"result":insertCanonicalMetaTag(dict["name"])

  def addMetaTag(self, metaDataId, tagName, value):
    if metaDataId is None or tagName is None or value is None:
        return({"result":"Fail"}))

    else:
        return (BL().insertMetaTag(metaDataId,tagName,value))

 def createMetaData(self)
          return{"result": BL().insertIntoMetaData()}

def deleteCanonicalMetaTag(self, id):
      if id is None:
        return {"result":"Fail"}
      else:          
        return (deleteTag(dict["id"])

  def deleteMetaTag(self,metaDataId,tagName,value):
    if metaDataId is None or tagName is None or value is None:
       return {"result":"Fail"}
    else:          
        return (BL().deleteMetaTag(metaDataId,tagName,value))

 def getAssetMetaTags(self,assetId):
        if assetID is None:
          return BL().getAssetMetaTags(dict['assetId'])

  def getCanonicalMetaTags(self):
    return (getAllTags())

  def updateMetaTag(self, metaDataId, oldTagName,oldValue,newTagName,newValue):
      if metaDataId is None or oldTagName is None or oldValue is None or newTagName is None or newValue is None:
           return {"result":"Fail"}
      else:  
          return BL().updateMetaTag(dict["metaDataId"],dict["oldTagName"],dict["oldValue"],dict["newTagName"],dict["newValue"])}))


   def updateCanonicalMetaTag(self,id):
    if id is None or name is None:
      return ({"result":"Fail"})
    else:
      return (updateTag(dict["id"],dict["name"]))
        
   # **********************************************************************************************
    # ************************************** Collection ************************************************
    # **********************************************************************************************

    def  createCollection(self,name):
      if name is None:
        return{"result": "Fail"}
      else:
       return {'result':BL().insertIntoCollection(dict["name"])}



 def getCollections(self, start, end):
      if start is  and end is:
        return (BL().getRangeOfCollections(dict["start"],dict["end"])
      else: 
        if collectionId is None:
          return ({"total": [""], "data": [{"id": [""], "name": [""], "timeStamp": [""]}]})
        else:   
           if id == -1:
             return {"total": [""], "data": [{"id": [""], "name": [""], "timeStamp": [""]}]}
           elif id == "all" :
              if limit in :
                return(BL().getAllCollections(dict["limit"]))
              else:
                return(BL().getAllCollections(-1))
            else:
             return(BL().getCollectionByID(id))




  def getPublicAssetsInCollection(self, p,ps,collectionId):
    if p is None:
      return "1";
    if ps is None:
      return "10";
    if collectionId is None:
      return ({"total": "-1", "data": [{}]})
    else:
     return (BL().getPublicAsssetsInCollection(dict['collectionId'],int(dict["p"]), int(dict["ps"])))
          

 