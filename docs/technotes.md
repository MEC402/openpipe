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

## Configure the system for local run time testing

* Configure Apache rules
   CGI-bin
   rewrite rules
     Have to modify conf file using the Directory rule to allow .htaccess and rewrite.

* change group and permission on /var/www
* enable module rewrite for rules: sudo a2enmod rewrite
* service apache2 restart
* cp config/htaccess.conf /var/www/html/.htaccess



