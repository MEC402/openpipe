#simple script to generate some statistics about canon tags and their values
import re
import string
import validators
import datetime
import sys

from sqlalchemy import and_

from backend.openpipeAPI.ORM.ORM import ORM
from backend.openpipeAPI.ORM.TO import TO

orm = ORM()
tables = TO().getClasses()
Topic = tables["metaTag"]

#confirm URI is correct
def checkURIString(anurstring):
#check for unprintable characters
   if not anurstring.isprintable():
      return False

   if not validators.url(anurstring):
      return False
   return True

#check optional strings
def checkOptString(avs):
#check for unprintable characters
    if not avs.isprintable():
      return False

    res = True
    if '{' in avs:
       res = False
    if '}' in avs:
       res = False
    if '\\' in avs:
       res = False
    if '\r' in avs:
       res = False
    if '\n' in avs:
       res = False
    if '\t' in avs:
       res = False

    return res

#confirm ID is correct
def checkIdString(aidstring):
#check for unprintable characters
   if not aidstring.isprintable():
      return False

   if not aidstring.isnumeric():
      return False
   return True


#check coordinate properly formated
def checkCoord(acordstring):
#check for unprintable characters
   if not acordstring.isprintable():
      return False

   if acordstring == "":
      return True

   try:
      float(acordstring)
   except:
           return False

   return True

#confirm that the string contains a properly formmated
#dimensional string
def checkPhysicalDimString(adimstring):
#check for unprintable characters
   if adimstring == "":
      return True # empty string ok

   if not adimstring.isprintable():
      return False

#check for 2 and only 2 commas
   if adimstring.count(",") != 2:
      return False

#check for the presence of exactly 3 numbers
   dimlist = adimstring.split(",")
   if len(dimlist) != 3:
       return False

   for x in dimlist:
        try:
           float(x)
        except:
           return False

   return True

#check the pixel dimensions string
def checkPixelDimString(adimstring):
#check for unprintable characters
   if adimstring == "":
      return True

   if not adimstring.isprintable():
      return False

#check for 1 and only 1 commas
   if adimstring.count(",") != 1:
      return False

#check for the presence of exactly 2 integernumbers
   dimlist = adimstring.split(",")
   if len(dimlist) != 2:
       return False

   for x in dimlist:
        if not x.isnumeric():
           return False

   return True

#check the date for proper format
def checkDate(adatestring):
#check for unprintable characters
   if not adatestring.isprintable():
      return False

   if adatestring == "":
      return True

   if not (adatestring.startswith("CE") or adatestring.startswith("BC")):
      return False

   return True

#check the global rules for strings - no unprintable characters
# no inappropriate ascii characters - like {, \\  etc

mappings=[]

empties = 0
nonprint = 0
printable = 0
total = 0
chardict = {'{': 0, '}':0, '\\': 0, '/': 0, '\r': 0, '\n': 0, '\t': 0}


assetResultSet = orm.executeSelect("select * from metaTag where tagName like 'openpipe_canonical_%';")
print("SELECT IS BACK")
fixlist = []
for d in assetResultSet['data']:
    total += 1
    addme = False
    #print(total)
    avs = d['value'][0]
    if avs == "":
      empties += 1

    if avs.isprintable():
       printable += 1
    else:
       nonprint += 1 
       addme = True
       print("add to Fix list")
       fixlist.append(d)

    #print(d)

    if '{' in avs:
       chardict['{'] += 1
       addme = True
    if '}' in avs:
       chardict['}'] += 1
       addme = True
    if '\\' in avs:
       chardict['\\'] += 1
       addme = True
       #print(avs,d)
    if '/' in avs:
       chardict['/'] += 1
    if '\r' in avs:
       chardict['\r'] += 1
       addme = True
    if '\n' in avs:
       chardict['\n'] += 1
       addme = True
    if '\t' in avs:
       chardict['\t'] += 1
       addme = True




print ("Empties = %d, Printable =%d, Nonprint=%d, Total=%d" % (empties,printable,nonprint,total))
print(chardict)
#lets update these entries

sqlstmt = ""
for x in fixlist:
   ts = x['value'][0]
   pvalue = ""
   for ix in ts:
      if ix.isprintable():
        if ix == "\"":
          pvalue = pvalue + "\\\"" 
        else:
          pvalue = pvalue + ix

   print(pvalue)
   if not pvalue.isprintable():
     print("printable not working")
     print(pvalue)
   else:
     #print("is printable")
     astmt = "update metaTag set value=\"%s\" where metaDataId='%s' and tagName='%s';" % (pvalue, x['metaDataId'][0],x['tagName'][0])
     #print(astmt)
     #orm.updateSqlMulti(astmt)

#actual update
#print(sqlstmt)


#sys.exit(0)

#check the physical dimensions Type
assetResultSet = orm.executeSelect("select * from metaTag where tagName = 'openpipe_canonical_physicalDimensions';")

dimerror = 0
dimcount = 0
dimtotal = 0
dimdefault = 0
for d in assetResultSet['data']:
    dimtotal += 1 
    if (len(d['value']) != 1):
       dimerror += 1 
    dimstring = d['value'][0]
    if checkPhysicalDimString(dimstring) == False:
       dimcount += 1
       print(dimstring)
       astmt = "update metaTag set value=\"\" where metaDataId='%s' and tagName='%s';" % ( d['metaDataId'][0],d['tagName'][0])
       print(astmt)
       #orm.updateSqlMulti(astmt)
#    else:
#       print(dimstring)
    if dimstring == '21.0,29.7,1.0':
       dimdefault += 1

print ("Dimerror = %d, DimFormat =%d, DimDefault=%d, Total=%d" % (dimerror,dimcount,dimdefault,dimtotal))


#check the IntegerString type
assetResultSet = orm.executeSelect("select * from metaTag where tagName = 'openpipe_canonical_id';")

idtotal = 0
iderror = 0
for d in assetResultSet['data']:
    idtotal += 1
    idstring = d['value'][0]
    if checkIdString(idstring) == False:
       iderror += 1
#       print(idstring)

print ("IdError = %d, Total=%d" % (iderror,idtotal))


#now check the URI type
assetResultSet = orm.executeSelect("select * from metaTag where tagName like 'openpipe_canonical_%Image';")

urtotal = 0
urerror = 0
for d in assetResultSet['data']:
    urtotal += 1
    urstring = d['value'][0]
    if not checkURIString(urstring):
       urerror += 1
       #print(urstring)
       #lets fix spaces
       if ' ' in urstring:
         ns = urstring.replace(' ', "%20")
         if checkURIString(ns):
            astmt = "update metaTag set value=\"%s\" where metaDataId='%s' and tagName='%s';" % (ns, d['metaDataId'][0],d['tagName'][0])
            print(astmt)
            #orm.updateSqlMulti(astmt)
    

print ("URI Error = %d, Total=%d" % (urerror,urtotal))


#now we check the Pixel Dimension entries
assetResultSet = orm.executeSelect("select * from metaTag where tagName like 'openpipe_canonical_%ImageDimensions';")
pdimtotal = 0
pdimerror = 0
emptydim = 0
for d in assetResultSet['data']:
    pdimtotal += 1
    pdimstring = d['value'][0]
    if not checkPixelDimString(pdimstring):
       pdimerror += 1
       print(pdimstring,d)
    if pdimstring == "":
       emptydim += 1



print ("Pixel Dim Error = %d, Empty= %d, Total=%d" % (pdimerror,emptydim,pdimtotal))



#now we check the Date entries
assetResultSet = orm.executeSelect("SELECT * FROM metaTag WHERE tagName = 'openpipe_canonical_date' or tagName='openpipe_canonical_firstDate' or tagName='openpipe_canonical_lastDate';")

datetotal = 0
daterror = 0
emptydate = 0
for d in assetResultSet['data']:
    datetotal += 1
    datestring = d['value'][0]
    if not checkDate(datestring):
       daterror += 1
       print(d)
    if datestring == "":
       emptydate += 1

print ("Date Error = %d, Empty= %d, Total=%d" % (daterror,emptydate,datetotal))

#now we check the Coordinate entries
assetResultSet = orm.executeSelect("SELECT * FROM metaTag WHERE tagName like 'openpipe_canonical_%tude';")

coordtotal = 0
coorderror = 0
emptycoord = 0
for d in assetResultSet['data']:
    coordtotal += 1
    coordstring = d['value'][0]
    if not checkCoord(coordstring):
       coorderror += 1
       print(coordstring,d)
    if coordstring == "":
       emptycoord += 1

print ("Coord Error = %d, Empty= %d, Total=%d" % (coorderror,emptycoord,coordtotal))

#let's see if we can clean up a string
def tryFixString(shortstring):
#first replace some characters
    workstring = shortstring
    if '\r' in workstring:
       workstring = workstring.replace('\r','')
    if '\n' in workstring:
       workstring = workstring.replace('\n','')
    if '\t' in workstring:
       workstring = workstring.replace('\t','')
    if '\\' in workstring:
       workstring = workstring.replace('\\','')


#let's try and fix a dictionary
    if workstring.startswith('{') and workstring.endswith('}'):
     # a dictionary
     redstring = workstring[1:-1]
     comlist = redstring.split(",")
     ilist = [item.split(":") for item in comlist]
     print(ilist)
     for x in ilist:
        if x[0] == "labelDesc":
           workstring = x[1]
    if workstring.startswith('[{') and workstring.endswith('}]'):
     redstring = workstring[2:-2]
     bg = redstring.find('biography:')
     end = redstring.find(',name_in_original_language')
     bgg = redstring.find(':',bg)
     biostring = redstring[bgg+1:end-1]

     #print(workstring)
     if 'nul' in biostring:  #biography is null use description
       redstring = workstring[2:-2]
       #print(redstring)
       bg = redstring.find('description:')
       end = redstring.find(',extent',bg)
       bgg = redstring.find(':',bg)
       workstring = redstring[bgg+1:end]
     else:
       workstring = biostring
     
    #print(workstring)
    return workstring


#handle all the optional string data items
assetResultSet = orm.executeSelect("select * from metaTag where tagName='openpipe_canonical_title' or tagName='openpipe_canonical_biography' or tagName='openpipe_canonical_moment' or tagName='openpipe_canonical_style' or tagName='openpipe_canonical_period' or tagName='openpipe_canonical_country' or tagName='openpipe_canonical_subject' or tagName='openpipe_canonical_Technique' or tagName='openpipe_canonical_School' or tagName='openpipe_canonical_Group' or tagName='openpipe_canonical_Dynasty' or tagName='openpipe_canonical_Reign' or tagName='openpipe_canonical_Nationality' or tagName='openpipe_canonical_Region' or tagName='openpipe_canonical_Feature' or tagName='openpipe_canonical_Site' or tagName='openpipe_canonical_Content' or tagName='openpipe_canonical_Function' or tagName='openpipe_canonical_marks' or tagName='openpipe_canonical_artist' or tagName='openpipe_canonical_culture' or tagName='openpipe_canonical_classification' or tagName='openpipe_canonical_genre' or tagName='openpipe_canonical_medium' or tagName='openpipe_canonical_nation' or tagName='openpipe_canonical_city';")


stringtotal = 0
stringerror = 0
stringempty = 0
count = 0
for d in assetResultSet['data']:
    stringtotal += 1
    shortstring = d['value'][0]
    if not checkOptString(shortstring):
       stringerror += 1
       tryfix = tryFixString(shortstring)
       print(tryfix)
       if checkOptString(tryfix):
          print("Fixed: " + tryfix)
          print(count)
          count += 1
          astmt = "update metaTag set value=\"%s\" where metaDataId='%s' and tagName='%s';" % (tryfix, d['metaDataId'][0],d['tagName'][0])
          print(astmt)
          #orm.updateSqlMulti(astmt)
    if shortstring == "":
       stringempty += 1

print ("string Error = %d, Empty= %d, Total=%d" % (stringerror,stringempty,stringtotal))
