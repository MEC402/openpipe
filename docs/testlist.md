# Tests to run against OpenPipe code sequences

This document lists out the tests to be run against openpipe to demonstrate
the system is working properly.

# Tests on the REST endpoints

## The following are the REST endpoints

### Search endpoints
/assetSoruces/allSources.py
/assetSources/museums.py

### Folders endpoints
/dataAccess/getcollections.py
/dataAccess/getAllLayouts.py
/dataAccess/getFolderLayout.py
/dataAccess/getPublicAssetsInCollection.py

### MetTags endpoints
/dataAccess/getCanonicalMetaTags.py
/dataAccess/getAssetMetaTags.py

### Assets endpoints
/dataAccess/getAllAssets.py

### GUID endpoints
/openpipe/data/{entityName}/{entityID}
/openpipe/data/{entityName}
/openpipe/data/entities
