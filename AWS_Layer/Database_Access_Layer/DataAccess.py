import mysql
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from DBInfo import DBInfo
from mysql.connector import Error


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

    def simpConnect(self):
        acon = mysql.connector.connect(
            host=self.connection["address"],
            user=self.connection["username"],
            passwd=self.connection["password"],
            database=self.connection["schema"]
        )
        return acon

    def executeSelectPersist(self, query, acon):
        jsonRes = {"total": 0, "data": [], "error": "executeSelect"}
        try:
            cursor = acon.cursor()
            cursor.execute(query, )
            records = cursor.fetchall()
            fieldNames = [i[0] for i in cursor.description]
            tlist = jsonRes['data']

            jsonRes = {'total': len(records), 'data': []}
            frange = range(len(fieldNames))
            for r in records:
                row = {}
                for i in frange:
                    row[fieldNames[i]] = [r[i]]
                tlist.append(row)
            #                jsonRes['data'].append(row)
            #            t0 = time.time()
            jsonRes['data'] = tlist
        #            t1 = time.time()

        except Error as e:
            #            print("Error reading data from MySQL table", e)
            pass

        finally:
            cursor.close()
        return jsonRes

    def executeSelect(self, query, params):
        try:
            connection = mysql.connector.connect(
                host=self.connection["address"],
                user=self.connection["username"],
                passwd=self.connection["password"],
                database=self.connection["schema"]
            )
            cursor = connection.cursor()
            cursor.execute(query, params)
            records = cursor.fetchall()
        except Error as e:
            #            print("Error reading data from MySQL table", e)
            pass

        finally:
            if (connection.is_connected()):
                connection.close()
                cursor.close()
        return records
