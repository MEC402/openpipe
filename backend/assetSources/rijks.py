#!/bin/python3

import requests
import json
import cgi
from multiprocessing.pool import ThreadPool

url = "https://www.rijksmuseum.nl/api/en/"


def cgiFieldStorageToDict(fieldStorage):
    """ Get a plain dictionary rather than the '.value' system used by the
   cgi module's native fieldStorage class. """
    params = {}
    for key in fieldStorage.keys():
        params[key] = fieldStorage[key].value
    return params


def searchForAssets(term):
    serviceName = "collection"
    params = {'key': "qvMYRE87",'format': "json",'q': term}
    response = requests.get(url=url + serviceName, params=params)
    data = response.json()
    return data


def getMetaTagMapping(assetOriginalID):
    serviceName = "collection/"+str(assetOriginalID)+"/"
    params = {'key': "qvMYRE87",'format': "json"}
    response = requests.get(url=url + serviceName, params=params)
    data = response.json()
    return data['artObject']


def getAssetMetaData(data):
    metaData = {}
    
    metaData['id'] = data['objectNumber']
    metaData['largeImage'] = data['webImage']["url"]
    metaData['smallImage'] = data['webImage']["url"]
    metaData['title'] = data['title']
    metaData['sourceData']=getMetaTagMapping(data['objectNumber'])

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
    total = retrievedAssets['count']
    if int(start) > total:
        start = total - 1
    if int(start) + int(step) > total:
        step = total - int(start) - 1

    assets = retrievedAssets['artObjects'][int(start):int(start) + int(step)]
    pool = ThreadPool(len(assets))
    for asset in assets:
        results.append(pool.apply_async(getAssetMetaData, args=[asset]))

    pool.close()
    pool.join()
    results = [r.get() for r in results]
    print(json.dumps(results))

