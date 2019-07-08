OpenPipe Content Production Solution for Managing Very Large Content Collections

# API Endpoint

## GET Schema

Get a JSON file with the structure of the Schema supported by OpenPipe systems.
https://mec402.boisestate.edu/wmuseum/api/schema/

## GET Artworks(Search)

Get a list of artworks available in the database

https://mec402.boisestate.edu/wmuseum/api/artworks/

Parameters


|Name | Type | Description |
|-----|------|------------|
|q | string | keyword or phrase that searches against all metadata in CMS |
|-----|------|------------|
|local | integer | 0 only searches OpenPipe CMS, 1 searchs all possible endpoints, even remote endpoints. |
|------|---------|--------|
| cache | integer | 0 do not cache results.  1 Cache resulting images |


## GET Collections(Search)

Get a list of collections availabe in the database

https://mec402.boisestate.edu/wmuseum/api/collections/

## GET panoramas(Search)

Get a list of collections available in the database

https://mec402.boisestate.edu/wmsuseum/api/panoramas/

