#!/bin/python3
 
import requests
import json
from MuseumsTM import MuseumsTM
from multiprocessing.pool import ThreadPool
import formatHelp
 
 
class SmithsonianMuseum(MuseumsTM):
 
   def __init__(self, schema):
       self.schema= schema
       self.name = "Smithsonian"
       self.canonmap = {
              "openpipe_canonical_id": "objectID",
        #       "openpipe_canonical_largeImage": "primaryImage",
        #       "openpipe_canonical_smallImage": "primaryImageSmall",
              "openpipe_canonical_title": "title",
              "openpipe_canonical_artist": "artistDisplayName",
              "openpipe_canonical_date": "date",
        #       "openpipe_canonical_culture":  "culture",
        #       "openpipe_canonical_classification": "classification",
        #       "openpipe_canonical_nation":  "country",
        #       "openpipe_canonical_city":  "city",
        #       "openpipe_canonical_tags":  "tags",
                # "openpipe_canonical_tags":  "tags",
              
              "openpipe_canonical_medium": "medium",
              "openpipe_canonical_physicalDimensions": "dimansions"
              
                       }
#        self.fullcanonmap = {
#                "id": "openpipe_canonical_id",
#                "title": "openpipe_canonical_title",
#                "creators": "openpipe_canonical_artist",
#                "culture": "openpipe_canonical_culture"
#                        }
#        self.canonmap = {
#                "title": "openpipe_canonical_title",
#                "creators": "openpipe_canonical_artist",
#                "culture": "openpipe_canonical_culture",
#                "medium": "openpipe_canonical_medium"
#                       }
 
 
   def searchForAssets(self, term):
          
#        parameters = {'q': term, 'key': self.attributes['key'] }
#        response = requests.get(url=self.attributes['url'], params=parameters)
#        data1 = response.json()
#        return data1
      
 
       parameters = {'q': term, 'api_key': 'imQAjl1QkgYj0EiPybG1lKaz4dp0AZSauYCgPi3B', 'rows' : 5}
       url = 'https://api.si.edu/openaccess/api/v1.0/category/art_design/search'
       response = requests.get(url=url, params=parameters)
       data1 = response.json()
      
       limit = 100
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
#        print(out)
  
       return out
     
   def getMetaTagMapping(self, data):   
       self.canonmap["openpipe_canonical_id"]=data['id']
       self.canonmap["openpipe_canonical_title"]=data['title']
       self.canonmap["openpipe_canonical_artist"]=data['content']['freetext']['name'][0]['content']
       self.canonmap["openpipe_canonical_date"]=data['content']['freetext']['date'][0]['content']
       self.canonmap["openpipe_canonical_medium"]=data['content']['freetext']['setName'][1]['content']
       self.canonmap["openpipe_canonical_fullImage"]=data['content']['descriptiveNonRepeating']['online_media']['media'][0]['thumbnail']
       self.canonmap["openpipe_canonical_physicalDimensions"]=data['content']['descriptiveNonRepeating']['online_media']['media'][0]['resources'][1]['dimensions']
       return self.canonmap
      
   def getAssetMetaData(self, assetId):
       assetId = str(assetId)
       parameters = {'q': " cat ", 'api_key': 'imQAjl1QkgYj0EiPybG1lKaz4dp0AZSauYCgPi3B'}
       url = 'https://api.si.edu/openaccess/api/v1.0/category/art_design/search'
       response = requests.get(url=url, params=parameters)
       data = response.json()
       metaData = self.getMetaTagMapping(data)
       return metaData
 
   def getData(self, q, page, pageSize):
       results = []
       retrievedAssets = self.searchForAssets(q)
#        print("************PRINTING RETRIVED ASSETS*************")
#        print(retrievedAssets)
#        print(len(retrievedAssets)) 
#        print("************END of RETRIVED ASSETS*************")
        
       start = (page - 1) * pageSize
       step = pageSize
       total = len(retrievedAssets)
       if total == 0:
           return {"data": [], "total": 0, "sourceName": "Smithsonian Museum"}
 
       if int(start) > total:
           start = total - 1
       if int(start) + int(step) > total:
           step = total - int(start) - 1
       print(start)
       print(step)
       assets = retrievedAssets[int(start):int(start) + int(step)]
       print(assets)
 
       pool = ThreadPool(len(assets))
       for asset in assets:
         if asset != None:
           results.append(pool.apply_async(self.getMetaTagMapping, args=[asset]))
       
       pool.close()
       pool.join()
       results = [r.get() for r in results]
       return {"data": results,
               "total": len(results),
               "sourceName": "Smithsonian Museum"}
 
 
if __name__=='__main__':
 
       print("*************************** search ********************************")
 
       sm=SmithsonianMuseum("")
      
       search=sm.searchForAssets(" cat ")
#        print(search)
      
       getdata = sm.getData(q=" cat ", page=1, pageSize= 8)
       a = json.dumps(getdata)
       print(a)
      
       print("************************** End search ***************************")
      

