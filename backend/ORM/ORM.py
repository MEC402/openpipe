import mysql
import sqlalchemy as db
from mysql.connector import Error
from sqlalchemy.orm import sessionmaker


class ORM:
    address = {'dev': "artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com",
               'production': "artmaster-production.c2p1mleoiwlk.us-west-2.rds.amazonaws.com"}
    databaseName = "artmaster"
    databaseHostAddress = address['dev']
    databaseUserName = "artmaster"
    databasePassword = "ArtMaster51"
    # TODO: Make this singleton
    # TODO: Password Manger
    def getSession(self):
        engine = db.create_engine(
            'mysql+mysqlconnector://' + self.databaseUserName + ':' + self.databasePassword + '@' + self.databaseHostAddress + '/' + self.databaseName)
        Session = sessionmaker(bind=engine)
        return Session()

    def selectAll(self, TOClass):
        session = self.getSession()
        result = session.query(TOClass).all()
        return result

    def insert(self, obj):
        session = self.getSession()
        result = session.add(obj)
        result = session.commit()
        session.flush()
        return obj.id

    def update(self, object):
        return

    def delete(self, obj):
        return

    def executeSelect(self, query):
        try:
            connection = mysql.connector.connect(
                host=self.databaseHostAddress,
                user=self.databaseUserName,
                passwd=self.databasePassword,
                database=self.databaseName
            )
            cursor = connection.cursor()
            cursor.execute(query, )
            records = cursor.fetchall()
            fieldNames = [i[0] for i in cursor.description]

            jsonRes = {'total': len(records), 'data': []}
            for r in records:
                row = {}
                for i in range(len(fieldNames)):
                    row[fieldNames[i]] = [r[i]]
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
