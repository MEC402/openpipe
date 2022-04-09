#!/bin/python3

from MuseumsTM import MuseumsTM

from multiprocessing.pool import ThreadPool

import requests
import formatHelp

from ImageUtil import ImageUtil


class MetMuseum(MuseumsTM):

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
                "objectID": "openpipe_canonical_id",
                "primaryImage": "openpipe_canonical_largeImage",
                "primaryImageSmall": "openpipe_canonical_smallImage",
                "title": "openpipe_canonical_title",
                "artistDisplayName": "openpipe_canonical_artist",
                "culture": "openpipe_canonical_culture",
                "classification": "openpipe_canonical_classification",
                "country": "openpipe_canonical_nation",
                "city": "openpipe_canonical_city",
                "tags": "openpipe_canonical_tags",
                "dimensions": "openpipe_canonical_physicalDimensions"
                        }
        self.canonmap = {
                "title": "openpipe_canonical_title",
                "artistDisplayName": "openpipe_canonical_artist",
                "culture": "openpipe_canonical_culture",
                "city": "openpipe_canonical_city",
                "medium": "openpipe_canonical_medium",
                "country": "openpipe_canonical_nation"
                        }


    def searchMetForAssets(self, term):
        serviceName = "search"
        params = {'q': term}
        response = requests.get(url=self.attributes['url'] + serviceName, params=params)
        data = response.json()
        return data


    def getMetaTagMapping(self, data):
        response = {}
        response = self.schema.copy()
        response["openpipe_canonical_source"] = ["MET"]
        response["openpipe_canonical_id"] = [data["objectID"]]
        response["openpipe_canonical_largeImage"] = [data["primaryImage"]]
        imageInfo = ImageUtil()
        dimentions = imageInfo.getPixelDimentions(response["openpipe_canonical_largeImage"][0])
        response["openpipe_canonical_largeImageDimensions"] = [str(dimentions[0]) + "," + str(dimentions[1])]
        response["openpipe_canonical_smallImage"] = [data["primaryImageSmall"]]
        dimentions = imageInfo.getPixelDimentions(response["openpipe_canonical_smallImage"][0])
        response["openpipe_canonical_smallImageDimensions"] = [str(dimentions[0]) + "," + str(dimentions[1])]
        response["openpipe_canonical_title"] = [data["title"]]
        response["openpipe_canonical_artist"] = [data["artistDisplayName"]]
        response["openpipe_canonical_culture"] = [data["culture"]]
        response["openpipe_canonical_classification"] = [data["classification"]]
        # self.schema.genre.push(data["city"])
        # self.schema.medium.push(data["city"])
        response["openpipe_canonical_nation"] = [data["country"]]
        response["openpipe_canonical_city"] = [data["city"]]
        if 'tags' in data.keys() and data["tags"] is not None:
            if len(data["tags"]) > 0:
                response["openpipe_canonical_tags"] = data["tags"]
        era = "CE"
        year1 = abs(int(data["objectBeginDate"]))
        year2 = abs(int(data["objectEndDate"]))
        if "B.C." in data["objectDate"]:
            era = "BC"
        response["openpipe_canonical_firstDate"] = [
            era + " " + str(year1) + " " + "JAN" + " " + "01" + " " + "00:00:00"]
        response["openpipe_canonical_lastDate"] = [era + " " + str(year2) + " " + "JAN" + " " + "01" + " " + "00:00:00"]
        response["openpipe_canonical_date"] = [response["openpipe_canonical_firstDate"][0],
                                               response["openpipe_canonical_lastDate"][0]]
        response.update(data)
        return response

    def getAssetMetaData(self, assetOriginalID):
        serviceName = "objects/" + str(assetOriginalID)
        response = requests.get(url=self.attributes['url'] + serviceName)
        data = response.json()
        metaData = self.getMetaTagMapping(data)
        return metaData

    def getData(self, q, page, pageSize):
        results = []
        retrievedAssets = self.searchMetForAssets(q)
        if retrievedAssets['total'] == 0:
            return {"data": [], "total": 0, "sourceName": "MET"}

        start = (page - 1) * pageSize
        step = pageSize

        if int(start) > retrievedAssets['total']:
            start = retrievedAssets['total'] - 1
        if int(start) + int(step) > retrievedAssets['total']:
            step = retrievedAssets['total'] - int(start) - 1
        assets = retrievedAssets['objectIDs'][int(start):int(start) + int(step)]

        pool = ThreadPool(len(assets))
        for assetId in assets:
            results.append(pool.apply_async(self.getAssetMetaData, args=[assetId]))
        pool.close()
        pool.join()
        results = [r.get() for r in results]
        return {"data": results, "total": retrievedAssets['total'], "sourceName": "MET"}


    
    def getCanonTags(self, anasset, aorm):
        musetag = []
#first we get the appropriate set of tags from the database
        for i in self.canonmap:
            mtag = aorm.getMetaTag(anasset, i['museumtag'])
            musetags.append(mtag)

#now we copy those tags over to the canon tags
## instead of just copying the value we need to properly format the value
        for i in self.canonmap:

            mytags['tagName'] = i['canontag']
            amtag = i['museumtag']
            #right here we would call a formater for this new value
            mytags['value'] = musetags[amtag]['value']

        return mytags


    def getMappedCanonTags(self, metadataid, aorm, alltags, curtagrow):
        response = {}
        tagcount = curtagrow
        response["openpipe_canonical_source"] = {"value": "The Metropolitan Museum of Art", "status": "unknown"}
#        print (alltags[tagcount]['metaDataId'][0], metadataid)
        while tagcount < len(alltags) and alltags[tagcount]['metaDataId'][0] == metadataid:
#          print(alltags[tagcount]['metaDataId'][0], tagcount, metadataid)
          if alltags[tagcount]['tagName'][0] in self.canonmap:
               atagname = alltags[tagcount]['tagName'][0]
               cantag = self.canonmap[atagname]
#               print(cantag,atagname,alltags[tagcount]['value'])

               if cantag not in response:
                   response[cantag] = {}
               response[cantag]['value'] = formatHelp.cleanList(alltags[tagcount]['value'])

          if alltags[tagcount]['tagName'][0] in self.canonmap.values():
               atagname = alltags[tagcount]['tagName'][0]
#               print(atagname,alltags[tagcount]['value'])

               if atagname not in response:
                   response[atagname] = {}
               response[atagname]['status'] = alltags[tagcount]['status'][0]


          tagcount += 1
        
        #handle tags that need processing, imaging


        #handle dates that need to be calculated.

        #handle special formatting cases: customized Museum formats

        return response, tagcount
