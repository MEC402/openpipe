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


def deleteTag(id):
    engine = db.create_engine(
        'mysql+mysqlconnector://artmaster:ArtMaster51@artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com/artmaster')
    connection = engine.connect()
    metadata = db.MetaData()
    canonicalMetaTag = db.Table('canonicalMetaTag', metadata, autoload=True, autoload_with=engine)
    deleletQuery = canonicalMetaTag.delete().where(canonicalMetaTag.c.id == id)
    result = connection.execute(deleletQuery)
    return result


print("Content-Type: text/json\n")
dict = cgiFieldStorageToDict(cgi.FieldStorage())


if 'id' not in dict.keys():
    print(json.dumps({"result":"Fail"}))
else:
    print(json.dumps(deleteTag(dict["id"]), default=str))