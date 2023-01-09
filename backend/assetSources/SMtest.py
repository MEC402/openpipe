from cgi import print_arguments
from email import header
from email.quoprimime import body_check
from html import entities
import json
import queryBody
import re
from wsgiref import headers
import requests
from MuseumsTM import MuseumsTM
from multiprocessing.pool import ThreadPool
import formatHelp


class ParisMuseum(MuseumsTM):

    def __init__(self, schema):
        self.schema= schema
        self.name = "Paris"
        self.canonmap = {
               "openpipe_canonical_id": "objectID",
               "openpipe_canonical_largeImage": "primaryImage",
               "openpipe_canonical_smallImage": "primaryImageSmall",
               "openpipe_canonical_title": "title", 
              # "openpipe_canonical_date":  "date",
               "openpipe_canonical_artist": "artistDisplayName",
              #  "openpipe_canonical_culture":  "culture",
              #  "openpipe_canonical_classification": "classification",
               "openpipe_canonical_nation":  "country",
               "openpipe_canonical_city":  "city",
               "openpipe_canonical_tags":  "tags",

              #  "openpipe_canonical_fullImage": "fullImage",
              #  "openpipe_canonical_firstDate":  "firstDate",
               "openpipe_canonical_lastDate": "endDate"
                       }
# ...................................................
        # self.fullcanonmap = {
        #         "id": "openpipe_canonical_id",
        #         "title": "openpipe_canonical_title",
        #         "creators": "openpipe_canonical_artist",
        #         "culture": "openpipe_canonical_culture"
        #                 }
        # self.canonmap = {
        #         "title": "openpipe_canonical_title",
        #         "creators": "openpipe_canonical_artist",
        #         "culture": "openpipe_canonical_culture",
        #         "medium": "openpipe_canonical_medium"
        #                 }


    def searchForAssets(self, term):
        
        url =  "https://apicollections.parismusees.paris.fr/graphql"
        header = {
            "Content-Type": "application/json",
            "auth-token": "323ac194-f611-4583-9620-b5e9351f56ad"
        }

#---------- List of museum-----------------------------------------
        prefixbody = '''
  query($limit: Int!,$offset: Int!) {
  nodeQuery(limit: $limit, offset: $offset, filter: {conditions: [
    {field: "type", value: "oeuvre"}
    {field: "field_oeuvre_types_objet.entity.field_lref_adlib", value: "4493"}
  ]}) {
    count
   '''

        body = prefixbody + queryBody.tailbody

        limit = 500
        out = []
        variables = {'limit':limit,'offset':0}
        # print(body)
        response = requests.post(url=url, headers=header, json={"query":body, 'variables':variables})
        data1 = response.json()
        #print(data1)
        out = out + data1['data']['nodeQuery']['entities']
        size_ = data1['data']['nodeQuery']['count']
        print(size_)

        for offset in range(limit,size_,limit):
          # print(offset)

          variables = {'limit':limit,'offset':offset}
          response = requests.post(url=url, headers=header, json={"query":body, 'variables':variables})
          data = response.json()
          #out.append(data)
          out= out + data['data']['nodeQuery']['entities']

          offset += limit
          print(len(data['data']['nodeQuery']['entities']))
          print(len(out))
          # print(data)
        #return {data1}
        # print(out[:10])
        
    
        return out
        

    def getMetaTagMapping(self, data):
        #total=len(data['data']['nodeQuery']["entities"])
        #data = data['data']['nodeQuery']["entities"][0]..???
        # data = data['data']['nodeById'] #......................................................................................??? change?................
  
        self.canonmap["openpipe_canonical_id"]=data["entityUuid"]
        self.canonmap["openpipe_canonical_title"]=data["title"]

        # start_date = data["fieldDateProduction"]["startYear"]
        end_date = data["fieldDateProduction"]["endYear"]
        if end_date is not None:
          self.canonmap["openpipe_canonical_lastDate"]= ["CE" + str(end_date) + " " + "JAN" + " " + "01" + " " + "00:00:00"]
          self.canonmap["openpipe_canonical_date"] = self.canonmap["openpipe_canonical_lastDate"][0]



        # if start_date != None:
        #   self.canonmap["openpipe_canonical_firstDate"]=start_date
        # if end_date is not None:
        #   self.canonmap["openpipe_canonical_lastDate"]=end_date

        self.canonmap["openpipe_canonical_artist"]=data["fieldOeuvreAuteurs"][0]["entity"]["fieldAuteurAuteur"]["entity"]["name"]
        if "fieldVisuels" in data and len(data["fieldVisuels"])>0:
          if data["fieldVisuels"][0]["entity"]["vignette"] != None:
            self.canonmap["openpipe_canonical_fullImage"] = data["fieldVisuels"][0]["entity"]["vignette"]

        
        return self.canonmap

    def getAssetMetaData(self, assetId):
        assetId = str(assetId)
        url =  "https://apicollections.parismusees.paris.fr/graphql"
        header = {
            "Content-Type": "application/json",
            "auth-token": "323ac194-f611-4583-9620-b5e9351f56ad"
        }



#............................................................................................................................   body='''{nodeQuery ......................    

        body='''{nodeQuery(filter: {conditions: [{field: "uuid", value: \"'''+assetId+'''\"}]}) {
    entities {
      entityUuid
      ... on NodeOeuvre {
        title
        absolutePath
        fieldLrefAdlib
        fieldUrlAlias
        fieldTitreDeMediation
        fieldSousTitreDeMediation
        fieldOeuvreAuteurs {
          entity {
            fieldAuteurAuteur {
              e   {
                name
                fieldPipDateNaissance {
                 startPrecision
                  startYear
                  startMonth
                  startDay
                  sort
                  endPrecision
                  endYear
                  endMonth
                  endDay
                  processed
                }
                fieldPipLieuNaissance
                fieldPipDateDeces {
                 startPrecision
                  startYear
                  startMonth
                  startDay
                  sort
                  endPrecision
                  endYear
                  endMonth
                  endDay
                  processed
                }
                 fieldLieuDeces
              }
            }
            fieldAuteurFonction {
              entity {
                name
              }
            }
          }
        }
        fieldVisuels {
          entity {
            name
            vignette
            publicUrl
          }
        }
        fieldDateProduction {
          startPrecision
          startYear
          startMonth
          startDay
          sort
          endPrecision
          endYear
          endMonth
          endDay
          century
          processed
        }
        fieldOeuvreSiecle {
           entity {
            name
          }
        }
        fieldOeuvreTypesObjet {
          entity {
            name
            fieldLrefAdlib
            entityUuid
          }
        }
        fieldDenominations {
          entity {
            name
          }
        }
        fieldMateriauxTechnique{
          entity {
            name
          }
        }
        fieldOeuvreDimensions {
          entity {
            fieldDimensionPartie {
              entity {
                name
              }
            }
            fieldDimensionType {
              entity {
                name
              }
            }
            fieldDimensionValeur
            fieldDimensionUnite {
             entity {
                name
              }
            }
          }
        }
        fieldOeuvreInscriptions{
          entity {
            fieldInscriptionType {
              entity {
                name
              }
            }
            fieldInscriptionMarque {
              value
            }
            fieldInscriptionEcriture {
              entity {
                name
              }
            }
          }
        }
        fieldOeuvreDescriptionIcono {
          value
        }
        fieldCommentaireHistorique {
          value
        }
        fieldOeuvreThemeRepresente	 {
          entity {
            name
          }
        }
        fieldLieuxConcernes {
          entity {
            name
          }
        }
        fieldModaliteAcquisition {
          entity {
            name
          }
        }
        fieldDonateurs {
          entity {
            name
          }
        }
        fieldDateAcquisition {
          startPrecision
          startYear
          startMonth
          startDay
          sort
          endPrecision
          endYear
          endMonth
          endDay
          century
          processed
        }
        fieldOeuvreNumInventaire
        fieldOeuvreStyleMouvement {
          entity {
            name
          }
        }
        fieldMusee {
          entity {
            name
          }
        }
        fieldOeuvreExpose {
          entity {
            name
          }
        }
        fieldOeuvreAudios {
          entity {
            fieldMediaFile {
              entity {
                url
                uri {
                  value
                  url
                }
              }
            }
          }
        }
        fieldOeuvreVideos {
          entity {
            fieldMediaVideoEmbedField
          }
        }
        fieldHdVisuel {
          entity {
            fieldMediaImage {
              entity {
                url
              }
            }
          }
        }
      }
    }
  }
}'''


#............................................................................................................................   end  ......................    

  
        response = requests.post(url=url, headers=header, json={"query":body})
        data = response.json()
        metaData = self.getMetaTagMapping(data)
        return metaData

    def getMetaDataByAssetID(self,objctID):
        serviceName = str(objctID)
        response = requests.get(url=self.url + serviceName)
        data = response.json()
        return data["data"]

    def getData(self, q, page, pageSize):
        results = []
        retrievedAssets = self.searchForAssets(q)
        print("************PRINTING RETRIVED ASSETS*************")
        # print(retrievedAssets)
        print("************END of RETRIVED ASSETS*************")
    # print(json.dumps({"root":out[:3]}))
        # test_out = pm.getMetaTagMapping(out[2]) 
        # print("Test Mapping")
        # print(test_out)

        start = (page - 1) * pageSize
        step = pageSize
        total = len(retrievedAssets)
        if total == 0:
            return {"data": [], "total": 0, "sourceName": "Paris Museum"}

        if int(start) > total:
            start = total - 1
        if int(start) + int(step) > total:
            step = total - int(start) - 1

        assets = retrievedAssets[int(start):int(start) + int(step)]

        # print(assets)

        pool = ThreadPool(len(assets))
        for asset in assets:
          if asset != None:
            results.append(pool.apply_async(self.getMetaTagMapping, args=[asset]))
            #results.append(pool.apply_async(self.getAssetMetaData, args=[asset["entityId"]]))...................................................
        pool.close()
        pool.join()
        results = [r.get() for r in results]
        return {"data": results,
                "total": 0,
                "sourceName": "Paris Museum"}


if __name__=='__main__':

    print("start of search")
    pm=ParisMuseum("")
    # d=pm.searchForAssets(" chat ")
    # print(d)
    # print(len(d["data"]["nodeQuery"]["entities"]))

    # # for dd in d["data"]["nodeQuery"]["entities"]:
    # #     print(dd)

    #################################...........................
    # a = pm.getData(" chat ",1,100).............................................
    # print(json.dumps(a)).......................................................
    m = pm.getData(q="chat", page=1, pageSize= 10)
    print("*************************** search ********************************") 
    print(m)
  

    

    print("End search") 
    
    
    
    
######################******* Start SM code***********#####################################

    
    #!/bin/python3
 
import requests
import json
from MuseumsTM import MuseumsTM
from multiprocessing.pool import ThreadPool
import formatHelp
 
 
class SmithsonianMuseum(MuseumsTM):
 
   def __init__(self, schema):
       self.schema= schema
       self.name = "Smithsonian"
       self.canonmap = {
              "openpipe_canonical_id": "objectID",
        #       "openpipe_canonical_largeImage": "primaryImage",
        #       "openpipe_canonical_smallImage": "primaryImageSmall",
              "openpipe_canonical_title": "title",
              "openpipe_canonical_artist": "artistDisplayName",
              "openpipe_canonical_date": "date",
        #       "openpipe_canonical_culture":  "culture",
        #       "openpipe_canonical_classification": "classification",
        #       "openpipe_canonical_nation":  "country",
        #       "openpipe_canonical_city":  "city",
        #       "openpipe_canonical_tags":  "tags",
                # "openpipe_canonical_tags":  "tags",
              
              "openpipe_canonical_medium": "medium",
              "openpipe_canonical_physicalDimensions": "dimansions"
              
                       }
#        self.fullcanonmap = {
#                "id": "openpipe_canonical_id",
#                "title": "openpipe_canonical_title",
#                "creators": "openpipe_canonical_artist",
#                "culture": "openpipe_canonical_culture"
#                        }
#        self.canonmap = {
#                "title": "openpipe_canonical_title",
#                "creators": "openpipe_canonical_artist",
#                "culture": "openpipe_canonical_culture",
#                "medium": "openpipe_canonical_medium"
#                       }
 
 
   def searchForAssets(self, term):
          
#        parameters = {'q': term, 'key': self.attributes['key'] }
#        response = requests.get(url=self.attributes['url'], params=parameters)
#        data1 = response.json()
#        return data1
      
 
       parameters = {'q': term, 'api_key': 'imQAjl1QkgYj0EiPybG1lKaz4dp0AZSauYCgPi3B', 'rows' : 5}
       url = 'https://api.si.edu/openaccess/api/v1.0/category/science_technology/search'
       response = requests.get(url=url, params=parameters)
       data1 = response.json()
       print("response:")
       print(data1)
      
       limit = 5
       out = []
      
       out = out + data1['response']['rows']
       size_ = data1['response']['rowCount']
       print(size_)
 
       for offset in range(0,size_,limit):
        #  print(offset)
 
         parameters = {'q': term, 'api_key': 'imQAjl1QkgYj0EiPybG1lKaz4dp0AZSauYCgPi3B', 'rows':5,'start':0}
         response = requests.get(url=url, params=parameters)
         data = response.json()
         out = out + data['response']['rows']
 
         offset += limit
       #   print(len(data['response']['rows']))
       #   print(len(out))
       # print(data)
       # return {data1}
       # print(out)
  
       return out
     
   def getMetaTagMapping(self, data): 
       temp = {
              "openpipe_canonical_id": "objectID",
              "openpipe_canonical_title": "title",
              "openpipe_canonical_artist": "artistDisplayName",
              "openpipe_canonical_date": "date",
              "openpipe_canonical_medium": "medium",
              "openpipe_canonical_physicalDimensions": "dimansions",
              "openpipe_canonical_datasource": "datasource"
              
                       }  
       print("in mapping:")
       print(data["title"],temp["openpipe_canonical_title"])
       temp["openpipe_canonical_id"]=data['id']
       temp["openpipe_canonical_title"]=data['title']
       temp["openpipe_canonical_artist"]=data['content']['freetext']['name'][0]['content']
#        self.canonmap["openpipe_canonical_date"]=data['content']['freetext']['date'][0]['content']
       temp["openpipe_canonical_medium"]=data['content']['freetext']['setName'][1]['content']
       temp["openpipe_canonical_fullImage"]=data['content']['descriptiveNonRepeating']['online_media']['media'][0]['thumbnail']
       temp["openpipe_canonical_physicalDimensions"]=data['content']['descriptiveNonRepeating']['online_media']['media'][0]['resources'][1]['dimensions']
       end_date = ((data['content']['freetext']['date'][0]['content']).upper()).replace('A','E')
       if end_date is not None:
          temp["openpipe_canonical_Date"]= [str(end_date) + " " + "JAN" + " " + "01" + " " + "00:00:00"][0]
       print(data["title"],temp["openpipe_canonical_title"])
       
       temp["openpipe_canonical_datasource"]=data['content']['descriptiveNonRepeating']['data_source']
       
       return temp
      
   def getAssetMetaData(self, assetId):
        #*************** Note: 
        # The assetId is a dictionary here that contains the whole asset info here not just the id   
        # the assetId name has not been change so it follows the parent class format
        # TODO: Fix the name later 
           
       metaData = self.getMetaTagMapping(assetId)
       return metaData
 
   def getData(self, q, page, pageSize):
       results = []
       retrievedAssets = self.searchForAssets(q)
#        print("************PRINTING RETRIVED ASSETS*************")
#        print(retrievedAssets)
#        print(len(retrievedAssets)) 
#        print("************END of RETRIVED ASSETS*************")
        
       start = (page - 1) * pageSize
       step = pageSize
       total = len(retrievedAssets)
       if total == 0:
           return {"data": [], "total": 0, "sourceName": "Smithsonian Museum"}
 
       if int(start) > total:
           start = total - 1
       if int(start) + int(step) > total:
           step = total - int(start) - 1
#        print(start)
#        print(step)
       assets = retrievedAssets[int(start):int(start) + int(step)]
#        print(assets)
 
       for asset in assets:
        #  print(asset["title"])
         results.append(self.getAssetMetaData(asset))
       print(results)
       return {"data": results,
               "total": len(results),
               "sourceName": "Smithsonian Museum"}
 
 
if __name__=='__main__':
 
       print("*************************** search ********************************")
 
       sm=SmithsonianMuseum("")
      
       search=sm.searchForAssets(" cat ")
       print(search)
       print("************************** End search ***************************")
       # getdata = sm.getData(q=" cat ", page=1, pageSize= 8)
       # a = json.dumps(getdata)
       
       # print(a)


      
######################******* End SM code***********#####################################




#################---------------- Start SM WORKING code --------------------###########################
      

#!/bin/python3
 
import requests
import json
from MuseumsTM import MuseumsTM
from multiprocessing.pool import ThreadPool
import formatHelp
 
 
class SmithsonianMuseum(MuseumsTM):
 
   def __init__(self, schema):
       self.schema= schema
       self.name = "Smithsonian"
       self.canonmap = {
              "openpipe_canonical_id": "objectID",
        #       "openpipe_canonical_largeImage": "primaryImage",
        #       "openpipe_canonical_smallImage": "primaryImageSmall",
              "openpipe_canonical_title": "title",
              "openpipe_canonical_artist": "artistDisplayName",
              "openpipe_canonical_date": "date",
        #       "openpipe_canonical_culture":  "culture",
        #       "openpipe_canonical_classification": "classification",
        #       "openpipe_canonical_nation":  "country",
        #       "openpipe_canonical_city":  "city",
        #       "openpipe_canonical_tags":  "tags",
                # "openpipe_canonical_tags":  "tags",
              
              "openpipe_canonical_medium": "medium",
              "openpipe_canonical_physicalDimensions": "dimansions"
              
                       }
#        self.fullcanonmap = {
#                "id": "openpipe_canonical_id",
#                "title": "openpipe_canonical_title",
#                "creators": "openpipe_canonical_artist",
#                "culture": "openpipe_canonical_culture"
#                        }
#        self.canonmap = {
#                "title": "openpipe_canonical_title",
#                "creators": "openpipe_canonical_artist",
#                "culture": "openpipe_canonical_culture",
#                "medium": "openpipe_canonical_medium"
#                       }
 
 
   def searchForAssets(self, term):
          
#        parameters = {'q': term, 'key': self.attributes['key'] }
#        response = requests.get(url=self.attributes['url'], params=parameters)
#        data1 = response.json()
#        return data1
      
 
       parameters = {'q': term, 'api_key': 'imQAjl1QkgYj0EiPybG1lKaz4dp0AZSauYCgPi3B', 'rows' : 5}
       url = 'https://api.si.edu/openaccess/api/v1.0/category/art_design/search'
       response = requests.get(url=url, params=parameters)
       data1 = response.json()
       print("response:")
#        print(data1)
      
       limit = 100
       out = []
      
       out = out + data1['response']['rows']
       size_ = data1['response']['rowCount']
#        print(size_)
 
       for offset in range(0,size_,limit):
        #  print(offset)
 
         parameters = {'q': term, 'api_key': 'imQAjl1QkgYj0EiPybG1lKaz4dp0AZSauYCgPi3B', 'rows':5,'start':0}
         response = requests.get(url=url, params=parameters)
         data = response.json()
         out = out + data['response']['rows']
 
         offset += limit
       #   print(len(data['response']['rows']))
       #   print(len(out))
       # print(data)
       # return {data1}
#        print(out)
  
       return out
     
   def getMetaTagMapping(self, data): 
       temp = {
              "openpipe_canonical_id": "objectID",
              "openpipe_canonical_title": "title",
              "openpipe_canonical_artist": "artistDisplayName",
              "openpipe_canonical_date": "date",
              "openpipe_canonical_medium": "medium",
              "openpipe_canonical_physicalDimensions": "dimansions",
              "openpipe_canonical_datasource": "datasource"
              
                       }  
       print("in mapping:")
       print(data["title"],temp["openpipe_canonical_title"])
       temp["openpipe_canonical_id"]=data['id']
       temp["openpipe_canonical_title"]=data['title']
       temp["openpipe_canonical_artist"]=data['content']['freetext']['name'][0]['content']
#        self.canonmap["openpipe_canonical_date"]=data['content']['freetext']['date'][0]['content']
       temp["openpipe_canonical_medium"]=data['content']['freetext']['setName'][1]['content']
       temp["openpipe_canonical_fullImage"]=data['content']['descriptiveNonRepeating']['online_media']['media'][0]['thumbnail']
       temp["openpipe_canonical_physicalDimensions"]=data['content']['descriptiveNonRepeating']['online_media']['media'][0]['resources'][1]['dimensions']
       end_date = ((data['content']['freetext']['date'][0]['content']).upper()).replace('A','E')
       if end_date is not None:
          temp["openpipe_canonical_Date"]= [str(end_date) + " " + "JAN" + " " + "01" + " " + "00:00:00"][0]
       print(data["title"],temp["openpipe_canonical_title"])
       
       temp["openpipe_canonical_datasource"]=data['content']['descriptiveNonRepeating']['data_source']
       
       return temp
      
   def getAssetMetaData(self, assetId):
        #*************** Note: 
        # The assetId is a dictionary here that contains the whole asset info here not just the id   
        # the assetId name has not been change so it follows the parent class format
        # TODO: Fix the name later 
           
       metaData = self.getMetaTagMapping(assetId)
       return metaData
 
   def getData(self, q, page, pageSize):
       results = []
       retrievedAssets = self.searchForAssets(q)
#        print("************PRINTING RETRIVED ASSETS*************")
#        print(retrievedAssets)
#        print(len(retrievedAssets)) 
#        print("************END of RETRIVED ASSETS*************")
        
       start = (page - 1) * pageSize
       step = pageSize
       total = len(retrievedAssets)
       if total == 0:
           return {"data": [], "total": 0, "sourceName": "Smithsonian Museum"}
 
       if int(start) > total:
           start = total - 1
       if int(start) + int(step) > total:
           step = total - int(start) - 1
#        print(start)
#        print(step)
       assets = retrievedAssets[int(start):int(start) + int(step)]
#        print(assets)
 
       for asset in assets:
        #  print(asset["title"])
         results.append(self.getAssetMetaData(asset))
       print(results)
       return {"data": results,
               "total": len(results),
               "sourceName": "Smithsonian Museum"}
 
 
if __name__=='__main__':
 
       print("*************************** search ********************************")
 
       sm=SmithsonianMuseum("")
      
       # search=sm.searchForAssets(" cat ")
       # print(search)
       print("************************** End search ***************************")
       getdata = sm.getData(q=" cat ", page=1, pageSize= 8)
       a = json.dumps(getdata)
       
       print(a)


#################---------------- End SM WORKING code --------------------###########################
       
      




################==== start PM data ===####################################################

{
  nodeQuery(
    filter: {conditions: [{field: "uuid", value: "651c7e41-f63e-4d27-b5e8-497aaa93272f"}]}
  ) {
    entities {
      entityUuid
      ... on NodeOeuvre {
        title
        absolutePath
        fieldLrefAdlib
        fieldUrlAlias
        fieldTitreDeMediation
        fieldSousTitreDeMediation
        fieldOeuvreAuteurs {
          entity {
            fieldAuteurAuteur {
              entity {
                name
                fieldPipDateNaissance {
                 startPrecision
                  startYear
                  startMonth
                  startDay
                  sort
                  endPrecision
                  endYear
                  endMonth
                  endDay
                  processed
                }
                fieldPipLieuNaissance
                fieldPipDateDeces {
                 startPrecision
                  startYear
                  startMonth
                  startDay
                  sort
                  endPrecision
                  endYear
                  endMonth
                  endDay
                  processed
                }
                 fieldLieuDeces
              }
            }
            fieldAuteurFonction {
              entity {
                name
              }
            }

          }
        }
        fieldVisuels {
          entity {
            name
            vignette
            publicUrl
          }
        }
        fieldDateProduction {
          startPrecision
          startYear
          startMonth
          startDay
          sort
          endPrecision
          endYear
          endMonth
          endDay
          century
          processed
        }
        fieldOeuvreSiecle {
           entity {
            name
          }
        }
        fieldOeuvreTypesObjet {
          entity {
            name
            fieldLrefAdlib
            entityUuid
          }
        }
        fieldDenominations {
          entity {
            name
          }
        }
        fieldMateriauxTechnique{
          entity {
            name
          }
        }
        fieldOeuvreDimensions {
          entity {
            fieldDimensionPartie {
              entity {
                name
              }
            }
            fieldDimensionType {
              entity {
                name
              }
            }
            fieldDimensionValeur
            fieldDimensionUnite {
             entity {
                name
              }
            }
          }
        }
        fieldOeuvreInscriptions{
          entity {
            fieldInscriptionType {
              entity {
                name
              }
            }
            fieldInscriptionMarque {
              value
            }
            fieldInscriptionEcriture {
              entity {
                name
              }
            }
          }
        }
        fieldOeuvreDescriptionIcono {
          value
        }
        fieldCommentaireHistorique {
          value

        }
        fieldOeuvreThemeRepresente	 {
          entity {
            name
          }
        }
        fieldLieuxConcernes {
          entity {
            name
          }
        }
        fieldModaliteAcquisition {
          entity {
            name
          }
        }
        fieldDonateurs {
          entity {
            name
          }
        }
        fieldDateAcquisition {
          startPrecision
          startYear
          startMonth
          startDay
          sort
          endPrecision
          endYear
          endMonth
          endDay
          century
          processed
        }
        fieldOeuvreNumInventaire
        fieldOeuvreStyleMouvement {
          entity {
            name
          }
        }
        fieldMusee {
          entity {
            name
          }
        }
        fieldOeuvreExpose {
          entity {
            name
          }
        }
        fieldOeuvreAudios {
          entity {
            fieldMediaFile {
              entity {
                url
                uri {
                  value
                  url
                }
              }
            }
          }
        }
        fieldOeuvreVideos {
          entity {
            fieldMediaVideoEmbedField
          }
        }
        fieldHdVisuel {
          entity {
            fieldMediaImage {
              entity {
                url
              }
            }
          }
        }
      }
    }
  }
}

################==== end PM data ===####################################################



#...................... start SM WEll working code ...............................


#!/bin/python3
 
import requests
import json
from MuseumsTM import MuseumsTM
from multiprocessing.pool import ThreadPool
import formatHelp
 
 
class SmithsonianMuseum(MuseumsTM):
 
   def __init__(self, schema):
       self.schema= schema
       self.name = "Smithsonian"
       self.canonmap = {
              "openpipe_canonical_id": "objectID",
        #       "openpipe_canonical_largeImage": "primaryImage",
        #       "openpipe_canonical_smallImage": "primaryImageSmall",
              "openpipe_canonical_title": "title",
              "openpipe_canonical_artist": "artistDisplayName",
              "openpipe_canonical_date": "date",
        #       "openpipe_canonical_culture":  "culture",
        #       "openpipe_canonical_classification": "classification",
        #       "openpipe_canonical_nation":  "country",
        #       "openpipe_canonical_city":  "city",
        #       "openpipe_canonical_tags":  "tags",
                # "openpipe_canonical_tags":  "tags",
              
              "openpipe_canonical_medium": "medium",
              "openpipe_canonical_physicalDimensions": "dimansions"
              
                       }
#        self.fullcanonmap = {
#                "id": "openpipe_canonical_id",
#                "title": "openpipe_canonical_title",
#                "creators": "openpipe_canonical_artist",
#                "culture": "openpipe_canonical_culture"
#                        }
#        self.canonmap = {
#                "title": "openpipe_canonical_title",
#                "creators": "openpipe_canonical_artist",
#                "culture": "openpipe_canonical_culture",
#                "medium": "openpipe_canonical_medium"
#                       }
 
 
   def searchForAssets(self, term):
          
#        parameters = {'q': term, 'key': self.attributes['key'] }
#        response = requests.get(url=self.attributes['url'], params=parameters)
#        data1 = response.json()
#        return data1
      
 
       parameters = {'q': term, 'api_key': 'imQAjl1QkgYj0EiPybG1lKaz4dp0AZSauYCgPi3B', 'rows' : 5}
       url = 'https://api.si.edu/openaccess/api/v1.0/category/art_design/search'
       response = requests.get(url=url, params=parameters)
       data1 = response.json()
       print("response:")
#        print(data1)
      
       limit = 100
       out = []
      
       out = out + data1['response']['rows']
       size_ = data1['response']['rowCount']
#        print(size_)
 
       for offset in range(0,size_,limit):
        #  print(offset)
 
       #   parameters = {'q': term, 'api_key': 'imQAjl1QkgYj0EiPybG1lKaz4dp0AZSauYCgPi3B', 'rows':5,'start':0}
       #   response = requests.get(url=url, params=parameters)
       #   data = response.json()
       #   out = out + data['response']['rows']
 
         offset += limit
       #   print(len(data['response']['rows']))
       #   print(len(out))
       # print(data)
       # return {data1}
#        print(out)
  
       return out
     
   def getMetaTagMapping(self, data): 
       temp = {
              "openpipe_canonical_id": "objectID",
              "openpipe_canonical_title": "title",
              "openpipe_canonical_artist": "artistDisplayName",
              "openpipe_canonical_date": "date",
              "openpipe_canonical_medium": "medium",
              "openpipe_canonical_physicalDimensions": "dimansions",
              "openpipe_canonical_datasource": "datasource"
              
                       }  
       print("in mapping:") #................................... to be removed
       print(data["title"],temp["openpipe_canonical_title"]) #................................... to be removed
       
       temp["openpipe_canonical_id"]=data['id']
       temp["openpipe_canonical_title"]=data['title']
       temp["openpipe_canonical_artist"]=data['content']['freetext']['name'][0]['content']
#        self.canonmap["openpipe_canonical_date"]=data['content']['freetext']['date'][0]['content']
       temp["openpipe_canonical_medium"]=data['content']['freetext']['setName'][1]['content']
       temp["openpipe_canonical_fullImage"]=data['content']['descriptiveNonRepeating']['online_media']['media'][0]['thumbnail']
       temp["openpipe_canonical_physicalDimensions"]=data['content']['descriptiveNonRepeating']['online_media']['media'][0]['resources'][1]['dimensions']
       end_date = ((data['content']['freetext']['date'][0]['content']).upper()).replace('A','E')
       if end_date is not None:
          temp["openpipe_canonical_date"]= [str(end_date) + " " + "JAN" + " " + "01" + " " + "00:00:00"][0]
          
       print(data["title"],temp["openpipe_canonical_title"]) #................................... to be removed
       
       temp["openpipe_canonical_datasource"]=data['content']['descriptiveNonRepeating']['data_source']
       
       return temp
      
   def getAssetMetaData(self, assetId):
        #*************** Note: 
        # The assetId is a dictionary here that contains the whole asset info here not just the id   
        # the assetId name has not been change so it follows the parent class format
        # TODO: Fix the name later 
           
       metaData = self.getMetaTagMapping(assetId)
       return metaData
 
   def getData(self, q, page, pageSize):
       results = []
       retrievedAssets = self.searchForAssets(q)
#        print("************PRINTING RETRIVED ASSETS*************")
#        print(retrievedAssets)
#        print(len(retrievedAssets)) 
#        print("************END of RETRIVED ASSETS*************")
        
       start = (page - 1) * pageSize
       step = pageSize
       total = len(retrievedAssets)
       if total == 0:
           return {"data": [], "total": 0, "sourceName": "Smithsonian Museum"}
 
       if int(start) > total:
           start = total - 1
       if int(start) + int(step) > total:
           step = total - int(start) - 1
#        print(start)
#        print(step)
       assets = retrievedAssets[int(start):int(start) + int(step)]
#        print(assets)
 
       for asset in assets:
        #  print(asset["title"])
         results.append(self.getAssetMetaData(asset))
       print(results)
       return {"data": results,
               "total": len(results),
               "sourceName": "Smithsonian Museum"}
 
 
if __name__=='__main__':
 
       print("*************************** search ********************************")
 
       sm=SmithsonianMuseum("")
      
       # search=sm.searchForAssets(" cat ")
       # print(search)
       print("************************** End search ***************************")
       getdata = sm.getData(q=" cat ", page=1, pageSize= 8)
       a = json.dumps(getdata)
       
       print(a)
       
       
      



#...................... start SM WEll working code ...............................