import sqlalchemy as db


class TO:
    def builClassesFromDB(self):
        engine = db.create_engine(
            'mysql+mysqlconnector://artmaster:ArtMaster51@artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com/artmaster')
        # connection = engine.connect()
        metadata = db.MetaData()
        print (metadata)


to = TO()
to.builClassesFromDB()

# https://www.freecodecamp.org/news/dynamic-class-definition-in-python-3e6f7d20a381/
