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


def getAllCollections(limit):
    result={}
    try:
        connection = mysql.connector.connect(
            host="artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com",
            user="artmaster",
            passwd="ArtMaster51",
            database="artmaster"
        )
        
        cursor = connection.cursor()
        if limit==-1:
          sql_select_Query = "select * from collection"
          cursor.execute(sql_select_Query)
        else:
          sql_select_Query = "select * from collection LIMIT %s"
          cursor.execute(sql_select_Query,(int(limit),))
        records = cursor.fetchall()
        result["total"] = cursor.rowcount
        rows=[]
        for row in records:
            rowInfo={}
            rowInfo["id"]=row[0]
            rowInfo["name"]=row[1]
            rowInfo["timeStamp"]=row[2]
            rows.append(rowInfo)
        result["data"]=rows
    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
    return result


def getCollectionByID(id):
    result={}
    try:
        connection = mysql.connector.connect(
            host="artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com",
            user="artmaster",
            passwd="ArtMaster51",
            database="artmaster"
        )

        sql_select_Query = "select * from collection where id= %s "
        cursor = connection.cursor()
        cursor.execute(sql_select_Query,(id,))
        records = cursor.fetchall()
        result["total"] = cursor.rowcount
        rows=[]
        for row in records:
            rowInfo={}
            rowInfo["id"]=row[0]
            rowInfo["name"]=row[1]
            rowInfo["timeStamp"]=row[2]
            rows.append(rowInfo)
        result["data"]=rows
    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
    return result

def getRangeOfCollections(start,end):
    result={}
    try:
        connection = mysql.connector.connect(
            host="artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com",
            user="artmaster",
            passwd="ArtMaster51",
            database="artmaster"
        )
        
        cursor = connection.cursor()
        sql_select_Query = "select * from collection LIMIT %s,%s"
        cursor.execute(sql_select_Query,(int(start),int(end),))
        records = cursor.fetchall()
        result["total"] = cursor.rowcount
        rows=[]
        for row in records:
            rowInfo={}
            rowInfo["id"]=row[0]
            rowInfo["name"]=row[1]
            rowInfo["timeStamp"]=row[2]
            rows.append(rowInfo)
        result["data"]=rows
    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
    return result


print("Content-Type: text/json\n")
dict = cgiFieldStorageToDict(cgi.FieldStorage())


if 'start' in dict.keys() and 'end' in dict.keys():
    print(json.dumps(getRangeOfCollections(dict["start"],dict["end"]), default=str))
else:
    if 'collectionId' not in dict.keys():
        print(json.dumps({"total": "", "data": [{"id": "", "name": "", "timeStamp": ""}]}))
    else:
        id = dict['collectionId']
        if id == -1:
            print(json.dumps({"total": "", "data": [{"id": "", "name": "", "timeStamp": ""}]}))
        elif id == "all":
            if 'limit' in dict.keys():
              print(json.dumps(getAllCollections(dict["limit"])))
            else:
              print(json.dumps(getAllCollections(-1), default=str))
        else:
            print(json.dumps(getCollectionByID(id), default=str))
