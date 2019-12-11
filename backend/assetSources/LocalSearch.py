#!/bin/python3

import requests
from multiprocessing.pool import ThreadPool
import mysql.connector
from mysql.connector import Error

class LocalSearch:

    def searchAssets(self, term):
        result = {}
        try:
            connection = mysql.connector.connect(
                host="artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com",
                user="artmaster",
                passwd="ArtMaster51",
                database="artmaster"
            )

            sql_select_Query = "SELECT asset.id FROM metaTag join asset on metaTag.metaDataId=asset.metaDataId where metaTag.value like %s group by asset.id;"
            cursor = connection.cursor()
            cursor.execute(sql_select_Query, ("%"+term+"%",))
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
                host="artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com",
                user="artmaster",
                passwd="ArtMaster51",
                database="artmaster"
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

        pool = ThreadPool(len(assets))
        for assetId in assets:
            results.append(pool.apply_async(self.getAssetMetaData, args=[assetId]))
        pool.close()
        pool.join()
        results = [r.get() for r in results]
        return {"data": results, "total": retrievedAssets['total'], "sourceName": "Local"}
