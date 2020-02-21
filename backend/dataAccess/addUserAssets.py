#!/bin/python3
import cgi
import json
from ORM.BL import BL

postBody = sys.stdin.read()
data = json.loads(postBody)

print("Content-Type: image/jpeg\n")
print(json.dumps(BL().addUserAssetFS(data), default=str))
print(json.dumps(BL().addUserAssetDB(data), default=str))