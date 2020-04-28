

#from abc import ABC, abstractmethod


class MuseumsTM():
    """
        The abstract class for museums. All new museum classes should inharit this class and override the methods below
    """
    def __init__(self, schema):
        """
        The constructor.
        :param schema: The proper canonical schema to make sure that the each search has all the canonicals
        """
        self.schema = schema
        self.name = "somemuseum"

    def setName(self,aname):
        self.name = aname

    def searchForAssets(self, term):
        """
        Query the muesum endpoints for a specific term.
        :param term: The search string like cat
        :return: the json result that the museum endpoint returns
        """
        pass

    def getMetaTagMapping(self, data):
        """
        The mapping from the museum metaTags to openpipe canonical tags
        :param data: The assets metatags from the museum api
        :return: A JSON with canonical metatags and the asset metatags that every value is an array
        """
        pass

    def getAssetMetaData(self, assetId):
        """
        Sends a get request to Muesum API to get the asset metadata
        :param assetId: The asset id in the museum
        :return: a json that contains the asset metadata
        """
        pass

    def getData(self, q, page, pageSize):
        """
        This function can be called from other classes to ask for search
        that the search has canonical mapping with paging capabilities
        :param q: search term
        :param page: page number
        :param pageSize: page size
        :return: JSON containing all the assets returned as the search result with the canonical tags in correct format.
        """
        pass
