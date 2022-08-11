#!/bin/python3

import requests
import json

from sqlalchemy import null

from MuseumsTM import MuseumsTM
from multiprocessing.pool import ThreadPool

from ImageUtil import ImageUtil
 
class HarvardArtMuseum(MuseumsTM):
 
   def __init__(self, schema):
       self.schema= schema
       self.name = "Smithsonian"
 
   def searchForAssets(self, term):
       
# -----The out is a list of 57 special artworks, and their request do not require an API key-----------------#
   
    #    url = 'https://iiif.harvardartmuseums.org/manifests/gallery/1600'
    #    response = requests.get(url=url)
    #    data1 = response.json()
    #    print(data1)

#----------------------------------------------------------------------------------------
       parameters = {'q': term, 'apikey': '6ca29b65-5793-4a72-831f-943e013def28', 'size' : 30, 'page':1}
       url = 'https://api.harvardartmuseums.org/object'
       response = requests.get(url=url, params=parameters)
       data1 = response.json()
       data11 = json.dumps(data1)
    #    print(json.dumps(data1['records']))
       
       limit = 500
       out = []
       out = out + data1['records']
       size_ = data1['info']['totalrecords']
       for offset in range(0,size_,limit):
         offset += limit
        #  print(offset)
       return out
    
    #    return data1
     
   def getMetaTagMapping(self, data): 
       temp = {
              "openpipe_canonical_id": "objectID",
              "openpipe_canonical_sourceid": "sourceID",
              "openpipe_canonical_source": "source",
              "openpipe_canonical_title": "title",
              "openpipe_canonical_artist": "artistDisplayName",
              "openpipe_canonical_date": "date",
              "openpipe_canonical_medium": "medium",
              "openpipe_canonical_physicalDimensions": "dimansions",
              "openpipe_canonical_fullImage": "fullImage",
              "openpipe_canonical_fullImageDimensions": "fullImageDimensions",
              "openpipe_canonical_largeImage": "largeImage",
              "openpipe_canonical_largeImageDimensions": "largeImageDimensions",
              "openpipe_canonical_smallImage": "smallImage",
              "openpipe_canonical_smallImageDimensions": "smallImageDimensions"
                       }  
       
       temp["openpipe_canonical_id"]=data['id'] 
       temp["openpipe_canonical_artist"]=data['people'][0]['displayname']
       temp["openpipe_canonical_date"]=data['dated']
       temp["openpipe_canonical_title"]=data['title']
       temp["openpipe_canonical_medium"]=data['medium']
       temp["openpipe_canonical_physicalDimensions"]=data['dimensions']
       if data['images']is not None:
        #    print(data['images'][0]['baseimageurl'])
           width = data['images'][0]['width']
           height = data['images'][0]['height']
           temp["openpipe_canonical_fullImageDimensions"] = str(width) + "," + str(height)
           temp["openpipe_canonical_smallImage"] = data['images'][0]['baseimageurl'] #- reused
           imageInfo = ImageUtil()
           dimentions1 = imageInfo.getPixelDimentions(temp["openpipe_canonical_smallImage"])
           temp["openpipe_canonical_smallImageDimensions"] = [str(dimentions1[0]) + "," + str(dimentions1[1])][0]
           temp["openpipe_canonical_largeImage"] = data['images'][0]['baseimageurl'] #- reused
           temp["openpipe_canonical_largeImageDimensions"] = [str(dimentions1[0]) + "," + str(dimentions1[1])][0] #- reused 
           temp["openpipe_canonical_sourceid"] = ""
           temp["openpipe_canonical_source"] = "Harvard"
       
    #    temp["openpipe_canonical_fullImage"]=data['images'][0]['baseimageurl']
       
       
        
   
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
           return {"data": [], "total": 0, "sourceName": "Harvard Art Museum"}
 
       if int(start) > total:
           start = total - 1
       if int(start) + int(step) > total:
           step = total - int(start) - 1

       assets = retrievedAssets[int(start):int(start) + int(step)]
 
       for asset in assets:
        
         results.append(self.getAssetMetaData(asset))
       
       return {"data": results,
               "total": len(results),
               "sourceName": "Harvard Art Museum"} 
 
if __name__=='__main__':
 
       sm=HarvardArtMuseum("")
       
    #    print("*************************** search ********************************")
       
    #    search=sm.searchForAssets(" cat ")
    #    print(json.dumps(search))
    
    #    print("************************** End search ***************************")
       
       print("*************************** START getData ********************************")
       
       getdata = sm.getData(q=" cat ", page=1, pageSize= 8)
       a = (getdata)
       print(a)
       
       print("*************************** END getData ********************************")
       
       



      
       
      

