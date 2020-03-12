import sys
from multiprocessing.pool import ThreadPool

from CanonicalSchema import CanonicalSchema
import aiohttp
import asyncio
from MetMuseum import MetMuseum
import time

s = time.perf_counter()
schema=CanonicalSchema().getSchema(1)
print("Schema")
print(time.perf_counter() - s)
print(sys.getsizeof(schema))


s = time.perf_counter()
met=MetMuseum(schema)
print("Object")
print(time.perf_counter() - s)
print(sys.getsizeof(met))

s = time.perf_counter()
page=1
pageSize=500
results = []
retrievedAssets = met.searchMetForAssets('cats')
start = (page - 1) * pageSize
step = pageSize

if int(start) > retrievedAssets['total']:
    start = retrievedAssets['total'] - 1
if int(start) + int(step) > retrievedAssets['total']:
    step = retrievedAssets['total'] - int(start) - 1
assets = retrievedAssets['objectIDs'][int(start):int(start) + int(step)]

print("Query Museum")
print(time.perf_counter() - s)
print(sys.getsizeof(assets))

s = time.perf_counter()

loop = asyncio.get_event_loop()
coroutines = [met.getAssetMetaData(assetId) for assetId in assets]
results = loop.run_until_complete(asyncio.gather(*coroutines))

print("Query MetaTags")
print(time.perf_counter() - s)
print(sys.getsizeof(results))

s = time.perf_counter()
pool = ThreadPool(len(results))
tempResults = []
for assetId in results:
    tempResults.append(pool.apply_async(met.getMetaTagMapping, args=[assetId]))
pool.close()
pool.join()
finalResults = [r.get() for r in tempResults]

res={"total": retrievedAssets['total'], "sourceName": "MET", "data": finalResults}

print("Images")
print(time.perf_counter() - s)
print(sys.getsizeof(res))