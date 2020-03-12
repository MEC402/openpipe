#! C:/Users/walluser/AppData/Local/Programs/Python/Python38-32/python.exe


import json
import sys

print ("Content-Type: text/json")
print("")

postBody = sys.stdin.read()
data = json.loads(postBody)

print(data)