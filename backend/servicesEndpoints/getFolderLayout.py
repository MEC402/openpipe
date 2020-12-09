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

dict={'folderId':134}

if 'folderId' not in dict.keys():
    print(json.dumps({"total": "", "data": [{"id": [""], "name": [""], "timeStamp": [""]}]}))
elif 'rt' not in dict.keys():
    print(json.dumps(BL().getCollectionByID(dict["folderId"]), default=str))
elif dict['rt']==1:
    print(json.dumps(BL().getFolderLayout(dict["folderId"]), default=str))


