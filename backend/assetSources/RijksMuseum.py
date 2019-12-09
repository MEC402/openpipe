#!/bin/python3

import requests
from multiprocessing.pool import ThreadPool

class RijksMuseum:

    url = "https://www.rijksmuseum.nl/api/en/"

    def __init__(self, schema):
        self.schema = schema

    def searchRijkForAssets(self, term, page, pageSize):
        serviceName = "collection"
        params = {'key': "qvMYRE87", 'format': "json", 'q': term, 'p': page, 'ps': pageSize }
        response = requests.get(url=self.url + serviceName, params=params)
        data = response.json()
        return data

    def getRijkMetaTagMapping(self,assetOriginalID):
        serviceName = "collection/" + str(assetOriginalID) + "/"
        params = {'key': "qvMYRE87", 'format': "json"}
        response = requests.get(url=self.url + serviceName, params=params)
        data = response.json()
        return self.getRijkAssetMetaData(data["artObject"])

    def getRijkAssetMetaData(self, data):
        response = {}
        response = self.schema.copy()
        response["source"] = ["Rijk"]
        response["id"] = [data["objectNumber"]]
        if data['webImage'] is not None:
            response["largeImage"] = [data["webImage"]["url"]]
            response["largeImageDimensions"] = [str(data["webImage"]["width"])+","+str(data["webImage"]["height"])]
            response["smallImage"] = [data["webImage"]["url"]]
            response["smallImageDimensions"] = [str(data["webImage"]["width"])+","+str(data["webImage"]["height"])]
        response["title"] = [data["title"]]
        if (len(data["principalMakers"]) > 0):
            response["artist"] = []
            for artist in data["principalMakers"]:
                response["artist"].append(artist["name"])
        # schema["culture"].append(data["culture"])
        # schema["classification"].append(data["classification"])
        # # schema.genre.push(data["city"])
        # # schema.medium.push(data["city"])
        # schema["nation"].append(data["country"])
        # schema["city"].append(data["city"])
        # schema["tags"] = data["tags"]
        return response

    def getData(self, q, page, pageSize):
        results = []
        retrievedAssets = self.searchRijkForAssets(q, page, pageSize)
        pool = ThreadPool(len(retrievedAssets))
        for assetId in retrievedAssets["artObjects"]:
            results.append(pool.apply_async(self.getRijkMetaTagMapping, args=[assetId["objectNumber"]]))
        pool.close()
        pool.join()
        results = [r.get() for r in results]
        return results