#!/bin/python3

import json

print("Content-Type: text/json\n")
with open('dsAppSettings.json') as json_file:
    data = json.load(json_file)
    print(json.dumps(data, default=str))




