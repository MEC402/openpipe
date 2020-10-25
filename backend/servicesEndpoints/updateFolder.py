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


if 'collectionId' not in dict.keys() or 'newName' not in dict.keys() or 'newImage' not in dict.keys() or 'newVerified' not in dict.keys():
    print(json.dumps({"result" : "Fail"}))
else:
    print(json.dumps(BL().updateFolder(dict["collectionId"], dict["newName"], dict["newImage"], dict["newVerified"]), default=str))