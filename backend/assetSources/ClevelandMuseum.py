#!/bin/python3

import requests
from MuseumsTM import MuseumsTM
from multiprocessing.pool import ThreadPool
import formatHelp
from FormatConvert import FormatConvert


class ClevelandMuseum(MuseumsTM):

    def __init__(self, schema):
        self.schema= schema
        self.name = "Met"
#        self.canonmap = {
#                "openpipe_canonical_id": "objectID",
#                "openpipe_canonical_largeImage": "primaryImage",
#                "openpipe_canonical_smallImage": "primaryImageSmall",
#                "openpipe_canonical_title": "title",
#                "openpipe_canonical_artist": "artistDisplayName",
#                "openpipe_canonical_culture":  "culture",
#                "openpipe_canonical_classification": "classification",
#                "openpipe_canonical_nation":  "country",
#                "openpipe_canonical_city":  "city",
#                "openpipe_canonical_tags":  "tags"
#                        }
        self.fullcanonmap = {
                "id": "openpipe_canonical_id",
                "title": "openpipe_canonical_title",
                "creators": "openpipe_canonical_artist",
                "culture": "openpipe_canonical_culture"
                        }
        self.canonmap = {
                "title": "openpipe_canonical_title",
                "creators": "openpipe_canonical_artist",
                "culture": "openpipe_canonical_culture",
                "medium": "openpipe_canonical_medium"
                        }


    def searchForAssets(self, term):
        params = {'q': term}
        response = requests.get(url=self.attributes['url'], params=params)
        data = response.json()
        return data

    def getMetaTagMapping(self, data):
        data = data["data"]
        response = {}
        response = self.schema.copy()
        response["openpipe_canonical_source"] = ["Cleveland"]
        response["openpipe_canonical_id"] = [data["id"]]
        if data['images'] is not None:
            response["openpipe_canonical_largeImage"] = [data["images"]["print"]["url"]]
            response["openpipe_canonical_largeImageDimensions"] = [
                str(data["images"]["print"]["width"]) + "," + str(data["images"]["print"]["height"])]
            response["openpipe_canonical_smallImage"] = [data["images"]["web"]["url"]]
            response["openpipe_canonical_smallImageDimensions"] = [
                str(data["images"]["web"]["width"]) + "," + str(data["images"]["web"]["height"])]
            response["openpipe_canonical_fullImage"] = [
                "http://mec402.boisestate.edu/cgi-bin/assetSources/getClevelandConvertedTif.py?id=" + str(data["id"])]
            # tileInfo = self.getTileImages(data["objectNumber"], 0)
            # response["openpipe_canonical_fullImageDimensions"] = []
        response["openpipe_canonical_title"] = [data["title"]]

        response["openpipe_canonical_artist"] = [FormatConvert.getClevArtists(data)]


        if len(data["culture"]) > 0:
            response["openpipe_canonical_culture"] = data["culture"]

        if data["creation_date_earliest"] is not None and data["creation_date_latest"] is not None and data["creation_date"] is not None:
            era="CE"
            year1 = abs(int(data["creation_date_earliest"]))
            year2 = abs(int(data["creation_date_latest"]))
            if "B.C." in data["creation_date"]:
                era="BC"
            response["openpipe_canonical_firstDate"] = [era+" "+str(year1)+" "+"JAN"+" "+"01"+" "+"00:00:00"]
            response["openpipe_canonical_lastDate"] = [era+" "+str(year2)+" "+"JAN"+" "+"01"+" "+"00:00:00"]
            response["openpipe_canonical_date"]=[response["openpipe_canonical_firstDate"][0],response["openpipe_canonical_lastDate"][0]]

            response["openpipe_canonical_physicalDimensions"] = [FormatConvert.getClevDimensions(data)]

        # response["classification"] = [data["classification"]]
        # self.schema.genre.push(data["city"])
        # self.schema.medium.push(data["city"])
        # response["nation"] = [data["country"]]
        # response["city"] = [data["city"]]
        # response["tags"] = data["tags"]
        response.update(data)
        return response

    def getAssetMetaData(self, assetId):
        serviceName = str(assetId)
        response = requests.get(url=self.attributes['url'] + serviceName)
        data = response.json()
        metaData = self.getMetaTagMapping(data)
        return metaData

    def getMetaDataByAssetID(self,objctID):
        serviceName = str(objctID)
        response = requests.get(url=self.url + serviceName)
        data = response.json()
        return data["data"]

    def getData(self, q, page, pageSize):
        results = []
        retrievedAssets = self.searchForAssets(q)

        start = (page - 1) * pageSize
        step = pageSize
        total = retrievedAssets['info']['total']
        if total == 0:
            return {"data": [], "total": 0, "sourceName": "Cleveland"}

        if int(start) > total:
            start = total - 1
        if int(start) + int(step) > total:
            step = total - int(start) - 1

        assets = retrievedAssets['data'][int(start):int(start) + int(step)]

        pool = ThreadPool(len(assets))
        for asset in assets:
            results.append(pool.apply_async(self.getAssetMetaData, args=[asset["id"]]))
        pool.close()
        pool.join()
        results = [r.get() for r in results]
        return {"data": results,
                "total": total,
                "sourceName": "Cleveland"}


    def getMappedCanonTags(self, metadataid, aorm, alltags, curtag):
        response = {}
        # get all the tags for this asset from the table
        #map them to openpipe_canonical
        response["openpipe_canonical_source"] = {"value": "Cleveland",
                                                 "status": "unknown"}
        tagcount = curtag
#        print (alltags[tagcount]['metaDataId'][0], metadataid)
        while tagcount < len(alltags) and alltags[tagcount]['metaDataId'][0] == metadataid:
#          print(alltags[tagcount]['metaDataId'][0], tagcount, metadataid)


         if alltags[tagcount]['tagName'][0] in self.canonmap:
               atagname = alltags[tagcount]['tagName'][0]
               cantag = self.canonmap[atagname]
               print(cantag,atagname,alltags[tagcount]['value'])
               if cantag not in response:
                   response[cantag] = {}
#properly format artist names for cleveland
               if atagname=="creators":
                  ares = formatHelp.ClevelandArtist(alltags[tagcount]['value'])
                  response[cantag]['value'] = formatHelp.cleanList(ares)
               else:
                    if atagname == 'culture':
                        print("CULTURE:", alltags[tagcount]['value'])
                        print("------")
                    response[cantag]['value'] = formatHelp.cleanList(alltags[tagcount]['value'])
                    if atagname == 'culture':
                      holdme = response[cantag]['value']
                      print("CULTMOD:", holdme, len(holdme))
                      print("------")


         if alltags[tagcount]['tagName'][0] in self.canonmap.values():
               atagname = alltags[tagcount]['tagName'][0]
               print(atagname,alltags[tagcount]['value'])

               if atagname not in response:
                   response[atagname] = {}
               response[atagname]['status'] = alltags[tagcount]['status'][0]

         tagcount += 1



        #handle tags that need processing, imaging


        #handle dates that need to be calculated.

        #handle special formatting cases: customized Museum formats


        return response,tagcount


