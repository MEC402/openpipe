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
        response["source"] = ["Cleveland"]
        response["id"] = [data["id"]]
        if data['images'] is not None:
            response["largeImage"] = [data["images"]["print"]["url"]]
            response["largeImageDimensions"] = [str(data["images"]["print"]["width"]) + "," + str(data["images"]["print"]["height"])]
            response["smallImage"] = [data["images"]["web"]["url"]]
            response["smallImageDimensions"] = [str(data["images"]["web"]["width"]) + "," + str(data["images"]["web"]["height"])]
        response["title"] = [data["title"]]
        response["artist"] = []
        for c in data["creators"]:
            response["artist"].append(c["description"])
        response["culture"] = data["culture"]
        # response["classification"] = [data["classification"]]
        # self.schema.genre.push(data["city"])
        # self.schema.medium.push(data["city"])
        # response["nation"] = [data["country"]]
        # response["city"] = [data["city"]]
        # response["tags"] = data["tags"]
        return response

    def getAssetMetaData(self, asset):
        serviceName = str(asset["id"])
        response = requests.get(url=self.url + serviceName)
        data = response.json()
        metaData = self.getMetaTagMapping(data)
        return metaData

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
        for assetId in assets:
            results.append(pool.apply_async(self.getAssetMetaData, args=[assetId]))
        pool.close()
        pool.join()
        results = [r.get() for r in results]
        return results
