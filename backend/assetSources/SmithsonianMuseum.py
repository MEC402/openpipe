#!/bin/python3

import requests
from MuseumsTM import MuseumsTM
from multiprocessing.pool import ThreadPool
import formatHelp


class SmithsonianMuseum(MuseumsTM):

    def __init__(self, schema):
        self.schema= schema
        self.name = "Smithsonian"
        self.canonmap = {
               "openpipe_canonical_id": "objectID",
               "openpipe_canonical_largeImage": "primaryImage",
               "openpipe_canonical_smallImage": "primaryImageSmall",
               "openpipe_canonical_title": "title",
               "openpipe_canonical_artist": "artistDisplayName",
               "openpipe_canonical_culture":  "culture",
               "openpipe_canonical_classification": "classification",
               "openpipe_canonical_nation":  "country",
               "openpipe_canonical_city":  "city",
               "openpipe_canonical_tags":  "tags"
                        }
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
        #                }


    def searchForAssets(self, term):
            
        # parameters = {'q': term, 'key': self.attributes['key'] }
        # response = requests.get(url=self.attributes['url'], params=parameters)
        # data = response.json()
        # return data
        

        parameters = {'q': term, 'api_key': 'imQAjl1QkgYj0EiPybG1lKaz4dp0AZSauYCgPi3B', 'rows' : 2}
        url = 'https://api.si.edu/openaccess/api/v1.0/search'
        response = requests.get(url=url, params=parameters)
        data1 = response.json()
        
        limit = 10000
        out = []
        
        out = out + data1['response']['rows']
        size_ = data1['response']['rowCount']
       

        print(size_)

        for offset in range(limit,size_,limit):
          print(offset)

          parameters = {'q': term, 'api_key': 'imQAjl1QkgYj0EiPybG1lKaz4dp0AZSauYCgPi3B', 'rows':limit,'start':0}
          response = requests.get(url=url, params=parameters)
          data = response.json()
          out = out + data['response']['rows']

          offset += limit
        #   print(len(data['response']['rows']))
        #   print(len(out))
        # print(data)
        # return {data1}
        print(out[:5])
    
        # return out
        
    def getMetaTagMapping(self, data):    
        self.canonmap["openpipe_canonical_id"]=data['response']['rows']['id']
        self.canonmap["openpipe_canonical_title"]=data['response']['rows']['title']
        print(data['response']['rows'])
        return self.canonmap
        
    def getAssetMetaData(self, assetId):
        assetId = str(assetId)
        parameters = {'q': " cat ", 'api_key': 'imQAjl1QkgYj0EiPybG1lKaz4dp0AZSauYCgPi3B'}
        url = 'https://api.si.edu/openaccess/api/v1.0/search'
        response = requests.get(url=url, params=parameters)
        data = response.json()
        metaData = self.getMetaTagMapping(data)
        return metaData

def getData(self, q, page, pageSize):
        results = []
        retrievedAssets = self.searchForAssets(q)

        start = (page - 1) * pageSize
        step = pageSize
        total = len(retrievedAssets)
        if total == 0:
            return {"data": [], "total": 0, "sourceName": "Smithsonian Museum"}

        if int(start) > total:
            start = total - 1
        if int(start) + int(step) > total:
            step = total - int(start) - 1

        assets = retrievedAssets[int(start):int(start) + int(step)]

        print(assets)

        pool = ThreadPool(len(assets))
        for asset in assets:
          if asset != None:
            results.append(pool.apply_async(self.getMetaTagMapping, args=[asset]))
        #     results.append(pool.apply_async(self.getAssetMetaData, args=[asset["entityId"]]))
        pool.close()
        pool.join()
        results = [r.get() for r in results]
        return {"data": results,
                "total": 0,
                "Smithsonian": "Paris Museum"}


if __name__=='__main__':

        print("*************************** search ********************************")

        sm=SmithsonianMuseum("") 
        
        # search=sm.searchForAssets(" cat ")
        # print(search)

        # map = sm.getMetaTagMapping(data['response']['rows'])
        # print(map)
        
        getdata = sm.getData(q=" cat ", page=1, pageSize= 20) 
        print(getdata)
        
        print("End search")
        