#!/bin/python3

import json
import cgi
from openpipeAPI.ORM.BL import BL


def cgiFieldStorageToDict(fieldStorage):
    """ Get a plain dictionary rather than the '.value' system used by the
    cgi module's native fieldStorage class. """
    params = {}
    for key in fieldStorage.keys():
        params[key] = fieldStorage[key].value
    return params

print("Content-Type: text/json\n")
dict = cgiFieldStorageToDict(cgi.FieldStorage())

dict={"assetId":123, "collectionId":123, "searchTerm":"aaaa"}

if 'assetId' not in dict.keys() and 'collectionId' not in dict.keys() and 'searchTerm' not in dict.keys():
    print(json.dumps({"result": "Fail"}, default=str))
else:
    print(json.dumps({"result": BL().insertIntoCollectionMember(dict["assetId"],dict["collectionId"],dict["searchTerm"])}, default=str))
