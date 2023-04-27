#!/bin/python3

import cgi
import json
from CanonicalSchema import CanonicalSchema
from MuseumsR import MuseumsR
from JSONMuseum import JSONMuseum

print("start Load");
amuseumreg = MuseumsR()
amuseumreg.loadMuseums()

#jm = JSONMuseum();
#jm.loadCanon();
#mydat = jm.getAssetMetaData("3267");
#print(mydat);

for m in amuseumreg.sourceobjs:
  print(m)


