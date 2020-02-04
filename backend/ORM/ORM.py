from sqlalchemy.orm import sessionmaker
import sqlalchemy as db
from TO import TO

class ORM:
    # TODO: Make this singleton
    # TODO: Password Manger
    def getSession(self):
        engine = db.create_engine(
            'mysql+mysqlconnector://artmaster:ArtMaster51@artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com/artmaster')
        Session = sessionmaker(bind=engine)
        return Session()

    def selectAll(self, TOClass):
        session = self.getSession()
        result = session.query(TOClass).all()
        return result

    def insert(self, obj):
        return

    def update(self, object):
        return

    def delete(self,obj):
        return


to=TO()
orm=ORM()
print(to.getClasses())
r=orm.selectAll(to.getClasses()['canonicalMetaTag'])
for a in r:
    print(a.default)