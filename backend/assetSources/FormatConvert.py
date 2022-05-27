#!/bin/python3


import requests
import formatHelp


# a set of static format converters for translating Museum Tags into Canonical Tag format
class FormatConvert:

      # extract a string value from a tag and return it as an element of a list
      def ConvertString(data, tagname):
          return ([data[tagname]])

      #extract the date information from the Met convert the sequence to a list.
      def getMetDate(data):
        era = "CE"
        year1 = abs(int(data["objectBeginDate"]))
        year2 = abs(int(data["objectEndDate"]))
        if "B.C." in data["objectDate"]:
            era = "BC"

        res = []
        res["openpipe_canonical_firstDate"] = [
            era + " " + str(year1) + " " + "JAN" + " " + "01" + " " + "00:00:00"]
        res["openpipe_canonical_lastDate"] = [era + " " + str(year2) + " " + "JAN" + " " + "01" + " " + "00:00:00"]
        res["openpipe_canonical_date"] = [res["openpipe_canonical_firstDate"][0], res["openpipe_canonical_lastDate"][0]]
        return (response)
