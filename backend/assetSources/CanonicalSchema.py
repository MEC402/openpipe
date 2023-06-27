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

class CanonicalSchema:
    def getSchema(self,type):
        connection_string = f'mysql+mysqlconnector://{dbusername_urlencoded}:{dbpassword_urlencoded}@{dbhost_urlencoded}/{dbschema_urlencoded}'
        engine = db.create_engine(connection_string)
        #    'mysql+mysqlconnector://artmaster:ArtMaster51@artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com/artmaster')
        connection = engine.connect()
        metadata = db.MetaData()
        canonicalMetaTag = db.Table('canonicalMetaTag', metadata, autoload=True, autoload_with=engine)
        query = db.select([canonicalMetaTag])
        result = connection.execute(query).fetchall()
        res = {}
        for row in result:
            if type == 0:
                res[row[1]] = [""]
            else:
                res[row[1]] = [row[2]]
        return res