
1.9413111999999995
1.8731451999999997
1.2551566999999988

#!/bin/python3

from multiprocessing.pool import ThreadPool

import requests
from ImageUtil import ImageUtil
import aiohttp
import asyncio
import time

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
        imageInfo=ImageUtil()
        dimentions=imageInfo.getPixelDimentions(response["openpipe_canonical_largeImage"][0])
        response["openpipe_canonical_largeImageDimensions"] = [str(dimentions[0])+","+str(dimentions[1])]
        response["openpipe_canonical_smallImage"] = [data["primaryImageSmall"]]
        dimentions = imageInfo.getPixelDimentions(response["openpipe_canonical_smallImage"][0])
        response["openpipe_canonical_smallImageDimensions"] = [str(dimentions[0])+","+str(dimentions[1])]
        response["openpipe_canonical_title"] = [data["title"]]
        response["openpipe_canonical_artist"] = [data["artistDisplayName"]]
        response["openpipe_canonical_culture"] = [data["culture"]]
        response["openpipe_canonical_classification"] = [data["classification"]]
        # self.schema.genre.push(data["city"])
        # self.schema.medium.push(data["city"])
        response["openpipe_canonical_nation"] = [data["country"]]
        response["openpipe_canonical_city"] = [data["city"]]
        if len(data["tags"]) > 0:
            response["openpipe_canonical_tags"] = data["tags"]
        era="CE"
        year1 = abs(int(data["objectBeginDate"]))
        year2 = abs(int(data["objectEndDate"]))
        if "B.C." in data["objectDate"]:
            era="BC"
        response["openpipe_canonical_firstDate"] = [era+" "+str(year1)+" "+"JAN"+" "+"01"+" "+"00:00:00"]
        response["openpipe_canonical_lastDate"] = [era+" "+str(year2)+" "+"JAN"+" "+"01"+" "+"00:00:00"]
        response["openpipe_canonical_date"]=[response["openpipe_canonical_firstDate"][0],response["openpipe_canonical_lastDate"][0]]

        response.update(data)
        return response

    async def getAssetMetaData(self, assetOriginalID):
        serviceName = "objects/" + str(assetOriginalID)
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url + serviceName) as response:
                return await response.json()

    def getData(self, q, page, pageSize):
        s = time.perf_counter()
        results = []
        retrievedAssets = self.searchMetForAssets(q)

        start = (page - 1) * pageSize
        step = pageSize

        if int(start) > retrievedAssets['total']:
            start = retrievedAssets['total'] - 1
        if int(start) + int(step) > retrievedAssets['total']:
            step = retrievedAssets['total'] - int(start) - 1
        assets = retrievedAssets['objectIDs'][int(start):int(start) + int(step)]
        print(time.perf_counter() - s)
        s = time.perf_counter()
        loop = asyncio.get_event_loop()
        coroutines = [self.getAssetMetaData(assetId) for assetId in assets]
        results = loop.run_until_complete(asyncio.gather(*coroutines))
        print(time.perf_counter() - s)
        s = time.perf_counter()
        pool = ThreadPool(len(results))
        tempResults=[]
        for assetId in results:
            tempResults.append(pool.apply_async(self.getMetaTagMapping, args=[assetId]))
        pool.close()
        pool.join()
        finalResults = [r.get() for r in tempResults]
        print(time.perf_counter() - s)

        return {"total": retrievedAssets['total'], "sourceName": "MET","data": finalResults}
