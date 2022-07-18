#!/bin/python3

import json
import cgi
from multiprocessing.pool import ThreadPool
#from MetMuseum import MetMuseum
#from RijksMuseum import RijksMuseum
#from ClevelandMuseum import ClevelandMuseum
from CanonicalSchema import CanonicalSchema
from MuseumsR import MuseumsR


def cgiFieldStorageToDict(fieldStorage):
    """ Get a plain dictionary rather than the '.value' system used by the cgi module's native fieldStorage class. """
    params = {}
    for key in fieldStorage.keys():
        params[key] = fieldStorage[key].value
    return params

print("Content-Type: text/json\n")

dict = cgiFieldStorageToDict(cgi.FieldStorage())

musename = "all"
# remberandt

#debuging code for test of implementation
# comment out before deploy
dict = {'q': 'cats',
         'p': 1,
         'ps': 10,
          'name': 'Paris'}

if 'type' not in dict.keys():
    dict["type"] = 1

if 'p' not in dict.keys():
    dict["p"] = 1

if 'ps' not in dict.keys():
    dict["ps"] = 10

if int(dict["p"]) < 1:
    dict["p"] = 1

if int(dict["ps"]) < 1:
    dict["ps"] = 1

if 'name' in dict.keys():
    musename = dict["name"]

if 'q' not in dict.keys():
    print(json.dumps([{}]))

else:
    threads = []
    museums = []
    results = []

    amuseumreg = MuseumsR()
    amuseumreg.loadMuseums()

#    cs=CanonicalSchema()
#    schema = cs.getSchema(int(dict["type"]))
#    met = MetMuseum(schema.copy())
#    museums.append(met)
#    rijks = RijksMuseum(schema.copy())
#    museums.append(rijks)
#    cleveland = ClevelandMuseum(schema.copy())
#    museums.append(cleveland)

    pool = ThreadPool(len(amuseumreg.sourceobjs))
    for museum in amuseumreg.sourceobjs:
       if musename == "all" or musename.lower() == museum.name.lower():
        threads.append(pool.apply_async(museum.getData, args=[dict["q"], int(dict["p"]), int(dict["ps"])]))
    pool.close()
    pool.join()

    response = {"total": 0,
                "museumCount":{},
                "data": []}

    for t in threads:
        result=t.get()
        response["museumCount"][result["sourceName"]]=result["total"]
        response["data"].extend(result["data"])

    response["total"] = len(response["data"])



    print(json.dumps(response))
