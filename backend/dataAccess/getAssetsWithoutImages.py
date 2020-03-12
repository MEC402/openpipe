#!/bin/python3

import json
from ORM.BL import BL

print("Content-Type: text/json\n")
print(json.dumps(BL().getAssetsWithoutImages(), default=str))