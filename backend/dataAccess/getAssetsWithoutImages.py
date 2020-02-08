#!/bin/python3

import json
import cgi
import sqlalchemy as db
from compute.nightlyRuns.VerifyAssets import VerifyAsset

print("Content-Type: text/json\n")
vf = VerifyAsset()
print(json.dumps(vf.listAssetsWithoutImage(), default=str))