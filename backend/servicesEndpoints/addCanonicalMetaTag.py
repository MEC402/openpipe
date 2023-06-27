#!/bin/python3

from datetime import datetime
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


def insertCanonicalMetaTag(name):
    connection_string = f'mysql+mysqlconnector://{dbusername_urlencoded}:{dbpassword_urlencoded}@{dbhost_urlencoded}/{dbschema_urlencoded}'
    engine = db.create_engine(connection_string)
#        'mysql+mysqlconnector://artmaster:ArtMaster51@artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com/artmaster')
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
