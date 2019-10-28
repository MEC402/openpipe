OpenPipe Content Production Solution for Managing Very Large Content Collections

# API Endpoints

## GET Collections(Search)

Get a list of collections available in the database

http://mec402.boisestate.edu/cgi-bin/dataAccess/getCollections.py

Parameters

|Name | Description | Required |
|-----|-------------|----------|
|name |name of the new collection |yes |


## GET Collections(Create)

Creates and adds a new collection to the database.

http://mec402.boisestate.edu/cgi-bin/dataAccess/createCollection.py

Parameters

|Name | Description | Required |
|-----|-------------|----------|
|collectionId |the specific id or all for all the collections |yes |
|start |starting id	 |no |
|end |ending id |no |


## GET Add Asset

Adds an asset into the database

http://mec402.boisestate.edu/cgi-bin/dataAccess/addAsset.py

Parameters

|Name | Description | Required |
|-----|-------------|----------|
|shortName |- |yes |
|uri |-	 |yes |
|idAtSource |- |yes |
|sourceId |- |yes |
|metaDataId |-	 |yes |
|scope |- |yes |


## GET Add Asset Into Collection

Adds an asset into an existed collection.

http://mec402.boisestate.edu/cgi-bin/dataAccess/addAssetIntoCollection.py

Parameters

|Name | Description | Required |
|-----|-------------|----------|
|assetId |- |yes |
|collectionId |-	 |yes |
|searchTerm |- |yes |


## GET Create Metadata

Creates a new Metadata type in the database.

http://mec402.boisestate.edu/cgi-bin/dataAccess/createMetaData.py

Parameters: None


## POST Create MetaTags

Creates a MetaTag in the database.

http://mec402.boisestate.edu/cgi-bin/dataAccess/createMetaTags.py

Parameters: None


## GET Public Assets in Collection

Returns a list of assets in given Collection.

http://mec402.boisestate.edu/cgi-bin/dataAccess/getPublicAssetsInCollection.py

Parameters

|Name | Description | Required |
|-----|-------------|----------|
|collectionId |- |yes |