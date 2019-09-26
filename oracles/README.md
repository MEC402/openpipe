
# Oracle Services
The python scripts each provide a service related to following:
  - artistsAliases.py- to find the alias names for a certain author (Using Getty ULAN Sevice) [click here to see the schema](http://mec402.boisestate.edu/cgi-bin/oracles/artistsAliases.py)
  - locationAliases.py- to find the other names used for a location (Using Getty TGN Service)[click here to see the schema](http://mec402.boisestate.edu/cgi-bin/oracles/locationAliases.py)

For more info on Getty vocabulary services go to:
http://www.getty.edu/research/tools/vocabularies/vocab_web_services.pdf

## Request and Response Format
 
<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;border-color:#9ABAD9;}
.tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:#9ABAD9;color:#444;background-color:#EBF5FF;}
.tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:#9ABAD9;color:#fff;background-color:#409cff;}
.tg .tg-c3ow{border-color:inherit;text-align:center;vertical-align:top}
.tg .tg-svo0{background-color:#D2E4FC;border-color:inherit;text-align:center;vertical-align:top}
</style>
<table class="tg">
  <tr>
    <th class="tg-c3ow">Method</th>
    <th class="tg-c3ow">Path</th>
    <th class="tg-c3ow">Parameters</th>
    <th class="tg-c3ow">Parameter Description</th>
    <th class="tg-c3ow">Required</th>
  </tr>
  <tr>
    <td class="tg-svo0" rowspan="3">GET</td>
    <td class="tg-svo0" rowspan="3">http://mec402.boisestate.edu/cgi-bin/oracles/artistsAliases.py</td>
    <td class="tg-svo0">searchName</td>
    <td class="tg-svo0">Name of the artist</td>
    <td class="tg-svo0">yes</td>
  </tr>
  <tr>
    <td class="tg-c3ow">role</td>
    <td class="tg-c3ow">Role of the artist like painter</td>
    <td class="tg-c3ow">no</td>
  </tr>
  <tr>
    <td class="tg-svo0">nation</td>
    <td class="tg-svo0">Nationality of the artist like Duch</td>
    <td class="tg-svo0">no</td>
  </tr>
  <tr>
    <td class="tg-c3ow" rowspan="3">GET</td>
    <td class="tg-c3ow" rowspan="3">http://mec402.boisestate.edu/cgi-bin/oracles/locationAliases.py</td>
    <td class="tg-c3ow">searchName</td>
    <td class="tg-c3ow">Name of the place</td>
    <td class="tg-c3ow">yes</td>
  </tr>
  <tr>
    <td class="tg-svo0">type</td>
    <td class="tg-svo0">Type of the place like city</td>
    <td class="tg-svo0">no</td>
  </tr>
  <tr>
    <td class="tg-c3ow">nation</td>
    <td class="tg-c3ow">Which nation the place belongs to like France</td>
    <td class="tg-c3ow">no</td>
  </tr>
</table>

## Deployment Notes:
### XAMPP Linux:
Enable CGI (Common Gateway Interface) go to /etc/httpd/conf/httpd.conf :
Search for “AddHandler” and add below lines or modify them.
```
AddHandler cgi-script .cgi .pl .py
```
Note: if you do not find any settings related to cgi-bin in httpd.conf add below settings in httpd.conf & create directory as per below settings
```
<Directory "/var/www/cgi-bin"> (Change path here accordingly)
AllowOverride None
Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
Require all granted
Allow from all
</Directory>
```
Go to cgi-bin directory (/var/www/cgi-bin) in XAMPP & put your script in there . Give proper permission to directory “chmod 755”.

Example of basic code:
```python
#!bin/python3
    print("Content-Type: text/html\n")
    print ("Hello")
```

### XAMPP Windows:

Open the directory where xammp was installed Go to apache\conf\httpd.conf put the below codes in the end of the file:
```
AddHandler cgi-script .py
ScriptInterpreterSource Registry-Strict
```
In same file search for `<IfModule dir_module>` When you've found it put  `index.py` in the end It will look something like this
```
<IfModule dir_module>
    DirectoryIndex index.php index.pl index.cgi index.asp index.shtml index.html index.htm \
    default.php default.pl default.cgi default.asp default.shtml default.html default.htm \
    home.php home.pl home.cgi home.asp home.shtml home.html home.htm index.py
</IfModule>
```
Example of basic code:
```python
#! C:/Python37-32/python.exe
    print("Content-Type: text/html\n")
    print ("Hello")
```
