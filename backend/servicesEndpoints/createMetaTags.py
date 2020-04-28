#!/bin/python3

import json
import sys

from openpipeAPI.ORM.BL import BL

postBody = sys.stdin.read()
data = json.loads(json.dumps(postBody))

print("Content-Type: text/json\n")
print(json.dumps(BL().insertIntoMetaTags(json.loads(data)), default=str))

