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


def getAllTags():
    engine = db.create_engine(
        'mysql+mysqlconnector://artmaster:ArtMaster51@artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com/artmaster')
    connection = engine.connect()
    metadata = db.MetaData()
    canonicalMetaTag = db.Table('canonicalMetaTag', metadata, autoload=True, autoload_with=engine)
    query = db.select([canonicalMetaTag])
    result = connection.execute(query).fetchall()
    res = {}
    for row in result:
        res[row[1]] =[row[2]]
    return res


print("Content-Type: text/json\n")
print(json.dumps(getAllTags(), default=str))