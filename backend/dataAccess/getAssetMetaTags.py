#!/bin/python3

import json
import cgi

from ORM.BL import BL


def cgiFieldStorageToDict(fieldStorage):
    params = {}
    for key in fieldStorage.keys():
        params[key] = fieldStorage[key].value
    return params

print("Content-Type: text/json\n")
dict = cgiFieldStorageToDict(cgi.FieldStorage())

if 'assetId' not in dict.keys():
    print(json.dumps({"total": "", "data": [{"id": [""], "name": [""], "timeStamp": [""]}]}))
else:
    print(json.dumps(BL().getAssetMetaTags(dict['assetId']), default=str))

