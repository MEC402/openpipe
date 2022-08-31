#!/bin/python3

import json

# Opening JSON file
f = open('museums.json')

# returns JSON object as
# a dictionary
data = json.load(f)

print("Content-Type: text/json\n")
json.dumps(data)

f.close()