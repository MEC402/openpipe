#test out all of the functions for manipulating the topics
import topAPI


#add a new equivalence topic set to the database table
aresult = topAPI.createTopicSet('title')
#aresult=7
print(aresult)

tresult = topAPI.addTopicValue('title', aresult, "AnotherValue")
print(tresult)

nresult = topAPI.getTopicSet('title', aresult)
print(aresult)


anid = topAPI.getTopicId('title','AnotherValue')
print(anid)

if topAPI.isTopicValueEqual('title', "AnotherValue", "TotallyDifferent"):
    print("yes")
else:
    print("no")

tresult = topAPI.removeTopicValue('title', aresult, "AnotherValue")
print(tresult)

nresult = topAPI.getTopicSet('title', aresult)
print(aresult)

topAPI.deleteTopicSet('title',aresult)

