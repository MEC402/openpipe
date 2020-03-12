#!/bin/python3

import cgi
import json
import os
import sys

from ImageUtil import ImageUtil
from RijksMuseum import RijksMuseum

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
    rijks = RijksMuseum({})
    imgUtil = ImageUtil()

    imgWidth = 0
    imgHeight = 0
    tileData = []
    tileData, imgWidth, imgHeight = rijks.getTileImages(dict["id"], 0)
    image = imgUtil.concatTiles(tileData, imgWidth, imgHeight)
    fileName = "Rijks_" + dict["id"] + '.jpg'
    image.save(path + fileName)

    sys.stdout.write("Content-Type: image/png\n")
    sys.stdout.write("Content-Length: " + str(os.stat(path + fileName).st_size) + "\n")
    sys.stdout.write("\n")
    sys.stdout.flush()
    sys.stdout.buffer.write(open(path + fileName, "rb").read())
