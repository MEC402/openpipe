#!/bin/python3

from MuseumsTM import MuseumsTM

from multiprocessing.pool import ThreadPool

import requests
import formatHelp
from FormatConvert import FormatConvert

from ImageUtil import ImageUtil


class JSONMuseum(MuseumsTM):

    def loadCanon(self):
    #first we read in the jsonboject
          apath = os.path.dirname(MuseumsTM.__file__)
          f = open(apath+'/jsonmuseum.json')
          museumjson = json.load(f)
          f.close()


    def __init__(self, schema):
        self.schema= schema
        self.name = "JSON"


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
        response["openpipe_canonical_id"] = FormatConvert.ConvertString(data,"objectID")
        response["openpipe_canonical_largeImage"] = FormatConvert.ConvertString(data,"primaryImage")

        imageInfo = ImageUtil()
        dimentions = imageInfo.getPixelDimentions(response["openpipe_canonical_largeImage"][0])
        response["openpipe_canonical_largeImageDimensions"] = [str(dimentions[0]) + "," + str(dimentions[1])]

        response["openpipe_canonical_smallImage"] = [data["primaryImageSmall"]]
        response["openpipe_canonical_smallImage"] = FormatConvert.ConvertString(data,"primaryImageSmall")
        dimentions = imageInfo.getPixelDimentions(response["openpipe_canonical_smallImage"][0])
        response["openpipe_canonical_smallImageDimensions"] = [str(dimentions[0]) + "," + str(dimentions[1])]

        response["openpipe_canonical_title"] = FormatConvert.ConvertString(data,"title")
        response["openpipe_canonical_artist"] = FormatConvert.ConvertString(data,"artistAlphaSort")
        response["openpipe_canonical_culture"] = FormatConvert.ConvertString(data,"culture")
        response["openpipe_canonical_medium"] = FormatConvert.ConvertString(data,"medium")

        response["openpipe_canonical_classification"] = FormatConvert.ConvertString(data,"classification")
        # self.schema.genre.push(data["city"])
        # self.schema.medium.push(data["city"])
        response["openpipe_canonical_nation"] = FormatConvert.ConvertString(data,"country")
        response["openpipe_canonical_city"] = FormatConvert.ConvertString(data,"city")

        #tags are outdated and should not be canonical
        #if 'tags' in data.keys() and data["tags"] is not None:
        #    if len(data["tags"]) > 0:
        #        response["openpipe_canonical_tags"] = data["tags"]


        #process the data information
        dateset = FormatConvert.getMetDate(data)
        response["openpipe_canonical_firstDate"] = dateset["openpipe_canonical_firstDate"]
        response["openpipe_canonical_lastDate"] = dateset["openpipe_canonical_lastDate"]
        response["openpipe_canonical_date"] = dateset["openpipe_canonical_date"]


        response["openpipe_canonical_physicalDimensons"] = FormatConvert.getMetDimensions(data)

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
