import json
import time

import firebase_admin
from firebase_admin import credentials, firestore
import google.cloud

# Input the DB credentials and connect to it
from openpipeAPI.ORM.ORM import ORM
from openpipeAPI.ORM.Schema import AssetSchema, MetaTagSchema, FolderSchema
from openpipeAPI.ORM.TO import TO

cred = credentials.Certificate("C:/Users/walluser/Desktop/firebase-admin-key.json")
firebase_admin.initialize_app(cred)

# Choose the collection that you want to connect to. collection = table
collection_name = "folders"

# creat a client object and test the connection by fetching the first two documents
store = firestore.client()
doc_ref = store.collection(collection_name).limit(2)

try:
    docs = doc_ref.get()
    for doc in docs:
        print(u'Doc Data:{}'.format(doc.to_dict()))
except google.cloud.exceptions.NotFound:
    print(u'Missing data')

# read the assets from mySQL and organize it as the map that you want to send to firestore
batched_data = []
orm = ORM()
tables = TO().getClasses()
FolderTable = tables["collection"]
MetaTagTable = tables["metaTag"]

folderMap = {}
metaTagMap = {}


startFetch = time.time()

metaTags = orm.session.query(MetaTagTable).order_by(MetaTagTable.metaDataId).all()
metaTag_schema = MetaTagSchema()

endFetch = time.time()

print("fetch time:"+ str(endFetch-startFetch))

startSort = time.time()
for mt in metaTags:
    metaDataId = mt.metaDataId
    if metaDataId in metaTagMap:
        metaTagMap[metaDataId]["metaData"].update(metaTag_schema.toJson(mt))
    else:
        metaTagMap[metaDataId] = {"metaData": metaTag_schema.toJson(mt)}
endSort = time.time()

print("sort time:"+ str(endSort-startSort))

print("done with metadata")

folders = orm.session.query(FolderTable).all()
folders_schema = FolderSchema(many=True)
folders = folders_schema.dump(folders)

for folder in folders:
    mdid = folder["metaDataId"]
    if mdid in metaTagMap:
        folderMap[mdid] = {"folderInfo": folder, "metaData": metaTagMap[mdid]["metaData"]}


for k in folderMap.keys():
    batched_data.append(folderMap.get(k))

print(batched_data)

# send the data in bulk

listSize=len(batched_data)
biteSize=100
q=int(listSize/biteSize)
r=listSize%biteSize

for i in range(0,q):
    print(i)
    batch = store.batch()
    for data_item in batched_data[i*biteSize:i*biteSize+biteSize]:
        doc_ref = store.collection(collection_name).document()
        batch.set(doc_ref, data_item)
    batch.commit()

batch = store.batch()
for data_item in batched_data[q*biteSize:q*biteSize+r]:
    doc_ref = store.collection(collection_name).document()
    batch.set(doc_ref, data_item)
batch.commit()