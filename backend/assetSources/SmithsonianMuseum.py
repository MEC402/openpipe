#!/bin/python3
 
from turtle import width
import requests
import json

from sympy import source
from MuseumsTM import MuseumsTM
from multiprocessing.pool import ThreadPool
import formatHelp
from ImageUtil import ImageUtil
 
 
class SmithsonianMuseum(MuseumsTM):
 
   def __init__(self, schema):
       self.schema= schema
       self.name = "Smithsonian"
 
   def searchForAssets(self, term):
          
#        parameters = {'q': term, 'key': self.attributes['key'] }
#        response = requests.get(url=self.attributes['url'], params=parameters)
#        data1 = response.json()
#        return data1
      
 
       parameters = {'q': term, 'api_key': 'imQAjl1QkgYj0EiPybG1lKaz4dp0AZSauYCgPi3B'}
       url = 'https://api.si.edu/openaccess/api/v1.0/category/art_design/search'
       response = requests.get(url=url, params=parameters)
       data1 = response.json()
      
       limit = 100
       out = []
      
       out = out + data1['response']['rows']
       size_ = data1['response']['rowCount']
 
       for offset in range(0,size_,limit):

         offset += limit
  
       return out
     
   def getMetaTagMapping(self, data): 
       temp = {
              "openpipe_canonical_id": "objectID",
              "openpipe_canonical_title": "title",
              "openpipe_canonical_artist": "artistDisplayName",
              "openpipe_canonical_date": "date",
              "openpipe_canonical_medium": "medium",
              "openpipe_canonical_physicalDimensions": "dimansions",
              "openpipe_canonical_fullImage": "fullImage",
              "openpipe_canonical_source": "source",
              "openpipe_canonical_sourceid": "sourceID",
              "openpipe_canonical_fullImageDimensions": "fullImageDimensions",
              "openpipe_canonical_largeImageDimensions": "largeImageDimensions",
              "openpipe_canonical_largeImage": "largeImage",
              "openpipe_canonical_smallImage": "smallImage",
              "openpipe_canonical_smallImageDimensions": "smallImageDimensions"
              
                       }  
       
       temp["openpipe_canonical_id"]=data['id']
       temp["openpipe_canonical_title"]=data['title']
       temp["openpipe_canonical_artist"]=data['content']['freetext']['name'][0]['content']
       temp["openpipe_canonical_medium"]=data['content']['freetext']['physicalDescription'][0]['content']
       width = data['content']['descriptiveNonRepeating']['online_media']['media'][0]['resources'][1]['width']
       height = data['content']['descriptiveNonRepeating']['online_media']['media'][0]['resources'][1]['width']
       temp["openpipe_canonical_physicalDimensions"]= str(width) + "," + str(height)
       end_date = ((data['content']['freetext']['date'][0]['content']).upper()).replace('A','E')
       if end_date is not None:
          temp["openpipe_canonical_date"]= [str(end_date) + " " + "JAN" + " " + "01" + " " + "00:00:00"][0]
       temp["openpipe_canonical_source"] = "Smithsonian"
       temp["openpipe_canonical_sourceid"] = "5"
       temp["openpipe_canonical_fullImage"]=data['content']['descriptiveNonRepeating']['online_media']['media'][0]['thumbnail']
       imageInfo = ImageUtil()
       dimentions = imageInfo.getPixelDimentions(temp["openpipe_canonical_fullImage"])
        
       temp["openpipe_canonical_fullImageDimensions"] = [str(dimentions[0]) + "," + str(dimentions[1])][0]
       temp["openpipe_canonical_largeImageDimensions"] = [str(dimentions[0]) + "," + str(dimentions[1])][0]
       temp["openpipe_canonical_smallImageDimensions"] = [str(dimentions[0]) + "," + str(dimentions[1])][0]
       temp["openpipe_canonical_largeImage"] = data['content']['descriptiveNonRepeating']['online_media']['media'][0]['thumbnail'] #-reused
       temp["openpipe_canonical_smallImage"] = data['content']['descriptiveNonRepeating']['online_media']['media'][0]['thumbnail'] #-reused
       
       
       return temp
      
   def getAssetMetaData(self, assetId):
           
       metaData = self.getMetaTagMapping(assetId)
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
 
       for asset in assets:
        
         results.append(self.getAssetMetaData(asset))
       
       return {"data": results,
               "total": len(results),
               "sourceName": "Smithsonian Museum"}
 
 
if __name__=='__main__':
 
       
 
       sm=SmithsonianMuseum("")
       
       # print("*************************** search ********************************")
       
       # search=sm.searchForAssets(" cat ")
       # print(search)
       # print("************************** End search ***************************")
       
       print("*************************** START getData ********************************")
       
       getdata = sm.getData(q=" cat ", page=1, pageSize= 8)
       a = json.dumps(getdata)
       print(a)
       
       print("*************************** END getData ********************************")
       
       



      
       
      

