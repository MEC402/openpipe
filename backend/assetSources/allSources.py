#!/bin/python3
import requests
import json
import xml.etree.ElementTree as ET
import cgi
import threading
from multiprocessing.pool import ThreadPool

url = "https://collectionapi.metmuseum.org/public/collection/v1/"

response = []


# def cgiFieldStorageToDict(fieldStorage):
#     """ Get a plain dictionary rather than the '.value' system used by the
#    cgi module's native fieldStorage class. """
#     params = {}
#     for key in fieldStorage.keys():
#         params[key] = fieldStorage[key].value
#     return params

def cgiFieldStorageToDict(fieldStorage):
    """ Get a plain dictionary rather than the '.value' system used by the
   cgi module's native fieldStorage class. """
    params = {}
    for key in fieldStorage.keys():
        params[key] = fieldStorage[key].value
    return params


def getSchema():
    return {
        "id": [-1000],
        "source": [
            "The OpenPipe Museum "
        ],
        "largeImage": [
            "http://mec402.boisestate.edu/assets/largeImage.jpg"
        ],
        "largeImageDimensions": [
            "4000,3000"
        ],
        "smallImage": [
            "http://mec402.boisestate.edu/assets/smallImage.jpg"
        ],
        "smallImageDimensions": [
            "1000,750"
        ],
        "artist": [
            "OpenPipe"
        ],
        "culture": [
            "OpenPipe"
        ],
        "classification": [
            "OpenPipe"
        ],
        "genre": [
            "art-fi"
        ],
        "medium": [
            "OpenPipe Pixels"
        ],
        "nation": [
            "OpenPipe People"
        ],
        "city": [
            "OpenPipe City"
        ],
        "tags": [
            "OpenPipeTag1,OpenPipeTag2,OpenPipe3"
        ]}


def searchMetForAssets(term):
    serviceName = "search"
    params = {'q': term}
    response = requests.get(url=url + serviceName, params=params)
    data = response.json()
    return data


def getMetaTagMapping(data):
    schema = getSchema()
    schema["source"] = ["MET"]
    schema["id"] = [data["objectID"]]
    schema["largeImage"] = [data["primaryImage"]]
    schema["smallImage"] = [data["primaryImageSmall"]]
    schema["title"] = [data["title"]]
    schema["artist"] = [data["artistDisplayName"]]
    schema["culture"] = [data["culture"]]
    schema["classification"] = [data["classification"]]
    # schema.genre.push(data["city"])
    # schema.medium.push(data["city"])
    schema["nation"] = [data["country"]]
    schema["city"] = [data["city"]]
    schema["tags"] = data["tags"]
    return schema


def getAssetMetaData(assetOriginalID):
    serviceName = "objects/" + str(assetOriginalID)
    response = requests.get(url=url + serviceName)
    data = response.json()
    metaData = getMetaTagMapping(data)

    return metaData


def getMetData(q):
    results = []
    retrievedAssets = searchMetForAssets(q)
    pool = ThreadPool(len(retrievedAssets))
    for assetId in retrievedAssets["objectIDs"][:10]:
        results.append(pool.apply_async(getAssetMetaData, args=[assetId]))
    pool.close()
    pool.join()
    results = [r.get() for r in results]
    return results


# --------------------------------------------------------------------------------------------------------

def searchRijkForAssets(term):
    url = "https://www.rijksmuseum.nl/api/en/"
    serviceName = "collection"
    params = {'key': "qvMYRE87", 'format': "json", 'q': term}
    response = requests.get(url=url + serviceName, params=params)
    data = response.json()
    return data


def getRijkMetaTagMapping(assetOriginalID):
    url = "https://www.rijksmuseum.nl/api/en/"
    serviceName = "collection/" + str(assetOriginalID) + "/"
    params = {'key': "qvMYRE87", 'format': "json"}
    response = requests.get(url=url + serviceName, params=params)
    data = response.json()
    return getRijkAssetMetaData(data["artObject"])


def getRijkAssetMetaData(data):
    schema = getSchema()
    schema["source"] = ["Rijk"]
    schema["id"] = [data["objectNumber"]]
    schema["largeImage"] = [data["webImage"]["url"]]
    schema["largeImageDimensions"] = [(data["webImage"]["width"], data["webImage"]["height"])]
    schema["smallImage"] = [data["webImage"]["url"]]
    schema["smallImageDimensions"] = [(data["webImage"]["width"], data["webImage"]["height"])]
    schema["title"] = [data["title"]]
    if (len(data["principalMakers"]) > 0):
        schema["artist"] = []
        for artist in data["principalMakers"]:
            schema["artist"].append(artist["name"])
    # schema["culture"].append(data["culture"])
    # schema["classification"].append(data["classification"])
    # # schema.genre.push(data["city"])
    # # schema.medium.push(data["city"])
    # schema["nation"].append(data["country"])
    # schema["city"].append(data["city"])
    # schema["tags"] = data["tags"]
    return schema

 
def getRijkData(q):
    results = []
    retrievedAssets = searchRijkForAssets(q)
    pool = ThreadPool(len(retrievedAssets))
    for assetId in retrievedAssets["artObjects"][:10]:
        results.append(pool.apply_async(getRijkMetaTagMapping, args=[assetId["objectNumber"]]))
    pool.close()
    pool.join()
    results = [r.get() for r in results]
    return results


print("Content-Type: text/json\n")
dict = cgiFieldStorageToDict(cgi.FieldStorage())
dict = {'q': 'cats'}
if 'q' not in dict.keys():
    print(json.dumps([{}]))
else:
    results = []
    results.extend(getMetData(dict["q"]))
    results.extend(getRijkData(dict["q"]))
    print(json.dumps(results))

# dict={'q':'cats'}
#
# if 'start' not in dict.keys():
#     dict["start"] = 0
#
# if 'step' not in dict.keys():
#     dict["step"] = 10
#
# if 'q' not in dict.keys():
#     print(json.dumps([{}]))
#
# else:
#     results = []
#     threads = []
#     x = threading.Thread(target=getMetData, args=[dict["q"]] )
#     threads.append(x)
#     x.start()
#
#     y = threading.Thread(target=getRijkData, args=[dict["q"]])
#     threads.append(y)
#     y.start()
#
#     for index, thread in enumerate(threads):
#         thread.join()
#
#     results = threads.get()
#     print(json.dumps(results))