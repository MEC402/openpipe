#!/bin/python3

import cgi, os
import cgitb;

cgitb.enable(display=0, logdir="/var/www/cgi-bin/dataAccess/logs/")
from ORM.BL import BL
from webdav3.client import Client
import json
import Slack
import traceback
import sys
import os

try:
    print("Content-Type: text/json")
    print()

    form = cgi.FieldStorage()

    fileitem = form["file"]
    if fileitem is not None and fileitem.file:
        sourcefileName = os.path.basename(fileitem.filename)
        ext = sourcefileName.partition('.')[-1]
        # baseURI="http://mec402.boisestate.edu/assets/uploads/"
    
        baseURL = os.getenv('UPLD_URL')

        sourceId = "666"
        folderId = 130

        data={"shortName":sourcefileName,"uri":baseURL,"folderId":folderId,"assetType":ext}
        uniqueFileName=BL().saveUploadAsset()

        # Save to server
        path = "../../html/assets/uploads/"
        open(path + uniqueFileName, 'wb').write(fileitem.file.read())
        print("{}")

        # Slack.sendMessage("FileUpload Successful")
except Exception as e:
    track = traceback.format_exc()
# Slack.sendMessage(track)


# options = {
#             'webdav_hostname': "http://mec402.boisestate.edu/",
#             'webdav_root': "webdav",
#             'webdav_login': "openpipedev",
#             'webdav_password': "openPipeArtMaster51"
#         }
#         client = Client(options)
#         with open(path + fileName, "rb") as local_file:
#             client.execute_request(action='upload', path="/user_assets/"+fileName, data=local_file)