#!/bin/python3

import requests
import json
import xml.etree.ElementTree as ET
import cgi
from multiprocessing.pool import ThreadPool

url = "https://collectionapi.metmuseum.org/public/collection/v1/"


def cgiFieldStorageToDict(fieldStorage):
    """ Get a plain dictionary rather than the '.value' system used by the
   cgi module's native fieldStorage class. """
    params = {}
    for key in fieldStorage.keys():
        params[key] = fieldStorage[key].value
    return params

def searchForAssets(term):
    serviceName = "search"
    params = {'q': term}
    response = requests.get(url=url + serviceName, params=params)
    data = response.json()
    return data


def getMetaTagMapping(data):
    metaData={}
    metaData['sourceData'] = data
    metaData['id'] = data['objectID']
    metaData['largeImage'] = data['primaryImage']
    metaData['smallImage'] = data['primaryImageSmall']
    metaData['title'] = data['title']
    return metaData


def getAssetMetaData(assetOriginalID):
    serviceName = "objects/" + str(assetOriginalID)
    response = requests.get(url=url + serviceName)
    data = response.json()
    metaData=getMetaTagMapping(data)
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
    if int(start) > retrievedAssets['total']:
        start = retrievedAssets['total'] - 1
    if int(start) + int(step) > retrievedAssets['total']:
        step = retrievedAssets['total'] - int(start) - 1
  
    assets = retrievedAssets['objectIDs'][int(start):int(start) + int(step)]
    pool = ThreadPool(len(assets))
    for assetId in assets:
        #results.append(getAssetMetaData(assetId))
        results.append(pool.apply_async(getAssetMetaData, args=[assetId]))

    pool.close()
    pool.join()
    results = [r.get() for r in results]
    print(json.dumps(results))



