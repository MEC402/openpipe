#!/bin/python3


import requests
import formatHelp
import json


# a set of static format converters for translating Museum Tags into Canonical Tag format
class FormatConvert:

      # extract a string value from a tag and return it as an element of a list
      @staticmethod
      def ConvertString(data, tagname):
          return ([data[tagname]])

      #extract the date information from the Met convert the sequence to a list.
      def getMetDate(data):
        era = "CE"
        year1 = abs(int(data["objectBeginDate"]))
        year2 = abs(int(data["objectEndDate"]))
        if "B.C." in data["objectDate"]:
            era = "BC"

        res = {}
        adate = era + " " + str(year1) + " " + "JAN" + " " + "01" + " " + "00:00:00"
        res["openpipe_canonical_firstDate"] = [adate]
        res["openpipe_canonical_lastDate"] = [era + " " + str(year2) + " " + "JAN" + " " + "01" + " " + "00:00:00"]
        res["openpipe_canonical_date"] = [res["openpipe_canonical_firstDate"][0], res["openpipe_canonical_lastDate"][0]]
        return (res)


      #extract the physical dimensions of the object
      # we are attempting to extract Height, Width, Depth
      # rules for the met.
      #  if height, width, depth present just use that.
      #  for the met: Length and Depth are the same thing.
      #  also we extract the largest Height, Width, and Depth values
      #  when multiple sizes are included in the array.
      def getMetDimensions(data):
        
        height = -1.0
        width = -1.0
        depth = -1.0
       
#        print("START-----")
#        print(data["measurements"])
#        print("----------")
        if (data["measurements"] ==  None):
           return ("-1.0, -1.0, -1.0")

        for x in data["measurements"]:
#           print(x)
           measure = x
           onem = x['elementMeasurements'];
#           print(onem)
           if 'Height' in onem:
#             print('Height found')
             nheight = float(onem['Height'])
#             print(nheight)
             if (nheight > height):
                height = nheight

           if 'Width' in onem:
#             print('Width found')
             nwidth = float(onem['Width'])
#             print(nwidth)
             if (nwidth > width):
                width = nwidth

           if 'Depth' in onem:
#             print('Depth found')
             ndepth = float(onem['Depth'])
#             print(ndepth)
             if (ndepth > depth):
                depth = ndepth

           if 'Length' in onem:
#             print('Length found')
             ndepth = float(onem['Length'])
#             print(ndepth)
             if (ndepth > depth):
                depth = ndepth

        #mj = json.loads(measure)
        #print(mj)
#        print("END-----")

        #restring = "H, W, D" cm, 21.0,29.7,1.0
        restring = str(height)+", "+str(width)+", "+str(depth)
#        print (restring)
        return (restring)

      #extract the physical dimensions of the Cleveland object
      # we are attempting to extract Height, Width, Depth
      # rules for the met.
      #  if height, width, depth present just use that.
      #  for the met: Length and Depth are the same thing.
      #  also we extract the largest Height, Width, and Depth values
      #  when multiple sizes are included in the array.
      def getClevDimensions(data):
        
        height = -1.0
        width = -1.0
        depth = -1.0
       
#        print("START-----")
#        print(data["measurements"])
#        print("----------")
        if (data["dimensions"] ==  None):
           return ("-1.0, -1.0, -1.0")

        if "overall" in data["dimensions"]:
          mysize = data["dimensions"]["overall"]
          if 'height' in mysize: height = mysize["height"]
          if 'width' in mysize: width = mysize["width"]
          if 'depth' in mysize: depth = mysize["depth"]

        #mj = json.loads(measure)
        #print(mj)
#        print("END-----")

        #restring = "H, W, D" cm, 21.0,29.7,1.0
        restring = str(height)+", "+str(width)+", "+str(depth)
#        print (restring)
        return (restring)

      #extract the Cleveland Artist names from the creators array
      def getClevArtists(data):
       
        artistname = ""
        if (data["creators"] ==  None):
           return ""
        for x in data["creators"]:
           if "role" in x:
             if x["role"] == "artist":
              artistname = x["description"]

        return (artistname)

      #extract the Rijks Artist names from the principalMaker 
      def getRijksArtist(data):
       
        artistname = ""
        if "principalMaker" in data:
          #print(data["principalMaker"])
          artistname = data["principalMaker"]
        elif "principalOrFirstMaker" in data:
          artistname = data["principalOrFirstMaker"]
        elif "principalMakers" in data:
            for pm in data["principalMakers"]:
               artistname = pm["name"]
	         

        return (artistname)

      #extract the physical dimensions of the Rijks object
      # we are attempting to extract Height, Width, Depth
      # rules for the met.
      #  if height, width, depth present just use that.
      #  for the met: Length and Depth are the same thing.
      #  also we extract the largest Height, Width, and Depth values
      #  when multiple sizes are included in the array.
      def getRijksDim(data):
        
        height = -1.0
        width = -1.0
        depth = -1.0
       
#        print("START-----")
#        print(data["measurements"])
#        print("----------")
        if (data["dimensions"] ==  None):
           return ("-1.0, -1.0, -1.0")


        for x in data["dimensions"]:
          if x["type"] == "height":
            height = float(x["value"])

          if x["type"] == "width":
            width = float(x["value"])

          if x["type"] == "depth":
            depth = float(x["value"])

          if x["type"] == "diameter":
            width = float(x["value"])

        #mj = json.loads(measure)
        #print(mj)
#        print("END-----")

        #restring = "H, W, D" cm, 21.0,29.7,1.0
        restring = str(height)+", "+str(width)+", "+str(depth)
#        print (restring)
        return (restring)

