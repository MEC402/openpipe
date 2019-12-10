#!/bin/python3

import requests
import json
import xml.etree.ElementTree as ET
import cgi
from multiprocessing.pool import ThreadPool
from MetMuseum import MetMuseum
from RijksMuseum import RijksMuseum
from ClevelandMuseum import ClevelandMuseum
from CanonicalSchema import CanonicalSchema


def cgiFieldStorageToDict(fieldStorage):
    """ Get a plain dictionary rather than the '.value' system used by the
   cgi module's native fieldStorage class. """
    params = {}
    for key in fieldStorage.keys():
        params[key] = fieldStorage[key].value
    return params


print("Content-Type: text/json\n")
dict = cgiFieldStorageToDict(cgi.FieldStorage())

# dict = {'q': 'van gogh',
#         'p': 1,
#         'ps': 10,
#         'name':"cleveland"}

if 'p' not in dict.keys():
    dict['p'] = 1

if 'ps' not in dict.keys():
    dict['ps'] = 10

if 'type' not in dict.keys():
    dict['type'] = 1

if 'q' not in dict.keys() or 'name' not in dict.keys():
    print(json.dumps([{}]))

else:
    cs = CanonicalSchema()

    if dict["name"].lower() == "met":
        met = MetMuseum(cs.getSchema(int(dict["type"])))
        results = met.getData(dict["q"], int(dict["p"]), int(dict["ps"]))
    elif dict["name"].lower() == "rijks":
        rijks = RijksMuseum(cs.getSchema(int(dict["type"])))
        results = rijks.getData(dict["q"], int(dict["p"]), int(dict["ps"]))
    elif dict["name"].lower() == "cleveland":
        cleveland = ClevelandMuseum(cs.getSchema(int(dict["type"])))
        results = cleveland.getData(dict["q"], int(dict["p"]), int(dict["ps"]))

    print(json.dumps(results))
