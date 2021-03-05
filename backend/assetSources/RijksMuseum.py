#!/bin/python3

import requests
import formatHelp
from MuseumsTM import MuseumsTM
from multiprocessing.pool import ThreadPool
#    url = "https://www.rijksmuseum.nl/api/en/"

class RijksMuseum(MuseumsTM):

    url = "https://www.rijksmuseum.nl/api/en/"


    def __init__(self, schema):
        self.schema= schema
        self.name = "Rijks"
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
                "objectNumber": "openpipe_canonical_id",
                "title": "openpipe_canonical_title",
                "principalMakers": "openpipe_canonical_artist",
                        }
        self.canonmap = {
                "title": "openpipe_canonical_title",
                "principalMakers": "openpipe_canonical_artist",
                "medium": "openpipe_canonical_medium",
                "culture": "openpipe_canonical_culture"
                        }



    def searchRijkForAssets(self, term, page, pageSize):
        serviceName = "collection"
        params = {'key': self.attributes['key'], 'format': "json", 'q': term, 'p': page, 'ps': pageSize}
        response = requests.get(url=self.attributes['url'] + serviceName, params=params)
        data = response.json()
        return data

    def getRijkMetaTagMapping(self, assetOriginalID):
        serviceName = "collection/" + str(assetOriginalID) + "/"
        params = {'key': self.attributes['key'], 'format': "json"}
        response = requests.get(url=self.attributes['url'] + serviceName, params=params)
        data = response.json()
        return self.getRijkAssetMetaData(data["artObject"])

    def getRijkAssetMetaData(self, data):
        response = {}
        response = self.schema.copy()
        response["openpipe_canonical_source"] = ["Rijk"]
        response["openpipe_canonical_id"] = [data["objectNumber"]]
        if data['webImage'] is not None:
            response["openpipe_canonical_largeImage"] = [data["webImage"]["url"]]
            response["openpipe_canonical_largeImageDimensions"] = [
                str(data["webImage"]["width"]) + "," + str(data["webImage"]["height"])]
            response["openpipe_canonical_smallImage"] = [data["webImage"]["url"]]
            response["openpipe_canonical_smallImageDimensions"] = [
                str(data["webImage"]["width"]) + "," + str(data["webImage"]["height"])]
            response["openpipe_canonical_fullImage"] = [
                "http://mec402.boisestate.edu/cgi-bin/assetSources/getRijksTiledImage.py?id=" + data["objectNumber"]]
            tileInfo = self.getTileImages(data["objectNumber"], 0)
            response["openpipe_canonical_fullImageDimensions"] = [str(tileInfo[1])+","+str(tileInfo[2])]

        response["openpipe_canonical_title"] = [data["title"]]
        if (len(data["principalMakers"]) > 0):
            response["openpipe_canonical_artist"] = []
            for artist in data["principalMakers"]:
                response["openpipe_canonical_artist"].append(artist["name"])

        era = "CE"
        year1 = abs(int(data["dating"]["yearEarly"]))
        year2 = abs(int(data["dating"]["yearLate"]))
        if "B.C." in data["dating"]["presentingDate"]:
            era = "BC"
        response["openpipe_canonical_firstDate"] = [era + " " + str(year1) + " " + "JAN" + " " + "01" + " " + "00:00:00"]
        response["openpipe_canonical_lastDate"] = [era + " " + str(year2) + " " + "JAN" + " " + "01" + " " + "00:00:00"]
        response["openpipe_canonical_date"] = [response["openpipe_canonical_firstDate"][0],
                                               response["openpipe_canonical_lastDate"][0]]
        # schema["culture"].append(data["culture"])
        # schema["classification"].append(data["classification"])
        # # schema.genre.push(data["city"])
        # # schema.medium.push(data["city"]) 
        # schema["nation"].append(data["country"])
        # schema["city"].append(data["city"])
        # schema["tags"] = data["tags"]

        response.update(data)
        return response

    def getData(self, q, page, pageSize):
        results = []
        retrievedAssets = self.searchRijkForAssets(q, page, pageSize)
        if len(retrievedAssets) == 0:
            return {"data": [], "total": 0, "sourceName": "Rijks"}
        pool = ThreadPool(len(retrievedAssets))

        for assetId in retrievedAssets["artObjects"]:
            results.append(pool.apply_async(self.getRijkMetaTagMapping, args=[assetId["objectNumber"]]))
        pool.close()
        pool.join()
        results = [r.get() for r in results]
        return {"data": results, "total": retrievedAssets["count"], "sourceName": "Rijks"}

    def getTileImages(self, objectId, z):
        tileData=0
        imgWidth=0
        imgHeight=0
        serviceName = "collection/" + objectId + "/tiles"
        params = {'key': self.attributes['key']}
        response = requests.get(url=self.attributes['url'] + serviceName, params=params)
        data = response.json()
        for d in data["levels"]:
            if d['name'] == "z" + str(z):
                tileData = d['tiles']
                imgWidth = d['width']
                imgHeight = d['height']
                break
        return tileData, imgWidth, imgHeight

    
    def getMappedCanonTags(self, metadataid, aorm,alltags,curtag):
        response = {}
        # get all the tags for this asset from the table
        response["openpipe_canonical_source"] = {'value': "Rijksmuseum Amsterdam", "status": "unknown"}
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
               if atagname=="principalMakers":
                  ares = formatHelp.RijksArtist(alltags[tagcount]['value'])
                  response[cantag]['value'] = formatHelp.cleanList(ares)
               else:
                  response[cantag]['value'] = formatHelp.cleanList(alltags[tagcount]['value'])



          if alltags[tagcount]['tagName'][0] in self.canonmap.values():
               atagname = alltags[tagcount]['tagName'][0]
               print(atagname,alltags[tagcount]['value'])

               if atagname not in response:
                   response[atagname] = {}
               response[atagname]['status'] = alltags[tagcount]['status'][0]


        #handle tags that need processing, imaging


        #handle dates that need to be calculated.

        #handle special formatting cases: customized Museum formats
          tagcount += 1


        return response, tagcount

