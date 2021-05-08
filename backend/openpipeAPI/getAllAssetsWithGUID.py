#!/bin/python3

import json
import cgi
import sys

from backend.openpipeAPI.ORM.BL import BL

def cgiFieldStorageToDict(fieldStorage):
    params = {}
    for key in fieldStorage.keys():
        params[key] = fieldStorage[key].value
    return params


print("Content-Type: text/json\n")
# sys.exit(0)
dict = cgiFieldStorageToDict(cgi.FieldStorage())

dict={'p':1,'ps':3,'type':0}

if 'p' not in dict.keys():
    dict['p'] = 1

if 'ps' not in dict.keys():
    dict['ps'] = 10

if 'changeStart' not in dict.keys():
    dict['changeStart'] = '1900-01-01'

if 'changeEnd' not in dict.keys():
    dict['changeEnd'] = '5000-01-01'

if 'type' not in dict.keys():
    dict['type'] = 1

# if dict['p'].isnumeric() != True:
#  data={"total": 0, "data": [], "error": "page value must be a number"}
# else:
data = BL().getAllAssetsWithGUID(int(dict["p"]), int(dict["ps"]), dict['changeStart'], dict['changeEnd'],
                                 int(dict['type']))

print(json.dumps(data, default=str))
