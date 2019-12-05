OpenPipe Feature List With Descriptions and Groupings

Last update Dec 5 2019

This document lists and explains the set of requirements for the OpenPipe tool set.
Explanations of features are included and the current status of the features is also provided.



*Digital Asset Management Features*

*Endpoints for External Access*
Online Downstream endpoints to list assets, list metadata, list schemas	med	available
Downstream endpoints produce Downstream Schema	low	2 days
World Museum Search Endpoint without local	med	3 hour
World Museum Search Endpoint with local	med	2 day
Downstream endpoint to list the catalog of Folders	low	available
Downstream endpoint to retrieve an asset from system	low	available
Downstream endpoint to retrieve metadata for assets or collections	low	available
Endpoint access to update metadata	low	available
Objects are not exposed externally unless set to ‘Published’ in OpenPipe. 	low	available
Endpoint to retrieve Metatags(topics).
Endpoint to modify Metatags(topics).

*Web Based User Interface*
Web interface for the director remote Museums and create collections.	med	available
Web interface for the director to search local	low	2 day
Web interface for the director to review and select content.	med	available
Web interface for the director to tag content and collections with metadata.	med	1 week
OpenPipe lets users browse all assets as image galleries.	med	available
OpenPipe lets users browse CR2, RW2 as online images	low	2 day
Web interface to retrieve Metatags(topics).
Web interface to modify Metatags(topics).
OpenPipe content is browsable globally.	low	available


*Command Line tools for Asset Management*
Program Script based way to attach metadata to collections.	low	2 day
Script Tool to create and manage collections of assets	low	1 week
Command tool Ability to create collections from sets of images.	low	available
Ability to ingest/upload images	med	available
Command Tool interface to retrieve Metatags(topics).
Command Tool interface to modify Metatags(topics).
OpenPipe supports data extraction via API to compute platforms.	low	2 days


*Content Management Features*
Let Users assign an order of elements in a collection.	low	2 day
Have priority for weighting for collection elements.	low	2 day
Sort by different properties associated with the elements of a collection.	med	1 week
include  Licence notices for all assets returned.	low	2 day
Objects can be marked as public or private.
All assets can have any number of Topics items (Metatags).
OpenPipe lets users store text and tags with any asset or Folder.	low	available
OpenPipe any assets may be linked together and named arbitrarily.	low	available
folders may deleted, combined, or split	med	1 week
OpenPipe provides a unique id for every asset in the system.	low	available
OpenPipe supports asset locking protections.	low	2 days

OpenPipe is protected by password access in all interfaces
. not implemented at this time
OpenPipe is interfaced to BSU SSO	high	1 month
. not implemented, requires OIT support.

*Content Management Programable Rule features*
OpenPipe maintains a collection of scope rules for auto-tagging assets.	med	1 week
OpenPipe supports applying tag rules to wildcard scoped assets and collections.	med	1 week

*Federated Database Integration*

Openpipe supports integration with external remote art database.
OpenPipe should support easily ingesting material from other sites.	med	1 month
OpenPipe supports caching of remote materials for improved performance.


*Required Developer Documentation*
Improved Technical Architecture Document for BSU OIT and Downstream	med	1 week
There should be an introductory users manual.
There should be an introductory developers manual.

*System Platform Features*
OpenPipe should support direct integration with AWS 

*broad requirements*

Topics should be easily adjustable -> A list of topics to show on wall, changeable.	high	available
. provide multiple interfaces for modification

OpenPipe is programmable via APIs in Python, Javascript and Web Services.	med	1 week
. the different interfaces listed above.


OpenPipe at some point globus transfer support would be useful.	med	1 week
OpenPipe needs to make saving student portfolios permanently a snap.	high	1 month
Maybe: OpenPipe should make it easy to push assets and collections elsewhere.	low	1 month




*Digital Production Management*

Feature	Complexity	Time
Nightly runs that highlight external assets that have been moved.	low	2 days
Nightly runs that highlight metadata that is missing.	low 	2 days
Todo Lists for Users to accept or correct asset data that is incomplete.	low	2 days
Rule based systems to automatically suggest corrections for mislabeled or incorrect items.	low	2 days
Ability to identify image sets that form panoramas	med	1 week
Ability to identify panoramas that form stereo pairs.	med	1 week
Ability to extract and process panoramas for stitching and viewing.	low	2 days
Ability to align stereo images with corrected warping.	high	1 month
Ability to generate web pages and push to web site for viewing.	med	1 week
Ability to generate tiled viewing versions of panoramas (other assets).	med	1 week
Ability to submit jobs to remote computing systems.	med	1 week
Ability to move files around and manage collections.	med	1 week
Ability to extract an image set (images stored in OpenPipes filestore).	low	2 days
Ability to replace an image set (replace images stored in OpenPipes filestore).	low	2 days
Ability to run scripts daily to check dbase validity.	low	1 week
Ability to generate synthetic data sets and meta data.	med	1 month
Ability to test data sets of over 4 Terabytes in size.	high	1 month
