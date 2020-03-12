#!/bin/python3

import json
import mysql.connector
from mysql.connector import Error
import cgi

from ORM.BL import BL


def cgiFieldStorageToDict(fieldStorage):
    """ Get a plain dictionary rather than the '.value' system used by the
   cgi module's native fieldStorage class. """
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

if 'collectionId' not in dict.keys():
    print(json.dumps({"total": "-1", "data": [{}]}))
else:
    print(json.dumps(BL().getPublicAsssetsInCollection(dict['collectionId'],int(dict["p"]), int(dict["ps"])), default=str))