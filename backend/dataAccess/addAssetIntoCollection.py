#!/bin/python3

import json
import cgi
import mysql.connector
from datetime import datetime


def cgiFieldStorageToDict(fieldStorage):
    """ Get a plain dictionary rather than the '.value' system used by the
    cgi module's native fieldStorage class. """
    params = {}
    for key in fieldStorage.keys():
        params[key] = fieldStorage[key].value
    return params


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


print("Content-Type: text/json\n")
dict = cgiFieldStorageToDict(cgi.FieldStorage())

if 'assetId' not in dict.keys() and 'collectionId' not in dict.keys() and 'searchTerm' not in dict.keys():
    print(json.dumps({"result": "Fail"}, default=str))
else:
    print(json.dumps(insertIntoCollectionMember(dict["assetId"],dict["collectionId"],dict["searchTerm"]), default=str))
