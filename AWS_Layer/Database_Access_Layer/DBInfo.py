import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv('DB_HOSTNAME')
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
schema = os.getenv('DB_SCHEMA')

class DBInfo:
    """Maintains DB credentials from environment variables"""
    data = {"production": {"address": host,
                           "schema": schema,
                           "username": username,
                           "password": password},
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
