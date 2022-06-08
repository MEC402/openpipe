#!/bin/python3

import requests
from MuseumsTM import MuseumsTM
from multiprocessing.pool import ThreadPool
import formatHelp


class SmithsonianMuseum(MuseumsTM):

    def __init__(self, schema):
        self.schema= schema
        self.name = "Smithsonian"
#        self.canonmap = {
#                "openpipe_canonical_id": "objectID",
#                "openpipe_canonical_largeImage": "primaryImage",
#                "openpipe_canonical_smallImage": "primaryImageSmall",
#                "openpipe_canonical_title": "title",
#                "openpipe_canonical_artist": "artistDisplayName",
#                "openpipe_canonical_culture":  "culture",
#                "openpipe_canonical_classification": "classification",
#                "openpipe_canonical_nation":  "country",
#                "openpipe_canonical_city":  "city",
#                "openpipe_canonical_tags":  "tags"
#                        }
        self.fullcanonmap = {
                "id": "openpipe_canonical_id",
                "title": "openpipe_canonical_title",
                "creators": "openpipe_canonical_artist",
                "culture": "openpipe_canonical_culture"
                        }
        self.canonmap = {
                "title": "openpipe_canonical_title",
                "creators": "openpipe_canonical_artist",
                "culture": "openpipe_canonical_culture",
                "medium": "openpipe_canonical_medium"
                        }


    def searchForAssets(self, term):
        # parameters = {'q': term, 'key': self.attributes['key'] }
        # response = requests.get(url=self.attributes['url'], params=parameters)
        # data = response.json()
        # return data


        parameters = {'q': term, 'api_key': 'imQAjl1QkgYj0EiPybG1lKaz4dp0AZSauYCgPi3B', ':category' : 'culture' }
        response = requests.get(url='https://api.si.edu/openaccess/api/v1.0/search', params=parameters)
        data = response.json()
        return data


if __name__=='__main__':

        print("start of search")
        sm=SmithsonianMuseum("") 
        d=sm.searchForAssets(" cat ")
        print(d)
        print("End search")
        