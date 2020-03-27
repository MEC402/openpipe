#!/bin/python3
import cgi, os
import cgitb; cgitb.enable()
from ORM.BL import BL
import json


print("Content-Type: text/html")
print()

form = cgi.FieldStorage()

fileitem = form["file"]
if fileitem is not None and fileitem.file:

    fileName = os.path.basename(fileitem.filename)
    shortName = fileName.partition('.')[0]
    uri = "testing123" + fileName
    idAtSource = 123123
    sourceId = "666"
    metaDataId = None
    scope = 0
    #Save to server
    # open(path, 'wb').write(fileitem.file.read())

    #Insert into sql tables
    BL().insertIntoAsset(shortName, uri, idAtSource, sourceId, metaDataId, scope)
    print(json.dumps(BL().insertIntoImages(shortName, fileName, uri), default=str))