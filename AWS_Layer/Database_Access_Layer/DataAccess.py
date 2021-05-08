import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from DBInfo import DBInfo


class DataAccess:
    connection = DBInfo().getConnectionInfo()
    engine = db.create_engine(
        'mysql+mysqlconnector://' + connection["username"] + ':' + connection["password"] + '@' +
        connection["address"] + '/' + connection["schema"])
    Session = sessionmaker(bind=engine)
    session = Session()

    def getSession(self):
        return self.session

    def commitClose(self):
        self.session.commit()
        self.session.close()
