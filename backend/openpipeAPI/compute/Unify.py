import traceback

import requests
import xml.etree.ElementTree as ET

import Slack
from openpipeAPI.ORM.BL import BL
from openpipeAPI.ORM.ORM import ORM


class Unify:
    """
        This class has methods that help the unification of the elements like artists
    """

    def unifyArtists(self):

        orm = ORM()
        groupedArtists = orm.executeSelect(
            "SELECT value,count(value) as freq FROM metaTag where tagName='openpipe_canonical_artist' group by value order by count(value) desc ")
        print(groupedArtists["data"])
        for artist in groupedArtists["data"][205:]:
            artistRawName = artist["value"][0]
            artistRawName = artistRawName.replace(")", "")
            splitRawName = artistRawName.split("(")
            nationality = ""
            artistName = splitRawName[0]
            if len(splitRawName) > 1:
                if self.isNationality(splitRawName[1].split(",")[0]):
                    nationality = splitRawName[1].split(",")[0]
            print(artistRawName)
            print(artistName)
            print(nationality)
            prefName = ""
            aliases = []
            try:
                if "Anonymous" in artistRawName or "anonymous" in artistRawName.lower():
                    artistName = "anonymous"
                if artistName != "" and artistName != "OpenPipe" and artistName != "anonymous":
                    res = self.getAliases(artistName, "", nationality)
                    if len(res) > 0:
                        res = res[0]
                        prefName = res["name"]
                        aliases = res["aliases"]
                if prefName != "":
                    artistName = prefName

                BL().addArtist(artistName, nationality, str(aliases))
            except Exception as e:
                track = traceback.format_exc()
                Slack.sendMessage(track)

    def isNationality(self, name):
        NATIONALITIES = {'Afghan': 'Afghan', 'Albanian': 'Albanian', 'Algerian': 'Algerian', 'American': 'American',
                         'Andorran': 'Andorran', 'Angolan': 'Angolan', 'Antiguans': 'Antiguans',
                         'Argentinean': 'Argentinean', 'Armenian': 'Armenian', 'Australian': 'Australian',
                         'Austrian': 'Austrian', 'Azerbaijani': 'Azerbaijani', 'Bahamian': 'Bahamian',
                         'Bahraini': 'Bahraini', 'Bangladeshi': 'Bangladeshi', 'Barbadian': 'Barbadian',
                         'Barbudans': 'Barbudans', 'Batswana': 'Batswana', 'Belarusian': 'Belarusian',
                         'Belgian': 'Belgian', 'Belizean': 'Belizean', 'Beninese': 'Beninese', 'Bhutanese': 'Bhutanese',
                         'Bolivian': 'Bolivian', 'Bosnian': 'Bosnian', 'Brazilian': 'Brazilian', 'British': 'British',
                         'Bruneian': 'Bruneian', 'Bulgarian': 'Bulgarian', 'Burkinabe': 'Burkinabe',
                         'Burmese': 'Burmese', 'Burundian': 'Burundian', 'Cambodian': 'Cambodian',
                         'Cameroonian': 'Cameroonian', 'Canadian': 'Canadian', 'Cape Verdean': 'Cape Verdean',
                         'Central African': 'Central African', 'Chadian': 'Chadian', 'Chilean': 'Chilean',
                         'Chinese': 'Chinese', 'Colombian': 'Colombian', 'Comoran': 'Comoran', 'Congolese': 'Congolese',
                         'Costa Rican': 'Costa Rican', 'Croatian': 'Croatian', 'Cuban': 'Cuban', 'Cypriot': 'Cypriot',
                         'Czech': 'Czech', 'Danish': 'Danish', 'Djibouti': 'Djibouti', 'Dominican': 'Dominican',
                         'Dutch': 'Dutch', 'Dutchman': 'Dutchman', 'Dutchwoman': 'Dutchwoman',
                         'East Timorese': 'East Timorese', 'Ecuadorean': 'Ecuadorean', 'Egyptian': 'Egyptian',
                         'Emirian': 'Emirian', 'Equatorial Guinean': 'Equatorial Guinean', 'Eritrean': 'Eritrean',
                         'Estonian': 'Estonian', 'Ethiopian': 'Ethiopian', 'Fijian': 'Fijian', 'Filipino': 'Filipino',
                         'Finnish': 'Finnish', 'French': 'French', 'Gabonese': 'Gabonese', 'Gambian': 'Gambian',
                         'Georgian': 'Georgian', 'German': 'German', 'Ghanaian': 'Ghanaian', 'Greek': 'Greek',
                         'Grenadian': 'Grenadian', 'Guatemalan': 'Guatemalan', 'Guinea-Bissauan': 'Guinea-Bissauan',
                         'Guinean': 'Guinean', 'Guyanese': 'Guyanese', 'Haitian': 'Haitian',
                         'Herzegovinian': 'Herzegovinian', 'Honduran': 'Honduran', 'Hungarian': 'Hungarian',
                         'I-Kiribati': 'I-Kiribati', 'Icelander': 'Icelander', 'Indian': 'Indian',
                         'Indonesian': 'Indonesian', 'Iranian': 'Iranian', 'Iraqi': 'Iraqi', 'Irish': 'Irish',
                         'Israeli': 'Israeli', 'Italian': 'Italian', 'Ivorian': 'Ivorian', 'Jamaican': 'Jamaican',
                         'Japanese': 'Japanese', 'Jordanian': 'Jordanian', 'Kazakhstani': 'Kazakhstani',
                         'Kenyan': 'Kenyan', 'Kittian and Nevisian': 'Kittian and Nevisian', 'Kuwaiti': 'Kuwaiti',
                         'Kyrgyz': 'Kyrgyz', 'Laotian': 'Laotian', 'Latvian': 'Latvian', 'Lebanese': 'Lebanese',
                         'Liberian': 'Liberian', 'Libyan': 'Libyan', 'Liechtensteiner': 'Liechtensteiner',
                         'Lithuanian': 'Lithuanian', 'Luxembourger': 'Luxembourger', 'Macedonian': 'Macedonian',
                         'Malagasy': 'Malagasy', 'Malawian': 'Malawian', 'Malaysian': 'Malaysian',
                         'Maldivan': 'Maldivan', 'Malian': 'Malian', 'Maltese': 'Maltese', 'Marshallese': 'Marshallese',
                         'Mauritanian': 'Mauritanian', 'Mauritian': 'Mauritian', 'Mexican': 'Mexican',
                         'Micronesian': 'Micronesian', 'Moldovan': 'Moldovan', 'Monacan': 'Monacan',
                         'Mongolian': 'Mongolian', 'Moroccan': 'Moroccan', 'Mosotho': 'Mosotho', 'Motswana': 'Motswana',
                         'Mozambican': 'Mozambican', 'Namibian': 'Namibian', 'Nauruan': 'Nauruan',
                         'Nepalese': 'Nepalese', 'Netherlander': 'Netherlander', 'New Zealander': 'New Zealander',
                         'Ni-Vanuatu': 'Ni-Vanuatu', 'Nicaraguan': 'Nicaraguan', 'Nigerian': 'Nigerian',
                         'Nigerien': 'Nigerien', 'North Korean': 'North Korean', 'Northern Irish': 'Northern Irish',
                         'Norwegian': 'Norwegian', 'Omani': 'Omani', 'Pakistani': 'Pakistani', 'Palauan': 'Palauan',
                         'Panamanian': 'Panamanian', 'Papua New Guinean': 'Papua New Guinean',
                         'Paraguayan': 'Paraguayan', 'Peruvian': 'Peruvian', 'Polish': 'Polish',
                         'Portuguese': 'Portuguese', 'Qatari': 'Qatari', 'Romanian': 'Romanian', 'Russian': 'Russian',
                         'Rwandan': 'Rwandan', 'Saint Lucian': 'Saint Lucian', 'Salvadoran': 'Salvadoran',
                         'Samoan': 'Samoan', 'San Marinese': 'San Marinese', 'Sao Tomean': 'Sao Tomean',
                         'Saudi': 'Saudi', 'Scottish': 'Scottish', 'Senegalese': 'Senegalese', 'Serbian': 'Serbian',
                         'Seychellois': 'Seychellois', 'Sierra Leonean': 'Sierra Leonean', 'Singaporean': 'Singaporean',
                         'Slovakian': 'Slovakian', 'Slovenian': 'Slovenian', 'Solomon Islander': 'Solomon Islander',
                         'Somali': 'Somali', 'South African': 'South African', 'South Korean': 'South Korean',
                         'Spanish': 'Spanish', 'Sri Lankan': 'Sri Lankan', 'Sudanese': 'Sudanese',
                         'Surinamer': 'Surinamer', 'Swazi': 'Swazi', 'Swedish': 'Swedish', 'Swiss': 'Swiss',
                         'Syrian': 'Syrian', 'Taiwanese': 'Taiwanese', 'Tajik': 'Tajik', 'Tanzanian': 'Tanzanian',
                         'Thai': 'Thai', 'Togolese': 'Togolese', 'Tongan': 'Tongan',
                         'Trinidadian or Tobagonian': 'Trinidadian or Tobagonian', 'Tunisian': 'Tunisian',
                         'Turkish': 'Turkish', 'Tuvaluan': 'Tuvaluan', 'Ugandan': 'Ugandan', 'Ukrainian': 'Ukrainian',
                         'Uruguayan': 'Uruguayan', 'Uzbekistani': 'Uzbekistani', 'Venezuelan': 'Venezuelan',
                         'Vietnamese': 'Vietnamese', 'Welsh': 'Welsh', 'Yemenite': 'Yemenite', 'Zambian': 'Zambian',
                         'Zimbabwean': 'Zimbabwean'}

        if name in NATIONALITIES:
            return True
        return False

    def getAliases(self, name, role, nationality):
        xml = self.searchArtist(name, role, nationality)
        if xml is not None:
            pars = self.parseXMLForSubjects(xml)
            print(len(pars))
            if len(pars)<20:
                for a in pars:
                    aliasXML = self.getArtistAliases(a['id'])
                    a['aliases'] = self.parseXMLForAliasNames(aliasXML)

                return pars
        return {}

    def getArtistAliases(self, subjectID):
        url = "http://vocabsservices.getty.edu/ULANService.asmx/"
        serviceName = "ULANGetSubject"
        params = {'subjectID': subjectID}

        r = requests.get(url=url + serviceName, params=params)
        data = r.content
        print(data)
        return data

    def searchArtist(self, name, role, nationality):
        url = "http://vocabsservices.getty.edu/ULANService.asmx/"
        serviceName = "ULANGetTermMatch"
        params = {'name': name,
                  'roleid': role,
                  'nationid': nationality}

        r = requests.get(url=url + serviceName, params=params)
        data = r.content
        print(data)
        return data

    def parseXMLForSubjects(self, xmlStr):
        root = ET.fromstring(xmlStr)
        subjects = []
        for item in root.findall('Subject'):
            ids = {}
            termCount = 0
            # iterate child elements of item
            for child in item:
                if child.tag == 'Subject_ID':
                    ids['id'] = child.text
                elif child.tag == 'Preferred_Term':
                    ids['name'] = child.text
                elif child.tag == 'Term':
                    termCount = termCount + 1
            ids['termCount'] = termCount
            subjects.append(ids)
        return subjects

    def parseXMLForAliasNames(self, xmlStr):
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


u = Unify()
u.unifyArtists()
