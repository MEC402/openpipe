#
# MuseumsR.py -> museums registry handler
#

import json
import MuseumsTM
import os

from CanonicalSchema import CanonicalSchema

class MuseumsR:
    def __init__(self):
      self.sources = [];
      self.sourceobjs = [];

    def loadMuseums(self):
#first we read in the jsonboject
      apath = os.path.dirname(MuseumsTM.__file__)
      f = open(apath+'/museums.json')
      museumjson = json.load(f)
      f.close()

#now we create a collection of Museum Objects to handle the specific museum
      for i in museumjson['museum1']:
#        print (i['class'])
        mod = __import__(i['class'])
        class_ = getattr(mod,i['class'])
        cs = CanonicalSchema()
        aschema = cs.getSchema(1)
        amuseum = class_(aschema)
        amuseum.setName(i['source'])
        amuseum.setAttr(i)
        self.sources.append(i['source'])
        self.sourceobjs.append(amuseum)
#        print(i)
#        print(i['source'])

#get a list of 'sourceid' to museum object
    def getSourceMap(self):
        sourcedict = {}
        for i in range(len(self.sources)):
             sourcedict[str(i+1)]= self.sourceobjs[i]
        return sourcedict

             

#test of class
#museumreg = MuseumsR()

#load the museums json file
#museumreg.loadMuseums()

