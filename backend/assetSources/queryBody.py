# toutes les valeurs de la fiche œuvres de cette œuvre.
# cet exemple utilise un filtre sur le champ uuid, renseignable sur toutes les entités de l'API.
# alternativement le champ field_lref_adlib peut être utilisé sur les contenus de type node (comme dans les autres exemples)
tailbody = '''
    entities {
      entityUuid
      ... on NodeOeuvre {
        title
        absolutePath
        fieldOeuvreAuteurs{
          entity{
            fieldAuteurAuteur{
              entity{
                name
              }
            }
          }
        }
        fieldDateProduction{
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
          }
        }
        fieldVisuels{
          entity{
            name
            vignette
            publicUrl
          }
        }
      }
    }
  }
} '''

# tailbody = '''
#     entities {
#       entityUuid
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
#         fieldOeuvreThemeRepresente	 {
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
#   }
# } '''
