#!/bin/python3

import cgi
import json
import os
import sys

from ImageUtil import ImageUtil
from ClevelandMuseum import ClevelandMuseum

path = "../cache/"


def cgiFieldStorageToDict(fieldStorage):
    """ Get a plain dictionary rather than the '.value' system used by the
   cgi module's native fieldStorage class. """
    params = {}
    for key in fieldStorage.keys():
        params[key] = fieldStorage[key].value
    return params


dict = cgiFieldStorageToDict(cgi.FieldStorage())

#dict = {'id': "142223"}

if 'id' not in dict.keys():
    print("Content-Type: text/json\n")
    print(json.dumps([{}]))

else:
    cleveland = ClevelandMuseum({})
    imgUtil = ImageUtil()

    imageURL = cleveland.getMetaDataByAssetID(dict["id"])["images"]["full"]["url"]
    print(imageURL)
    # TODO: get conversion type from the parameter
    conversionType = "jpg"
    fileName = "Cleveland_" + str(dict["id"])
    imgUtil.convertImageFromURL(imageURL, path, fileName, conversionType)

    sys.stdout.write("Content-Type: image/jpg\n")
    sys.stdout.write("Content-Length: " + str(os.stat(path + fileName+"."+conversionType).st_size) + "\n")
    sys.stdout.write("\n")
    sys.stdout.flush()
    sys.stdout.buffer.write(open(path + fileName, "rb").read())
