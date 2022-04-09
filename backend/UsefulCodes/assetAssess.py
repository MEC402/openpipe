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

import operator



#get a complete list of all assets in the federation
def getAssets(aorm):
#    tables = TO().getClasses()
#    MetaTag = tables["metaTag"]
    res =aorm.executeSelect("""SELECT * FROM asset order by metaDataId;""")
    return res

def get_tagName(atag):
    print (atag)
    return atag.get('tagName')

#get the canonical topic names that must exist for each asset
def getCanons(aorm):
#    res = aorm.executeSelect("""SELECT name FROM canonicalMetaTag where req='yes'""")
    res = aorm.executeSelect("""SELECT name FROM canonicalMetaTag""")
    ares=[]
    for an in res['data']:
        ares.append(an['name'][0])
    return ares

#get the canonical topic names that must exist for each asset
def getCanonTopics(aorm):
    res = aorm.executeSelect("""SELECT tagName, status, value FROM metaTag where tagName like 'openpipe_canonical_%';""")
    ares=[]
    for an in res['data']:
        ares.append(an)
    ares.sort(key=operator.itemgetter('tagName','status'))
#    print(ares)
    return ares

#get the canonical topic names that must exist for each asset
def getAssetCanonTags(anasset,aorm):
    query="SELECT tagName, status, value FROM metaTag where metaDataId=" +str(anasset['metaDataId'][0]) +" and tagName like 'openpipe_canonical_%';" 
#    print(query)
    res = aorm.executeSelect(query)
    ares={}
    for an in res['data']:
        ares[an['tagName'][0]] = {'value': an['value'][0], 'status': an['status'][0]}
    return ares

#update a set of specific cannon tags for a specific asset
def updateAssetCanonTags(anasset, cantag, aorm):

    for acan in cantag:
       avalue = cantag[acan]['value']
       astatus = cantag[acan]['status']
       if astatus == 'formatted':
 #       print(avalue)
 #       print(astatus)
 #       print(acan)
        query="update metaTag set value=\'"+avalue +"\', status=\'"+astatus+"\' where metaDataId=\'" +str(anasset['metaDataId'][0]) +"\' and tagName=\'"+acan+"\';"
 #       print(query)
        #res = aorm.executeSelect(query)



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

    sqlsrc = """select t1.metaDataId, t2.value from metaTag t1 inner join metaTag t2 on t1.metaDataId=t2.metaDataId where t1.tagName='%s' and t1.value='%s' and t2.tagName='dimensions';""" %( topic, defstring)
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
    nums = re.compile('[0-9]+\.?[0-9]*')

    mysize = sizelist[0]
    numlist = nums.findall(mysize)
    if len(numlist) > 0: sizedict['width'] = numlist[0]
    if len(numlist) > 1: sizedict['height'] = numlist[1]
    if len(numlist) > 2: sizedict['depth'] = numlist[2]

    return sizedict

def extractH2Sizes(sizelist):
    sizedict ={}
    sizedict['height'] = "29.7"
    sizedict['width'] = "21.0"
    sizedict['depth'] = "1.0"
    nums = re.compile('[0-9]+\.?[0-9]*')

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
    acount = [0,0,0,0,0,0,0,0,0,0,0,0]
    onetime = 1
    updlist =[]

#first build our regular expression for some of the cases
    mysizes = re.compile('\'*width\'*\s*:\s*[0-9]+.[0-9]*|\'*height\'*\s*:\s*[0-9]+.[0-9]*|\'*depth\'*\s*:\s*[0-9]+.[0-9]*')
    myovr = re.compile('\([0-9]+.[0-9]*.*?cm.*?\)')
    myhre = re.compile('\(\s*[0-9]+\.?[0-9]*\s*x\s*[0-9]+\.?[0-9]*\s*x\s*[0-9]+\.?[0-9]*\s*cm.*\)')
    myhre2 = re.compile('\(\s*[0-9]+.[0-9]*\s*x\s*[0-9]+.[0-9]*\s*cm.*?\)')
    myhre3 = re.compile('\(\s*[0-9]+\.*[0-9]*\s*cm.*?\)')
    for adim in adimlist:
        width = defwidth
        height = defheight
        depth = defdepth
        akv = {'height': "29.7", "width": "21.0", "depth": "1.0"}
        ares = {'metadataid': adim['metaDataId'][0]}
#        print(ares)
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
                   ares['dims'] = akv
                   updlist.append(ares)
                   iparsecount += 1
#                 print(akv)
#                 else:
#                     print(matchstring)
#                 print("++++++++++++++++++")
                 acount[10] += 1
                 nummatch += 1
        elif (str.startswith(matchstring, "Overall")):
#                 print(matchstring)
                 dimlist = myovr.findall(matchstring)
                 if (len(dimlist) > 0):
                   akv = extractOvrSizes(dimlist)
                   ares['dims'] = akv
                   updlist.append(ares)
                   iparseoverall += 1
                 else:
                     print(dimlist)
#                 print(akv)
                 acount[11] += 1
                 nummatch += 1
                 ioverall += 1
        elif (str.startswith(matchstring, "H.")):
#                 print(ascii(matchstring))
                 matchstring  = matchstring.replace("\xd7","x")
                 adimlist = myhre.findall(matchstring)
                 adimlist2 = myhre2.findall(matchstring)
                 adimlist3 = myhre3.findall(matchstring)
#                 print("MOAT" + ascii(matchstring))
                 if (len(adimlist) > 0):
                     akv = extractH3Sizes(adimlist)
                     ares['dims'] = akv
                     updlist.append(ares)
#                     print(akv)
                 elif (len(adimlist2) > 0):
                     akv = extractH2Sizes(adimlist2)
                     print(akv)
                     ares['dims'] = akv
                     updlist.append(ares)
                 elif (len(adimlist3) > 0):
                     akv = extractH3Sizes(adimlist3)
                     ares['dims'] = akv
                     updlist.append(ares)
                 else:
                     print(matchstring)
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
                 ares['dims'] = akv
                 updlist.append(ares)
                 ibparse += 1
#                 print(dimdict)
                 acount[7] += 1
                 nummatch += 1
        elif (str.startswith(matchstring, "Height:")):
#                print(matchstring)
                 acount[8] += 1
                 nummatch += 1
        elif len(matchstring) > 0 and (matchstring[0].isdigit()):
#                 print(matchstring)
                 matchstring  = matchstring.replace("\xd7","x")
                 adimlist = myhre.findall(matchstring)
                 adimlist2 = myhre2.findall(matchstring)
#                 print("MOAT" + ascii(matchstring))
                 if (len(adimlist) > 0):
                     akv = extractH3Sizes(adimlist)
                     ares['dims'] = akv
                     updlist.append(ares)
#                     print(akv)
                 elif (len(adimlist2) > 0):
                     akv = extractH2Sizes(adimlist2)
#                     print(akv)
                     ares['dims'] = akv
                     updlist.append(ares)
#                 else:
#                     print(matchstring);
                 acount[9] += 1
                 nummatch += 1
        else:
#           print ("Unrecognized dimensions format: %s" % adim['value'][0])
           unknowndim += 1

    print("Total Unknown Dimension tags = %d out of %d" % (unknowndim,totaldim))
    print("Total Empty Dimension tags = %d out of %d" % (nodims,totaldim))
    print("Number matched = %d/%d" % (nummatch,totaldim))
    print("for { successfully parsed %d/%d" % (iparsecount, innercount))
    print("for 'Overall' successfully parsed %d/%d" % (iparseoverall, ioverall))
    print("for '[{' successfully parsed %d/%d" % (ibparse, ibsize))
    print(acount)
    return(updlist)

def updateDimensions(aorm,dimlist):
    #create a series of update strings with commands
    sqlstring = "update metaTag set value=%s where metaDataId=%s and tagName='openpipe_canonical_physicalDimensions';" 
    datalist = []
    for adim in dimlist:
      #step one generate the dimension string in: W,H,D format
      whdstring = "%s, %s, %s" % (adim['dims']['width'],
                                  adim['dims']['height'],
                                  adim['dims']['depth'])
#      print (adim)
      atuple = (whdstring, adim['metadataid'])
      datalist.append(atuple)

#    print(datalist)
    aorm.batchSql(datalist,sqlstring,False)


##connect to the federation
#aorm =ORM()
#
###here we are going to generate a report about the assets stored in the Table
###the report will tell us how many assets there are.
###How many are missing some tags
###How many have incorrect values on their CanonicalTopic Tags
#
##get the asset list
#ares = getAssets(aorm)
#
##how many assets are there in the table:
#print("The Federated Asset Table Has %d assets." % len(ares['data']))
#
##how many of those have physicalDimensions canonTopic?
#pres = getPhysical(aorm)
#print ("There are %d assets with Physical Dimensions." % len(pres['data']))
#
#if len(pres['data']) != len(ares['data']):
#    mres = getNotIn(aorm,'openpipe_canonical_physicalDimensions')
#    print ("The following %d assets do not have proper physical dimensions" % len(mres['data']))
#    for r in mres['data']:
#        print (r)
#
##how many of these have default values
#dres = getDefault(aorm,'openpipe_canonical_physicalDimensions')
#print("The following %d assets have default physical Dimensions" % len(dres['data']))
##for r in dres['data']:
##     print (r)
#
##now we will use the original source dimensions
##it appears that all assets use 'dimensions' in the original museum list
#
##get all canonical dimensions with museum data
#dres = getDimensions(aorm,'openpipe_canonical_physicalDimensions')
#print ("There are %d default dimension Assets to fix" % len(dres['data']))
#updlist = correctDimensions(aorm,dres['data'])
#print(len(updlist))
##print(updlist)
#updateDimensions(aorm,updlist)
#
##completed
#
#
##output the asset list
##for r in ares['data']:
##    print(r)
##    mid = r["id"][0]
##    orm.insert(MetaTag(metaDataId=mid, tagName="openpipe_canonical_moment", value=0))
##orm.commitClose()
