#!/bin/python3

import cgi
import json
import sys
import os

import requests
from ImageUtil import ImageUtil
from RijksMuseum import RijksMuseum
import base64

path = "../cache/"


def cgiFieldStorageToDict(fieldStorage):
    """ Get a plain dictionary rather than the '.value' system used by the
   cgi module's native fieldStorage class. """
    params = {}
    for key in fieldStorage.keys():
        params[key] = fieldStorage[key].value
    return params


dict = cgiFieldStorageToDict(cgi.FieldStorage())

# dict = {'id':"SK-A-5005"}

if 'id' not in dict.keys():
    print("Content-Type: text/json\n")
    print(json.dumps([{}]))

else:
    url = "https://www.rijksmuseum.nl/api/nl/collection/"
    rijks = RijksMuseum({})
    imgUtil = ImageUtil()
    serviceName = dict["id"] + "/tiles"
    params = {'key': "qvMYRE87"}
    response = requests.get(url=url + serviceName, params=params)
    data = response.json()
    imgWidth = 0
    imgHeight = 0
    tileData = []
    for d in data["levels"]:
        if d['name'] == "z0":
            tileData = d['tiles']
            imgWidth = d['width']
            imgHeight = d['height']
            break
    image = imgUtil.concatTiles(tileData, imgWidth, imgHeight)
    fileName = "Rijks_" + dict["id"] + '.jpg'
    image.save(path + fileName)

    sys.stdout.write("Content-Type: image/png\n")
    sys.stdout.write("Content-Length: " + str(os.stat(path + fileName).st_size) + "\n")
    sys.stdout.write("\n")
    sys.stdout.flush()
    sys.stdout.buffer.write(open(path + fileName, "rb").read())


