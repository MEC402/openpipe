#!/bin/python3

import json
import sys

from openpipeAPI.ORM.BL import BL

postBody = sys.stdin.read()
data = json.loads(json.dumps(postBody))

with open('data.json', 'w') as outfile:
    json.dump(data, outfile)

print("Content-Type: text/json\n")
print('success')