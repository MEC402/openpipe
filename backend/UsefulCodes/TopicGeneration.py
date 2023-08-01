import itertools
import re
import spacy
from sqlalchemy import and_

from backend.openpipeAPI.ORM.ORM import ORM
from backend.openpipeAPI.ORM.TO import TO

orm = ORM()
tables = TO().getClasses()
MetaData = tables["metaData"]
Topic = tables["topic"]

guidMappingResultSet = orm.executeSelect(
    """SELECT * FROM artmaster.guidType;""")

guidCodeMap = {}

for guidMap in guidMappingResultSet["data"]:
    guidCodeMap[guidMap["name"][0]] = str(guidMap["code"][0])

print(guidCodeMap)

canonicalTagResultSet = orm.executeSelect(
    """SELECT * FROM artmaster.canonicalMetaTag;""")

miscMetaTagData = set([])

compressionCount = 0

nlp = spacy.load("en_core_web_sm")

insertDataArray = []


def saveTopics(metaTagData, guidName, guidCode):
    for m in metaTagData:
        insertDataArray.append(Topic(name=m, type=guidName, code=guidCode))
        print(metaTagData)

    orm.bulkInsert(insertDataArray)
    print("insertSize = "+str(len(insertDataArray)))

    # print("compressionCount = "+str(compressionCount))
    orm.commitClose()


def make_histogram(dictf, limit, plotName):
    import matplotlib.pyplot as plt
    import numpy as np

    map = dict(itertools.islice(dictf.items(), limit))
    plt.figure(figsize=(30, 20))

    plt.bar(map.keys(), map.values(), 1.0, color='g')

    plt.xticks(rotation=90)

    # Add a title and labels to the axes
    plt.title("Frequency of the " + plotName + " tag values")
    # Define the x label
    plt.xlabel('Tag')
    # Define the y label
    plt.ylabel('Frequency')

    # Add a grid to the plot
    plt.grid(axis='y', alpha=0.75)

    # Add a legend to the plot
    plt.legend(['Freq'], loc='upper left')

    # Display the histogram
    # plt.show()
    plt.savefig("plots/" + plotName + '.png')


def tokenize(topicMetaTagResultSet):
    topics = {}
    ukw = []
    for topicMetaTag in topicMetaTagResultSet["data"]:
        metaTagValue = str(topicMetaTag["value"][0])
        doc = nlp(metaTagValue)

        # print(metaTagValue)
        for token in doc:
            if not token.is_stop:
                # print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
                #       token.shape_, token.is_alpha, token.is_stop)
                if token.pos_ == "PROPN" or token.pos_ == "NOUN" or token.pos_ == "VERB":
                    lemma = token.lemma_.lower()
                    if lemma in topics:
                        topics[lemma] += 1
                    else:
                        topics[lemma] = 1

        # print("_________________________________________")

    sorted_topics = sorted(topics.items(), key=lambda x: x[1], reverse=True)
    topics = dict(sorted_topics)

    print(len(topics))
    print(topics)
    print(len(ukw), ukw)
    make_histogram(topics, 50, "tokens")
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    return topics

def artist_topics(topicMetaTagResultSet):
    # topicValue = re.sub(r"\([^()]*\)", "", str(topicMetaTag["value"][0]).strip()).strip().lower()
    topics = {}
    ukw = []
    for topicMetaTag in topicMetaTagResultSet["data"]:
        pf = False
        metaTagValue = str(topicMetaTag["value"][0])
        doc = nlp(metaTagValue)

        # print(metaTagValue)

        for ent in doc.ents:
            # print(ent.text, ent.start_char, ent.end_char, ent.label_)

            if ent.label_ in ["ORG", "PERSON"]:
                pf = True
                lemma = ent.text.lower()
                if lemma in topics:
                    topics[lemma] += 1
                else:
                    topics[lemma] = 1

        if not pf:
            for token in doc:
                if not token.is_stop:
                    # print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
                    #       token.shape_, token.is_alpha, token.is_stop)
                    if token.pos_ == "PROPN" or token.pos_ == "NOUN":
                        lemma = token.lemma_.lower()
                        if lemma in topics:
                            topics[lemma] += 1
                        else:
                            topics[lemma] = 1

        # print("_________________________________________")

    sorted_topics = sorted(topics.items(), key=lambda x: x[1], reverse=True)
    topics = dict(sorted_topics)

    print(len(topics))
    print(topics)
    print(len(ukw), ukw)
    make_histogram(topics, 100, "artist")
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    return topics


def city_topics(topicMetaTagResultSet):
    topics = {}
    ukw = []
    for topicMetaTag in topicMetaTagResultSet["data"]:
        pf = False
        metaTagValue = str(topicMetaTag["value"][0])
        doc = nlp(metaTagValue)

        # print(metaTagValue)

        for ent in doc.ents:
            # print(ent.text, ent.start_char, ent.end_char, ent.label_)

            if ent.label_ in ["GPE", "LOC", "ORG", "PERSON", "NORP"]:
                pf = True
                lemma = ent.text.lower()
                if lemma in topics:
                    topics[lemma] += 1
                else:
                    topics[lemma] = 1

        if pf == False:
            for token in doc:
                if not token.is_stop:
                    # print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
                    #       token.shape_, token.is_alpha, token.is_stop)
                    if token.pos_ == "PROPN" or token.pos_ == "NOUN" or token.pos_ == "VERB":
                        lemma = token.lemma_.lower()
                        if lemma in topics:
                            topics[lemma] += 1
                        else:
                            topics[lemma] = 1

        # print("_________________________________________")

    sorted_topics = sorted(topics.items(), key=lambda x: x[1], reverse=True)
    topics = dict(sorted_topics)

    print(len(topics))
    print(topics)
    print(len(ukw), ukw)
    make_histogram(topics, 100, "city")
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    return topics


def medium_topics(topicMetaTagResultSet):
    topics = {}
    ukw = []
    for topicMetaTag in topicMetaTagResultSet["data"]:
        metaTagValue = str(topicMetaTag["value"][0])
        doc = nlp(metaTagValue)

        # print(metaTagValue)
        for token in doc:
            if not token.is_stop:
                if token.pos_ == "PROPN" or token.pos_ == "NOUN" or token.pos_ == "VERB":
                    lemma = token.lemma_.lower()
                    if lemma in topics:
                        topics[lemma] += 1
                    else:
                        topics[lemma] = 1

        # print("_________________________________________")

    sorted_topics = sorted(topics.items(), key=lambda x: x[1], reverse=True)
    topics = dict(sorted_topics)

    print(len(topics))
    print(topics)
    print(len(ukw), ukw)
    make_histogram(topics, 50, "medium")
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    return topics


def culture_topics(topicMetaTagResultSet):
    topics = {}
    ukw = []
    for topicMetaTag in topicMetaTagResultSet["data"]:
        pf = False
        metaTagValue = str(topicMetaTag["value"][0])
        doc = nlp(metaTagValue)

        # print(metaTagValue)

        for ent in doc.ents:
            if ent.label_ in ["DATE", "GPE", "LOC", "ORG", "PERSON", "NORP"]:
                pf = True
                lemma = ent.text.lower()
                if lemma in topics:
                    topics[lemma] += 1
                else:
                    topics[lemma] = 1

        if pf == False:
            for token in doc:
                if not token.is_stop:
                    # print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
                    #       token.shape_, token.is_alpha, token.is_stop)
                    if token.pos_ == "PROPN" or token.pos_ == "NOUN" or token.pos_ == "VERB":
                        lemma = token.lemma_.lower()
                        if lemma in topics:
                            topics[lemma] += 1
                        else:
                            topics[lemma] = 1

                # print(ent.text, ent.start_char, ent.end_char, ent.label_)

        # print("_________________________________________")

    sorted_topics = sorted(topics.items(), key=lambda x: x[1], reverse=True)
    topics = dict(sorted_topics)

    print(len(topics))
    print(topics)
    print(len(ukw), ukw)
    make_histogram(topics, 100, "culture")
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    return topics


def classification_topics(topicMetaTagResultSet):
    topics = {}
    ukw = []
    for topicMetaTag in topicMetaTagResultSet["data"]:
        metaTagValue = str(topicMetaTag["value"][0])
        doc = nlp(metaTagValue)

        # print(metaTagValue)

        for token in doc:
            if not token.is_stop:
                if token.pos_ == "PROPN" or token.pos_ == "NOUN" or token.pos_ == "VERB":
                    lemma = token.lemma_.lower()
                    if lemma in topics:
                        topics[lemma] += 1
                    else:
                        topics[lemma] = 1
        # print("_________________________________________")

    sorted_topics = sorted(topics.items(), key=lambda x: x[1], reverse=True)
    topics = dict(sorted_topics)

    print(len(topics))
    print(topics)
    print(len(ukw), ukw)
    make_histogram(topics, 100, "classification")
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    return topics


def nation_topics(topicMetaTagResultSet):
    topics = {}
    ukw = []
    for topicMetaTag in topicMetaTagResultSet["data"]:
        pf = False
        metaTagValue = str(topicMetaTag["value"][0])
        doc = nlp(metaTagValue)

        # print(metaTagValue)

        for ent in doc.ents:
            if ent.label_ in ["GPE", "LOC", "NORP"]:
                pf = True
                lemma = ent.text.lower()
                if lemma in topics:
                    topics[lemma] += 1
                else:
                    topics[lemma] = 1

        if pf == False:
            for token in doc:
                if not token.is_stop:
                    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
                          token.shape_, token.is_alpha, token.is_stop)
                    if token.pos_ == "PROPN" or token.pos_ == "NOUN" or token.pos_ == "VERB":
                        lemma = token.lemma_.lower()
                        if lemma in topics:
                            topics[lemma] += 1
                        else:
                            topics[lemma] = 1

                # print(ent.text, ent.start_char, ent.end_char, ent.label_)

        # print("_________________________________________")

    sorted_topics = sorted(topics.items(), key=lambda x: x[1], reverse=True)
    topics = dict(sorted_topics)

    print(len(topics))
    print(topics)
    print(len(ukw), ukw)
    make_histogram(topics, 100, "nation")
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    return topics


def run_topic_generation(canonicalTagName):
    tagName = canonicalTagName.split("_")[2].lower()
    guidCode = guidCodeMap[tagName]
    guidName = tagName
    print(tagName, guidCode)

    topicMetaTagResultSet = orm.executeSelect(
        "select distinct value from metaTag where tagName=\'" + canonicalTagName + "\'")
    if canonicalTagName == "openpipe_canonical_artist":
        t = artist_topics(topicMetaTagResultSet)
        saveTopics(t, guidName, guidCode)
    elif canonicalTagName == "openpipe_canonical_city":
        t = city_topics(topicMetaTagResultSet)
        saveTopics(t, guidName, guidCode)
    elif canonicalTagName == "openpipe_canonical_medium":
        t = medium_topics(topicMetaTagResultSet)
    elif canonicalTagName == "openpipe_canonical_title":
        t = tokenize(topicMetaTagResultSet)
        saveTopics(t, guidName, guidCode)
    elif canonicalTagName == "openpipe_canonical_culture":
        t = culture_topics(topicMetaTagResultSet)
        saveTopics(t, guidName, guidCode)
    elif canonicalTagName == "openpipe_canonical_classification":
        t = classification_topics(topicMetaTagResultSet)
        saveTopics(t, guidName, guidCode)
    elif canonicalTagName == "openpipe_canonical_nation":
        t = nation_topics(topicMetaTagResultSet)
        saveTopics(t, guidName, guidCode)


names = ["artist", "medium", "culture", "city", "nation", "classification", "title"]
for i in names:
    tagName = i
    run_topic_generation("openpipe_canonical_" + tagName)

# run_topic_generation("openpipe_canonical_" + "culture")

# for canonicalTag in canonicalTagResultSet["data"]:
#     print("**********************************************")
#     canonicalTagName = canonicalTag["name"][0]
#     # banCanonicals = ["openpipe_canonical_id", "openpipe_canonical_fullImage", "openpipe_canonical_smallImage",
#     #                  "openpipe_canonical_largeImage", "openpipe_canonical_biography",
#     #                  "openpipe_canonical_sourceLargeImage",
#     #                  "openpipe_canonical_sourceSmallImage", "openpipe_canonical_sourceFullImage",
#     #                  "openpipe_canonical_thumbnailImage", "openpipe_canonical_thumbnailImageDimensions",
#     #                  "openpipe_canonical_defaultImage", "openpipe_canonical_webImage",
#     #                  "openpipe_canonical_defaultImageDimensions", "openpipe_canonical_webImageDimensions",
#     #                  "openpipe_canonical_galleryImage", "openpipe_canonical_galleryImageDimensions"]
#
#     tagName = canonicalTagName.split("_")[2].lower()
#
#     metaTagData = set()
#
#     if tagName in guidCodeMap:
#         print(canonicalTag)
#
#         guidCode = guidCodeMap[tagName]
#         guidName = tagName
#         print(tagName, guidCode)
#
#         # canonicalTagName="openpipe_canonical_genre"
#         topicMetaTagResultSet = orm.executeSelect(
#             "select distinct value from metaTag where tagName=\'" + canonicalTagName + "\'")
#
#         if canonicalTagName == "openpipe_canonical_artist":
#             artist_topics(topicMetaTagResultSet)
#         elif canonicalTagName == "openpipe_canonical_city":
#             city_topics(topicMetaTagResultSet)
#         # print(topicValue)
#
#         # if len(metaTagData) == 0:
#         #     # print("its empty")
#         #     metaTagData.add(topicValue)
#         #     # print(topicValue)
#         # else:
#         #     for mt in metaTagData.copy():
#         #         # print(mt, topicValue)
#         #         if topicValue.startswith(mt) or mt.startswith(topicValue):
#         #             # print("in here")
#         #             compressionCount+=1
#         #             if len(topicValue)<len(mt) and len(topicValue)>0:
#         #                 print(topicValue+"___________"+mt)
#         #                 metaTagData.remove(mt)
#         #                 metaTagData.add(topicValue)
#         #             elif len(mt)<=0:
#         #                 metaTagData.remove(mt)
#         #                 metaTagData.add(topicValue)
#         #
#         #         elif topicValue not in metaTagData:
#         #             # print("hi")
#         #             metaTagData.add(topicValue)
#
#         # for m in metaTagData:
#         #     # print(m)
#         #     insertDataArray.append(Topic(name=m, type=guidName, code=guidCode))
#         # print(metaTagData)
#         # # print(insertDataArray)
#
#
# # orm.bulkInsert(insertDataArray)
# # print("insertSize = "+str(len(insertDataArray)))
# #
# # print("compressionCount = "+str(compressionCount))
# # orm.commitClose()
