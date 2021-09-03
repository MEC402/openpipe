import time

import boto3

from backend.openpipeAPI.ORM.ORM import ORM
from backend.openpipeAPI.ORM.Schema import AssetSchema, MetaTagSchema
from backend.openpipeAPI.ORM.TO import TO

# Get the service resource.

dynamodb = boto3.resource('dynamodb',
                          region_name='us-west-2',
                          aws_access_key_id="",
                          aws_secret_access_key="")  # replace with the correct key

# Instantiate a table resource object without actually
# creating a DynamoDB table. Note that the attributes of this table
# are lazy-loaded: a request is not made nor are the attribute
# values populated until the attributes
# on the table resource are accessed or its load() method is called.
table = dynamodb.Table('assets')

# Print out some data about the table.
# This will cause a request to be made to DynamoDB and its attribute
# values will be set based on the response.
print(table.creation_date_time)

# read the assets from mySQL and organize it as the map that you want to send to aws
batched_data = []
orm = ORM()
tables = TO().getClasses()
AssetTable = tables["asset"]
MetaTagTable = tables["metaTag"]

assetMap = {}
metaTagMap = {}

print("Fetch started")

startFetch = time.time()

metaTags = orm.session.query(MetaTagTable).order_by(MetaTagTable.metaDataId).all()
metaTag_schema = MetaTagSchema()

endFetch = time.time()

print("fetch time:" + str(endFetch - startFetch))

startSort = time.time()
for mt in metaTags:
    metaDataId = mt.metaDataId
    if metaDataId in metaTagMap:
        metaTagMap[metaDataId]["metaData"].update(metaTag_schema.toJson(mt))
    else:
        metaTagMap[metaDataId] = {"metaData": metaTag_schema.toJson(mt)}
endSort = time.time()

print("sort time:" + str(endSort - startSort))

print("done with metadata")

assets = orm.session.query(AssetTable).all()
assets_schema = AssetSchema(many=True)
assets = assets_schema.dump(assets)

for asset in assets:
    mdid = asset["metaDataId"]
    if mdid in metaTagMap:
        assetMap[mdid] = {"id": int(asset['id']), "assetInfo": asset, "metaData": metaTagMap[mdid]["metaData"]}

for k in assetMap.keys():
    batched_data.append(assetMap.get(k))

print(batched_data[0])

print("Entering batch write to dynamo DB")
with table.batch_writer() as batch:
    for item in batched_data[195:]:
        # print(item)
        batch.put_item(item)

print(" Finished batch write to dynamo DB")
