#!/bin/python3
import cgi
import json

from backend.openpipeAPI.ORM.BL import BL

def cgiFieldStorageToDict(fieldStorage):
    params = {}
    for key in fieldStorage.keys():
        params[key] = fieldStorage[key].value
    return params


dict = cgiFieldStorageToDict(cgi.FieldStorage())

print("Content-Type: text/json\n")

dict={'p':1000,'ps':10}

if 'p' not in dict.keys():
    dict['p'] = 1

if 'ps' not in dict.keys():
    dict['ps'] = 10


print(json.dumps(BL().getTopics(int(dict["p"]),int(dict["ps"])), default=str))
