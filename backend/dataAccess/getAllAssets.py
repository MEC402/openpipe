#!/bin/python3

import json
import mysql.connector
from mysql.connector import Error
import cgi



def getAllAssets():
    result = {}
    try:
        connection = mysql.connector.connect(
            host="artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com",
            user="artmaster",
            passwd="ArtMaster51",
            database="artmaster"
        )

        sql_select_Query = "SELECT id,metaDataId,shortName FROM asset limit 500;"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        result["total"] = cursor.rowcount
        rows = []
        for row in records:
            rowInfo = {"id":row[0],"metaDataId":row[1], "name":row[2]}
            metaDataId=row[1]
            sql_select_Query = "select tagName,value from metaTag where metaDataId=%s"
            if (metaDataId):
                cursor = connection.cursor()
                cursor.execute(sql_select_Query, (metaDataId,))
                metaTagsRecords = cursor.fetchall()
                for metaTagRow in metaTagsRecords:
                    rowInfo[metaTagRow[0]]=metaTagRow[1]
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
print(json.dumps(getAllAssets(), default=str))