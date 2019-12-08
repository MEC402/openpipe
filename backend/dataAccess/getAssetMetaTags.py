#!/bin/python3

import json
import cgi
import mysql.connector
from mysql.connector import Error




def cgiFieldStorageToDict(fieldStorage):
    """ Get a plain dictionary rather than the '.value' system used by the
   cgi module's native fieldStorage class. """
    params = {}
    for key in fieldStorage.keys():
        params[key] = fieldStorage[key].value
    return params


def getAssetMetaTags(id):
    result = {}
    try:
        connection = mysql.connector.connect(
            host="artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com",
            user="artmaster",
            passwd="ArtMaster51",
            database="artmaster"
        )

        sql_select_Query = "select metaTag.id, asset.id as assetId, tagName, value from asset join metaTag on asset.metaDataId=metaTag.metaDataId where asset.id=%s"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query, (id,))
        records = cursor.fetchall()
        result["total"] = cursor.rowcount
        rows = []
        for row in records:
            rowInfo = {}
            rowInfo["id"] = [row[0]]
            rowInfo["assetId"] = [row[1]]
            rowInfo["tagName"] = [row[2]]
            rowInfo["value"] = [row[3]]
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

if 'assetId' not in dict.keys():
    print(json.dumps({"total": "", "data": [{"id": [""], "name": [""], "timeStamp": [""]}]}))
else:
    id = dict['assetId']
    print(json.dumps(getAssetMetaTags(id), default=str))

