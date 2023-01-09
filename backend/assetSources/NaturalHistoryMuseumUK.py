#!/bin/python3
 
import requests
import json
from MuseumsTM import MuseumsTM
from multiprocessing.pool import ThreadPool
import formatHelp
 
 
class NaturalHistoryMuseumUK(MuseumsTM):
 
   def __init__(self, schema):
       self.schema= schema
       self.name = "NaturalHistoryUK"
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
      
 
       parameters = {'q': term}
       url = 'http://demo.ckan.org/api/3/action/package_search'
       response = requests.post(url=url, params=parameters)
       data1 = response.json()
       print(data1)
 
 
if __name__=='__main__':
 
       print("*************************** start search ********************************")
 
       nhm = NaturalHistoryMuseumUK("")
      
       search = nhm.searchForAssets("cat")
       print(search)
       
       print("************************** End search ***************************")
    #    getdata = sm.getData(q=" cat ", page=1, pageSize= 8)
    #    a = json.dumps(getdata)
    #    print(a)
      
       
      

