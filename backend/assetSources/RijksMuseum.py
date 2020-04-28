#!/bin/python3

import requests
from multiprocessing.pool import ThreadPool



import aiohttp
import asyncio



class RijksMuseum:
    url = "https://www.rijksmuseum.nl/api/en/"

    def __init__(self, schema):
        self.schema = schema

    def searchRijkForAssets(self, term, page, pageSize):
        serviceName = "collection"
        params = {'key': "qvMYRE87", 'format': "json", 'q': term, 'p': page, 'ps': pageSize}
        response = requests.get(url=self.url + serviceName, params=params)
        data = response.json()
        return data

    # async def getAssetMetaData(self, assetOriginalID):
    #     serviceName = "collection/" + str(assetOriginalID) + "/"
    #     params = {'key': "qvMYRE87", 'format': "json"}
    #     async with aiohttp.ClientSession() as session:
    #         async with session.get(self.url + serviceName, params=params,) as response:
    #             return await response.json()

    def getAssetMetaData(self, assetOriginalID):
        serviceName = "collection/" + str(assetOriginalID) + "/"
        params = {'key': "qvMYRE87", 'format': "json"}
        response = requests.get(url=self.url + serviceName, params=params)
        data = response.json()
        metaData = self.getMetaTagMapping(data)
        return metaData

    def getMetaTagMapping(self, data):
        response = {}
        response = self.schema.copy()
        data = data['artObject']
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
            # tileInfo = self.getTileImages(data["objectNumber"], 0)
            # response["openpipe_canonical_fullImageDimensions"] = [str(tileInfo[1])+","+str(tileInfo[2])]

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
        params = {'key': "qvMYRE87"}
        response = requests.get(url=self.url + serviceName, params=params)
        data = response.json()
        for d in data["levels"]:
            if d['name'] == "z" + str(z):
                tileData = d['tiles']
                imgWidth = d['width']
                imgHeight = d['height']
                break
        return tileData, imgWidth, imgHeight

