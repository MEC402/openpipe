from geotext import GeoText
import spacy
import re


class Formatter:

    def __init__(self):
        pass

    def countryInput(self,countryString):


        nlp = spacy.load("en_core_web_sm")
        doc = nlp(countryString)

        return doc.ents
            # print(ent.text, ent.start_char, ent.end_char, ent.label_)

    def removePrantesis(self, inpStr):
        result = re.sub(r"\((.*?)\)", "", inpStr)

        return result

