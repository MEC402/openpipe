#!/bin/python3

import json
import cgi

from openpipeAPI.oracles.Oracle import Oracle


def cgiFieldStorageToDict(fieldStorage):
    """ Get a plain dictionary rather than the '.value' system used by the
   cgi module's native fieldStorage class. """
    params = {}
    for key in fieldStorage.keys():
        params[key] = fieldStorage[key].value
    return params

print("Content-Type: text/json\n")
dict = cgiFieldStorageToDict(cgi.FieldStorage())

if 'type' not in dict.keys():
    dict['type']=''

if 'nation' not in dict.keys():
    dict['nation']=''

if 'searchName' not in dict.keys():
    print(json.dumps([{"name": "", "id": "", "termCount": 0, "aliases": [], "coordinates": {"latitude": {"degrees": "-1", "minutes": "-1", "seconds": "-1", "direction": "", "decimal": "-1"}, "longitude": {"degrees": "-1", "minutes": "-1", "seconds": "-1", "direction": "", "decimal": "-1"}}}]
))

else:
    res = Oracle().getLocationInfo(dict['searchName'], dict['type'], dict['nation'])
    print(json.dumps(res))









 


