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


class ParisMuseum(MuseumsTM):

    def __init__(self, schema):
        self.schema= schema
        self.name = "Paris"
        self.canonmap = {
               "openpipe_canonical_id": "objectID",
               "openpipe_canonical_largeImage": "primaryImage",
               "openpipe_canonical_smallImage": "primaryImageSmall",
               "openpipe_canonical_title": "title", 
              # "openpipe_canonical_date":  "date",
               "openpipe_canonical_artist": "artistDisplayName",
              #  "openpipe_canonical_culture":  "culture",
              #  "openpipe_canonical_classification": "classification",
               "openpipe_canonical_nation":  "country",
               "openpipe_canonical_city":  "city",
               "openpipe_canonical_tags":  "tags",

              #  "openpipe_canonical_fullImage": "fullImage",
              #  "openpipe_canonical_firstDate":  "firstDate",
               "openpipe_canonical_lastDate": "endDate"
                       }
# ...................................................
        # self.fullcanonmap = {
        #         "id": "openpipe_canonical_id",
        #         "title": "openpipe_canonical_title",
        #         "creators": "openpipe_canonical_artist",
        #         "culture": "openpipe_canonical_culture"
        #                 }
        # self.canonmap = {
        #         "title": "openpipe_canonical_title",
        #         "creators": "openpipe_canonical_artist",
        #         "culture": "openpipe_canonical_culture",
        #         "medium": "openpipe_canonical_medium"
        #                 }


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
              "openpipe_canonical_physicalDimensions": "dimansions"
              
                       }  
        temp["openpipe_canonical_id"]=data["entityUuid"]
        temp["openpipe_canonical_title"]=data["title"]
        end_date = data["fieldDateProduction"]["endYear"]
        if end_date is not None:
          temp["openpipe_canonical_date"] = "CE" + str(end_date) + " " + "JAN" + " " + "01" + " " + "00:00:00"
        else:
          temp["openpipe_canonical_date"]=""
        temp["openpipe_canonical_artist"]=data["fieldOeuvreAuteurs"][0]["entity"]["fieldAuteurAuteur"]["entity"]["name"]
        if "fieldVisuels" in data and len(data["fieldVisuels"])>0:
          if data["fieldVisuels"][0]["entity"]["vignette"] != None:
            temp["openpipe_canonical_fullImage"] = data["fieldVisuels"][0]["entity"]["vignette"]
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


  

    

   