from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

from DBInfo import DBInfo


class TO:
    __classes = {}

    def builClassesFromDB(self):
        connection = DBInfo().getConnectionInfo()
        engine = create_engine(
            'mysql+mysqlconnector://' + connection["username"] + ':' + connection["password"] + '@' + connection[
                "address"] + '/' + connection["schema"])

        Base = automap_base()
        Base.prepare(engine, reflect=True)

        for mappedclass in Base.classes:
            self.__classes[mappedclass.__name__] = mappedclass

    def getClasses(self):
        if len(self.__classes.keys()) <= 0:
            self.builClassesFromDB()
        return self.__classes
