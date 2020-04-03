#!/bin/python3

import requests
from multiprocessing.pool import ThreadPool


class ClevelandMuseum:
    url = "https://openaccess-api.clevelandart.org/api/artworks/"

    def __init__(self, schema):
        self.schema = schema

    def searchForAssets(self, term):
        params = {'q': term}
        response = requests.get(url=self.url, params=params)
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
        if len(data["creators"]) > 0:
            response["openpipe_canonical_artist"] = []
            for c in data["creators"]:
                response["openpipe_canonical_artist"].append(c["description"])
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
        response = requests.get(url=self.url + serviceName)
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
