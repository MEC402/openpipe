#!/bin/python3

import json
import sys
# from ORM.BL import BL
from openpipeAPI.ORM.BL import BL

postBody = sys.stdin.read()
data = json.loads(postBody)

print("Content-Type: text/json\n")
print(json.dumps(BL().saveFolderLayout(data), default=str))