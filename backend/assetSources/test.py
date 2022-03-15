# import json
# import cgi
# import mysql.connector
# from datetime import datetime
# import sys
import sqlalchemy as db


#
# def insertIntoMetaTags(i):
#     try:
#         connection = mysql.connector.connect(
#             host="artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com",
#             user="artmaster",
#             passwd="ArtMaster51",
#             database="artmaster"
#         )
#         cursor = connection.cursor(prepared=True)
#
#
#         sql_insert_query = """ INSERT INTO metaTag (metaDataId,tagName,value,timestamp) VALUES (%s,%s,%s,%s)"""
#         insert_tuple_1 = (i, "openpipe_canonical_metaData_Date", "CE 02019 DEC 11 14:00:00", datetime.now())
#         cursor.execute(sql_insert_query, insert_tuple_1)
#         connection.commit()
#         return {"result": "Success"}
#
#     except mysql.connector.Error as error:
#         return {"result": "Failed to insert record into Laptop table {}".format(error)}
#     finally:
#         if (connection.is_connected()):
#             cursor.close()
#             connection.close()
#
#
# for i in range(1,4215):
#     print(insertIntoMetaTags(i))

# from getImageInfo import getImageInfo
# import urllib.request as urllib2
# from io import BytesIO
# from PIL import Image
#
# href="https://images.metmuseum.org/CRDImages/eg/original/DP245141.jpg"
# im = Image.open(BytesIO(urllib2.urlopen(href).read()))
# width, height = im.size
#
# print(str(width)+","+str(height))


# import requests
# from RijksMuseum import RijksMuseum
# from ImageUtil import ImageUtil
# from PIL import Image
#
#
# url = "https://www.rijksmuseum.nl/api/nl/collection/"
# rijks=RijksMuseum({})
# imgUtil= ImageUtil()
# assetsID=rijks.searchRijkForAssets('cats',1,1)
# for a in assetsID['artObjects'] :
#     serviceName = a['objectNumber']+"/tiles"
#     params = {'key': "qvMYRE87"}
#     response = requests.get(url=url + serviceName, params=params)
#     data = response.json()
#     imgWidth = 0
#     imgHeight = 0
#     tileData = []
#     for d in data["levels"]:
#         if d['name'] == "z0":
#             tileData = d['tiles']
#             imgWidth = d['width']
#             imgHeight = d['height']
#             break
#     image=imgUtil.concatTiles(tileData, imgWidth, imgHeight)
#     image.save('pillow_concat_h.jpg')

# from ClevelandMuseum import ClevelandMuseum
# from ImageUtil import ImageUtil
#
# c=ClevelandMuseum({})
# a=c.getData("cats",1,1)
#
# print(a["data"][0]["images"]["full"])
# imgUtil= ImageUtil()
# imgUtil.convertImageFromURL(a["data"][0]["images"]["full"]["url"],"jpg")


# def updateTag():
#     engine = db.create_engine(
#         'mysql+mysqlconnector://artmaster:ArtMaster51@artmuseum.c2p1mleoiwlk.us-west-2.rds.amazonaws.com/artmaster')
#     connection = engine.connect()
#     metadata = db.MetaData()
#     metaTag = db.Table('metaTag', metadata, autoload=True, autoload_with=engine)
#
#     updateQuery = metaTag.update(). \
#         where(metaTag.c.tagName == "openpipe_canonical_metaData_Date"). \
#         values(tagName='openpipe_canonical_date', value='CE YYYYY MMM DD HH:MM:SS')
#
#     result = connection.execute(updateQuery)
#     return result
#
#
# updateTag()

#!/usr/bin/env python3
# areq.py

# """Asynchronously get links embedded in multiple pages' HMTL."""
#
# import asyncio
# import logging
# import re
# import sys
# from typing import IO
# import urllib.error
# import urllib.parse
#
# import aiofiles
# import aiohttp
# from aiohttp import ClientSession
#
# logging.basicConfig(
#     format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
#     level=logging.DEBUG,
#     datefmt="%H:%M:%S",
#     stream=sys.stderr,
# )
# logger = logging.getLogger("areq")
# logging.getLogger("chardet.charsetprober").disabled = True
#
# HREF_RE = re.compile(r'href="(.*?)"')
#
# async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
#     """GET request wrapper to fetch page HTML.
#
#     kwargs are passed to `session.request()`.
#     """
#
#     resp = await session.request(method="GET", url=url, **kwargs)
#     resp.raise_for_status()
#     logger.info("Got response [%s] for URL: %s", resp.status, url)
#     html = await resp.text()
#     return html
#
# async def parse(url: str, session: ClientSession, **kwargs) -> set:
#     """Find HREFs in the HTML of `url`."""
#     found = set()
#     try:
#         html = await fetch_html(url=url, session=session, **kwargs)
#     except (
#         aiohttp.ClientError,
#         aiohttp.http_exceptions.HttpProcessingError,
#     ) as e:
#         logger.error(
#             "aiohttp exception for %s [%s]: %s",
#             url,
#             getattr(e, "status", None),
#             getattr(e, "message", None),
#         )
#         return found
#     except Exception as e:
#         logger.exception(
#             "Non-aiohttp exception occured:  %s", getattr(e, "__dict__", {})
#         )
#         return found
#     else:
#         for link in HREF_RE.findall(html):
#             try:
#                 abslink = urllib.parse.urljoin(url, link)
#             except (urllib.error.URLError, ValueError):
#                 logger.exception("Error parsing URL: %s", link)
#                 pass
#             else:
#                 found.add(abslink)
#         logger.info("Found %d links for %s", len(found), url)
#         return found
#
# async def write_one(file: IO, url: str, **kwargs) -> None:
#     """Write the found HREFs from `url` to `file`."""
#     res = await parse(url=url, **kwargs)
#     if not res:
#         return None
#     async with aiofiles.open(file, "a") as f:
#         for p in res:
#             await f.write(f"{url}\t{p}\n")
#         logger.info("Wrote results for source URL: %s", url)
#
# async def bulk_crawl_and_write(file: IO, urls: set, **kwargs) -> None:
#     """Crawl & write concurrently to `file` for multiple `urls`."""
#     async with ClientSession() as session:
#         tasks = []
#         for url in urls:
#             tasks.append(
#                 write_one(file=file, url=url, session=session, **kwargs)
#             )
#         await asyncio.gather(*tasks)
#
# if __name__ == "__main__":
#     import pathlib
#     import sys
#
#     assert sys.version_info >= (3, 7), "Script requires Python 3.7+."
#     here = pathlib.Path(__file__).parent
#
#     with open(here.joinpath("urls.txt")) as infile:
#         urls = set(map(str.strip, infile))
#
#     outpath = here.joinpath("foundurls.txt")
#     with open(outpath, "w") as outfile:
#         outfile.write("source_url\tparsed_url\n")
#
#     asyncio.run(bulk_crawl_and_write(file=outpath, urls=urls))
# from assetSources.LocalSearch import LocalSearch

# local = LocalSearch()
# results = local.getData('cats',1, 1000)

insertSize=80480
biteSize=1000
q=int(insertSize/biteSize)
r=insertSize%biteSize

a=[]
for i in range(0,80481):
    a.append(i)

print(q,r)

for i in range(0,q):
    print(a[i*biteSize:i*biteSize+biteSize])


