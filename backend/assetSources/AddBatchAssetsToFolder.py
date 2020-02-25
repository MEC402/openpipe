from multiprocessing.pool import ThreadPool

from MetMuseum import MetMuseum
from RijksMuseum import RijksMuseum
from ClevelandMuseum import ClevelandMuseum
import sqlalchemy as db
import mysql.connector
from datetime import datetime


def insertIntoMetaTags(data,mid):
    try:
        connection = mysql.connector.connect(
            host="artmaster-production.c2p1mleoiwlk.us-west-2.rds.amazonaws.com",
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
            host="artmaster-production.c2p1mleoiwlk.us-west-2.rds.amazonaws.com",
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
            host="artmaster-production.c2p1mleoiwlk.us-west-2.rds.amazonaws.com",
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
            host="artmaster-production.c2p1mleoiwlk.us-west-2.rds.amazonaws.com",
            user="artmaster",
            passwd="ArtMaster51",
            database="artmaster"
        )

        cursor = connection.cursor(prepared=True)
        sql_insert_query = """ INSERT INTO asset (shortName, uri, IdAtSource, sourceId, metaDataId, scope) VALUES (%s, %s, %s, %s, %s, %s)"""
        insert_tuple_1 = (shortName, uri, idAtSource, sourceId, metaDataId,scope)
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
        'mysql+mysqlconnector://artmaster:ArtMaster51@artmaster-production.c2p1mleoiwlk.us-west-2.rds.amazonaws.com/artmaster')
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



def searchMuseum(term,collectionid):
    print("hi")
    ms = ClevelandMuseum(getSchema(1))
    sourceID=3
    r=20
    pool = ThreadPool(r)
    for l in range(1,r):
        getInfo(l,term,collectionid,sourceID,ms)
    # for l in range(1,r):
    #     pool.apply_async(getInfo, args=[l,term,collectionid,sourceID,ms])
    # pool.close()
    # pool.join()


def addAsset(i,term,collectionid,sourceID):
    print(i["openpipe_canonical_title"][0])
    mid = insertIntoMetaData()
    aid = insertIntoAsset(i["openpipe_canonical_title"][0], "", i["openpipe_canonical_id"][0], sourceID, mid, 0)
    insertIntoCollectionMember(aid, collectionid, term)
    print(i["openpipe_canonical_title"][0]+":   "+insertIntoMetaTags(i, mid))

def getInfo(pageNumber,term,collectionid,sourceID,ms):
    print("pageNumber= "+ str(pageNumber))
    result = ms.getData(term, pageNumber, 100)
    print(result)
    pool = ThreadPool(len(result["data"]))
    for i in result["data"]:
        pool.apply_async(addAsset, args=[i, term, collectionid,sourceID])
    pool.close()
    pool.join()

# rembrandt
searchMuseum("paris ",20)