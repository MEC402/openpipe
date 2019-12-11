from MetMuseum import MetMuseum
from RijksMuseum import RijksMuseum
from ClevelandMuseum import ClevelandMuseum
import sqlalchemy as db
import mysql.connector
from datetime import datetime


def insertIntoMetaTags(data,mid):
    try:
        connection = mysql.connector.connect(
            host="artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com",
            user="artmaster",
            passwd="ArtMaster51",
            database="artmaster"
        )
        cursor = connection.cursor(prepared=True)

        metaDataId = ''
        for key in data.keys():
            if str(key).find("openpipe")>=0:
                value = data[key][0]
            else:
                value = data[key]
            sql_insert_query = """ INSERT INTO metaTag (metaDataId,tagName,value,timestamp) VALUES (%s,%s,%s,%s)"""
            insert_tuple_1 = (mid, key, str(value), datetime.now())
            cursor.execute(sql_insert_query, insert_tuple_1)
            connection.commit()
        return {"result": "Success"}

    except mysql.connector.Error as error:
        return {"result": "Failed to insert record into Laptop table {}".format(error)}
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

def insertIntoMetaData():
    try:
        connection = mysql.connector.connect(
            host="artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com",
            user="artmaster",
            passwd="ArtMaster51",
            database="artmaster"
        )

        cursor = connection.cursor(prepared=True)
        sql_insert_query = """ INSERT INTO metaData (timestamp) VALUES (%s)"""
        cursor.execute(sql_insert_query, (datetime.now(),))
        connection.commit()
        return cursor.lastrowid

    except mysql.connector.Error as error:
        return {"result": "Fail"}
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

def insertIntoCollectionMember(assetId,collectionId,searchTerm):
    try:
        connection = mysql.connector.connect(
            host="artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com",
            user="artmaster",
            passwd="ArtMaster51",
            database="artmaster"
        )

        cursor = connection.cursor(prepared=True)
        sql_insert_query = """ INSERT INTO collectionMember(assetId, collectionId, searchTerm, timestamp) VALUES (%s, %s, %s, %s);"""
        insert_tuple_1 = (assetId,collectionId,searchTerm, datetime.now())
        cursor.execute(sql_insert_query, insert_tuple_1)
        connection.commit()
        return {"result": cursor.lastrowid}

    except mysql.connector.Error as error:
        return {"result": "Fail"}
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

def insertIntoAsset(shortName, uri, idAtSource, sourceId, metaDataId,scope):
    try:
        connection = mysql.connector.connect(
            host="artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com",
            user="artmaster",
            passwd="ArtMaster51",
            database="artmaster"
        )

        cursor = connection.cursor(prepared=True)
        sql_insert_query = """ INSERT INTO asset (shortName, uri, IdAtSource, sourceId, metaDataId, scope, timestamp) VALUES (%s, %s, %s, %s, %s, %s,%s)"""
        insert_tuple_1 = (shortName, uri, idAtSource, sourceId, metaDataId,scope, datetime.now())
        cursor.execute(sql_insert_query, insert_tuple_1)
        connection.commit()
        return cursor.lastrowid

    except mysql.connector.Error as error:
        return {"result": "Fail"}
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

def getSchema(type):
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



def searchMuseum(term):
    print("hi")
    ms = MetMuseum(getSchema(1))
    for l in range(1,10):
        print(l)
        result = ms.getData(term, l, 100)
        print(result)
        ind = 0
        for i in result["data"]:
            print(ind)
            mid = insertIntoMetaData()
            aid = insertIntoAsset(i["openpipe_canonical_title"][0], "", i["openpipe_canonical_id"][0], 1, mid, 0)
            insertIntoCollectionMember(aid, 17, term)
            print(insertIntoMetaTags(i, mid))
            ind = ind + 1
# rembrandt
searchMuseum("early middle ages")