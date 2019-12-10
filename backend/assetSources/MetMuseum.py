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
        response["openpipe_canonical_source"] = ["MET"]
        response["openpipe_canonical_id"] = [data["objectID"]]
        response["openpipe_canonical_largeImage"] = [data["primaryImage"]]
        response["openpipe_canonical_smallImage"] = [data["primaryImageSmall"]]
        response["openpipe_canonical_title"] = [data["title"]]
        response["openpipe_canonical_artist"] = [data["artistDisplayName"]]
        response["openpipe_canonical_culture"] = [data["culture"]]
        response["openpipe_canonical_classification"] = [data["classification"]]
        # self.schema.genre.push(data["city"])
        # self.schema.medium.push(data["city"])
        response["openpipe_canonical_nation"] = [data["country"]]
        response["openpipe_canonical_city"] = [data["city"]]
        response["openpipe_canonical_tags"] = data["tags"]
        response.update(data)
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
        return {"data": results, "total": retrievedAssets['total'], "sourceName": "MET"}
