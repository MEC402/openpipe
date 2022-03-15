#the set of python functions for manipulating and managing topic sets


# A topic entry is a set that contains a collection of values that
# are considered to be equivalent.  For example the artist names:
#  Van Gogh and V. Gogh are considered to be equivalent

# the functions in this file provide the mechanism for listing the
# sets for a given topic and for listing the members of a set
# and all basic Create,Retrieval,Update, and Delete operations

import json
import mysql
import sys
sys.path.append('../')
from ORM.ORM import ORM

#create a new empty topic equivalency set depend on auto increment of id
def createTopicSet(atopic):
#add new entry
    myorm = ORM()
    sqlcmd = 'insert into '+atopic+' ( name ) values ( "openpipe_name" );'
#    print(sqlcmd)
    results = myorm.executeSQL(sqlcmd)
#    print(results)

    sqlcmd = 'select max(id) from ' + atopic
    results = myorm.executeSelect(sqlcmd)
    adat = results['data']
    return adat[0]['max(id)'][0]


#delete a topic set completely
def deleteTopicSet(atopic, aid):
    myorm = ORM()
#first delete all the values for the id.
    sqlcmd = 'delete from '+atopic+'_tags where topic_id="'+str(aid)+'";'
#    print(sqlcmd)
    results = myorm.executeSQL(sqlcmd)

#now delete the id itself
    sqlcmd = 'delete from '+atopic+' where id="'+str(aid)+'";'
#    print(sqlcmd)
    results = myorm.executeSQL(sqlcmd)
#    print(results)

#get all the members of a given topic set
def getTopicSet(atopic, aid):
    myorm = ORM()
    sqlcmd = 'select * from '+atopic+'_tags where topic_id="'+str(aid)+'";'
#    print(sqlcmd)
    results = myorm.executeSelect(sqlcmd)
    return results

# now handle the members of the topic set
#add a new value to a topic equivalance set
def addTopicValue(atopic, aid, avalue):
    myorm = ORM()
    sqlcmd = 'insert into '+atopic+'_tags (value, topic_id) values ("'+avalue+'",  "' + str(aid)+'");'
#    print(sqlcmd)
    results = myorm.executeSQL(sqlcmd)
    return results

# remove the specified value from the equivalency set
def removeTopicValue(atopic, aid, avalue):
    myorm = ORM()
    sqlcmd = 'delete from '+atopic+'_tags where value="'+avalue+'" and topic_id="'+str(aid)+'";'
#    print(sqlcmd)
    results = myorm.executeSQL(sqlcmd)
    return results


# check for equivalency
def isTopicValueEqual(atopic, avalue1, avalue2):
    anid1 = getTopicId(atopic,avalue1)
    anid2 = getTopicId(atopic,avalue2)
    if anid1 == anid2: return True
#    print("false")
    return False

# get member set
def getTopicId(atopic, avalue):
    myorm = ORM()
    sqlcmd = 'select * from '+atopic+'_tags where value="'+avalue+'";'
#    print(sqlcmd)
    results = myorm.executeSelect(sqlcmd)
    adat = results['data']
#    print(adat)
    if len(adat) <= 0: return -1
    if len(adat[0]['topic_id']) <= 0: return -1
    return adat[0]['topic_id'][0]

