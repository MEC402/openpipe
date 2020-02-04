from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import reflection
from sqlalchemy.orm import create_session
from sqlalchemy.ext.automap import automap_base

import inspect


class TO:
    __classes = {}

    def builClassesFromDB(self):
        engine = create_engine(
            'mysql+mysqlconnector://artmaster:ArtMaster51@artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com/artmaster')
        metadata = MetaData()

        Base = automap_base()
        Base.prepare(engine, reflect=True)

        session = create_session(bind=engine)
        for mappedclass in Base.classes:
            self.__classes[mappedclass.__name__] = mappedclass


    def getClasses(self):
        if len(self.__classes.keys())<=0:
            self.builClassesFromDB()
        return self.__classes


# to = TO()
# print(to.getClasses())
# print(to.getClasses())

# https://www.freecodecamp.org/news/dynamic-class-definition-in-python-3e6f7d20a381/

     # metadata.reflect(bind=engine)
        #
        # insp = reflection.Inspector.from_engine(engine)
        # tables=insp.get_table_names()
        # for t in tables:
        #
        #     print(insp.get_columns(t))
        # attributes = inspect.getmembers(self.__classes['asset'], lambda a: not (inspect.isroutine(a)))
        # print([a for a in attributes if not (a[0].startswith('__') and a[0].endswith('__'))])