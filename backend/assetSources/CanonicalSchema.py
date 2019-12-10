import sqlalchemy as db
class CanonicalSchema:
    def getSchema(self,type):
        engine = db.create_engine(
            'mysql+mysqlconnector://artmaster:ArtMaster51@artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com/artmaster')
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