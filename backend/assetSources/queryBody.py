
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

