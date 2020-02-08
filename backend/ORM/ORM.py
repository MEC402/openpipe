import mysql
import sqlalchemy as db
from mysql.connector import Error
from sqlalchemy.orm import sessionmaker


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
        session = self.getSession()
        result = session.add(obj)
        result=session.commit()
        print(result)
        session.flush()
        return result

    def update(self, object):
        return

    def delete(self, obj):
        return

    def executeSelect(self, query):
        try:
            connection = mysql.connector.connect(
                host="artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com",
                user="artmaster",
                passwd="ArtMaster51",
                database="artmaster"
            )
            cursor = connection.cursor()
            cursor.execute(query, )
            records = cursor.fetchall()
            fieldNames = [i[0] for i in cursor.description]

            jsonRes = {'total': len(records), 'data': []}
            for r in records:
                row = {}
                for i in range(len(fieldNames)):
                    row[fieldNames[i]] = r[i]
                jsonRes['data'].append(row)

        except Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if (connection.is_connected()):
                connection.close()
                cursor.close()
        return jsonRes

# to=TO()
# orm=ORM()
# print(to.getClasses())
# r=orm.selectAll(to.getClasses()['canonicalMetaTag'])
# for a in r:
#     print(a.default)
