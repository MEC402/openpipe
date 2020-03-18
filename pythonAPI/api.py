import json
import cgi
import sys
from datetime import datetime
import sqlalchemy as db
import cgi, os
import cgitb; cgitb.enable()
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import mysql.connector
from mysql.connector import Error
import sqlalchemy as db

from ORM.BL import BL


class OpenPipePy:
    def addAsset(self, shortName, uri, idAtSource, sourceId, metaDataId, scope):
        if shortName is None or uri is None or idAtSource is None or sourceId is None or metaDataId is None or scope is None:
            return {"result": "Fail"}
        else:
            return {"result": BL().insertIntoAsset(dict["shortName"], dict["uri"], dict["idAtSource"],
                                            dict["sourceId"], dict["metaDataId"], dict["scope"])}

    def addAssetIntoCollection(self, assetId, collectionId, searchTerm):
        if assetId is None or  collectionId is None or searchTerm is None:
           return {"result": "Fail"}
        else:
             {"result": BL().insertIntoCollectionMember(dict["assetId"],dict["collectionId"],dict["searchTerm"])}

    def addCanonicalMetaTag:



    def addUserAssets: 




    def  createCollection(self,name):
      if name is None:
        return{"result": "Fail"}
      else:
        {'result':BL().insertIntoCollection(dict["name"])}

    def createMetaData(self)
          return{"result": BL().insertIntoMetaData()}


    def createMetaTags(self):
          return {insertIntoMetaTags(data)}

    def createMetaTagsBV1.0():



    def deleteCanonicalMetaTag(self, id):
      if id is None:
        return {"result":"Fail"}
      else:          
        return (deleteTag(dict["id"])

    def getAllAssets(self,p,ps,changeStart,changeEnd,type):
      if p is None:
          return "1";
      if ps is None:
          return "10";
      if changeStart is None:
          return "1900-01-01";
      if changeEnd is None:
        return "5000-01-01";

      def getAssetMetaTags(self,assetId):
        if assetID is None:
          return getAssetMetaTags(dict['assetId'])


  def getAssetMetaTags(self, assetId):
        if assetID is None:
          return ({"total": "", "data": [{"id": [""], "name": [""], "timeStamp": [""]}]})


  def getAssetsReport(self):
     return (BL().getAssetReport())

  def getAssetsWithoutImages(self):
    return (getAssetsWithoutImages())

  def getCanonicalMetaTags(self):
    return (getAllTags())

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
     return (BL().getPublicAsssetsInCollection(dict['collectionId'],int(dict["p"]), int(dict["ps"])), default=str)
          

  def updateCanonicalMetaTag(self,id):
    if id is None or name is None:
      return ({"result":"Fail"})
    else:
      return (updateTag(dict["id"],dict["name"]), default=str)
