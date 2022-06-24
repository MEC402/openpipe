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

#---------- List of museum-----------------------------------------
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
        variables = {'limit':limit,'offset': (pageNumber - 1) * limit} #
        # print(body)
        response = requests.post(url=url, headers=header, json={"query":body, 'variables':variables})
        data1 = response.json()
        # print(data1)
        out = out + data1['data']['nodeQuery']['entities']
        size_ = data1['data']['nodeQuery']['count']
        print(size_)

        # for offset in range(0,size_,limit):
        #   # print(offset)

        #   variables = {'limit':limit,'offset':offset}
        #   response = requests.post(url=url, headers=header, json={"query":body, 'variables':variables})
        #   print(response.text)
        #   data = response.json()
        #   #out.append(data)
        #   out= out + data['data']['nodeQuery']['entities']

        #   offset += limit
        #   print(len(data['data']['nodeQuery']['entities']))
        #   print(len(out))
          # print(data)
        #return {data1}
        # print(out[:10])
        
    
        return out
        

    def getMetaTagMapping(self, data):
        print(data)
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

        # start_date = data["fieldDateProduction"]["startYear"]
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
        #*************** Note: 
        # The assetId is a dictionary here that contains the whole asset info here not just the id   
        # the assetId name has not been change so it follows the parent class format
        # TODO: Fix the name later 
        
        metaData = self.getMetaTagMapping(assetId)
        return metaData

    def getData(self, q, page, pageSize):
        results = []
        retrievedAssets = self.searchForAssets(q, pageSize = pageSize, pageNumber = page)
        print("************PRINTING RETRIVED ASSETS*************")
        # print(retrievedAssets)
        print("************END of RETRIVED ASSETS*************")
    # print(json.dumps({"root":out[:3]}))
        # test_out = pm.getMetaTagMapping(out[2]) 
        # print("Test Mapping")
        # print(test_out)

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
        # print(assets)
        # print(assets)


        for asset in assets:
        #  print(asset["title"])
          if asset != None:
            results.append(self.getAssetMetaData(asset))
        print(results)
        return {"data": results,
                "total": len(results),
                "sourceName": "Paris Museum"}


if __name__=='__main__':

    print("start of search")
    pm=ParisMuseum("")
    # d=pm.searchForAssets(" chat ")
    # print(d)
    # print(len(d["data"]["nodeQuery"]["entities"]))

    # # for dd in d["data"]["nodeQuery"]["entities"]:
    # #     print(dd)

    #################################...........................
    # a = pm.getData(" chat ",1,100).............................................
    # print(json.dumps(a)).......................................................
    m = pm.getData(q="chat", page=1, pageSize= 20)
    print("*************************** search ********************************") 
    a = json.dumps(m)
    print(a)
  

    

    print("End search") 