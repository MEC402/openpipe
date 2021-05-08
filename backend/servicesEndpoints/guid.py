#!/bin/python3
import cgi
import json

from backend.openpipeAPI.ORM.BL import BL


def cgiFieldStorageToDict(fieldStorage):
    params = {}
    for key in fieldStorage.keys():
        params[key] = fieldStorage[key].value
    return params


print("Content-Type: text/json\n")

dict = cgiFieldStorageToDict(cgi.FieldStorage())
dict = {"path": "asset/ "}
guids = dict['path'].split("/")
if len(guids) < 2:
    guids[1] = ""
data = BL().getGUIDInfo(guids[0], guids[1])
print(json.dumps(data, default=str))
