Creation Date: May 17th 2020

This directory contains python scripts for managing 'Topics' in the OpenPipe system.

Topics are commonly search categories that consist of various similar values.

The source of named Topics come from the OpenPipe Canonical Tags definition

The following Topics are the initial set at this time

* title: managed by equivalance database
* source: managed by equivalance database
* artist: managed by equivalence database
* culture: managed by equivalence database
* genre: managed by equivalence database
* medium: managed by equivalence database
* nation: managed by equivalence database
* city: managed by equivalence database
* largeImageDimensions: managed by runtime check
* smallImageDimensions: managed by runtime check
* fullImageDimensions: managed by runtime check
* date: managed by runtime comparison


Python Files in this directory:

topSetup.py: create the databases used for topic equivalency
topAPI.py create the basic CRUD methods for handling topics
topcmd.py command line tool for reviewing topic information
topsweep.py   program that sweeps the asset meta tags to fill in topics tables

dimCheck.py  simple python script that compares dimensions for equivalency.
dateCheck.py compares dates to see if equivalent or not.  Returns difference.
