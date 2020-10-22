Within the SQL database a table is maintained that specifies the
Canonical Meta Tags that the Openpipe system monitors for all of the assets it manages.  

These canonical tags need to be present for every asset that has been properly ingested into the openpipe system.  if any of these tags are not ingested the asset is considered incomplete.

The following are the current Canonical Tags as of Oct 21st 2020.
This document can become quickly out of date because the Database is the definitive standard for the list of Canonical Tags.  So the following is not exhaustive.

The schema for the Canonical MetaTag table should be:

* id  - the unique internal database id for the canonical tag.
* name - the name of the tag.  Always begins with openpipe_canonical_
* default - the default value for the tag if no value available.
* format - a string that shows the format of the tag value using sprint syntax.
* timestamp - the last time the tag entry was modified.

As of Oct 21st 2020 there are 20 unique canonical tags in the system
The current list is shown below:

| ID | Name | default | Timestamp |
1 | openpipe_canonical_id | -1 | 2019-10-15 00:00:00
2 | openpipe_canonical_title | OpenPipe | 2019-10-13 00:00:00
3 | openpipe_canonical_source | The OpenPipe Museum  | 2019-10-13 00:00:00
4 | openpipe_canonical_largeImage | http://mec402.boisestate.edu/assets/largeImage.jpg | 2019-10-15 00:00:00
5 | openpipe_canonical_largeImageDimensions | 4000,3000 | 2019-10-15 00:00:00
6 | openpipe_canonical_smallImage | http://mec402.boisestate.edu/assets/smallImage.jpg | 2019-10-15 00:00:00
7 | openpipe_canonical_smallImageDimensions | 1000,750 | 2019-10-15 00:00:00
8 | openpipe_canonical_artist | OpenPipe | 2019-10-15 00:00:00
9 | openpipe_canonical_culture | OpenPipe | 2019-10-15 00:00:00
10 | openpipe_canonical_classification | OpenPipe | 2019-10-15 00:00:00
11 | openpipe_canonical_genre | art-fi | 2019-10-15 00:00:00
12 | openpipe_canonical_medium | OpenPipe Pixels | 2019-10-15 00:00:00
13 | openpipe_canonical_nation | OpenPipe People | 2019-10-15 00:00:00
14 | openpipe_canonical_city | OpenPipe City | 2019-10-15 00:00:00
15 | openpipe_canonical_tags | OpenPipeTag | 2019-10-15 00:00:00
16 | openpipe_canonical_fullImage | http://mec402.boisestate.edu/assets/largeImage.jpg | 
17 | openpipe_canonical_fullImageDimensions | 4000,3000 | 
18 | openpipe_canonical_date | CE YYYYY MMM DD HH:MM:SS | 
19 | openpipe_canonical_firstDate | CE YYYYY MMM DD HH:MM:SS | 
20 | openpipe_canonical_lastDate | CE YYYYY MMM DD HH:MM:SS | 
21 | asdf |  | 2020-05-28 18:53:51


