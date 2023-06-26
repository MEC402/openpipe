import os
from dotenv import load_dotenv

load_dotenv()

dbhost = os.getenv('DB_HOSTNAME')
dbusername = os.getenv('DB_USERNAME')
dbpassword = os.getenv('DB_PASSWORD')
dbschema = os.getenv('DB_SCHEMA')

class DBInfo:
    """Maintains DB credentials from environment variables"""
    data = {"production": {"address": dbhost,
                           "schema": dbschema,
                           "username": dbusername,
                           "password": dbpassword},
            "dev": {"address": "artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com",
                    "schema": "artmaster",
                    "username": "artmaster",
                    "password": "ArtMaster51"},
            "host": {"address": "localhost",
                    "schema": "artmaster",
                    "username": "root",
                    "password": "artMaster51!"}
                    }

    def getConnectionInfo(self):
        return self.data["production"]
