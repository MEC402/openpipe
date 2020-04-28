#!/bin/sh 
# this shell script copies files to the web destination directory
cp config/htaccess.conf /var/www/html/.htaccess
cp -r ORM /var/www/cgi-bin/dataAccess/

