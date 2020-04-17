import json

import mysql
import sqlalchemy as db
from mysql.connector import Error
from sqlalchemy.orm import sessionmaker

from ORM.DBInfo import DBInfo


class ORM:
    connection = DBInfo().getConnectionInfo()
    engine = db.create_engine(
        'mysql+mysqlconnector://' + connection["username"] + ':' + connection["password"] + '@' +
        connection["address"] + '/' + connection["schema"])
    Session = sessionmaker(bind=engine)
    session = Session();

    fetchTime = 0
    forTime = 0

    # TODO: Password Manger

    def getSession(self):
        return self.session

    def selectAll(self, TOClass):
        result = self.session.query(TOClass).all()
        return result

    def insert(self, obj):
        self.session.add(obj)
        self.session.flush()
        return obj.id

    def bulkInsert(self, objArray):
        self.session.bulk_save_objects(objArray)
        self.session.flush()
        return objArray[0].id

    def update(self, object):
        return

    def delete(self, obj):
        self.session.delete(obj)
        self.session.flush()
        return obj.id

    def commitClose(self):
        self.session.commit()
        self.session.close()

    def executeSelect(self, query, param):
        import time

        t0 = time.time()

        try:
            connection = mysql.connector.connect(
                host=self.connection["address"],
                user=self.connection["username"],
                passwd=self.connection["password"],
                database=self.connection["schema"]
            )
            cursor = connection.cursor()
            cursor.execute(query, param)
            records = cursor.fetchall()
            fieldNames = [i[0] for i in cursor.description]

            t1 = time.time()

            self.fetchTime = t1 - t0

            t0 = time.time()
            jsonRes = {'total': len(records), 'data': []}
            for r in records:
                row = {}
                for i in range(len(fieldNames)):
                    row[fieldNames[i]] = [r[i]]
                jsonRes['data'].append(row)
            t1 = time.time()

            self.forTime = t1 - t0
            jsonRes["fetch"] = self.fetchTime
            jsonRes["for"] = self.forTime

        except Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if (connection.is_connected()):
                connection.close()
                cursor.close()
        return jsonRes

    def batchInsert(self, data, query):
        try:
            connection = mysql.connector.connect(
                host=self.connection["address"],
                user=self.connection["username"],
                passwd=self.connection["password"],
                database=self.connection["schema"]
            )
            cursor = connection.cursor()
            cursor.executemany(query, data)
            # affected_rows = cursor.rowcount

            # print("Number of rows affected : {}".format(affected_rows))
            connection.commit()

        except Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if (connection.is_connected()):
                connection.close()
                cursor.close()

