#!/bin/python3

import json
import sys

from ORM.BL import BL

postBody = sys.stdin.read()
data = json.loads(postBody)

print("Content-Type: text/json\n")
print(json.dumps(BL().insertIntoMetaTags(data), default=str))
