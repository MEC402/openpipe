#!/bin/python3

from cgi import print_arguments
from email import header
from email.quoprimime import body_check
from html import entities
import json
import queryBody
import re
from wsgiref import headers
import requests
from MuseumsTM import MuseumsTM
from multiprocessing.pool import ThreadPool
import formatHelp
from ImageUtil import ImageUtil


class ParisMuseum(MuseumsTM):

    def __init__(self, schema):
        self.schema= schema
        self.name = "Paris"
        
    def searchForAssets(self, term, pageSize, pageNumber):
        
        url =  "https://apicollections.parismusees.paris.fr/graphql"
        header = {
            "Content-Type": "application/json",
            "auth-token": "323ac194-f611-4583-9620-b5e9351f56ad"
        }
        
        prefixbody = '''
  query($limit: Int!,$offset: Int!) {
  nodeQuery(limit: $limit, offset: $offset, filter: {conditions: [
    {field: "type", value: "oeuvre"}
    {field: "field_oeuvre_types_objet.entity.field_lref_adlib", value: "4493"}
  ]}) {
    count
   '''

        body = prefixbody + queryBody.tailbody

        limit = pageSize
        out = []
        variables = {'limit':limit,'offset': (pageNumber - 1) * limit} 
        response = requests.post(url=url, headers=header, json={"query":body, 'variables':variables})
        data1 = response.json()
        out = out + data1['data']['nodeQuery']['entities']
        size_ = data1['data']['nodeQuery']['count']
        
        return out
        

    def getMetaTagMapping(self, data):
       
        temp = {
              "openpipe_canonical_id": "objectID",
              "openpipe_canonical_title": "title",
              "openpipe_canonical_artist": "artistDisplayName",
              "openpipe_canonical_date": "date",
              "openpipe_canonical_medium": "medium",
              "openpipe_canonical_physicalDimensions": "dimansions",
              "openpipe_canonical_source": "source",
              "openpipe_canonical_sourceid": "sourceID",
              "openpipe_canonical_fullImageDimensions": "fullImageDimensions",
              "openpipe_canonical_largeImageDimensions": "largeImageDimensions",
              "openpipe_canonical_largeImage": "largeImage",
              "openpipe_canonical_smallImage": "smallImage",
              "openpipe_canonical_smallImageDimensions": "smallImageDimensions"
                       } 
        temp["openpipe_canonical_source"] = "Paris"
        temp["openpipe_canonical_id"]=data["entityUuid"]
        temp["openpipe_canonical_title"]=data["title"]
        end_date = data["fieldDateProduction"]["endYear"]
        if end_date is not None:
          temp["openpipe_canonical_date"] = "CE" + " " + str(end_date) + " " + "JAN" + " " + "01" + " " + "00:00:00"
        else:
          temp["openpipe_canonical_date"]=""
        temp["openpipe_canonical_artist"]=data["fieldOeuvreAuteurs"][0]["entity"]["fieldAuteurAuteur"]["entity"]["name"]
        if "fieldVisuels" in data and len(data["fieldVisuels"])>0:
          if data["fieldVisuels"][0]["entity"]["vignette"] != None:
            temp["openpipe_canonical_fullImage"] = data["fieldVisuels"][0]["entity"]["vignette"] 
            temp["openpipe_canonical_largeImage"] = data["fieldVisuels"][0]["entity"]["vignette"]
            temp["openpipe_canonical_smallImage"] = data["fieldVisuels"][0]["entity"]["vignette"]

        # temp["openpipe_canonical_physicalDimensions___"]=data["fieldOeuvreDimensions"][0]["entity"]["fieldDimensionValeur"] #... revisit, Dimension is not accessible
        
        # print(data["fieldOeuvreDimensions"][0])
        
        # temp["openpipe_canonical_medium"] = data["fieldMateriauxTechnique"][0]["entity"]["name"] #... revist the french vs english
        # medium = data["fieldMaterialsTechnical"][0]["entity"]["name"]
        # if medium is not None:
        #   temp["openpipe_canonical_medium"] = data["fieldMaterialsTechnical"][0]["entity"]["name"]
        # else:
        #   temp["openpipe_canonical_medium"] = ""
        
        temp["openpipe_canonical_sourceid"] = "4"
        temp["openpipe_canonical_physicalDimensions"] = (str(21.0) + "," + str(29.7) + "," + str(1.0))
        imageInfo = ImageUtil()
        dimentions = imageInfo.getPixelDimentions(temp["openpipe_canonical_fullImage"])
        temp["openpipe_canonical_fullImageDimensions"] = [str(dimentions[0]) + "," + str(dimentions[1])][0] 
        temp["openpipe_canonical_smallImageDimensions"] = [str(dimentions[0]) + "," + str(dimentions[1])][0] 
        temp["openpipe_canonical_largeImageDimensions"] = [str(dimentions[0]) + "," + str(dimentions[1])][0]
        
        return temp

    def getAssetMetaData(self, assetId):
        
        metaData = self.getMetaTagMapping(assetId)
        return metaData

    def getData(self, q, page, pageSize):
        results = []
        retrievedAssets = self.searchForAssets(q, pageSize = pageSize, pageNumber = page)

        start = (page - 1) * pageSize
        step = pageSize
        total = len(retrievedAssets)
        if total == 0:
            return {"data": [], "total": 0, "sourceName": "Paris Museum"}

        if int(start) > total:
            start = total - 1
        if int(start) + int(step) > total:
            step = total - int(start) - 1

        assets = retrievedAssets[int(start):int(start) + int(step)]
    
        for asset in assets:
       
          if asset != None:
            results.append(self.getAssetMetaData(asset))
       
        return {"data": results,
                "total": len(results),
                "sourceName": "Paris Museum"}

if __name__=='__main__':
 
      
 
       pm=ParisMuseum("")
       
      #  print("*************************** search ********************************")
      #  search=pm.searchForAssets(" cat ", pageSize = 1, pageNumber = 8)
      #  print(search)
      #  print("************************** End search ***************************")
       
       print("*************************** START getData ********************************")
       
       getdata = pm.getData(q=" cat ", page=1, pageSize= 5)
       a = json.dumps(getdata)
       print(a)
       
       print("*************************** START getData ********************************")


  

    

   