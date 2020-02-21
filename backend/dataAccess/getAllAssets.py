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

if 'p' not in dict.keys():
    dict['p'] = 1

if 'ps' not in dict.keys():
    dict['ps'] = 10

if 'changeStart' not in dict.keys():
    dict['changeStart'] = '1900-01-01'

if 'changeEnd' not in dict.keys():
    dict['changeEnd'] = '5000-01-01'

# dict={'p':1,'ps':3,'changeStart':'2019-12-11','changeEnd':'2019-12-11'}

print(json.dumps(BL().getAllAssets(int(dict["p"]), int(dict["ps"]), dict['changeStart'], dict['changeEnd']), default=str))
