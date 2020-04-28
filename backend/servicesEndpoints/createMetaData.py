#!/bin/python3

import json

from openpipeAPI.ORM.BL import BL

print("Content-Type: text/json\n")
print(json.dumps({"result": BL().insertIntoMetaData()}))
