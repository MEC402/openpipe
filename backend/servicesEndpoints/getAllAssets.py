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


dict={'p':1,'ps':3,'type':1}

if 'p' not in dict.keys():
    dict['p'] = 1

if 'ps' not in dict.keys():
    dict['ps'] = 10

if 'changeStart' not in dict.keys():
    dict['changeStart'] = '1900-01-01'

if 'changeEnd' not in dict.keys():
    dict['changeEnd'] = '5000-01-01'

if 'type' not in dict.keys():
    dict['type'] = 0

data=BL().getAllAssets(int(dict["p"]), int(dict["ps"]), dict['changeStart'], dict['changeEnd'])

if(dict['type']==1):
    dt=BL().getCanonicalTags().values()
    print(dt)
    for dd in data['data']:
        for d in dd.keys():
            if "openpipe_canonical_" in d:
                for i in dd[d]:
                    if i in dt:
                        print(i)
                        dd[d]=[""]
                        break

print(json.dumps(data, default=str))
