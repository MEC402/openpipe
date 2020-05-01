#!/bin/python3

from multiprocessing.pool import ThreadPool
from MuseumsTM import MuseumsTM
import json
import requests

from ImageUtil import ImageUtil

# backup of URL
#    url = "https://api.europeana.eu/api/v2/"

def fA(aitem):
   if isinstance(aitem,list):
      return aitem[0]
   else:
      return aitem

class EuropeMuseum(MuseumsTM):

    def searchEuropeForAssets(self, term):
        serviceName = "search.json"
        params = {'query': term, 'wskey': self.attributes['key'] , "rows": 100}
        if "dataprovider" in self.attributes:
           params["DATA_PROVIDER"] = self.attributes['dataprovider']
        response = requests.get(url=self.attributes['url'] + serviceName, params=params)
        data = response.json()
        return data


    def getMetaTagMapping(self, data):
        response = {}
#        response = self.schema.copy()
        response["openpipe_canonical_source"] = self.attributes["source"]
        response["openpipe_canonical_id"] = [data["id"]]
        if "edmIsShownAt" in data:
          response["openpipe_canonical_largeImage"] = [data["edmIsShownAt"]]
#        imageInfo = ImageUtil()
#        dimentions = imageInfo.getPixelDimentions(response["openpipe_canonical_largeImage"][0])
#        response["openpipe_canonical_largeImageDimensions"] = [str(dimentions[0]) + "," + str(dimentions[1])]
#        response["openpipe_canonical_smallImage"] = [data["primaryImageSmall"]]
#        dimentions = imageInfo.getPixelDimentions(response["openpipe_canonical_smallImage"][0])
#        response["openpipe_canonical_smallImageDimensions"] = [str(dimentions[0]) + "," + str(dimentions[1])]

        if "title" in data:
          response["openpipe_canonical_title"] = [fA(data["title"])]
        if "dcCreator" in data:
          response["openpipe_canonical_artist"] = [fA(data["dcCreator"])]

#        response["openpipe_canonical_culture"] = [data["culture"]]
#      response["openpipe_canonical_classification"] = [data["classification"]]
        # self.schema.genre.push(data["city"])
        # self.schema.medium.push(data["city"])
#        response["openpipe_canonical_nation"] = [data["country"]]
#        response["openpipe_canonical_city"] = [data["city"]]
#        if 'tags' in data.keys() and data["tags"] is not None:
#            if len(data["tags"]) > 0:
#                response["openpipe_canonical_tags"] = data["tags"]
#        era = "CE"
#        year1 = abs(int(data["objectBeginDate"]))
#        year2 = abs(int(data["objectEndDate"]))
#        if "B.C." in data["objectDate"]:
#            era = "BC"
#        response["openpipe_canonical_firstDate"] = [
#            era + " " + str(year1) + " " + "JAN" + " " + "01" + " " + "00:00:00"]
#        response["openpipe_canonical_lastDate"] = [era + " " + str(year2) + " " + "JAN" + " " + "01" + " " + "00:00:00"]
#        response["openpipe_canonical_date"] = [response["openpipe_canonical_firstDate"][0],
#                                               response["openpipe_canonical_lastDate"][0]]
#        response.update(data)
        return response

    def getAssetMetaData(self, aitem, assetOriginalID):
        data = aitem
        metaData = self.getMetaTagMapping(data)
        return metaData

    def getData(self, q, page, pageSize):
        results = []
        retrievedAssets = self.searchEuropeForAssets(q)
        if "error" in retrievedAssets:
           return {"data": [], "total": 0, "sourceName": "Europe", "error": "failed"}

        if retrievedAssets['itemsCount'] == 0:
            return {"data": [], "total": 0, "sourceName": "Europe"}

        start = (page - 1) * pageSize
        step = pageSize

        if int(start) > retrievedAssets['itemsCount']:
            start = retrievedAssets['itemsCount'] - 1
        if int(start) + int(step) > retrievedAssets['itemsCount']:
            step = retrievedAssets['itemsCount'] - int(start) - 1
        assets = retrievedAssets['items']
        results = []
        for item in assets:
          results.append(self.getAssetMetaData(item, item['id'])) 

#        pool = ThreadPool(len(assets))
#        for assetId in assets:
#            results.append(pool.apply_async(self.getAssetMetaData, args=[assetId]))
#        pool.close()
#        pool.join()
#        results = [r.get() for r in results]
        return {"data": results, "total": retrievedAssets['itemsCount'], "sourceName": self.attributes['source']}
