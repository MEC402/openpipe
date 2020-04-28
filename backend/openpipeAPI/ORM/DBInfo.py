class DBInfo:
    data = {"production": {"address": "artmaster-production.c2p1mleoiwlk.us-west-2.rds.amazonaws.com",
                           "schema": "artmaster",
                           "username": "artmaster",
                           "password": "ArtMaster51"},
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
        return self.data["dev"]
