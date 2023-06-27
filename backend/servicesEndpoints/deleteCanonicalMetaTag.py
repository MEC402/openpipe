#!/bin/python3

import json
import cgi
import sqlalchemy as db

from urllib.parse import quote
from dotenv import load_dotenv
import os

load_dotenv()

environment = os.getenv('ENVIRONMENT')

if environment == 'dev':
    dbhost_urlencoded = quote(os.getenv('DB_HOSTNAME_DEV'))
    dbusername_urlencoded = quote(os.getenv('DB_USERNAME_DEV'))
    dbpassword_urlencoded = quote(os.getenv('DB_PASSWORD_DEV'))
    dbschema_urlencoded = quote(os.getenv('DB_SCHEMA_DEV'))

elif environment == 'prod':
    dbhost_urlencoded = quote(os.getenv('DB_HOSTNAME_PROD'))
    dbusername_urlencoded = quote(os.getenv('DB_USERNAME_PROD'))
    dbpassword_urlencoded = quote(os.getenv('DB_PASSWORD_PROD'))
    dbschema_urlencoded = quote(os.getenv('DB_SCHEMA_PROD'))

def cgiFieldStorageToDict(fieldStorage):
    """ Get a plain dictionary rather than the '.value' system used by the
   cgi module's native fieldStorage class. """
    params = {}
    for key in fieldStorage.keys():
        params[key] = fieldStorage[key].value
    return params


def deleteTag(id):
    connection_string = f'mysql+mysqlconnector://{dbusername_urlencoded}:{dbpassword_urlencoded}@{dbhost_urlencoded}/{dbschema_urlencoded}'
    engine = db.create_engine(connection_string)
#        'mysql+mysqlconnector://artmaster:ArtMaster51@artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com/artmaster')
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