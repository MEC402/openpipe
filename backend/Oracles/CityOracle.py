from AbstractOracle import OracleMasterTemplate
from backend.Oracles.Formatter import Formatter
from backend.openpipeAPI.ORM.ORM import ORM
from backend.openpipeAPI.ORM.TO import TO


class CityOracle(OracleMasterTemplate):

    def runOracle(self):
        orm = ORM()

        stm = """SELECT * FROM metaTag where tagName='openpipe_canonical_city' and status='formatted' group by value;"""
        res = orm.executeSelect(stm)
        orm.commitClose()

        cf = Formatter()
        i = 1

        allTopicValues = []

        for r in res['data']:

            i = i + 1

            metaTagId = r['id'][0]
            metaTagValue = r['value'][0]


            validLabels=['GPE','ORG','LOC','NORP']
            cn=cf.countryInput(metaTagValue)
            print(i)
            print(r['id'][0], r['value'][0])
            temp=[]
            for c in cn:
                lb=c.label_
                print(c.text, c.label_)

                if lb in validLabels:
                    temp.append(c.text)

            finalTopicString=""
            if len(temp)>1:
                for t in temp:
                    finalTopicString+=t+','
            elif len(temp)==0:
                finalTopicString=metaTagValue
            else:
                finalTopicString=temp[0]

            allTopicValues.append(finalTopicString)


        uniqueTopics=set(allTopicValues)
        print("City:")
        print("# ALL Topics",len(allTopicValues))
        print("# unique Topics",len(uniqueTopics))
        print(uniqueTopics)


            # topicId = self.isKnown(metaTagValue, r)
            # if topicId != -1:
            #     self.assignTopicToMetaTag(metaTagId, topicId)
            # else:
            #     self.addNewTopic(metaTagValue)

    def isKnown(self, tagValue, additionalTagInfo):

        return -1

    def addNewTopic(self, topicValue):
        orm = ORM()
        tables = TO().getClasses()
        Topic = tables["topic"]
        mid = orm.insert(Topic(name=topicValue, description='nation description',type='nation',))
        return mid

    def assignTopicToMetaTag(self, metaTagId, topicId):

        orm = ORM()
        tables = TO().getClasses()
        MetaTag = tables["metaTag"]
        orm.session.query(MetaTag).filter(MetaTag.id == int(metaTagId)).update({"topic_id": topicId,"status":"known"})

