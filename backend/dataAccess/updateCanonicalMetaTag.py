#!/bin/python3

import json
import cgi
import sqlalchemy as db


def cgiFieldStorageToDict(fieldStorage):
    """ Get a plain dictionary rather than the '.value' system used by the
   cgi module's native fieldStorage class. """
    params = {}
    for key in fieldStorage.keys():
        params[key] = fieldStorage[key].value
    return params


def updateTag(id,name):
    engine = db.create_engine(
        'mysql+mysqlconnector://artmaster:ArtMaster51@artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com/artmaster')
    connection = engine.connect()
    metadata = db.MetaData()
    canonicalMetaTag = db.Table('canonicalMetaTag', metadata, autoload=True, autoload_with=engine)

    updateQuery = canonicalMetaTag.update().\
            where(canonicalMetaTag.c.id==id).\
            values(name=name)

    result = connection.execute(updateQuery)
    return result


print("Content-Type: text/json\n")
dict = cgiFieldStorageToDict(cgi.FieldStorage())

if 'id' not in dict.keys() or 'name' not in dict.keys():
    print(json.dumps({"result":"Fail"}))
else:
    print(json.dumps(updateTag(dict["id"],dict["name"]), default=str))


