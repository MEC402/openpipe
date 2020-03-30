#!/bin/python3

import json
import cgi

from ORM.BL import BL

print("Content-Type: text/json\n")

data={"total":1,
      "data":[
        "http://mec402.boisestate.edu/cgi-bin/openpipe/data/folder/29"
      ]}

print(json.dumps(data, default=str))
