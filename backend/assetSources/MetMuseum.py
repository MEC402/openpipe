#!/bin/python3

import requests
from multiprocessing.pool import ThreadPool


class MetMuseum:
    url = "https://collectionapi.metmuseum.org/public/collection/v1/"

    def __init__(self, schema):
        self.schema = schema

    def searchMetForAssets(self, term):
        serviceName = "search"
        params = {'q': term}
        response = requests.get(url=self.url + serviceName, params=params)
        data = response.json()
        return data

    def getMetaTagMapping(self, data):
        response = {}
        response = self.schema.copy()
        response["source"] = ["MET"]
        response["id"] = [data["objectID"]]
        response["largeImage"] = [data["primaryImage"]]
        response["smallImage"] = [data["primaryImageSmall"]]
        response["title"] = [data["title"]]
        response["artist"] = [data["artistDisplayName"]]
        response["culture"] = [data["culture"]]
        response["classification"] = [data["classification"]]
        # self.schema.genre.push(data["city"])
        # self.schema.medium.push(data["city"])
        response["nation"] = [data["country"]]
        response["city"] = [data["city"]]
        response["tags"] = data["tags"]
        return response

    def getAssetMetaData(self, assetOriginalID):
        serviceName = "objects/" + str(assetOriginalID)
        response = requests.get(url=self.url + serviceName)
        data = response.json()
        metaData = self.getMetaTagMapping(data)
        return metaData

    def getData(self, q, page, pageSize):
        results = []
        retrievedAssets = self.searchMetForAssets(q)

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
        return results
