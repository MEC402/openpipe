#!/bin/python3

import json
import cgi
import mysql.connector
from datetime import datetime

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


print("Content-Type: text/json\n")


print(json.dumps({"result":insertIntoMetaData()}))
