Technical Notes for OpenPipe 

Tools used in development of the system:

* Python
* Apache version xxx
* Angular



# How To Set Up OpenPipe Dev Environment

## Install the following packages

* Install apache web server
* Install angular
* install python
   install all of mysql connectors as root.
   install mysql alchemy as root
   install requests, xmltodict, json 

## Configure the system for local run time testing

* Configure Apache rules
   CGI-bin
   rewrite rules
     Have to modify conf file using the Directory rule to allow .htaccess and rewrite.

* change group and permission on /var/www
* enable module rewrite for rules: sudo a2enmod rewrite
* service apache2 restart
* cp config/htaccess.conf /var/www/html/.htaccess


# Museum Handler Design structure

The following is the design of the classes and configuration for integrating an external Museum into the OpenPipe system:

## Objects
museums.json -> a json file with the list of museums integrated into the system.
MuseumsR.py -> read load and connect museums into a running openpipe
MuseumTM.py  -> a generic museum template that is used to plug in a museum.

## formats
museums.json 
{
 "museum1": {"source": "museumname","searchurl": "asearchurl","class": "pythonclass", "key": "hashkey if needed" },
 "museum2": {"source": "museumname","searchurl": "asearchurl","class": "pythonclass" },
"museum3":  {"source": "museumname","searchurl": "asearchurl","class": "pythonclass" }
}

## MuseumsR.py design 

This object maintains a list of museums connected into the openpipe system

* loads the json file of museums interface
* maintains a list of all available sources.
* maintans a list of source museum classes
* 
* implements search across all museums
* implements search on a list of museums
* implements get of an asset from a museum

## MuseumsTM.py handler for an individual museum
## 

* class objects:
*   name -> museum name
*   searchurl -> search url
*   getobject -> get an object 
*
*   search(querystring)
*   getobject(objectid)

