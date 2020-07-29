#!/bin/python3

import json
import cgi
import sqlalchemy as db

from openpipeAPI.ORM.BL import BL


def cgiFieldStorageToDict(fieldStorage):
    """ Get a plain dictionary rather than the '.value' system used by the
   cgi module's native fieldStorage class. """
    params = {}
    for key in fieldStorage.keys():
        params[key] = fieldStorage[key].value
    return params


def getAllTags():
    result=BL().getCanonicalTags()
    res = {}
    for key in result:
         res[key.replace('openpipe_canonical_', '')] =[result[key]]
    return res


print("Content-Type: text/json\n")
print(json.dumps(getAllTags(), default=str))