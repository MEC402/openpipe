#!/bin/python3

import json
import cgi
from multiprocessing.pool import ThreadPool
import sqlalchemy as db
from MetMuseum import MetMuseum
from RijksMuseum import RijksMuseum
from ClevelandMuseum import ClevelandMuseum


def cgiFieldStorageToDict(fieldStorage):
    """ Get a plain dictionary rather than the '.value' system used by the cgi module's native fieldStorage class. """
    params = {}
    for key in fieldStorage.keys():
        params[key] = fieldStorage[key].value
    return params


def getSchema():
    engine = db.create_engine(
        'mysql+mysqlconnector://artmaster:ArtMaster51@artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com/artmaster')
    connection = engine.connect()
    metadata = db.MetaData()
    canonicalMetaTag = db.Table('canonicalMetaTag', metadata, autoload=True, autoload_with=engine)
    query = db.select([canonicalMetaTag])
    result = connection.execute(query).fetchall()
    res = {}
    for row in result:
        res[row[1]] = [row[2]]
    return res


print("Content-Type: text/json\n")
schema = getSchema()

dict = cgiFieldStorageToDict(cgi.FieldStorage())

# dict = {'q': 'cats',
#         'p': 1,
#         'ps': 20}

if 'p' not in dict.keys():
    dict["p"] = 1

if 'ps' not in dict.keys():
    dict["ps"] = 10

if int(dict["p"]) < 1:
    dict["p"] = 1

if int(dict["ps"]) < 1:
    dict["ps"] = 1

if 'q' not in dict.keys():
    print(json.dumps([{}]))

else:
    threads = []
    museums = []
    results = []

    met = MetMuseum(schema.copy())
    museums.append(met)
    rijks = RijksMuseum(schema.copy())
    museums.append(rijks)
    cleveland = ClevelandMuseum(schema.copy())
    museums.append(cleveland)
    # results.extend(met.getData(dict["q"], dict["p"], dict["ps"]))
    # results.extend(rijks.getData(dict["q"], dict["p"], dict["ps"]))
    # results.extend(cleveland.getData(dict["q"], dict["p"], dict["ps"]))

    pool = ThreadPool(len(museums))
    for museum in museums:
        threads.append(pool.apply_async(museum.getData, args=[dict["q"], int(dict["p"]), int(dict["ps"])]))
    pool.close()
    pool.join()

    for t in threads:
        results.extend(t.get())

    response = {"total": len(results),
                "data": results}

    print(json.dumps(response))
