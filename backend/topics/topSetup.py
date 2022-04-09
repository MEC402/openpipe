# connect to the remote sql server and create the set of topic tables

import json
import mysql

#this is done to allow module loads from other sibling level packages
#seems very hacky
import sys
sys.path.append('../')

from ORM.DBInfo import DBInfo
from ORM.ORM import ORM

#instantiate the Object for connecting to the database
myorm = ORM()

#create a topic table and a topic_tags table
def createNamedTable(aname):
    sqlcmd = 'create table '+aname+' AS (select id, name, otherNames, insertTime, lastModified from artist where 1=2)'
    results = myorm.executeSQL(sqlcmd)
    print(results)

    sqlcmd = 'create table '+aname+'_tags (id int, value varchar(255), topic_id int)'
    results = myorm.executeSQL(sqlcmd)
    print(results)

#simple test of SQL database access
sqlcmd = 'select * from artist'
results = myorm.executeSelect(sqlcmd)
#print(results)

# create the title topic table: 
createNamedTable("title")


# create the source topic table: 
createNamedTable("source")


# create the artist topic table: 
#     this table already exists createNamedTable("artist")

# create the culture topic table: 
createNamedTable("culture")

# create the genre topic table: 
createNamedTable("genre")

# create the medium topic table: 
createNamedTable("medium")

# create the nation topic table: 
createNamedTable("nation")

# create the city topic table: 
createNamedTable("city")


