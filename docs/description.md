Openpipe

Openpipe is a distributed content management system with asset management and production pipeline as its two major components. The asset management component is a federated database that allows for fetch and viewing of multiple museum assets as a whole. The production pipeline is responsible for graphic jobs like efficient image ingest, panorama stitching, and etc. These components shape Openpipe architecture.

Openpipe is designed based on a distributed architecture and has the following characteristics:

* loosely coupled components
* URI and HTML for communication
* JSON array data format
* Federated resources

Openpipe implementation consists of two parts: front-end and back-end. The front-end is developed with Angular and ngx-admin template. The UI is used to allow the world museum curator to perform the following tasks:
Search for assets in different museums as well as local file storage
* Create Folders
* Put assets into folders
* Show all the tracked assets
* Show assets meta-data
* Edit assets meta-data

The backend is developed using python with a Amazon RDS as its database. The backend does the compute jobs as well as providing the API endpoints available at: http://mec402.boisestate.edu/endpoints.html