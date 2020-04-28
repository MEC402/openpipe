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

if 'metaDataId' not in dict.keys() or 'oldTagName' not in dict.keys() or 'oldValue' not in dict.keys() or 'newTagName' not in dict.keys() or 'newValue' not in dict.keys():
    print(json.dumps({"result": "Fail"}, default=str))
else:
    print(json.dumps({"result": BL().updateMetaTag(dict["metaDataId"],dict["oldTagName"],dict["oldValue"],dict["newTagName"],dict["newValue"])}, default=str))