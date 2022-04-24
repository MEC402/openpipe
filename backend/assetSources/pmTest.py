#!/bin/python3

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

               "openpipe_canonical_fullImage": "fullImage",
               "openpipe_canonical_firstDate":  "firstDate",
               "openpipe_canonical_lastDate": "endDate"
                       }
# ...................................................
        self.fullcanonmap = {
                "id": "openpipe_canonical_id",
                "title": "openpipe_canonical_title",
                "creators": "openpipe_canonical_artist",
                "culture": "openpipe_canonical_culture"
                        }
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
        
        print(json.dumps({"root":out[:3]}))
        test_out = pm.getMetaTagMapping(out[1]) 
        print("Test Mapping")
        print(test_out)

    def getMetaTagMapping(self, data):
        #total=len(data['data']['nodeQuery']["entities"])
        #data = data['data']['nodeQuery']["entities"][0]..???
        # data = data['data']['nodeById'] #......................................................................................??? change?................
  
        self.canonmap["openpipe_canonical_id"]=data["entityUuid"]
        self.canonmap["openpipe_canonical_title"]=data["title"]

        start_date = data["fieldDateProduction"]["startYear"]
        end_date = data["fieldDateProduction"]["endYear"]
        if start_date != None:
          self.canonmap["openpipe_canonical_firstDate"]=start_date
        if end_date is not None:
          self.canonmap["openpipe_canonical_lastDate"]=end_date

        self.canonmap["openpipe_canonical_artist"]=data["fieldOeuvreAuteurs"][0]["entity"]["fieldAuteurAuteur"]["entity"]["name"]
        
        if data["fieldVisuels"][0]["entity"]["vignette"] != None:
           self.canonmap["openpipe_canonical_fullImage"] = data["fieldVisuels"][0]["entity"]["vignette"]

        ########
        # vin = []; pub = []
        # vig = data["fieldVisuels"][0]["entity"]["vignette"]
        # publ = data["fieldVisuels"][0]["entity"]["publicUrl"]
        # for i in range(len(data)): #should be an array of vig and publ urls
        #     if vig is not None:
        #       vin.append(i)
        #     if publ is not None:
        #       pub.append(i)
        # total_v = len(vin)
        # total_p = len(pub)
        # print('#vignette Url = ',total_v,'\n#publicUrl = ',total_p,data.shape)
        ########

        # response = self.schema.copy()
        # response["openpipe_canonical_source"] = ["Cleveland"]
      
        # if data['images'] is not None:
        #     response["openpipe_canonical_largeImage"] = [data["images"]["print"]["url"]]
        #     response["openpipe_canonical_largeImageDimensions"] = [
        #         str(data["images"]["print"]["width"]) + "," + str(data["images"]["print"]["height"])]
        #     response["openpipe_canonical_smallImage"] = [data["images"]["web"]["url"]]
        #     response["openpipe_canonical_smallImageDimensions"] = [
        #         str(data["images"]["web"]["width"]) + "," + str(data["images"]["web"]["height"])]
        #     response["openpipe_canonical_fullImage"] = [
        #         "http://mec402.boisestate.edu/cgi-bin/assetSources/getClevelandConvertedTif.py?id=" + str(data["id"])]
        #     # tileInfo = self.getTileImages(data["objectNumber"], 0)
        #     # response["openpipe_canonical_fullImageDimensions"] = []
        # response["openpipe_canonical_title"] = [data["title"]]
        # if len(data["creators"]) > 0:
        #     response["openpipe_canonical_artist"] = []
        #     for c in data["creators"]:
        #         response["openpipe_canonical_artist"].append(c["description"])
        # if len(data["culture"]) > 0:
        #     response["openpipe_canonical_culture"] = data["culture"]

        # if data["creation_date_earliest"] is not None and data["creation_date_latest"] is not None and data["creation_date"] is not None:
        #     era="CE"
        #     year1 = abs(int(data["creation_date_earliest"]))
        #     year2 = abs(int(data["creation_date_latest"]))
        #     if "B.C." in data["creation_date"]:
        #         era="BC"
        #     response["openpipe_canonical_firstDate"] = [era+" "+str(year1)+" "+"JAN"+" "+"01"+" "+"00:00:00"]
        #     response["openpipe_canonical_lastDate"] = [era+" "+str(year2)+" "+"JAN"+" "+"01"+" "+"00:00:00"]
        #     response["openpipe_canonical_date"]=[response["openpipe_canonical_firstDate"][0],response["openpipe_canonical_lastDate"][0]]

        # response["classification"] = [data["classification"]]
        # self.schema.genre.push(data["city"])
        # self.schema.medium.push(data["city"])
        # response["nation"] = [data["country"]]
        # response["city"] = [data["city"]]
        # response["tags"] = data["tags"]
        # response.update(data)
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


#.......................................................................nodeById(id: "'''+assetId+'''"..........................................................................

#         body='''{
#   nodeById(id: "'''+assetId+'''"

#   ) {
  
#       entityUuid
#       entityId
#       ... on NodeOeuvre {
#         title
#         absolutePath
#         fieldLrefAdlib
#         fieldUrlAlias
#         fieldTitreDeMediation
#         fieldSousTitreDeMediation
#         fieldOeuvreAuteurs {
#           entity {
#             fieldAuteurAuteur {
#               entity {
#                 name
#                 fieldPipDateNaissance {
#                  startPrecision
#                   startYear
#                   startMonth
#                   startDay
#                   sort
#                   endPrecision
#                   endYear
#                   endMonth
#                   endDay
#                   processed
#                 }
#                 fieldPipLieuNaissance
#                 fieldPipDateDeces {
#                  startPrecision
#                   startYear
#                   startMonth
#                   startDay
#                   sort
#                   endPrecision
#                   endYear
#                   endMonth
#                   endDay
#                   processed
#                 }
#                  fieldLieuDeces
#               }
#             }
#             fieldAuteurFonction {
#               entity {
#                 name
#               }
#             }

#           }
#         }
#         fieldVisuels {
#           entity {
#             name
#             vignette
#             publicUrl
#           }
#         }
#         fieldDateProduction {
#           startPrecision
#           startYear
#           startMonth
#           startDay
#           sort
#           endPrecision
#           endYear
#           endMonth
#           endDay
#           century
#           processed
#         }
#         fieldOeuvreSiecle {
#            entity {
#             name
#           }
#         }
#         fieldOeuvreTypesObjet {
#           entity {
#             name
#             fieldLrefAdlib
#             entityUuid
#           }
#         }
#         fieldDenominations {
#           entity {
#             name
#           }
#         }
#         fieldMateriauxTechnique{
#           entity {
#             name
#           }
#         }
#         fieldOeuvreDimensions {
#           entity {
#             fieldDimensionPartie {
#               entity {
#                 name
#               }
#             }
#             fieldDimensionType {
#               entity {
#                 name
#               }
#             }
#             fieldDimensionValeur
#             fieldDimensionUnite {
#              entity {
#                 name
#               }
#             }
#           }
#         }
#         fieldOeuvreInscriptions{
#           entity {
#             fieldInscriptionType {
#               entity {
#                 name
#               }
#             }
#             fieldInscriptionMarque {
#               value
#             }
#             fieldInscriptionEcriture {
#               entity {
#                 name
#               }
#             }
#           }
#         }
#         fieldOeuvreDescriptionIcono {
#           value
#         }
#         fieldCommentaireHistorique {
#           value

#         }
#         fieldOeuvreThemeRepresente   {
#           entity {
#             name
#           }
#         }
#         fieldLieuxConcernes {
#           entity {
#             name
#           }
#         }
#         fieldModaliteAcquisition {
#           entity {
#             name
#           }
#         }
#         fieldDonateurs {
#           entity {
#             name
#           }
#         }
#         fieldDateAcquisition {
#           startPrecision
#           startYear
#           startMonth
#           startDay
#           sort
#           endPrecision
#           endYear
#           endMonth
#           endDay
#           century
#           processed
#         }
#         fieldOeuvreNumInventaire
#         fieldOeuvreStyleMouvement {
#           entity {
#             name
#           }
#         }
#         fieldMusee {
#           entity {
#             name
#           }
#         }
#         fieldOeuvreExpose {
#           entity {
#             name
#           }
#         }
#         fieldOeuvreAudios {
#           entity {
#             fieldMediaFile {
#               entity {
#                 url
#                 uri {
#                   value
#                   url
#                 }
#               }
#             }
#           }
#         }
#         fieldOeuvreVideos {
#           entity {
#             fieldMediaVideoEmbedField
#           }
#         }
#         fieldHdVisuel {
#           entity {
#             fieldMediaImage {
#               entity {
#                 url
#               }
#             }
#           }
#         }
#       }
#     }
#   }'''

  #...............................................................................................................................................................
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

        start = (page - 1) * pageSize
        step = pageSize
        total = retrievedAssets['data']['nodeQuery']["count"]
        if total == 0:
            return {"data": [], "total": 0, "sourceName": "Paris Museum"}

        if int(start) > total:
            start = total - 1
        if int(start) + int(step) > total:
            step = total - int(start) - 1

        assets = retrievedAssets['data']['nodeQuery']["entities"][int(start):int(start) + int(step)]

        pool = ThreadPool(len(assets))
        for asset in assets:
            results.append(pool.apply_async(self.getAssetMetaData, args=[asset["entityUuid"]]))
            #results.append(pool.apply_async(self.getAssetMetaData, args=[asset["entityId"]]))...................................................
        pool.close()
        pool.join()
        results = [r.get() for r in results]
        return {"data": results,
                "total": total,
                "sourceName": "Paris Museum"}


if __name__=='__main__':

    print("start of search")
    pm=ParisMuseum("")
    d=pm.searchForAssets(" chat ")
    print(d)
    # print(len(d["data"]["nodeQuery"]["entities"]))

    # # for dd in d["data"]["nodeQuery"]["entities"]:
    # #     print(dd)

    #################################...........................
    # a = pm.getData(" chat ",1,100).............................................
    # print(json.dumps(a)).......................................................

    #pm.getData(q="chat", page=1, pageSize= 10)
    # print(m)
  

    

    print("End search")