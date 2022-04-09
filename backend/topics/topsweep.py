# topsweep.py
#
# sweep through the asset meta tag list for each topic and generate unique
# data elements that can be added to topic values

import sys
sys.path.append('../')
from ORM.ORM import ORM

import topAPI


def sweepTopic(atopic):
  myorm = ORM()
    
#first we extract all metatags form the asset metatag table with this topic into a list.
  sqlcmd= 'select * from metaTag where tagName="openpipe_canonical_'+atopic+'";'
  print(sqlcmd)
  results = myorm.executeSelect(sqlcmd)
#  print(results)

#by using a set we get only unique values
  valueset = set()
  for adi in results['data']:
      newvalue = adi['value'][0]
      valueset.add(newvalue)

#  print(valueset)
  print(len(valueset))


#  then in the advanced version we do some magic to find equivalent values (this is not written yet

# now we take this list and fill in the topic table entries for the values.
  for topicitem in valueset:
      #first create a topic set
      newid = topAPI.createTopicSet(atopic)
      #now add the topicitems
      print(topicitem)
      topAPI.addTopicValue(atopic,newid,topicitem)



#below we execute the sweep across all topics

#sweepTopic("title")
#sweepTopic("source")  these are special
#sweepTopic("artist")  these are special
##sweepTopic("culture")
##sweepTopic("genre")
##sweepTopic("medium")
##sweepTopic("nation")
##sweepTopic("city")



