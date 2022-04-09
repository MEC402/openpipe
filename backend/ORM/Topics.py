import json

import sys
from ORM.ORM import ORM
from ORM.TO import TO
import requests
import time

# this class simply returns a list of acceptable entityName entries

def removeCanon(alongname):
    res = alongname[len("openpipe_canonical_"):]
    return res

class Topics:
    sourceTable = {'MET': 1, 'Rijk': 2, 'Cleveland': 3}
    tables = TO().getClasses()


    def getCanonicalTagsList(self) -> json:
        """ Get all the canonical tags from DB and Returns a json obj.

            Returns
            -------
            JSON
                {
                ...,
                tagName:Default value,
                ...
                }
        """
        # select all CanonicalTags by Passing in the Class
        canonicalTags = ORM().selectAll(self.tables["canonicalMetaTag"])
        res = [];
        for c in canonicalTags:
            trimname = removeCanon(c.name)
#            print(trimname,file=sys.stderr)   
#            print(c.name,file=sys.stderr)   
            res.append(trimname)
        return res


    def getCanonicalTagsJSON(self) -> json:
        """ Get all the canonical tags from DB and Returns a json obj.

            Returns
            -------
            JSON
                {
                ...,
                tagName:Default value,
                ...
                }
        """
        # select all CanonicalTags by Passing in the Class
        canonicalTags = ORM().selectAll(self.tables["canonicalMetaTag"])
        res = {}
        for c in canonicalTags:
            trimname = removeCanon(c.name)
            res[trimname] = c.default
        return res
