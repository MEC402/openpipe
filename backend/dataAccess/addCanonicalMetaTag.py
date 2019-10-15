#!/bin/python3

from datetime import datetime
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


def insertCanonicalMetaTag(name):
    engine = db.create_engine('mysql+mysqlconnector://artmaster:ArtMaster51@artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com/artmaster')
    connection = engine.connect()
    metadata = db.MetaData()
    canonicalMetaTag = db.Table('canonicalMetaTag', metadata, autoload=True, autoload_with=engine)
    ins = canonicalMetaTag.insert().values(name=name, timestamp=datetime.now())
    result = connection.execute(ins)
    return result.inserted_primary_key


print("Content-Type: text/json\n")
dict = cgiFieldStorageToDict(cgi.FieldStorage())

if 'name' not in dict.keys():
    print(json.dumps({"result": "Fail"}, default=str))
else:
    print(json.dumps({"result":insertCanonicalMetaTag(dict["name"])}))
