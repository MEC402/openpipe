from abc import ABC, abstractmethod


class OracleMasterTemplate(ABC):
    """
        The abstract class for Oracles. All oracles classes should inherit this class and override the methods below
    """
    def __init__(self):
        """
        The constructor.
        :param schema: The proper canonical schema to make sure that the each search has all the canonicals
        """
        pass

    def generateOracle(self):
        """
        Generate initial value from current data
        :param term: The search string like cat
        :return: the json result that the museum endpoint returns
        """
        pass

    def isKnown(self, tagValue, additionalTagInfo):
        """
        Check if the tag value is know by the oracle
        :param tagValue: The metatag value from the museum api
        :param additionalTagInfo: The additional metatags to help with the classification of the tagvalue
        :return: id of the known topic
        """
        pass

    def addNewTopic(self, topicValue):
        """
        Create a new topic
        :param topicValue: The value of the new topic
        :return: id of the new topic
        """
        pass

    def assignTopicToMetaTag(self, metaTagId, topicId):
        """
        Create a new topic
        :param metaTagId: The id of the metaTag
        :param topicId: The id of the metaTag Topic
        :return: id of the metaTag
        """
        pass

