#!/bin/python3

import requests
import json
import cgi
from multiprocessing.pool import ThreadPool

url = "https://openaccess-api.clevelandart.org/api/artworks/"


def cgiFieldStorageToDict(fieldStorage):
    """ Get a plain dictionary rather than the '.value' system used by the
   cgi module's native fieldStorage class. """
    params = {}
    for key in fieldStorage.keys():
        params[key] = fieldStorage[key].value
    return params


def searchForAssets(term):
    params = {'q': term}
    response = requests.get(url=url, params=params)
    data = response.json()
    return data


def getMetaTagMapping(assetOriginalID):
    serviceName = str(assetOriginalID) + "/"
    response = requests.get(url=url)
    data = response.json()
    return data


def getAssetMetaData(data):
    metaData = {}
    metaData['id'] = data['id']
    if data['images'] is not None:
        metaData['largeImage'] = data['images']['print']["url"]
        metaData['smallImage'] = data['images']['web']["url"]
    else:
        metaData['largeImage'] = ""
        metaData['smallImage'] = ""
    metaData['title'] = data['title']
    metaData['sourceData'] = data

    return metaData


print("Content-Type: text/json\n")
dict = cgiFieldStorageToDict(cgi.FieldStorage())

if 'start' not in dict.keys():
    dict['start'] = 0

if 'step' not in dict.keys():
    dict['step'] = 10

if 'q' not in dict.keys():
    print(json.dumps([{}]))

else:
    results = []

    retrievedAssets = searchForAssets(dict['q'])
    start = dict['start']
    step = dict['step']
    total = retrievedAssets['info']['total']
    if int(start) > total:
        start = total - 1
    if int(start) + int(step) > total:
        step = total - int(start) - 1

    assets = retrievedAssets['data'][int(start):int(start) + int(step)]
    pool = ThreadPool(len(assets))
    for asset in assets:
        results.append(pool.apply_async(getAssetMetaData, args=[asset]))

    pool.close()
    pool.join()
    results = [r.get() for r in results]
    print(json.dumps(results))


