#!/bin/python3

import requests
from multiprocessing.pool import ThreadPool
import mysql.connector
from mysql.connector import Error

from dotenv import load_dotenv
import os

load_dotenv()

environment = os.getenv('ENVIRONMENT')

if environment == 'dev':
    dbhost = os.getenv('DB_HOSTNAME_DEV')
    dbusername = os.getenv('DB_USERNAME_DEV')
    dbpassword = os.getenv('DB_PASSWORD_DEV')
    dbschema = os.getenv('DB_SCHEMA_DEV')
elif environment == 'prod':
    dbhost = os.getenv('DB_HOSTNAME_PROD')
    dbusername = os.getenv('DB_USERNAME_PROD')
    dbpassword = os.getenv('DB_PASSWORD_PROD')
    dbschema = os.getenv('DB_SCHEMA_PROD')

class LocalSearch:

    def setName(self,aname):
        self.name = aname

    def searchAssets(self, term):
        result = {}
        try:
            connection = mysql.connector.connect(
                host=dbhost,
                user=dbusername,
                passwd=dbpassword,
                database=dbschema
            )

            sql_select_Query = "SELECT asset.id, MATCH(metaTag.tagName,metaTag.value) AGAINST(%s IN NATURAL LANGUAGE MODE) as relevance FROM metaTag join asset on metaTag.metaDataId=asset.metaDataId where MATCH(metaTag.tagName,metaTag.value) AGAINST(%s IN NATURAL LANGUAGE MODE)  ORDER BY relevance DESC"
            cursor = connection.cursor()
            cursor.execute(sql_select_Query, (term,term))
            records = cursor.fetchall()
            result["total"] = cursor.rowcount
            rows = []
            for row in records:
                rows.append(row[0])
            result["assetIDs"] = rows
        except Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if (connection.is_connected()):
                connection.close()
                cursor.close()
        return result

    def getAssetMetaData(self, id):
        result = {}
        try:
            connection = mysql.connector.connect(
                host=dbhost,
                user=dbusername,
                passwd=dbpassword,
                database=dbschema
            )

            sql_select_Query = "select tagName, value from asset join metaTag on asset.metaDataId=metaTag.metaDataId where asset.id=%s"
            cursor = connection.cursor()
            cursor.execute(sql_select_Query, (id,))
            records = cursor.fetchall()
            result["assetID"] = id
            for row in records:
                rowInfo = {}
                if str(row[0]).find("openpipe") >= 0:
                    result[row[0]] = [row[1]]
                else:
                    result[row[0]] = row[1]
        except Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if (connection.is_connected()):
                connection.close()
                cursor.close()
        return result


    def getData(self, q, page, pageSize):
        results = []
        retrievedAssets = self.searchAssets(q)

        start = (page - 1) * pageSize
        step = pageSize

        if int(start) > retrievedAssets['total']:
            start = retrievedAssets['total'] - 1
        if int(start) + int(step) > retrievedAssets['total']:
            step = retrievedAssets['total'] - int(start) - 1
        assets = retrievedAssets['assetIDs'][int(start):int(start) + int(step)]
        if len(retrievedAssets['assetIDs'])>0:
            pool = ThreadPool(len(assets))
            for assetId in assets:
                results.append(pool.apply_async(self.getAssetMetaData, args=[assetId]))
            pool.close()
            pool.join()
            results = [r.get() for r in results]
            return {"data": results, "total": retrievedAssets['total'], "sourceName": "Local"}
        else:
            return {"data": [], "total": 0, "sourceName": "Local"}
