import os
from dotenv import load_dotenv

load_dotenv()

environment = os.getenv('ENVIRONMENT')

if environment == 'dev':
    dbhost = os.getenv('DB_HOSTNAME_DEV')
    dbusername = os.getenv('DB_USERNAME_DEV')
    dbpassword = os.getenv('DB_PASSWORD_DEV')
    dbschema = os.getenv('DB_SCHEMA_DEV')
elif environment == 'prod':
    dbhost = os.getenv('DB_HOSTNAME_PROD')
    dbusername = os.getenv('DB_USERNAME_PROD')
    dbpassword = os.getenv('DB_PASSWORD_PROD')
    dbschema = os.getenv('DB_SCHEMA_PROD')

class DBInfo:
    data = {"production": {"address": dbhost,
                           "schema": dbschema,
                           "username": dbusername,
                           "password": dbpassword},
            "dev": {"address": dbhost,
                    "schema": dbschema,
                    "username": dbusername,
                    "password": dbpassword},
            "host": {"address": "localhost",
                    "schema": "artmaster",
                    "username": "root",
                    "password": "artMaster51!"}
                    }

    def getConnectionInfo(self):
        return self.data["production"]
