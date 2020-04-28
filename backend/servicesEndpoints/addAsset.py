#!/bin/python3
import cgi
import json
from openpipeAPI.ORM.BL import BL


def cgiFieldStorageToDict(fieldStorage):
    params = {}
    for key in fieldStorage.keys():
        params[key] = fieldStorage[key].value
    return params


print("Content-Type: text/json\n")
dict = cgiFieldStorageToDict(cgi.FieldStorage())

# dict={"shortName":"test", "uri":"test", "idAtSource":123, "sourceId":223, "metaDataId":1234,"scope":1}

if 'shortName' not in dict.keys() and 'uri' not in dict.keys() and 'idAtSource' not in dict.keys() \
        and 'sourceId' not in dict.keys() and 'metaDataId' not in dict.keys() and 'scope' not in dict.keys():
    print(json.dumps({"result": "Fail"}, default=str))
else:
    print(json.dumps({"result":BL().insertIntoAsset(dict["shortName"],dict["uri"],dict["idAtSource"],
                                                    dict["sourceId"],dict["metaDataId"],dict["scope"])}))
