#! C:/Python37-32/python.exe

import cgi
import requests
import json
import xml.etree.ElementTree as ET


def cgiFieldStorageToDict(fieldStorage):
    """ Get a plain dictionary rather than the '.value' system used by the
   cgi module's native fieldStorage class. """
    params = {}
    for key in fieldStorage.keys():
        params[key] = fieldStorage[key].value
    return params


def getArtistAliases(subjectID):
    url = "http://vocabsservices.getty.edu/ULANService.asmx/"
    serviceName = "ULANGetSubject"
    params = {'subjectID': subjectID}

    r = requests.get(url=url + serviceName, params=params)
    data = r.content
    return data


def searchArtist(name, role, nationality):
    url = "http://vocabsservices.getty.edu/ULANService.asmx/"
    serviceName = "ULANGetTermMatch"
    params = {'name': name,
              'roleid': role,
              'nationid': nationality}

    r = requests.get(url=url + serviceName, params=params)
    data = r.content
    return data


def parseXMLForSubjects(xmlStr):
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


def parseXMLForAliasNames(xmlStr):
    root = ET.fromstring(xmlStr)
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
    return names


print("Content-Type: text/json\n")
dict = cgiFieldStorageToDict(cgi.FieldStorage())

if 'role' not in dict.keys():
    dict['role']=''

if 'nation' not in dict.keys():
    dict['nation']=''

if 'searchName' not in dict.keys():
    print(json.dumps([{"name": '', "id": "", "termCount": 0, "aliases": []}]))

else:
    xml = searchArtist(dict['searchName'], dict['role'], dict['nation'])
    pars = parseXMLForSubjects(xml)

    for a in pars:
        aliasXML = getArtistAliases(a['id'])
        a['aliases'] = parseXMLForAliasNames(aliasXML)

    print(json.dumps(pars))
