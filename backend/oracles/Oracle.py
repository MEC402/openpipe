import json
import xml.etree.ElementTree as ET
import requests


class Oracle:

    def getLocationAliases(self,subjectID):
        url = "http://vocabsservices.getty.edu/TGNService.asmx/"
        serviceName = "TGNGetSubject"
        params = {'subjectID': subjectID}

        r = requests.get(url=url + serviceName, params=params)
        data = r.content
        return data

    def searchLocation(self,name, role, nationality):
        url = "http://vocabsservices.getty.edu/TGNService.asmx/"
        serviceName = "TGNGetTermMatch"
        params = {'name': name,
                  'placetypeid': role,
                  'nationid': nationality}

        r = requests.get(url=url + serviceName, params=params)
        data = r.content
        return data

    def parseXMLForSubjects(self,xmlStr):
        root = ET.fromstring(xmlStr)
        subjects = []
        for item in root.findall('Subject'):
            ids = {}
            termCount = 0
            # iterate child elements of item
            for child in item:
                # print(child.tag)
                # print(child.attrib)
                # print(child.text)
                if child.tag == 'Subject_ID':
                    ids['id'] = child.text
                elif child.tag == 'Preferred_Term':
                    ids['name'] = child.text
                elif child.tag == 'Term':
                    termCount = termCount + 1
            ids['termCount'] = termCount
            subjects.append(ids)
        return subjects

    def parseXMLForAliasNames(self,xmlStr):
        root = ET.fromstring(xmlStr)
        info = {}
        coordinateInformation = {}
        names = []
        for item in root.findall('Subject'):
            for child in item:
                if child.tag == 'Terms':
                    for c in child:
                        if c.tag == 'Preferred_Term':
                            for cc in c:
                                if cc.tag == 'Term_Text':
                                    names.append(cc.text)
                        elif c.tag == 'Non-Preferred_Term':
                            for cc in c:
                                if cc.tag == 'Term_Text':
                                    names.append(cc.text)
                elif child.tag == 'Coordinates':
                    for coordinates in child:
                        for coordinateDetails in coordinates:
                            if coordinateDetails.tag == 'Latitude':
                                latitudeInfo = {}
                                for latitudeValues in coordinateDetails:
                                    latitudeInfo[latitudeValues.tag.lower()] = latitudeValues.text
                                coordinateInformation['latitude'] = latitudeInfo
                            elif coordinateDetails.tag == 'Longitude':
                                longitudeInfo = {}
                                for longitudeValues in coordinateDetails:
                                    longitudeInfo[longitudeValues.tag.lower()] = longitudeValues.text
                                coordinateInformation['longitude'] = longitudeInfo
        info['coordinates'] = coordinateInformation;
        info['aliases'] = names
        return info

    def getLocationInfo(self,searchName,type,nation):
        xml = self.searchLocation(searchName,type,nation)
        pars = self.parseXMLForSubjects(xml)
        for a in pars:
            aliasXML = self.getLocationAliases(a['id'])
            results = self.parseXMLForAliasNames(aliasXML)
            a['aliases'] = results['aliases']
            a['coordinates'] = results['coordinates']
        return pars