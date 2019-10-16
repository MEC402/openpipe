#!/bin/python3

import json
import cgi
import mysql.connector
from datetime import datetime
import sys


def insertIntoMetaTags():
    postBody = sys.stdin.read()
    data = json.loads(postBody)
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
            if key == 'metaDataId':
                metaDataId = data[key]
            else:
                value = data[key]
                sql_insert_query = """ INSERT INTO metaTag (metaDataId,tagName,value,timestamp) VALUES (%s,%s,%s,%s)"""
                insert_tuple_1 = (metaDataId, key, value, datetime.now())
                cursor.execute(sql_insert_query, insert_tuple_1)
                connection.commit()
        return {"result": "Success"}

    except mysql.connector.Error as error:
        return {"result": "Failed to insert record into Laptop table {}".format(error)}
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()


print("Content-Type: text/json\n")
print(json.dumps(insertIntoMetaTags(), default=str))
