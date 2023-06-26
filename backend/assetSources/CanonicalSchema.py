import sqlalchemy as db

from urllib.parse import quote
import os
from dotenv import load_dotenv

load_dotenv()

dbhost_urlencoded = quote(os.getenv('DB_HOSTNAME'))
dbusername_urlencoded = quote(os.getenv('DB_USERNAME'))
dbpassword_urlencoded = quote(os.getenv('DB_PASSWORD'))
dbschema_urlencoded = quote(os.getenv('DB_SCHEMA'))

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