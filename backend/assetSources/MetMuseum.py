#!/bin/python3

from MuseumsTM import MuseumsTM

from multiprocessing.pool import ThreadPool

import requests

from ImageUtil import ImageUtil


class MetMuseum(MuseumsTM):

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
