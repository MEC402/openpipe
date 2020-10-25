#!/bin/python3

import json
import cgi

from openpipeAPI.ORM.BL import BL


def cgiFieldStorageToDict(fieldStorage):
    params = {}
    for key in fieldStorage.keys():
        params[key] = fieldStorage[key].value
    return params


print("Content-Type: text/json\n")
dict = cgiFieldStorageToDict(cgi.FieldStorage())

dict={"collectionId":"all"}


if 'start' in dict.keys() and 'end' in dict.keys():
    print(json.dumps(BL().getRangeOfCollections(dict["start"],dict["end"]), default=str))
else:
    if 'collectionId' not in dict.keys():
        print(json.dumps({"total": [""], "data": [{"id": [""], "name": [""], "timeStamp": [""]}]}))
    else:
        id = dict['collectionId']
        if id == -1:
            print(json.dumps({"total": [""], "data": [{"id": [""], "name": [""], "timeStamp": [""]}]}))
        elif id == "all":
            if 'limit' in dict.keys():
              print(json.dumps(BL().getAllCollections(dict["limit"])))
            else:
              print(json.dumps(BL().getAllCollections(-1), default=str))
        else:
            print(json.dumps(BL().getCollectionByID(id), default=str))
