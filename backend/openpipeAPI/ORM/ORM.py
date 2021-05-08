import json

import mysql
import sqlalchemy as db
from mysql.connector import Error
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool


import time

from backend.openpipeAPI.ORM.DBInfo import DBInfo


class ORM:
    connection = DBInfo().getConnectionInfo()
    engine = db.create_engine(
        'mysql+mysqlconnector://' + connection["username"] + ':' + connection["password"] + '@' +
        connection["address"] + '/' + connection["schema"])
    Session = sessionmaker(bind=engine)
    session = Session();

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

    def executeSelect(self, query):
        jsonRes = {"total": 0, "data": [], "error": "executeSelect"}
        try:
            connection = mysql.connector.connect(
                host=self.connection["address"],
                user=self.connection["username"],
                passwd=self.connection["password"],
                database=self.connection["schema"]
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
            #            print("Error reading data from MySQL table", e)
            pass

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
            #            print("Error reading data from MySQL table", e)
            pass

        finally:
            if (connection.is_connected()):
                connection.close()
                cursor.close()

# to=TO()
# orm=ORM()
# print(to.getClasses())
# r=orm.selectAll(to.getClasses()['canonicalMetaTag'])
# for a in r:
#     print(a.default)
