#
# MuseumsR.py -> museums registry handler
#

import json
import MuseumsTM

from CanonicalSchema import CanonicalSchema

class MuseumsR:
    def __init__(self):
      self.sources = [];
      self.sourceobjs = [];

    def loadMuseums(self):
#first we read in the jsonboject
      f = open('museums.json')
      museumjson = json.load(f)
      f.close()

#now we create a collection of Museum Objects to handle the specific museum
      for i in museumjson['museum1']:
        print (i['class'])
        mod = __import__(i['class'])
        class_ = getattr(mod,i['class'])
        cs = CanonicalSchema()
        aschema = cs.getSchema(1)
        amuseum = class_(aschema)
        amuseum.setName(i['source'])
        amuseum.setAttr(i)
        self.sources.append(i['source'])
        self.sourceobjs.append(amuseum)
        print(i)
        print(i['source'])
             

#test of class
#museumreg = MuseumsR()

#load the museums json file
#museumreg.loadMuseums()

