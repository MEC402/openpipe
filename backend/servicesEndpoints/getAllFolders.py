#!/bin/python3

# ___________________________________________________________
#                This is an endpoint for the UI
#                     Just to make it faster
# ___________________________________________________________

import json
import cgi

from openpipeAPI.ORM.BL import BL

print("Content-Type: text/json\n")

print(json.dumps(BL().getAllFolders(), default=str))
