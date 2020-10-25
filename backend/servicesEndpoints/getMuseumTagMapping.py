import json
import cgi

from openpipeAPI.ORM.BL import BL

print("Content-Type: text/json\n")
print(json.dumps(BL().getTagMapping(), default=str))
