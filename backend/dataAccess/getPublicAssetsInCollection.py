#!/bin/python3

import json
import mysql.connector
from mysql.connector import Error
import cgi


def cgiFieldStorageToDict(fieldStorage):
    """ Get a plain dictionary rather than the '.value' system used by the
   cgi module's native fieldStorage class. """
    params = {}
    for key in fieldStorage.keys():
        params[key] = fieldStorage[key].value
    return params

def getPublicAsssetsInCollection(collectionId,page,pageSize):
    result = {}
    try:
        connection = mysql.connector.connect(
            host="artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com",
            user="artmaster",
            passwd="ArtMaster51",
            database="artmaster"
        )

        start = (page - 1) * pageSize
        step = pageSize

        sql_select_Query = "SELECT assetId,metaDataId FROM collectionMember JOIN asset ON collectionMember.assetId = asset.id WHERE scope=0 and collectionId = %s limit %s,%s "
        cursor = connection.cursor()
        cursor.execute(sql_select_Query, (collectionId,start,step))
        records = cursor.fetchall()
        result["total"] = cursor.rowcount
        rows = []
        for row in records:
            rowInfo = {"id":[row[0]]}
            metaDataId=row[1]
            sql_select_Query = "select tagName,value from metaTag where metaDataId=%s"
            cursor = connection.cursor()
            cursor.execute(sql_select_Query, (metaDataId,))
            metaTagsRecords = cursor.fetchall()
            for metaTagRow in metaTagsRecords:
                rowInfo[metaTagRow[0]]=[metaTagRow[1]]
            rows.append(rowInfo)
        result["data"] = rows
    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
    return result

print("Content-Type: text/json\n")
dict = cgiFieldStorageToDict(cgi.FieldStorage())

if 'p' not in dict.keys():
    dict['p'] = 1

if 'ps' not in dict.keys():
    dict['ps'] = 10

if 'collectionId' not in dict.keys():
    print(json.dumps({"total": "-1", "data": [{}]}))
else:
    id = dict['collectionId']
    print(json.dumps(getPublicAsssetsInCollection(id,int(dict["p"]), int(dict["ps"])), default=str))