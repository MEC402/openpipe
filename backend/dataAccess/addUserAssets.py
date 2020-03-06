#!/bin/python3
import cgi
import json
from ORM.BL import BL

postBody = sys.stdin.read()
data = json.loads(postBody)

print("Content-Type: image/jpeg\n")
# insert into database
print(json.dumps(BL().insertUserAsset(data), default=str))
# call script to move files to correct location#
# print(json.dumps(BL().addUserAssetDB(data), default=str))