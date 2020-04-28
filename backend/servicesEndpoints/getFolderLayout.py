#!/bin/python3

import json
import cgi


def cgiFieldStorageToDict(fieldStorage):
    params = {}
    for key in fieldStorage.keys():
        params[key] = fieldStorage[key].value
    return params

print("Content-Type: text/json\n")
dict = cgiFieldStorageToDict(cgi.FieldStorage())

if 'folderId' not in dict.keys():
    print(json.dumps({"total": "", "data": [{"id": [""], "name": [""], "timeStamp": [""]}]}))
elif int(dict['folderId']) == 29:
    result={"folderId":29, "metaDataId":4979, "assets":[
        {"assetID":"http://mec402.boisestate.edu/cgi-bin/openpipe/data/asset/1","geometry":"497 x 624 + 0 + 0", "wall": "center"},
        {"assetID":"http://mec402.boisestate.edu/cgi-bin/openpipe/data/asset/2", "geometry": "2328 x 3722 + 499 + 0", "wall": "center"},
        {"assetID":"http://mec402.boisestate.edu/cgi-bin/openpipe/data/asset/3", "geometry": "2328 x 3722 + 5155 + 0", "wall": "center"},
        {"assetID":"http://mec402.boisestate.edu/cgi-bin/openpipe/data/asset/4", "geometry": "3791 x 3792 + 5155 + 0", "wall": "center"},
        {"assetID":"http://mec402.boisestate.edu/cgi-bin/openpipe/data/asset/5", "geometry": "2328 x 3722 + 499 + 0", "wall": "center"},
        {"assetID":"http://mec402.boisestate.edu/cgi-bin/openpipe/data/asset/6", "geometry": "2328 x 3722 + 499 + 0", "wall": "center"},
        {"assetID":"http://mec402.boisestate.edu/cgi-bin/openpipe/data/asset/7", "geometry": "2328 x 3722 + 499 + 0", "wall": "center"},
        {"assetID":"http://mec402.boisestate.edu/cgi-bin/openpipe/data/asset/8", "geometry": "2328 x 3722 + 499 + 0", "wall": "center"},
        {"assetID":"http://mec402.boisestate.edu/cgi-bin/openpipe/data/asset/9", "geometry": "2328 x 3722 + 499 + 0", "wall": "center"},
        {"assetID":"http://mec402.boisestate.edu/cgi-bin/openpipe/data/asset/10", "geometry": "2328 x 3722 + 499 + 0", "wall": "center"},
        {"assetID":"http://mec402.boisestate.edu/cgi-bin/openpipe/data/asset/11", "geometry": "2328 x 3722 + 499 + 0", "wall": "center"},
        {"assetID":"http://mec402.boisestate.edu/cgi-bin/openpipe/data/asset/12", "geometry": "2328 x 3722 + 499 + 0", "wall": "center"},
    ]}
    print(json.dumps(result, default=str))
