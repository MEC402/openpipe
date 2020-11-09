#assetAssess.py

#check assets for correctness in various ways and generate statistics
#about the accuracy.

import hjson
import sys
from parse  import *
import re

#this is a hack: the mods to sys.path should be done in a config element
sys.path.append('e:/builds/openpipe/backend')

from openpipeAPI.ORM.BL import BL
from openpipeAPI.ORM.ORM import ORM
from openpipeAPI.ORM.TO import TO



def getAssets(aorm):
    tables = TO().getClasses()
    MetaTag = tables["metaTag"]
    res =aorm.executeSelect("""SELECT * FROM asset;""")
    return res

def getPhysical(aorm):
    tables = TO().getClasses()
    MetaTag = tables["metaTag"]
    res =aorm.executeSelect("""select * from artmaster.asset inner join metaTag ON asset.metaDataId=metaTag.metaDataId where metaTag.tagName='openpipe_canonical_physicalDimensions';""")
    return res

def getNotIn(aorm,topic):
    tables = TO().getClasses()
    MetaTag = tables["metaTag"]
    sqlsrc = """select * from artmaster.asset where asset.metaDataId not in (select metaDataId from metaTag where metaTag.tagName='"""
    sqltail = """');"""
    sqltext = sqlsrc + topic + sqltail
    res =aorm.executeSelect(sqltext)
    return res

def getDefault(aorm,topic):
    tables = TO().getClasses()
    MetaTag = tables["metaTag"]

    sqldef = "select canonicalMetaTag.default from canonicalMetaTag where name='%s';" % topic
#    print(sqldef)
    defvalue =aorm.executeSelect(sqldef)
    defstring = defvalue['data'][0]['default'][0]
    print (defstring)

    sqlsrc = """select * from artmaster.asset inner join metaTag ON asset.metaDataId=metaTag.metaDataId where metaTag.tagName='%s' and metaTag.value='%s';""" %(topic,defstring)
    sqltext = sqlsrc 
    print(sqltext)
    res =aorm.executeSelect(sqltext)
    return res

def getDimensions(aorm,topic):
    tables = TO().getClasses()
    MetaTag = tables["metaTag"]

    sqldef = "select canonicalMetaTag.default from canonicalMetaTag where name='%s';" % topic
#    print(sqldef)
    defvalue =aorm.executeSelect(sqldef)
    defstring = defvalue['data'][0]['default'][0]
    print (defstring)

    sqlsrc = """select t1.metaDataId, t2.value from metaTag t1 inner join metaTag t2 on t1.metaDataId=t2.metaDataId where t1.tagname='%s' and t2.tagName='dimensions';""" %topic
    sqltext = sqlsrc 
    print(sqltext)
    res =aorm.executeSelect(sqltext)
    return res

def extractSizes(sizelist):
    sizedict ={}
    sizedict['height'] = "29.7"
    sizedict['width'] = "21.0"
    sizedict['depth'] = "1.0"

    for i in reversed(sizelist):
        kv = i.split(":")
#        print(kv)
        strippedkey=kv[0].strip('\'')
        sizedict[strippedkey] = kv[1];
    return sizedict

#parse the unusual Overall dimensions
def extractOvrSizes(sizelist):
    sizedict ={}
    sizedict['height'] = "29.7"
    sizedict['width'] = "21.0"
    sizedict['depth'] = "1.0"
    nums = re.compile('[0-9]+.[0-9]*')

    mysize = sizelist[0]
    numlist = nums.findall(mysize)
    if len(numlist) > 0: sizedict['width'] = numlist[0]
    if len(numlist) > 1: sizedict['height'] = numlist[1]
    if len(numlist) > 2: sizedict['depth'] = numlist[2]

    return sizedict

#parse the unusual Overall dimensions
def extractH3Sizes(sizelist):
    sizedict ={}
    sizedict['height'] = "29.7"
    sizedict['width'] = "21.0"
    sizedict['depth'] = "1.0"
    nums = re.compile('[0-9]+.[0-9]*')

    mysize = sizelist[0]
    numlist = nums.findall(mysize)
    if len(numlist) > 0: sizedict['width'] = numlist[0]
    if len(numlist) > 1: sizedict['height'] = numlist[1]
    if len(numlist) > 2: sizedict['depth'] = numlist[2]

    return sizedict

#parse the unusual Bracket dimensions
def extractBSizes(sizelist):
    sizedict ={}
    sizedict['height'] = "29.7"
    sizedict['width'] = "21.0"
    sizedict['depth'] = "1.0"
    scale = 1.0

  
    #first find units
    for i in sizelist:
      if (i['value'] != "None") and (i['value'] != "null"):
#        print(i['value'])
        if (i['unit'] == "mm"):
            i['value'] = str(float(i['value'])/100.0)

        if 'height' in i.keys(): siezdict['height'] = i['value']
        if 'width' in i.keys(): siezdict['width'] = i['value']
        if 'depth' in i.keys(): siezdict['depth'] = i['value']

    return sizedict

#correct the dimension topic for Met asset
#this function should be in the Met Museum object
#aorm is the link to the database
#adim is the current object to change, it has a default canon value
def correctDimensions(aorm,adimlist):
    #first we convert the dimensions string into proper format
    #this should be in the Museum handling code but is here for now
    unknowndim = 0
    nummatch = 0
    nodims = 0
    defwidth = 21.0
    defheight = 29.7
    defdepth = 1.0
    innercount = 0
    iparsecount = 0
    ioverall = 0
    iparseoverall = 0
    ibsize = 0
    ibparse = 0
    totaldim = len(adimlist)
    acount = [0,0,0,0,0,0,0,0,0]
    onetime = 1

#first build our regular expression for some of the cases
    mysizes = re.compile('\'*width\'*\s*:\s*[0-9]+.[0-9]*|\'*height\'*\s*:\s*[0-9]+.[0-9]*|\'*depth\'*\s*:\s*[0-9]+.[0-9]*')
    myovr = re.compile('\([0-9]+.[0-9]*.*?cm.*?\)')
    myhre = re.compile('\([0-9]+.[0-9]*\s*x\s*[0-9]+.[0-9]*\s*x\s*[0-9]+.[0-9]*\s*cm\)')
    for adim in adimlist:
        width = defwidth
        height = defheight
        depth = defdepth
        akv = {'height': "29.7", "width": "21.0", "depth": "1.0"}
        matchstring = adim['value'][0]
        if (len(matchstring) < 1):
#            print("No dimensions given")
            nodims += 1
        elif (str.startswith(matchstring, "{")):
#                 print("------------------")
#                 print(matchstring)
                 innercount += 1
                 dimlist = mysizes.findall(matchstring)
#                 print(dimlist)
                 if (len(dimlist) > 0):
                   akv = extractSizes(dimlist)
                   iparsecount += 1
#                 print(akv)
#                 print("++++++++++++++++++")
                 nummatch += 1
        elif (str.startswith(matchstring, "Overall")):
#                 print(matchstring)
                 dimlist = myovr.findall(matchstring)
                 if (len(dimlist) > 0):
                   akv = extractOvrSizes(dimlist)
                   iparseoverall += 1
                 else:
                     print(dimlist)
#                 print(akv)
                 nummatch += 1
                 ioverall += 1
        elif (str.startswith(matchstring, "H.")):
#                 print(matchstring)
                 adimlist = myhre.findall(matchstring)
                 if (len(adimlist) > 0):
                     akv = extractH3Sizes(adimlist)
                     print(akv)
                 acount[0] += 1
                 nummatch += 1
        elif (str.startswith(matchstring, "h.")):
#                print(matchstring)
                 acount[1] += 1
                 nummatch += 1
        elif (str.startswith(matchstring, "Sheet:")):
#                print(matchstring)
                 acount[2] += 1
                 nummatch += 1
        elif (str.startswith(matchstring, "sheet:")):
#                print(matchstring)
                 acount[3] += 1
                 nummatch += 1
        elif (str.startswith(matchstring, "Image:")):
#                print(matchstring)
                 acount[4] += 1
                 nummatch += 1
        elif (str.startswith(matchstring, "l.")):
#                print(matchstring)
                 acount[5] += 1
                 nummatch += 1
        elif (str.startswith(matchstring, "L.")):
#                print(matchstring)
                 acount[6] += 1
                 nummatch += 1
        elif (str.startswith(matchstring, "[{")):
#                 print(matchstring)
                 ibsize += 1
                 if "\'unit\'" in matchstring:
                     arp = matchstring.replace("None", "\'None\'")
                 else:
                     arp = matchstring.replace(":","\':\'")
                     arp = arp.replace("{","{\'")
                     arp = arp.replace("}","\'}")
                     arp = arp.replace(",","\',\'")
                     arp = arp.replace("}\',\'{","},{")
#                 print(arp)
                 dimobj = hjson.loads(arp)
                 akv = extractBSizes(dimobj)
                 ibparse += 1
#                 print(dimdict)
                 acount[7] += 1
                 nummatch += 1
        elif (str.startswith(matchstring, "Height:")):
#                print(matchstring)
                 acount[8] += 1
                 nummatch += 1
        elif len(matchstring) > 0 and (matchstring[0].isdigit()):
#                print(matchstring)
                 nummatch += 1
        else:
#           print ("Unrecognized dimensions format: %s" % adim['value'][0])
           unknowndim += 1

    #third ensure the string is in centimeters

    #now we modify the canonical entry in the table

    #finally we format a bulk update for changing all at once

    print("Total Unknown Dimension tags = %d out of %d" % (unknowndim,totaldim))
    print("Total Empty Dimension tags = %d out of %d" % (nodims,totaldim))
    print("Number matched = %d/%d" % (nummatch,totaldim))
    print("for { successfully parsed %d/%d" % (iparsecount, innercount))
    print("for 'Overall' successfully parsed %d/%d" % (iparseoverall, ioverall))
    print("for '[{' successfully parsed %d/%d" % (ibparse, ibsize))
    print(acount)



#connect to the federation
aorm =ORM()

##here we are going to generate a report about the assets stored in the Table
##the report will tell us how many assets there are.
##How many are missing some tags
##How many have incorrect values on their CanonicalTopic Tags

#get the asset list
ares = getAssets(aorm)

#how many assets are there in the table:
print("The Federated Asset Table Has %d assets." % len(ares['data']))

#how many of those have physicalDimensions canonTopic?
pres = getPhysical(aorm)
print ("There are %d assets with Physical Dimensions." % len(pres['data']))

if len(pres['data']) != len(ares['data']):
    mres = getNotIn(aorm,'openpipe_canonical_physicalDimensions')
    print ("The following %d assets do not have proper physical dimensions" % len(mres['data']))
    for r in mres['data']:
        print (r)

#how many of these have default values
dres = getDefault(aorm,'openpipe_canonical_physicalDimensions')
print("The following %d assets have default physical Dimensions" % len(dres['data']))
#for r in dres['data']:
#     print (r)

#now we will use the original source dimensions
#it appears that all assets use 'dimensions' in the original museum list

#get all canonical dimensions with museum data
dres = getDimensions(aorm,'openpipe_canonical_physicalDimensions')
print ("There are %d default dimension Assets to fix" % len(dres['data']))
correctDimensions(aorm,dres['data'])

#completed


#output the asset list
#for r in ares['data']:
#    print(r)
#    mid = r["id"][0]
#    orm.insert(MetaTag(metaDataId=mid, tagName="openpipe_canonical_moment", value=0))
#orm.commitClose()
